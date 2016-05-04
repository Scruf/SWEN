  $(document).ready(function(){
  $('.doctors').click(function(){
      var doctor_user_name = $(".doctor_name").val();
      var url = "http://127.0.0.1:8000/HealthNet/api/doctor_names/"+doctor_user_name;
      $.ajax({
        url:url,
        type:'GET',
        data:({}),
        crossDomain:true,
        dataType:'jsonp',
        success:function(data){
          var names= [];
          data.filter(function(el){
            var full_name = el.first_name+" "+el.last_name;
            names.push(full_name);
          });
          var options ={
            url:"http://127.0.0.1:8000/HealthNet/api/doctor_names/"+doctor_user_name,
            getValue:"first_name",
            list:{
              match:{
                enabled: true
              }
            },
          };
          $('.doctors').easyAutocomplete(options);
          }
        });
      });


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
