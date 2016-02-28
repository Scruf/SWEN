//test email
$(document).ready(function(){
	$("#sign_up").submit(function(event){
		alert("Hello");
	});
});
function check_email(val){
	if(val.length<1)
		return false;
	else{
	var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(val);
	}

}
//test first and last name
function check_first_last_name(val){
	if (val.length<1)
		return false;
	else{
		var counter = 0;
		val.split("").filter(function(v){
			if (isNaN(v))
				counter++;
		});

		return counter == val.length;
	}


}
//test password
function check_password(val1,val2){
    if (val1.length<6)
        return false;
    if (val2.length<6)
        return false;
    else
        return val1===val2;
}
function check_symptoms(val){
    if(val.length<5)
        return false;
    else
        return true;
}
console.log("Inside the Sign Up Page");
function on_submit(){

	var username = document.getElementById("username"),
	 password = document.getElementById("password"),
	 first_name = document.getElementById("first_name"),
	 last_name = document.getElementById("last_name"),
	 email = document.getElementById("email"),
	 passwword_confirmation = document.getElementById('passwword_confirmation'),
	 cellphone = document.getElementById("cell_phone"),
	 symptoms = document.getElementById("symptoms");
	 if (!check_first_last_name(first_name))
	 		alert("First Name could not be left blank");
	if(!check_first_last_name(last_name))
			alert("Last Name coould not be left blank");
	if(!check_first_last_name(username))
			alert("Username could not be left blank");
	if (!check_password(password,passwword_confirmation))
			alert("Password is inccorect");
	 if (!check_email(email))
			alert("Email is inccorect");
	if(!check_symptoms(symptoms))
			alert('Symptoms are inccorect');
}
