import os
import re
import random
import hashlib
import hmac
import database
from string import letters

import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

secret = '31bd41fff8aa4157a5d2fec13c99451d'

def hashPassword(password, username):
    """ Creates a password salt """
    return hashlib.sha256(password + username + secret).hexdigest()

def make_secure_val(val):
    """ Generates a hashed value """
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    """ Function check if the value is secure """
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    """ Function uses USER_RE regular expression to see if username is valid """
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    """ Function uses PASS_RE regular expression to see if username is valid """
    return password and PASS_RE.match(password)

def render_str(template, **params):
    """ Gets a given template and allows paramanters timport os"""
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        """
        Used to write to a given site through string, paramanters and
        functions
        """
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        """ Gets a given template and allows paramanters to be passed. """
        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kw):
        """Calls render_str and write to display the jinja template."""
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        """
        Method takes in a name, value, and expiration it creates a cookie.

        The name parameter takes in any value and converts it to a string.

        The val parameter takes in any value and converts it to a string.

        The exp parameter takes in integer representing the number of
        seconds before expiration.

        A null or non integer value in the expiration parameter sets a
        session cookie.
        """
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        """
        Method takes in the name of a cookie and returns its' value.
        Remember that the value of a cookie will be in plain text format.
        """
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def logout(self):
        """ Method that logs the user out by altering the cookie """
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def error(self):
        """ Renders an error site """
        self.render('error.html')

    def initialize(self, *a, **kw):
        """ This is the handler class for the main page for the blog. """
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and database.User.getUserById(uid)

class MainPage(BaseHandler):
    """ This is the handler class for the main page for the blog. """
    def get(self):
        posts = database.Post.query()
        self.render('index.html', posts = posts)

class AccountPage(BaseHandler):
    """ Handles the  rendering the account page """
    def get(self):
        """ Renders the account page. """
        self.render('account.html')

class LoginPage(BaseHandler):
    def get(self):
        """ Renders the login page. """
        self.render('login.html')

    def post(self):
        """ Method that handles a user login. """
        name = self.request.get('username')
        password = self.request.get('password')
        password_hash = hashPassword(password, name)
        user = database.User.getUserByNameAndPassword(
            name, password_hash)
        if user:
            self.set_secure_cookie('user_id', str(
                               database.User.getUserId(user)))
            self.redirect('/')
        else:
            msg = 'Invalid login'
            self.render('login.html', error = msg)

class RegisterPage(BaseHandler):
    """ Handles the registration of a user account """
    def get(self):
        self.render('register.html')

    def post(self):
        """ Handles the post request from register.html """
        name = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')

        if valid_username(name):
            if valid_password(password):
                if password == verify:
                    user = database.User.getUserByName(name)
                    if user:
                        if user.user_name == name:
                            msg = "The username already exisits."
                            self.render('register.html', error = msg)
                    else:
                        password_hash = hashPassword(password, name)
                        user_id = database.User.addUser(name, password_hash)
                        self.set_secure_cookie('user_id', str(user_id))
                        self.redirect('/')
                else:
                    msg = "The passwords do not match."
                    self.render('register.html', error = msg)
            else:
                msg = "That wasn't a valid password."
                self.render('register.html', error = msg)
        else:
            msg = "That's not a valid username."
            self.render('register.html', error = msg)

class LogoutPage(BaseHandler):
    """ Handles the proccess of a user logging off of their account """
    def get(self):
        """ Logs the user out """
        self.logout()
        self.redirect('/')



class PostPage(BaseHandler):
    def get(self, post_id):
        post = database.Post.getPost(int(post_id))
        if not post:
            return self.error()
        comments = database.Comment.getCommentsByPostId(post_id)
        like_text = 'Like'
        if self.user:
            user = self.user
            like = database.LikePost.getLikeByPostAndAuthor(post_id,
            user.user_name)
            if like:
                like_text = 'Liked'
        self.render("viewpost.html", post = post, comments = comments,
        like = like_text)

class AddPostPage(BaseHandler):
    """ Handles the adding of a post. Authenticates the user. """
    def get(self):
        if self.user:
            self.render("addpost.html")
        else:
            self.redirect("/login")

    def post(self):
        """ Handles the POST (add post) request from addpost.html """
        if not self.user:
            return self.redirect('/')

        user = self.user
        title = self.request.get('title')
        content = self.request.get('content')
        author = user.user_name
        post_id = database.Post.addPost(title = title,
                                        content = content,
                                        author = author)
        self.redirect('/post/' + str(post_id))


