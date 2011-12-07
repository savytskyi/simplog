<!DOCTYPE html>
<html lang='en'>
<head profile="http://www.w3.org/2005/10/profile">
	<title>{{pagename}}</title>
	<meta charset="utf-8">
	<link rel="icon" type="image/png" href="/static/img/favicon.png" />
	<link rel="apple-touch-icon" href="/static/img/image.png" />
	<link id='style' rel="stylesheet" href="/static/css/styles.css"/>
	<script src="/static/js/jquery-1.7.min.js"></script>
	<script src="/static/js/script.js"></script>
	
</head>
<body>
	<div id="blackHeader" onclick="javascript:scroll('#logo')">
		<a href="{{siteAddress[1]}}">{{siteAddress[0]}}</a>
		<a href="{{blogAddress[1]}}">{{blogAddress[0]}}</a>
		%for key in tags:
			<a href="{{blogAddress[1]}}/tag/{{tags[key]}}">{{key}}</a>
		%end
	</div>
	<div id="header"><H1><a href="{{blogAddress[1]}}" id="logo">{{pagename}}</a></H1></div>
	<div id="main">
		%i = 0
		%for post in posts:
			<div>
				<H2><a href="{{blogAddress[1]}}/post-{{post[0]}}">{{post[1]}}</a></H2>
				<div id="articleText">
					{{!post[2]}}
				</div>
				<p style="text-align: right;">
					%if post[3] is None:
						Secret date
					%else:
						{{post[3]}}
					%end
				</p>
			</div>
			%i += 1
		%end
		<!--if we have more than 1 page-->
		%if pages > 1:
			<div id="pageSection">
			%i = 0
			%while i < int(pages):	
				%i += 1
				%if i != currentPage:	
					<div class="pageNumber"><a href="{{blogAddress[1]}}/page-{{i}}">{{i}}</a></div>
				%else:
					<div id="currentPage" class="pageNumber">{{i}}</div>	
				%end
			%end			
			</div>
		%end
	</div>
	<div id="footer">
		{{pagename}}. Created with <a href="http://simplog.be">Blog engine</a>.
	</div>
</body>
</html>
