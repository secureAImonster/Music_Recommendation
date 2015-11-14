var mongoose = require('mongoose');
var uniqueValidator = require('mongoose-unique-validator');

var feedbackSchema = mongoose.Schema({
	_id: Number,
	song: {type: Number, ref: 'Song'},
	status: Number,
	playtimes: Number
});

var Feedback = mongoose.model('Feedback', feedbackSchema);

module.exports = Feedback;
