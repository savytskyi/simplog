<!DOCTYPE html>
<html lang='en'>
<head profile="http://www.w3.org/2005/10/profile">
	<title>{{postInfo[1]}}</title>
	<meta charset="utf-8">
	<link rel="icon" type="image/png" href="/static/img/favicon.png" />
	<link rel="apple-touch-icon" href="/static/img/image.png" />
	<link id='style' rel="stylesheet" href="/static/css/styles.css"/>
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
	<div id="header"><H1><a href="{{blogAddress[1]}}" id="logo">{{pagename}}</a></H1></div>
	<div id="main">
		<div>
			<H2>{{postInfo[1]}}</H2>
			<div id="articleText">
				{{!postInfo[2]}}
			</div>
			<div id="social">
				%if postInfo[3] is not None:
					%postTags = postInfo[3].decode('utf-8').split(',')
					%for tag in postTags:
						<a href="{{blogAddress[1]}}/tag/{{tag}}">{{tag}}</a>
					%end
				%end	
				
				<p id="date">
					%if postInfo[4] is None:
						Secret date
					%else:
						{{postInfo[4]}}
					%end
				</p>
				
				
					
				<!--Twi-->
				<a href="https://twitter.com/share" class="twitter-share-button" data-count="horizontal" data-via="k_savitsky">Tweet</a><script type="text/javascript" src="//platform.twitter.com/widgets.js"></script>
				<!--G+1-->
				<div class="g-plusone" data-size="medium" data-href="{{blogAddress[1]}}/post-{{postInfo[0]}}"></div>
				<!--FB Like-->
				<div style="position: relative; bottom: 4px; right: 10px;;padding-bottom: 15px;"class="fb-like" data-href="{{blogAddress[1]}}/post-{{postInfo[0]}}" data-send="false" data-layout="button_count" data-width="50" data-show-faces="false"></div>
				
				<!--FB COMMENTS-->
				<div class="fb-comments" data-href="{{blogAddress[1]}}/post-{{postInfo[0]}}" data-num-posts="5" data-width="750"></div>
			</div>
	</div>
	
	
	<!-- FB Root -->
	<div id="fb-root"></div>
	<script src="http://connect.facebook.net/en_US/all.js#xfbml=1"></script>
	<!-- G+ Root -->
	<script type="text/javascript">
	  (function() {
	    var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
	    po.src = 'https://apis.google.com/js/plusone.js';
	    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
	  })();
	</script>
</body>
</html>
