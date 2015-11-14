//Modelから引っ張ってくる情報
var User = require('../models/User');
var Genre = require('../models/Genre');
var Song = require('../models/Song');
var History = require('../models/History');
var Feedback = require('../models/Feedback');

var async = require('async');

const SONG_NUM = 100;
const PLAY_TIMES = 10;

//時間の文字列を調整
var toDoubleDigits = function(num) {
  num += "";
  if (num.length === 1) {
    num = "0" + num;
  }
 return num;     
};

//日付を取得 
var mmddyyyy = function() {
	var date = new Date();
	var yyyy = toDoubleDigits(date.getFullYear());
	var mm = toDoubleDigits(date.getMonth() + 1);
	var dd = toDoubleDigits(date.getDate());
	return mm + '/' + dd + '/' + yyyy;
};

//時間を取得
var hhmiss = function() {
	var date = new Date();
	var hh = toDoubleDigits(date.getHours());
	var mi = toDoubleDigits(date.getMinutes());
	var ss = toDoubleDigits(date.getSeconds());
	return hh + ':' + mi + ':' + ss;
};

var date = mmddyyyy();	
var time = hhmiss();		

var users = [
	{	
		"_id" : 0,
		"name" : 'ichiki',
		"mail_address": 'btrax.com',
		"password" : '1234'
	}/*,
	{
		"_id" : 1,
		"name" : 'hiroki',
		"mail_address": 'gurage.com',
		"password" : '3456'
	}*/
];

function handleError(err){
	console.log(err);
}

var total = users.length;
var result_users = [];
function saveUser(callback){
	var user = new User(users.pop());

	user.save(function(err, saved){
		if (err) throw err;//handle error

		result_users.push(saved);
		if (--total) saveUser(callback);
		else callback(result_users);
	})
}


var genres = ["genre1","genre2","genre3","genre4","genre5","genre6","genre7","genre8","genre9","genre10"];	
function saveGenre(index,callback){
 	var name = genres[index];
	var genre  = new Genre({
		_id:  index,
		name: name,
	});
		  
	genre.save(function (err, saved) {
		if (err) return handleError(err);
	
		if (index != genres.length-1){
			index++;
			saveGenre(index,callback);
		}
		else{
			callback();
		}
	});
}

var result_songs = [];
var song_total = SONG_NUM;
function saveSong(user,callback){
	var song_id = SONG_NUM-song_total;
 	var genre_id = song_id%genres.length;
	var song  = new Song({
		_id:  song_id,
		name: "song" + song_id,
		user: user._id,
		genre: genre_id,
		playtimes: PLAY_TIMES //set default 
	});
		  
	song.save(function (err, saved) {
		if (err) return handleError(err);
	
		result_songs.push(saved);

		if (--song_total) saveSong(user,callback);
		else callback(result_songs);
	});
}

var temperatures = [6.5, 8.2, 10.7, 9.5, 6.1, 20.5, 30.1, 16, 18.2, 19.5];
var weathers = [0.75, 0.6, 0.5, 0.4, 0.3, 0.25]; 	
var play_times = PLAY_TIMES;
function saveHistory(count,index,songs,callback){
	var song_total = songs.length - index;
	var song = songs[index];
	var weather = weathers[Math.floor(Math.random() * weathers.length)];
	var temp = temperatures[Math.floor(Math.random() * temperatures.length)];
	var history  = new History({
		_id:  count,
		song: song._id,
		temp: temp, 
		weather: weather,
		date: date, 
		time: time	
	});
		  
	history.save(function (err) {
		if (err) return handleError(err);
	
		if (--play_times){
			count++;
			saveHistory(count,index,songs,callback);
		}else{
			if(--song_total){
				count++;
				index++;
				play_times = PLAY_TIMES;
				saveHistory(count,index,songs,callback);	
			}else{
				callback();
			}
		}
	});
}

var statuses = [-1,0,1];
function saveFeedback(count,index,songs,callback){
	var song_total = songs.length - index;
	var len = SONG_NUM-song_total;
	var song = songs[len];
	var status = statuses[Math.floor(Math.random() * 3)];
	
	var feedback  = new Feedback({
		_id:  count,
		song: song._id,
		status: status, 
		playtimes: play_times	
	});
	
	feedback.save(function (err) {
		if (err) return handleError(err);
	
		if (--play_times){
			count++;
			saveFeedback(count,index,songs,callback);
		}else{
			if(--song_total){
				count++;
				index++;
				play_times = PLAY_TIMES/2;
				saveFeedback(count,index,songs,callback);	
			}else{
				callback();
			}
		}
	});
}

async.waterfall([
	//Genre
	function(callback){
		saveGenre(0,function(){
			console.log("save genre");
			callback(null);
		});
	},
	//User
	function(callback){
		saveUser(function(users){
			console.log("save user");
			callback(null,users);
		});
	},
	//Song
	function(users, callback){
		var user = users[0];
		saveSong(user,function(songs){
			console.log("save song");
			callback(null, songs);
		});
	},
	//History
	function(songs, callback){
		var count = 0;
		var index = 0;
		saveHistory(count,index,songs,function(){
			console.log("save history");
			callback(null, songs);
		});
	},
	//Feedback
	function(songs, callback){
		play_times = PLAY_TIMES/2;
		var count = 0;
		var index = 0;
		saveFeedback(count,index,songs,function(){
			console.log("save feedback");
			callback(null);
		});
	},
], 
function (err) {
	if(err) {
		throw err;
	}
	console.log('Save All');
	process.exit();
}
);

