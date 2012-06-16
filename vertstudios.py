# Vert studios website. Yay!

from settings import *
from flask import (
 Flask, render_template, request, g, abort, flash, redirect, 
 render_template, url_for
)
from helpers.rss import get_blog_feed
from contact.contact import contact_page
from blog.blog import blog
from flaskext.markdown import Markdown
from jinja2 import TemplateNotFound

# App configuration
app = Flask(__name__)
app.secret_key = SECRET_KEY
Markdown(app)
app.register_blueprint(contact_page)
app.register_blueprint(blog)

@app.before_request
def before_request():
  def get_body_id():
    if request.path == '/':
      g.bodyID = "index"
    
    # The contact page was styled with a body id of work, and i don't 
    # feel like taking the time to fix the styles to make it match.
    elif request.path == '/contact':
      g.bodyID = "work"

    # Else, just get the first part of the path name as the bodyID.
    else:
      g.bodyID = request.path[1:].split('/')[0]

  # Grant access to the dev/production environment variable
  def get_env():
    g.env = FLASK_ENV

  # Determine cloudfront vs s3 content delivery
  def set_assets_dir():
    if FLASK_ENV == "production":
      g.assets = "http://assets.vertstudios.com"
    else:
      g.assets = "static"

  get_body_id()
  get_env()
  set_assets_dir()
  

@app.errorhandler(404)
def page_not_found(e):
      return render_template('404.html'), 404

#####################################################################
# Routes
#####################################################################

@app.route('/')
def home():
  # Get HTML for the home page rss feed
  rssFeed = get_blog_feed(CACHE_DIR, BLOG_CACHE_FILE, NUM_BLOG_POSTS)
  return render_template("index.html", rssFeed=rssFeed)

@app.route('/work')
def work():
  return render_template("work.html")

@app.route('/services')
def services():
  return render_template("services.html")

@app.route('/about')
def about():
  return render_template("about.html")


if __name__ == "__main__":
	app.run(debug=True)
