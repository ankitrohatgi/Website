# Render website

import csv
import math
from jinja2 import Environment, FileSystemLoader, Template

class Blog:
    def __init__(self, postDataDir, postTemplate, blogPageTemplate, feedTemplate, blogOutputDir):
        self.posts = []
        self.postDataDir = postDataDir
        self.postDatabase = postDataDir + 'posts.csv'
        self.postTemplateFile = postTemplate
        self.pageTemplateFile = blogPageTemplate
        self.feedTemplate = feedTemplate
        self.outputDir = blogOutputDir

        # Settings
        self.postsPerPage = 3
        self.baseLocationRelativeToPost = "../../"
        self.baseLocationRelativeToPage = "../"
    
    def fetchInfo(self):
        with open(self.postDatabase, "rb") as fh:
            reader = csv.reader(fh, quotechar='"')
            for row in reader:
                if len(row) == 3:
                    postInfo = BlogPost()
                    postInfo.date = row[0]
                    postInfo.title = row[1]
                    postInfo.contentPath = self.postDataDir + row[2]
                    postInfo.fileName = row[2]
                    self.posts.append(postInfo)

    def getPageCount(self):
        return int(math.ceil(len(self.posts) / (1.0*self.postsPerPage)))

    def renderPages(self, env):
        postCount = len(self.posts)
        pageCount = self.getPageCount()
        for pagei in range(1, pageCount+1):
            print 'Rendering page:', pagei, 'of', pageCount
            
            postStartIndex = (pagei-1)*self.postsPerPage
            postEndIndex = postStartIndex + self.postsPerPage - 1
            if postEndIndex >= postCount:
                postEndIndex = postCount - 1

            pagePosts = self.posts[postStartIndex:postEndIndex+1]

            for post in pagePosts:
                post.getContent(env, self.baseLocationRelativeToPage)

            blogPageInfo = BlogPageInfo()
            blogPageInfo.pageNumber = pagei
            blogPageInfo.pageCount = pageCount

            template = env.get_template(self.pageTemplateFile)
            pageHtml = template.render(posts=pagePosts, pageInfo=blogPageInfo, base_dir=self.baseLocationRelativeToPage)
            fileName = ''
            if pagei == 1:
                fileName = self.outputDir + 'index.html'
            else:
                fileName = self.outputDir + 'page' + str(pagei) + '.html'
            page_file = open(fileName, 'w')
            page_file.write(pageHtml)
            page_file.close()


    def renderPosts(self, env):
        if len(self.posts) == 0:
            return
        for blogPost in self.posts:
            print 'Rendering post:', blogPost.title
            template = env.get_template(self.postTemplateFile)
            blogPost.getContent(env, self.baseLocationRelativeToPost)
            pageHtml = template.render(post=blogPost, base_dir=self.baseLocationRelativeToPost)
            post_file = open(self.outputDir + 'posts/' + blogPost.fileName, 'w')
            post_file.write(pageHtml)
            post_file.close()
            blogPost.clearContent()

    def renderRSS(self, env):
        if len(self.posts) == 0:
            return

        print("Rendering RSS feed")

        for post in self.posts:
            post.getContent(env, "http://arohatgi.info/WebPlotDigitizer/")

        template = env.get_template(self.feedTemplate)
        pageHtml = template.render(posts=self.posts, base_dir="http://arohatgi/info/WebPlotDigitizer/")
        rss_file = open(self.outputDir + 'WebPlotDigitizer.rss', 'w')
        rss_file.write(pageHtml)
        rss_file.close()

class BlogPost:
    def __init__(self):
        self.date = "No Date"
        self.title = "No Title"
        self.category = "No Category"
        self.contentPath = "NoPage.html"
        self.fileName = "NoPage.html"
        self.content = "<b>Blank!</b>"

    def getContent(self, env, baseDir): # read html content and render?
        postFile = open(self.contentPath, 'r')
        template = Template(postFile.read())
        self.content = template.render(base_dir=baseDir)
        postFile.close()

    def clearContent(self):
        self.content = ""

class BlogPageInfo:
    def __init__(self):
        self.pageCount = 1
        self.pageNumber = 1

class Website:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader('templates'))
        
    def renderPage(self, filename):
        print "Rendering:", filename
        pageTemplate = self.env.get_template(filename)
        page = pageTemplate.render()
        pageFile = open(filename, 'w')
        pageFile.write(page)
        pageFile.close()

    def renderSimplePages(self):
        self.renderPage("index.html") 
        self.renderPage("development.html") 
        self.renderPage("citation.html") 
        self.renderPage("tutorial.html") 

    def renderBlog(self):
        blog = Blog("data/blog/", "_post.html", "_blogPage.html", "_newsFeed.rss", "blog/")
        blog.fetchInfo()
        blog.renderPosts(self.env)
        blog.renderPages(self.env)
        blog.renderRSS(self.env)

    def render(self):
        self.renderBlog()
        self.renderSimplePages()

if __name__ == "__main__":
    w = Website()
    w.render()

