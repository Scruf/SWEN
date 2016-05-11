
$(document).ready(function(){
  function getCookie(c_name) {
      if (document.cookie.length > 0) {
          c_start = document.cookie.indexOf(c_name + "=");
          if (c_start != -1) {
              c_start = c_start + c_name.length + 1;
              c_end = document.cookie.indexOf(";", c_start);
              if (c_end == -1) c_end = document.cookie.length;
              return unescape(document.cookie.substring(c_start, c_end));
          }
      }
      return "";
  }
  var user_name = $(".sender_name").val();
  var sender;
  var receiver= "";
  var username = "";
  var area = "";
  var sent_from="";
  var options = {
    url:"http://127.0.0.1:8000/HealthNet/api/message/"+user_name+"/view/",
    getValue: function(el){
      username = el.user_name;
      sender =el.sender;
      sent_from = el.from;
      receiver = el.receiver;
      area = el.area;
      return el.name;
    },
    list: {
      match:{
        enabled:true
      }
    },
  };

  $('.to').easyAutocomplete(options);
  $('.send_message').click(function(){

    if (user_name==username){
      alert("You cannot send message to yourself");
      return;
    }
    if(username.length==1){
      alert("Please enter name of the person you'd like to contact");
      return;
    }
    if($(".body-area").val().length==1){
      alert("Please enter message");
      return ;
    }
    var url = "http://127.0.0.1:8000/HealthNet/api/message/send/";
    $.ajax({
      headers:{
        "X-CSRFToken":getCookie("csrftoken"),
      },
      url:url,
      type:'POST',
      data:{
        'sender':user_name,
        'to':username,
        'time_stamp':new Date().toString(),
        'text_body':$(".body-area").val()
      },
      success: function(){

        console.log(sent_from);
        if(sent_from==='Doctor')
          document.location.href='http://127.0.0.1:8000/HealthNet/doctor/'+user_name+"/";
        if (sent_from==='Nurse')
          document.location.href = 'http://127.0.0.1:8000/HealthNet/nurse/'+user_name+"/";
        if(sent_from==='Patient')
          document.location.href = 'http://127.0.0.1:8000/HealthNet/'+user_name+"/";
      }
    })
  });
});
