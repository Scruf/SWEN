  $(document).ready(function(){

  $(".hours").click(function(){
    var date = $(".date-input").val();
    if (date=='' || date.length<1){
      alert("Date field cannot be left empty");
      return;
    }

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
        if (data.error){
             var message = "<h3>"+data.message+"</h3>";
            $(message).insertAfter(".hours");
            $(".date-input").val("");
        }

      }
    });
  });
});
