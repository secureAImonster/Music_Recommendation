var mongoose = require('mongoose');
var uniqueValidator = require('mongoose-unique-validator');
//mongoose.connect('mongodb://localhost/prefy');

var songSchema = mongoose.Schema({
	_id: Number,
	name: String,
	user: {type: Number, ref: 'User' },
	genre: {type: Number, ref: 'Genre'},
	playtimes: Number
});

var Song = mongoose.model('Song', songSchema);

module.exports = Song;

