
var express = require('express'),
    app = express(),
    mongoose = require('mongoose'),
    morgan = require('morgan'),
    Movie = require('./Movie'),
    body_parser = require('body-parser'),
    method_override = require('method-override'),
    mongo_db_uri = "mongodb://ek5442:NokiaLumia920@ds033875.mlab.com:33875/movies";
mongoose.connect(mongo_db_uri);
var db = mongoose.connection;
//connect to a databse
db.on('error',console.error.bind(console, 'connection error:'));
//set static filies location
app.use(express.static(__dirname+'/public'));
//log every request with morgan
app.use(morgan('dev'));
app.use(body_parser.urlencoded({'extended':'true'}));
app.use(body_parser.json());
app.use(body_parser.json({type: 'application/vnd.api+json'})); // parse application/vnd.api+json as json
app.use(method_override('X-HTTP-Method-Override')); // override with the X-HTTP-Method-Override header in the request

app.listen(8000);
console.log("Application listening to port 8000");
app.get('/api/Movies',function(req,res){
    Movie.find(function(err,data){
        if (err)
            res.send(err);

        else {
            console.log(data)
            res.send(data);
        }
    });
});
app.get('/',function(req,res){
   res.sendfile('./public/views/index.html');
});
app.get('/books',function(req,res){
    res.sendfile('./public/views/books.html')
});
app.get('/projects',function(req,res){
    res.sendfile('./public/views/projects.html')
});
