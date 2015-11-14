var mongoose = require('mongoose');
var uniqueValidator = require('mongoose-unique-validator');

var genreSchema = mongoose.Schema({
	_id: Number,
	name: String
});

var Genre = mongoose.model('Genre', genreSchema);

module.exports = Genre;

