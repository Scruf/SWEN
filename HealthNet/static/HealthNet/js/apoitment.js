$(document).ready(function(){

  $(".hours").click(function(){
    var date = $(".date-input").val();
    var doctor_user_name = $(".doctor_name").val();
    var full_date = date.split("-").join("");
    var url = "http://127.0.0.1:8000/HealthNet/api/apoitment/"+doctor_user_name+"/"+full_date;
    $.ajax({
      url:url,
      type:'GET',
      data:({}),
      crossDomain:true,
      dataType:'jsonp',
      success: function(data){

        data.filter(function(el){
          if(el.availbale_hours && el.day && el.month){
            $("<input type=time class=time>").insertBefore(".hours");
          }
          //if its not in the year and the month is greater
          if (el.availbale_hours && el.day){
              $("<input type=time class=time>").insertBefore(".hours");
          }
          
        })
      }
    });
  });
});
