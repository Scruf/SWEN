  $(document).ready(function() {
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
      var doctor_user_name = $(".doctor_name").val();
      var user_name = "";
      var date = "";
      var time = "";
      var options = {
          url: "http://127.0.0.1:8000/HealthNet/api/doctor_names/" + doctor_user_name,
          getValue: function(element) {
              user_name = element.username;
              return element.name;
          },
          list: {
              match: {
                  enabled: true
              }
          },
      };
      $('.doctors').easyAutocomplete(options);
      $('.doctor_names').click(function() {
          $(".doctors").show();

      });

      $(".hours").click(function() {
          date = $(".date-input").val();
          var doctor_name = $('.doctors').val();

          if (date == '' || date.length < 1) {
              alert("Date field cannot be left empty");
              return;
          }
          var doctor_user_name = $(".doctor_name").val();
          var returned_obj = $(".doctors");
          console.log(returned_obj);
          var full_date = date.split("-").join("");
          if (user_name != "") {
              doctor_user_name = user_name;
          }
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
                  if (!data.error) {
                      $(".time_input").insertAfter(".date-input");
                      $(".time_input").show();
                      $(".submit_apoitment").show();
                      time = $(".time_input").val();

                  }

              }
          });

      });
      $(".submit_apoitment").click(function() {
          var patient_user_name = document.URL.split("/")[4];
          var time = $(".time_input").val();
          var doctors_name =$('.doctors');
          if (user_name!='')
            doctor_user_name=user_name

          if (time != "") {
              var url = "http://127.0.0.1:8000/HealthNet/api/appoitment/submit/";
              $.ajax({
                  headers: {
                      "X-CSRFToken": getCookie("csrftoken")
                  },
                  url: url,
                  type: 'POST',
                  data: ({
                      'patient_user_name': patient_user_name,
                      'time': time,
                      'doctor_name':doctor_user_name,
                      'date':date
                  }),
                  success: function(data) {

                  }
              });
          } else {
              alert('Please enter the time you would like to meet with the doctor');
              return;
          }

      })
  });
