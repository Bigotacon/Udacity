#!/usr/bin/env python
import os
import jinja2
import webapp2
import re
import hashlib
import hmac
from string import letters
from google.appengine.ext import db

SECRET = "IMSOSMART"

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

# for the cookies


def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()


def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))


def check_secure_val(h):
    value = h.split('|')[0]
    if h == make_secure_val(value):
        return value


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


def render_post(response, post):
    response.out.write('<b>' + post.subject + '</b><br>')
    response.out.write(post.content)


class MainPage(Handler):

    def get(self):
        items = self.request.get_all("food")
        self.render("shopping_list.html", items=items)


class Rot13Page(Handler):

    def get(self):
        self.render("rot13.html", text="")

    def rot13fn(self, word):
        output = ""
        abc = "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz"
        abc13 = "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm"
        for char in word:
            if char in abc:
                k = abc.index(char)
                output += char.replace(char, abc13[k])
            else:
                output += char
        return output

    def post(self):
        rot13 = self.request.get("rot13text")
        rot13 = self.rot13fn(rot13)
        if rot13:
            self.render('rot13.html', text=rot13)
        else:
            self.render("rot13.html", text=rot13 + 'else')


class SignUp(Handler):

    def get(self):
        self.render('signup.html')

    def validate_username(self, username):
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        return USER_RE.match(username)

    def validate_password(self, password):
        PASSWORD_RE = re.compile("^.{3,20}$")
        return PASSWORD_RE.match(password)

    def validate_email(self, email):
        EMAIL_RE = re.compile("^[\S]+@[\S]+.[\S]+$")
        return EMAIL_RE.match(email)

    def post(self):
        username_display = self.request.get("username")
        username = self.validate_username(self.request.get("username"))
        password_display = self.request.get("password")
        password = self.validate_password(self.request.get('password'))
        retype_password_display = self.request.get("retype_password")
        retype_password = self.validate_password(self.request.get('retype_password'))
        email = self.validate_email(self.request.get('email'))
        email_present = self.request.get('email')

        # checks if username and password is valid
        if(username and password):
            # checks if password matches
            if(password_display == retype_password_display):
                # check to see if the user has a valid email or no email
                if(not(email_present) or email):
                    self.write("Welcome, " + username_display + ".")
                else:
                    self.render('signup.html',
                                email_message="Please enter a valid email.",
                                username_value=username_display,
                                password_value="",
                                )
            elif(password_display != retype_password_display):
                self.render('signup.html', password_message="Password doesnt match",
                            username_value=username_display, password_value="")
        else:
            self.render('signup.html', username_message="Please select a valid username.",
                        password_message="Please select a valid password.", username_value=username_display, password_value="")


class Art(db.Model):
    title = db.StringProperty(required=True)
    art = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class Asciichan(Handler):

    def render_front(self, title="", art="", error=""):
        arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")
        self.render("front.html", title=title, art=art, error=error, arts=arts)

    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")

        if title and art:
            a = Art(title=title, art=art)
            # stores new art data in the database
            a.put()
            self.redirect('/asciichan')
        else:
            error = "We need a title and some art work!"
            self.render_front(title, art, error=error)


# blog starts here

def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class Post(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p=self)


class BlogFront(Handler):

    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 10")
        self.render('blogfront.html', posts=posts)


class PostPage(Handler):

    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        self.render("permalink.html", post=post)

        # def get(self, id, title="", blog=""):
        #     blogs = db.GqlQuery("SELECT * FROM Blog WHERE num = 1")
        #     self.render("postpage.html", title=title, blog=blog)


class NewPost(Handler):

    def get(self):
        self.render("newpost.html")

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(parent=blog_key(), subject=subject, content=content)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject, content=content, error=error)


class Account(Handler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        visits = 0
        visits_cookie_str = self.request.cookies.get('visits')
        if visits_cookie_str:
            cookie_val = check_secure_val(visits_cookie_str)
            if cookie_val:
                visits = int(cookie_val)

        visits += 1

        new_cookie_val = make_secure_val(str(visits))

        self.response.headers.add_header('Set-Cookie', 'visits= %s' % new_cookie_val)
        if visits > 1000:
            self.write("You are the best one!")
        else:
            self.write("You have been here %s times!" % visits)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/rot13', Rot13Page),
    ('/signup', SignUp),
    ('/asciichan', Asciichan),
    ('/blog/?', BlogFront),
    ('/blog/newpost', NewPost),
    ('/blog/([0-9]+)', PostPage),
    ('/account', Account),
], debug=True)
