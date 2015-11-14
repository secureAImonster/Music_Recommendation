var express = require('express');
var router = express.Router();
var Weather = require('./weather');
var async = require('async');

//Modelから引っ張ってくる情報
var User = require('../models/User');
var Genre = require('../models/Genre');
var Song = require('../models/Song');
var History = require('../models/History');
var Feedback = require('../models/Feedback');

//レコメンデーション結果を呼び出す
var analysis = require('../ML/exec_recommendation');


router.get('/', function(req, res, next) {
	var user_id = 0;
	async.waterfall([
		function(callback){
			Song.find({user: user_id})
			.populate('user')
			.populate('genre')
			.exec(function (err, songs) {
				if (err) console.log(err);
				var results = [];
				songs.sort(function(a,b) {
					    return a._id - b._id;
				});
				getFeedbackObject(songs,results,function(feedback_data){
					callback(null,feedback_data);	
				});
			});
		},
		
		//天気情報の取得 {city, weather,temp}
		function(feedbacks_data, callback){
			Weather.get('SanFrancisco',function(weathers){
				callback(null, weathers);
			});
		},
		
		//Recommendation	
		function(weathers, callback){
			var date = mmddyyyy();	
			var time = hhmiss();	
			//本当はこれをつかう
			console.log(weathers.weather);
			var input_data = [date, time, weathers.temp, weathers.weather, '1', '1', user_id]; 
			//var input_data = [date, time, '25.2', 'sunny', '1', '1', user_id]; 
			console.log('input user action data:' + input_data);
			analysis.result_recommendation(input_data, function(song_id){
    			console.log('Recommend result song_id : '+ song_id);
				callback(null, song_id);
			});
		},

		//song_idから楽曲情報を取得
  		function(song_id, callback){
			Song.find({_id: song_id})
			.populate('genre')
			.exec(function (err, songs) {
				if (err) console.log(err);
				var song = songs[0];
				
				var music = {
          id: song.id,
					title: song.name,
					genre: song.genre.name,
					icon : ""	
				};
					
				callback(null,music);	
			});
			
		}
  ], 
  function (err, music) {
		if(err) {
			throw err;
		}
		
		var data = {
		  info: {
			title: 'Prefy',
			is_logined: false,
      user_id: user_id
		  },
		  music: music	
		};
		res.render('index', data);
	}
  );

});

//曲に対するフィードバックの合計値を返す [[song_id, playtimes, feedback sum]]
function getFeedbackObject(songs,results,callback){
	var list = songs.length;
	var song_id = songs[0]._id;
	var genre_id = songs[0].genre._id;
	Feedback.find({song: song_id})
	.populate('song')
	.exec(function (err, feedbacks) {
		if (err) console.log(err);
		var sum = 0;
		for(var i = 0; i < feedbacks.length; i++){
			sum += feedbacks[i].status;	
		}
		var feedback_data = [
			song_id,
			genre_id,
			feedbacks[0].song.playtimes,
			sum	
		];
		results.push(feedback_data);
		//先頭を取得
		if(--list){
			songs.shift();	
			getFeedbackObject(songs,results,callback);
		}else{
			callback(results);
		}
	});
}

router.post('/', function(req, res, next) {
});

module.exports = router;

var toDoubleDigits = function(num) {
   num += "";
   if (num.length === 1) {
     num = "0" + num;
   }
   return num;     
};
  
var mmddyyyy = function() {
	var date = new Date();
	var yyyy = toDoubleDigits(date.getFullYear());
	var mm = toDoubleDigits(date.getMonth() + 1);
	var dd = toDoubleDigits(date.getDate());
	return mm + '/' + dd + '/' + yyyy;
};

var hhmiss = function() {
	var date = new Date();
	var hh = toDoubleDigits(date.getHours());
	var mi = toDoubleDigits(date.getMinutes());
	var ss = toDoubleDigits(date.getSeconds());
	return hh + ':' + mi + ':' + ss;
};

