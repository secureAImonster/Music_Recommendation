var mongoose = require('mongoose');
var uniqueValidator = require('mongoose-unique-validator');

var historySchema = mongoose.Schema({
	_id: Number,
	song: {type: Number, ref: 'Song'},
	temp: Number,
	weather: Number,
	time: String,
	date: String
});

var History = mongoose.model('History', historySchema);

module.exports = History;
