var mongoose = require('mongoose');
var uniqueValidator = require('mongoose-unique-validator');
mongoose.connect('mongodb://localhost/prefy');

var userSchema = mongoose.Schema({
	_id:  Number,
	name: String,
	mail_address: { type: String, required: 'メールアドレスを入力してください', unique: true },
	password: {type: String, required: true }
});

userSchema.plugin(uniqueValidator, { message: 'すでに登録されているメールアドレスです' });
var User = mongoose.model('User', userSchema);

module.exports = User;
