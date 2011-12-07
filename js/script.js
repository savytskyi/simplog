function loadXMLDoc(url,element) {
	var xmlhttp;
	if (window.XMLHttpRequest) {
		// code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp=new XMLHttpRequest();
	} else {
		// code for IE6, IE5
		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.onreadystatechange=function() {
		if (xmlhttp.readyState==4 && xmlhttp.status==200) {
			document.getElementById("postEditor").innerHTML=xmlhttp.responseText;
		}
	}
	xmlhttp.open("GET",url,true);
	xmlhttp.send();
}

function afterBlur(elem) {
	if (elem == 'password') {
		elem = document.getElementById(elem);
		if (elem.value.length == 0) {
			elem.value = 'pwd';
			elem.style.color = 'grey';
		}
	} else if (elem == 'username') {
		elem = document.getElementById(elem);
		if (elem.value.length == 0) {
			elem.value = 'username';
			elem.style.color = 'grey';
		}
	} else if (elem == 'title') {
		elem = document.getElementById(elem);
		if (elem.value.length == 0) {
			elem.value = 'Title';
			elem.style.color = 'grey';
		}
	} else if (elem == 'tags') {
		elem = document.getElementById(elem);
		if (elem.value.length == 0) {
			elem.value = 'Tags. Please separate tags with coma';
			elem.style.color = 'grey';
		}
	} else if (elem == 'postDate') {
		elem = document.getElementById(elem);
		if (elem.value.length == 0) {
			elem.value = 'Date';
			elem.style.color = 'grey';
		}
	}
}

function checkLoginScreen() {
	login = document.getElementById('username').value;
	pass = document.getElementById('password').value;
	if (login == 'username' || login.length > 32 || login.length < 3) {
		wrongLogin();
		return false;
	}
	if (pass.length > 64 || pass.length <= 3) {
		wrongPass();
		return false;
	}
	return true;
}

function textCheck() {
	title = document.getElementById('title').value;
	textLength = document.getElementById('post').value.length;
	tagsLength = document.getElementById('tags').value.length;
	if (title == 'Title') {
		if (confirm("Do you really want to use this title?") == false)
			return false;
	}
	if (title.length == 0 || title.length > 100) {
		alert('Your title is empty or too long');
		return false;
	}	
	if (textLength == 0) {
		emptyPost();
		return false;
	}
	if (tagsLength > 255) {
		alert('Too many tags. Please use less than 20');
		return false;
	}
	postDate = document.getElementById('postDate').value;
	separators = new Array (',','.','-','\\',' ','/');
	for (i=0; i<separators.length; i++) {
		dateCorrect = true;
		splitted = new Array();
		splitted = postDate.split(separators[i])
		if (splitted.length == 3) {
		//yyyy:mm:dd
			//why 2020? I can't predict, maybe you'll want to write post from future ^_^
			if ((splitted[0] < 1995 || splitted[0] > 2020) &&
			(splitted[0] < 0 || splitted[0] > 20)) {
				dateCorrect  = false;
			}
			if (splitted[1] < 1 || splitted[1] > 12) {
				dateCorrect = false
			}
			if (splitted[2] < 1 || splitted[2] > 31) {
				dateCorrect = false
			}
			
			
			if (dateCorrect == true)
				break
		} else dateCorrect = false;
	}
	if (dateCorrect == false) {
		wrongDate();
		return false;
	}
	return true;
}

function showHide(showElem, hideElem) {
	var se = document.getElementById(showElem);
	var he = document.getElementById(hideElem);
	 if ((se) && (he)) {
	 	if (se.style.display == 'block') {
	 		se.style.display = 'none';
	 	} else {
	 		se.style.display = 'block';
	 		he.style.display = 'none';
	 	}
	 }
}

function checkTags() {
	tagString = document.getElementById('headerTags').value;
	tags = tagString.split('\n');
	if (tags.length > 0) {		
		for(i = 0; i<tags.length; i++) {
			var tag = tags[i].split(':');
			if (tag.length != 2) {
				alert('Tags had entered in a wrong format');
				return false;
			}
		}	
	} else {
		alert('Tags field is empty, or tags entered in a wrong format');
		return false;
	}
	return true;
}

function getDate(elem) {
	var currentDate = new Date();
	var month = currentDate.getMonth()+1;
	var day = currentDate.getDate();
	var year = currentDate.getFullYear();
	today = (year + "-" + month + "-" + day);
	document.getElementById(elem).value = today;
}

function changeDate(dateStr) {
	cBox = document.getElementById('today');
	dateField = document.getElementById('postDate');
	if (cBox.checked) {
		getDate('postDate');
		dateField.readOnly = true;
		
	} else {
		dateField.value = dateStr;
		dateField.readOnly = false;
	}
}

function wrongDate() {
	alert('You entered the wrong date. Please enter it in YYYY-MM-DD format');
}

function emptyPost() {
	alert('Your post is empty. It is not good :)');
}

function wrongPass() {
	alert('Wrong password');
}

function wrongLogin() {
	alert('Wrong login');
}