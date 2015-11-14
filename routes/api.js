var express = require('express');
var router = express.Router();
var Weather = require('./weather');
var async = require('async');

//Modelを取得
var User = require('../models/User');
var Genre = require('../models/Genre');
var Song = require('../models/Song');
var History = require('../models/History');
var Feedback = require('../models/Feedback');

//学習させるためのファイルへのパス
var NeuralNetwork = require('../ML/analysis/call_pyfile');

//再生した楽曲情報をsave
//_id,song,weather,status,playtimes
router.get('/played', function(req, res, next) {
	var song_id = req.query.song_id;
	async.waterfall([
		
		//再生回数を取得
		function(callback){
			Weather.get('SanFrancisco',function(weathers){
				callback(null, weathers);
			});
		},
		
		//dataを整形し、Historyにsave	
		function(weathers, callback) {
			var date = mmddyyyy();	
			var time = hhmiss();	
			
			incrementHistoryId(function(id){
				var history  = new History({
					_id:  id,
					song: song_id,
					weather: weathers.weather,
					date: date, 
					time: time	
				});
					  
				history.save(function (err) {
					if (err){
						callback(null, 'error');
					}
				
					callback(null, 'success');
				});
			});
		}

		
	],
	function (err, message) {
		res.json({ message: message });
	});

});

//feedbackボタンが押された時に呼び出される
// _id,song,status,playtimes
router.get('/feedback', function(req, res, next) {
	var song_id = req.query.song_id;
	var status = req.query.status;
	
	async.waterfall([
		
		//再生回数を取得
		function(callback){
			Song.find({_id: song_id})
			.exec(function (err, songs) {
				if (err) console.log(err);
				callback(null,songs[0].playtimes);
			});
		
		},
		
		//feedbackをsave		
		function(playtimes, callback) {
			incrementFeedbackId(function(id){
				var feedback  = new Feedback({
					_id:  id,
					song: song_id,
					status: status, 
					playtimes: playtimes	
				});
				
				feedback.save(function (err) {
					if (err){
						callback(null,'error');
					}
					callback(null,'success');
				});
			
			});
		}

		
	],
	function (err, message) {
		res.json({ message: message });
	});

});

//学習を実行する
router.get('/learning', function(req, res, next) {
	var user_id = req.query.user_id;
  NeuralNetwork.startLearning(user_id, function(result){
    console.log('Learning: '+ result);
    res.json({ message: "LEARNING SUCCESS!!!!!!" });
  });
});



module.exports = router;


function incrementFeedbackId(callback) {
	Feedback.find({},{},{sort:{_id: -1},limit:1},
	function(err, feedbacks){
		if (err) console.log(err);
		
		var feedback_id = feedbacks[0]._id;
		var increment_id = feedback_id + 1;
		console.log(increment_id);
		callback(increment_id);
	});
		
}

function incrementHistoryId(callback) {
	History.find({},{},{sort:{_id: -1},limit:1},
	function(err, histories){
		if (err) console.log(err);
		var history_id = histories[0]._id;
		var increment_id = history_id + 1;
		callback(increment_id);
	});
		
}

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

