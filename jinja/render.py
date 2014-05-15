# Render website

import csv
from jinja2 import Environment, FileSystemLoader

class Blog:
    def __init__(self, postDataDir, postTemplate, blogPageTemplate, blogOutputDir):
        self.posts = []
        self.postDataDir = postDataDir
        self.postDatabase = postDataDir + 'posts.csv'
        self.postTemplateFile = postTemplate
        self.pageTemplateFile = blogPageTemplate
        self.outputDir = blogOutputDir

        # Settings
        self.postsPerPage = 5
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
                    postInfo.getContent()
                    self.posts.append(postInfo)

    def getPageCount(self):
        return len(self.posts) / self.postsPerPage + 1

    def renderPages(self, env):
        postCount = len(self.posts)
        pageCount = self.getPageCount()
        for pagei in range(1, pageCount+1):
            
            postStartIndex = (pagei-1)*self.postsPerPage
            postEndIndex = postStartIndex + self.postsPerPage
            if postEndIndex >= postCount:
                postEndIndex = postCount - 1

            pagePosts = self.posts[postStartIndex:postEndIndex+1]
            print 'Rendering page:', pagei, 'of', pageCount
            template = env.get_template(self.pageTemplateFile)
            pageHtml = template.render(posts=pagePosts, base_dir=self.baseLocationRelativeToPage)
            fileName = ''
            if pagei == 1:
                fileName = self.outputDir + 'index.html'
            else:
                fileName = self.outputDir + 'page' + pagei + '.html'
            page_file = open(fileName, 'w')
            page_file.write(pageHtml)
            page_file.close()


    def renderPosts(self, env):
        if len(self.posts) == 0:
            return
        for blogPost in self.posts:
            print 'Rendering post:', blogPost.title
            template = env.get_template(self.postTemplateFile)
            pageHtml = template.render(post=blogPost, base_dir=self.baseLocationRelativeToPost)
            post_file = open(self.outputDir + 'posts/' + blogPost.fileName, 'w')
            post_file.write(pageHtml)
            post_file.close()




class BlogPost:
    def __init__(self):
        self.date = "No Date"
        self.title = "No Title"
        self.category = "No Category"
        self.contentPath = "NoPage.html"
        self.fileName = "NoPage.html"
        self.content = "<b>Blank!</b>"

    def getContent(self): # read html content and render?
        pass

def renderBlog(env):
    blog = Blog("data/blog/", "_post.html", "_blogPage.html", "blog/")
    blog.fetchInfo()
    blog.renderPosts(env)
    blog.renderPages(env)

if __name__ == "__main__":
    env = Environment(loader=FileSystemLoader('templates'))
    renderBlog(env)
