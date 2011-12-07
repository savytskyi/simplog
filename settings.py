##### WARNING ######
#If you have other html-pages, php-pages, etc, that will be available from this domain,
#put it into /mainsite/ folder of simplog. It will be available from there, not from default host's public_html folder!
#for example, you have index.html and error.php, which must be available from yourdomain.com/index.html or yourdomain.com
#and yourdomain.com/error.php JUST PUT IT INTO /mainsite/ FOLDER!


#####
##### SERVER
#####
rootfolder = '/home/simplog/public_html' #folder, where this file stored

     ###for example, your blog will be on http://example.com/blog
     ###here, main domain is http://example.com, and blog address is http://example.com/blog
domain = ["simplog.be","http://simplog.be/"] #name of your site and main domain. Last symbol in domain must be /
bAddress = ["blog","http://simplog.be/simplog"] #name of your blog and blog address. You can't use / at the end of the blog address
hostIP = 'simlog.be'
sitename = 'Simplog' #Site name. It will be visible on the top of every page
blogLink = '/simplog/' #it can't be empty. First and last symbols must be / Like this: /simplog/ or /blog!/

cookiesAge = 604800 #cookies timeout in seconds. 1 week by default. Or write your timout
postPerPage = 10 #post per page

