<!DOCTYPE html>
<html lang='en'>
<head profile="http://www.w3.org/2005/10/profile">
	<title>Installation script</title>
	<meta charset="utf-8">
	<!--<link id='s0yle' rel="stylesheet" href="/static/css/styles.css"/>-->
	<link rel="icon" type="image/png" href="/static/img/favicon.png" />
	<link rel="apple-touch-icon" href="/static/img/image.png" />
	<script type="text/javascript">
		function check(){
			minPassLength = 4;
			login = document.getElementById('login').value;
			pass = document.getElementById('password').value;
			confirmed = document.getElementById('confirmed').value;
			email = document.getElementById('email').value;
			if ((login.length > 32) || (login.length < 3)) {
				wrongLogin();
				return false;
			} else {
			}
			if ((pass.length > 64) || (pass.length < minPassLength) 
				|| (pass != confirmed)) {
				wrongPass(pass,confirmed);
				return false;
			} 
			var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
			if(reg.test(email) == false) {
				alert('Invalid Email Address');
				return false;
			}
			if (!login.match(/^[0-9_a-z-]+$/i)) { 
				alert('You can use only latin symbols, digits,"-" and "_" for login');
				return false;
			}
			 
			return true;
		}
		function wrongLogin() {
			alert('Username must contains 4 characters or more');
		}
		function wrongPass(pass, confirmed) {
			if (pass != confirmed) {
				alert('Passwords do not match');
			}
			if ((pass.length < minPassLength) || (pass.length > 64)) {
				alert('Password must contains 4 characters or more');
			}
		}
	</script>
	<style type="text/css">
		input {
			margin-top:2px;
			margin-bottom:10px;
			width:400px;
			text-align:center;
		}
		#installForm {
			color:#8e8e8e;
			width:550px;
			height:400px;			
			background:#f3f3f2;
			position:absolute;
			padding-top:50px;			
			left:50%;
			margin-left:-275px;
			top:15%;
			text-align:center;
			-webkit-box-shadow:0 0 5px grey;
			-Moz-box-shadow:0 0 3px grey;
			-o-box-shadow:0 0 5px grey;
			-webkit-border-radius:50px;
			-Moz-border-radius:50px;
			border-radius:50px;
		}
		.installScreen {
			font-size:36px;
		}
	</style>
</head>
<body>
	<form id="installForm" onsubmit="return check()" action="/install" method="POST">	
		{{errorStr}}<br /><input class="installScreen" name="login" id="login" type="text" /><br />
		Password<br /><input class="installScreen" name="password" id="password" type="password" /><br />
		Confirm<br /><input class="installScreen" name="confirmed" id="confirmed" type="password" /><br />
		Email<br /><input class="installScreen" name="email" id="email" type="email" />
		<input style="font-size:12px; width:150px; margin-top:13px;" class="installScreen" name="submit" type="submit" value="create my account" />
	</form>
</body>
</html>
