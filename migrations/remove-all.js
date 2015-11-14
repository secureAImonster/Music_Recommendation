//Modelから引っ張ってくる情報
var User = require('../models/User');
var Song = require('../models/Song');
var History = require('../models/History');
var Feedback = require('../models/Feedback');

var async = require('async');

async.waterfall([
	//User
	function(callback){
		User.remove({}, function(err) {
			if (err) console.log(err);
			else callback(null);
		});
	},
	//Song
	function(callback){
		Song.remove({}, function(err) {
			if (err) console.log(err);
			else callback(null);
		});
	},
	//History
	function(callback){
		History.remove({}, function(err) {
			if (err) console.log(err);
			else callback(null);
		});
	},
	//Feedback
	function(callback){
		Feedback.remove({}, function(err) {
			if (err) console.log(err);
			else callback(null);
		});
	},
], 
function (err) {
	if(err) {
		throw err;
	}
	console.log('remove All');
	process.exit();
}
);
