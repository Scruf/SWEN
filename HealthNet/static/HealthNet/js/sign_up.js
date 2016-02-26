//test email
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
