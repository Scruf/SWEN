  $(document).ready(function() {
      var doctor_user_name = $(".doctor_name").val();
      var options = {
          url: "http://127.0.0.1:8000/HealthNet/api/doctor_names/" + doctor_user_name,
          getValue: "name",
          list: {
              match: {
                  enabled: true
              }
          },
      };
      $('.doctors').easyAutocomplete(options);
      $('.doctor_names').click(function(){
        $(".doctors").show();

      });

      $(".hours").click(function() {
          var date = $(".date-input").val();
          var doctor_name = $('.doctors').val();

          if (date == '' || date.length < 1) {
              alert("Date field cannot be left empty");
              return;
          }

          var doctor_user_name = $(".doctor_name").val();
          var returned_obj = $(".doctors");
          console.log(returned_obj); 
          var full_date = date.split("-").join("");
          var url = "http://127.0.0.1:8000/HealthNet/api/apoitment/" + doctor_user_name + "/" + full_date;
          $.ajax({
              url: url,
              type: 'GET',
              data: ({}),
              crossDomain: true,
              dataType: 'jsonp',
              success: function(data) {
                  if (data.error) {
                      var message = "<h3>" + data.message + "</h3>";
                      $(message).insertAfter(".hours");
                      $(".date-input").val("");
                  }
                  if (!data.error){
                    $(".time_input").insertAfter(".date-input");
                    $(".time_input").show();

                  }

              }
          });
      });
  });
