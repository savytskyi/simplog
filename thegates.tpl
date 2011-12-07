<!DOCTYPE html>
<html lang='en'>
<head profile="http://www.w3.org/2005/10/profile">
	<title>Gates of {{pagename}}</title>
	<meta charset="utf-8">
	<link id='style' rel="stylesheet" href="/static/css/styles.css"/>
	<link rel="icon" type="image/png" href="/static/img/favicon.png" />
	<link rel="apple-touch-icon" href="/static/image.png" />
	<script src="/static/js/script.js"></script>
</head>
<body>
	<div id="blackHeader">
		<a href="{{siteAddress[1]}}">{{siteAddress[0]}}</a>
		<a href="{{blogAddress[1]}}">{{blogAddress[0]}}</a>
		%for key in tags:
			<a href="{{blogAddress[1]}}/tag/{{tags[key]}}">{{key}}</a>
		%end
	</div>
	<!--redirectTo-->
	%act = blogAddress[1] + '/signin'
	%if redirectTo != '':
		%act = blogAddress[1] + '/signin/' + redirectTo
	%end
	<!--<form action="{{blogAddress[1]}}/signin" id="loginPage" onsubmit="return checkLoginScreen()" method="post">	-->	
	<form action="{{blogAddress[1]}}/signin" id="loginPage" onsubmit="return checkLoginScreen()" method="post">
		<span>{{errorStr}}</span><br/><input class="login" name="login" type="text" id="username" value="username"
			onfocus="this.value=''; this.style.color = 'black'" onblur="afterBlur('username');"/>
		<input class="login" name="password" type="password" id="password" value="pwd"
			onfocus="this.value=''; this.style.color = 'black'" onblur="afterBlur('password');"/><br />
		<input name="submit" style="width:150px; margin-top:7px" type="submit" value="log me in!" />
	</form>
</body>
</html>
