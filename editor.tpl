<!DOCTYPE html>
<html lang='en'>
<head profile="http://www.w3.org/2005/10/profile">
	<title>Edit</title>
	<meta charset="utf-8">
	<link rel="icon" type="image/png" href="/static/img/favicon.png" />
	<link rel="apple-touch-icon" href="/static/img/image.png" />
	<link id='style' rel="stylesheet" href="/static/css/styles.css"/>
	<script src="/static/js/script.js"></script>
	<script src="/static/js/tinyeditor.js"></script>
	
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
		<div id="postSection" style="float:left;">
			<form id="editPostForm" onsubmit="postEditor.post(); return textCheck()" action="{{blogAddress[1]}}/savepost-{{postInfo[0]}}" method="post">
				<input type="text" class="newpost" name="title" id="title" value="{{postInfo[1]}}"/><br />
				<textarea class="newpost" name="post" id="post" style="text-align: justify; color:black; height:400px;">{{postInfo[2]}}</textarea><br/>
				%if postInfo[3] == '' or postInfo[3] is None or postInfo[3] == ' ':
					%postTags = 'Tags. Please separate tags with coma'
				%else:
					%postTags = postInfo[3]
				%end
				<input type="text" class="newpost" name="tags" id="tags" value="{{postTags}}" onfocus="if (this.value=='Tags. Please separate tags with coma') this.value=''; this.style.color = 'black'" onblur="afterBlur('tags')" /><br />
				<input type="date" class="newpost" name="postDate" id="postDate" value="{{postInfo[4]}}"/><br />
				Today's date <input type="checkbox" id="today" onclick="changeDate('{{postInfo[4]}}')"/>
				<input name="submit" style="width:150px;" type="submit" value="Edit post" />
			</form>
			<a href="{{blogAddress[1]}}/logout" style="position: relative; top: 20px;">Log out</a>
		</div>
		
		<div id="sideMenu">
			<a style="color: grey;" href="#" onclick="showHide('postEditor','headerTagsEditor'); loadXMLDoc('{{blogAddress[1]}}/postListFrom','editPosts')">edit post</a> | 
			<a style="color: grey;" href="#" onclick="showHide('headerTagsEditor','postEditor')">edit header</a>
			<div id="postEditor"></div>
			<div id="headerTagsEditor">
				<form id="addTagsToHeader" onsubmit="return checkTags()" action="{{blogAddress[1]}}/addTags" method="post" >
					<textarea name="headerTags" id="headerTags" style="width: 150px; color:black; height:270px;">
						%for tag in tags:
							{{tag}}:{{tags[tag]}}
						%end
					</textarea><br />
					<input name="submitTags" style="width:100px;" type="submit" value="Add tags" />
				</form>	
			</div>
		</div>		
	</div>
	<script type="text/javascript">
	getDate('postDate');
	postEditor = new TINY.editor.edit('editor',{
		id:'post',
		width:584,
		height:350,
		cssclass:'te',
		controlclass:'tecontrol',
		rowclass:'teheader',
		dividerclass:'tedivider',
		controls:['bold','italic','underline','strikethrough','|','subscript','superscript','|',
				  'orderedlist','unorderedlist','|','outdent','indent','|','leftalign',
				  'centeralign','rightalign','blockjustify','|','unformat','|','undo','redo','n',
				  'font','size','style','|','image','hr','link','unlink','|','cut','copy','paste','print'],
		footer:true,
		fonts:['Verdana','Arial','Georgia','Trebuchet MS'],
		xhtml:true,
		cssfile:'/static/css/styles.css',
		bodyid:'editor',
		footerclass:'tefooter',
		toggle:{text:'source',activetext:'wysiwyg',cssclass:'toggle'},
		resize:{cssclass:'resize'}
	});
	</script>
</body>
</html>
