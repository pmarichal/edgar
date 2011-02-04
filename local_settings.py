# -*- coding: utf-8 -*-
from bottle import redirect
from urllib import quote_plus as qp

################
#  CONFIGURATION
#
#  These values can be overridden in a "local_settings.py" file so that
#  your local changes don't require merging into new versions of cony.
################

DEBUG = True
#  Stand-alone server running as a daemon on port 8080
SERVER_MODE = 'STANDALONE' # or 'WSGI', or 'CGI'
SERVER_PORT = 8080
SERVER_HOST = 'localhost'  # or '' to allow on all interfaces

#  local templates
TEMPLATES = dict(
   layout = """
<!DOCTYPE html>
<html>
   <head>
       <title>{{ title or u'Edgar — Smart bookmarks' }}</title>
       <style>
       body {
           background-color: #202020;
           color: #ddd;
           font: 14px/150% "Helvetica Neue", Arial, Helvetica, Geneva, sans-serif;
       }
       
       a {
           text-decoration: none;
           color: #f69d2c;
       }

       a:hover {
           text-decoration: underline;
       }
       
       h1 {
           font-family: "Reminga OT", "Hofler Text", "Times New Roman", Times, serif;
           color: #f69d2c;
       }
       
       .container {
           margin: 2em 200px 2em 200px; background: #444;
           padding: 1em 1em 0.5em 1em;
       }
       
       .container header {
           border-bottom: 1px solid #BBB;
           margin-bottom: 2em;
       }
       .container dl.help dd {
           margin-bottom: 1em;
       }
       .container dl.help dt {
           font-weight: bold;
       }
       .container footer {
           border-top: 1px solid #BBB;
           text-align: center;
       }
       .container footer p {
           font-size: 0.75em;
           margin-top: 0.5em;
           margin-bottom: 0.2em;
       }
       </style>
   </head>
   <body>
       <a href="https://github.com/pmarichal/edgar"><img style="position: absolute; top: 0; right: 0; border: 0;" src="https://assets1.github.com/img/30f550e0d38ceb6ef5b81500c64d970b7fb0f028?repo=&url=http%3A%2F%2Fs3.amazonaws.com%2Fgithub%2Fribbons%2Fforkme_right_orange_ff7600.png&path=" alt="Fork me on GitHub"></a>
       <div class="container">
           <header><h1>{{ title }}</h1></header>
           %include
           <footer>
               <p class="copyright">Opensource. By <a href="http://pmarichal.net/">Philippe Marichal</a>. <a href="https://github.com/pmarichal/edgar">Fork it</a> at the GitHub.</p>
               <p class="thanks"><a href="http://pmarichal.net/geekeries/2011/02/03/edgar/">Edgar</a> is a fork from <a href="https://github.com/svetlyak40wt/cony">cony</a> by Alexander Artemenko. Original idea was stolen from Facebook's <a href="https://github.com/facebook/bunny1/">bunny1</a>, many thanks to them.</p>
           </footer>
       </div>
   </body>
</html>
""",
   help = """
   <dl class="help">
   %for item in items:
       <dt>{{ item[0] }}</dt>
       <dd>{{ item[1] }}</dt>
   %end
   </dl>
%rebase layout title='Help — Edgar'
""",
   weather = """
      <p />Display the weather in the specified location.  For example,
      you could enter the following locations:
      <dl class="help">
      %for example in examples:
      <dt>{{ example }}</dt>
      %end
      </dl>
      %rebase layout title = 'Weather Help'
      """,
   translate = """
      <p />Translate the text using Google Translate. For example,
      you could enter the following translations:
      <dl class="help">
      %for example in examples:
      <dt>{{ example }}</dt>
      %end
      </dl>
      %rebase layout title = 'Translate Help'
      """,
   )

def cmd_weather(term):
   '''Look up weather forecast in the specified location.'''
   examples = [ 'Moscow, Russia', 'Fort Collins, Colorado' ]
   if term and term != 'help':
      redirect('http://weather.yahoo.com/search/weather?location=%s' % term)
   else:
      #  render the "weather" template defined above, pass "examples"
      return dict(examples = examples)

cmd_w = cmd_weather

def cmd_translate(term):
    """Translates the text using Google Translate."""
    examples = [ "en fr procrastination  (to translate the word 'procrastination' from english to french) ",
                  "My Tayler is rich  (This would do a default translation en -> fr) ", 
                  "'es fr Amigos  (to translate from spanish to french the word 'amigos') " ]
    tokens = term.split(' ', 2)
    if term and term == 'help':
        return dict(examples = examples)
    if len(tokens) < 3:
        direction = 'en|fr'
    else:
        direction = '%s|%s' % (tokens[0], tokens[1])
        term = tokens[2]
    redirect('http://translate.google.com/#%s|%s' % (direction, term))

cmd_tr = cmd_translate

def cmd_fl(term):
    """Search among Flickr photos under Creative Commons license."""
    redirect('http://www.flickr.com/search/?q=%s&l=cc&ss=0&ct=0&mt=all&w=all&adv=1' % term)

def cmd_pep(term):
    """Search a Python Enhancement Proposal by it's number. For example: 'pep 8'."""
    redirect('http://www.python.org/dev/peps/pep-%0.4d/' % int(term))

def cmd_dj(term):
    """Django documentation search (trunk)."""
    redirect(
        'http://docs.djangoproject.com/search/?q=%s&release=1' % term
    )

def cmd_yt(term):
    """Searches YouTube or goes to it"""
    if term:
        redirect("http://www.youtube.com/results?search_query=%s&search_type=&aq=-1&oq=" % term)
    else:
        redirect("http://www.youtube.com/")

def cmd_imdb(term):
    """Searches Imdb or goes to it"""
    if term:
        redirect("http://www.imdb.com/find?s=all&q=%s" % qp(term))
    else:
        redirect("http://www.imdb.com/")

def cmd_tv(term):
    """Searches tvrage or goes to it"""
    if term:
        redirect("http://www.tvrage.com/search.php?search=%s" % qp(term))
    else:
        redirect("http://www.tvrage.com/")
        
def cmd_wi(term):
    """Searches Wikipedia or goes to it"""
    if term:
        redirect("http://www.wikipedia.org/search-redirect.php?search=%s&language=en&go=++%%E2%%86%%92++&go=Go" % qp(term))
    else:
        redirect("http://www.wikipedia.org/")

def cmd_man(term):
    """Gives the man page for the specified unix command."""
    redirect ("http://man.cx/%s" % term)