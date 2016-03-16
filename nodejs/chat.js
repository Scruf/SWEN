var http = require('http')
    server = http.createServer().listen(4000),
    io = require('socket.io').listen(server),
    cookie_reader = require('cookie'),
    quiery_string = require('querystring'),
    redis = require('redis'),
    sub = redis.createClient();
sub.subscribe('chat');
/*
io.configure(function(){
  io.set('authorization',function(data,accept){
    if(data.header.cookie){
      data.cooking = cookie_reader.parse(data.headers.cookie);
      return accept(null,true);
    }
    return accept('error',false);
  });
  io.set('log level',1);
});
*/
io.sockets.on('connection',function(socket){
  sub.on('message',function(chanel,message){
    socket.send(message);
  });
  sockets.on('send_mesage',function(message){
    values = quiery_string.stringify({
      comment:message,
      sessionid: socket.handshake.cookie['sessionid'],
    });
    //makesure to point to a diffiert
    var option = {
      host:'localhost/HealtNet',
      port: 3000,
      path:'/node_api',
      method: 'POST',
      headers: {
        'Content-Type':'application/x-www-form-urlencoded',
        'Content-Length':values.length
      }
    };
    var req = http.get(options,function(res){
      res.setEncoding('utf8');

      res.on('data',function(message){
        if(message!='Working'){
          console.log("Message"+message);
        }
      });
    });
    req.write(values);
    req.end();
  })
})