class EditPostPage(BaseHandler):
    """ Handles the editing of a post. Authenticates the user.  """
    def get(self, post_id):
        post = database.Post.getPost(int(post_id))
        if not post:
            self.error()
            return

        self.render("addpost.html", post = post)
    def post(self, post_id):
        """ Handles the POST (edit post) request from addpost.html """
        if not self.user:
            return self.redirect('/')

        user = self.user
        title = self.request.get('title')
        content = self.request.get('content')
        #post_id = self.request.get('post_id')
        author = user.user_name
        database.Post.editPost(title = title,
                               content = content,
                               author = author,
                               post_id = post_id)
        self.redirect('/post/' + str(post_id))

class DeletePost(BaseHandler):
    """ Handles the deleting of a post. Validates the user.  """
    def get(self):
        self.redirect('/')

    def post(self):
        """ Handles the POST (delete post) request from delete.html """
        if not self.user:
            return self.redirect('/')

        user = self.user
        post_id = self.request.get('postid')
        post = database.Post.getPost(post_id)

        if post.post_author == user.user_name:
            success = database.Post.deletePost(int(post_id))
            if success:
                self.render('index.html')
                self.redirect('/')
        else:
            self.error(401)
            return

class AddComment(BaseHandler):
    """ Handles the adding of a comment. Validates the user. """
    def post(self):
        if not self.user:
            return self.redirect('/')

        user = self.user
        post_id = self.request.get('post_id')
        content = self.request.get('content')


        if post_id and content:
            database.Comment.addComment(post_id = post_id, text = content,
            author = user.user_name)
            return self.redirect('/post/'+post_id)
        else:
            return self.error()

class EditComment(BaseHandler):
    """ Handles the edtiting of a comment. Validates the user. """
    def post(self):
        """ Handles the POST request to edit the commment"""
        if not self.user:
            return self.redirect('/')

        user = self.user
        post_id = self.request.get('post_id')
        content = self.request.get('content')
        commment = database.Comment.getComment(post_id)

        if comment.comment_author == user.user_name:
            database.Comment.addComment(post_id = post_id, text = content,
            author = user.user_name)
            database.Comment.editComment

            return self.redirect('/post/'+post_id)

        else:
            return self.error()
        #
        # if post_id and content:
        #     database.Comment.addComment(post_id = post_id, text = content, author = user.user_name)
        #     return self.redirect('/post/'+post_id)
        # else:
        #     return self.error()

class DeleteComment(BaseHandler):
    """ Handles the deleting of a comment. Validates the user. """
    def get(self):
        self.redirect('/')

    def post(self):
        """ Handles the POST request to delete the comment. """
        if not self.user:
            return self.redirect('/')

        user = self.user
        comment_id = self.request.get('comment_id')
        comment = database.Comment.getComment(comment_id)

        if comment.comment_author == user.user_name:
            success = database.Comment.deleteComment(int(comment_id))
            if success:
                return self.redirect('/')
        else:
            self.error(401)
            return

class AddLike(BaseHandler):
    """ Handles the like of a comment."""
    def get(self, post_id):
        if not self.user:
            return self.redirect('/')

        user = self.user
        post = database.Post.getPost(post_id)
        if not post:
            return self.redirect('/')
        like = database.LikePost.getLikeByPostAndAuthor(post_id, user.user_name)
        if like:
            database.LikePost.deleteLike(like.key.id())
        else:
            if post.post_author == user.user_name:
                return self.redirect('/')
            else:
                database.LikePost.addLike(post_id, user.user_name)

        return self.redirect('/post/'+post_id)

        if post_id and content:
            database.Comment.addComment(post_id = post_id, text = content,
            author = user.user_name)
            return self.redirect('/post/'+post_id)
        else:
            return self.error()

class DeleteLike(BaseHandler):
    """ Handles the delete of a like for a comment."""
    def get(self):
        self.redirect('/')

    def post(self):
        """ Handles the POST request to delete the like. """
        if not self.user:
            return self.redirect('/')

        user = self.user
        post_id = self.request.get('postid')
        post = database.Post.getPost(post_id)

        if post.post_author == user.user_name:
            success = database.Post.deletePost(int(post_id))
            if success:
                self.render('index.html')
                self.redirect('/')
        else:
            self.error(401)
            return

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/account', AccountPage),
    ('/login', LoginPage),
    ('/register', RegisterPage),
    ('/logout', LogoutPage),
    ('/newpost', AddPostPage),
    ('/editpost/([0-9]+)', EditPostPage),
    ('/post/([0-9]+)', PostPage),
    ('/delete', DeletePost),
    ('/addcomment', AddComment),
    ('/editcomment', EditComment),
    ('/deletecomment', DeleteComment),
    ('/addlike/([0-9]+)', AddLike),
    ('/deletelike', DeleteLike),
], debug=True)
