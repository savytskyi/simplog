<!DOCTYPE html>
<html lang='en'>
<head profile="http://www.w3.org/2005/10/profile">
	<title>post data</title>
	<meta charset="utf-8">
	<link rel="icon" type="image/png" href="/static/img/favicon.png" />
	<link rel="apple-touch-icon" href="/static/img/image.png" />
	<link id='style' rel="stylesheet" href="/static/css/styles.css"/>
	<script src="/static/js/script.js"></script>
	<style>
		a {
			color: grey;
		}
	</style>
</head>
<body>
	%if not fP: 
		<a href="#" onclick="loadXMLDoc('{{blogAddress[1]}}/postListFrom-{{previousPost}}','editPosts')">Newer posts</a>
	%end
	%for post in posts:
		<div style="text-align:center; padding-top: 5px;">
			{{post[1]}}<br>
			<span style="font-size:14px;">{{post[3]}} <a href="{{blogAddress[1]}}/editpost-{{post[0]}}">Edit</a> |
			<a href="{{blogAddress[1]}}/delete-{{post[0]}}">Delete</a></span>
		</div>
	%end
	%if not lP:
		<a href="#" onclick="loadXMLDoc('{{blogAddress[1]}}/postListFrom-{{nextPost}}','editPosts')">Older posts</a>
	%end
</body>
</html>

					