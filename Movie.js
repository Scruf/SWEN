var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var movieSchema  = new Schema({
	title:String,
	path:String,
	drive_name:String,
	size:String,
	extension:String
});

var Movie = mongoose.model('Movie',movieSchema);
module.exports=Movie;
