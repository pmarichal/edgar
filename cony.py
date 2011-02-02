#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import route, run, request, redirect
from bottle import SimpleTemplate, template
import bottle

try:
    from conyconfig import *
except ImportError, e:
    if not e.args or e.args[0] != 'No module named conyconfig':
        raise

    ################
    #  CONFIGURATION
    #
    #  These values can be moved out into a "conyconfig.py" file so that
    #  your local changes don't require merging into new versions of cony.
    ################
    DEBUG = True

    ################################################
    #  Uncomment only one of these SERVER_* sections
    ################################################
    #  Stand-alone server running as a daemon on port 8080
    SERVER_STANDALONE = True
    SERVER_STANDALONE_PORT = 8080
    SERVER_STANDALONE_HOST = 'localhost'
    #SERVER_STANDALONE_HOST = ''    #  to allow on all interfaces

    #SERVER_WSGI = True

    #SERVER_CGI = True


def cmd_g(term):
    """Google search."""
    redirect('http://www.google.com/search?q=%s' % term)


def cmd_pypi(term):
    """Python package index search.

    If there is exact match, then redirects right to the package's page.
    """
    import urllib
    try:
        direct_url = 'http://pypi.python.org/pypi/%s/' % term
        result = urllib.urlopen(direct_url)
    except Exception, e:
        pass
    else:
        if result.code == 200:
            redirect(direct_url)

    redirect('http://pypi.python.org/pypi?:action=search&term=%s&submit=search' % term)


def cmd_p(term):
    """Python documentation search."""
    redirect('http://docs.python.org/search.html?q=%s&check_keywords=yes&area=default' % term)


cmd_fallback = cmd_g

# Templates related part

_TEMPLATES = dict( # {{{
    layout = """
<!DOCTYPE html>
<html>
    <head>
        <title>{{ title or u'Cony — Smart bookmarks' }}</title>
        <style>
        .container {
            margin: 2em 200px 2em 200px; background: #EEE;
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
        <div class="container">
            <header><h1>{{ title }}</h1></header>
            %include
            <footer>
                <p class="copyright">Opensource. By <a href="mailto:svetlyak.40wt@gmail.com">Alexander Artemenko</a>. <a href="http://github.com/svetlyak40wt/cony/">Fork it</a> at the GitHub.</p>
                <p class="thanks">Idea was stolen from Facebook's <a href="https://github.com/facebook/bunny1/">bunny1</a>, thanks them a lot.</p>
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
%rebase layout title='Help — Cony'
"""
) # }}}


class VerySimpleTemplate(SimpleTemplate):
    """ A wrapper around Bottle templates, allows to
        define templates right in the same file keeping
        ability to use inheritance.
    """
    def __init__(self, source=None, name=None, **kwargs):
        if source is None and name is not None:
            source = _TEMPLATES[name]
        super(VerySimpleTemplate, self).__init__(
            source=source, name=name, **kwargs
        )


try:
    from local_commands import *
    if 'TEMPLATES' in locals():
        _TEMPLATES.update(TEMPLATES)
except ImportError:
    pass


def cmd_help(term):
    """Shows all available commands."""
    items = []
    for name, obj in sorted(globals().items()):
        if name != 'cmd_fallback' and name.startswith('cmd_') and callable(obj):
            if obj is cmd_fallback:
                items.append((name[4:] + ' (default)', obj.__doc__))
            else:
                items.append((name[4:], obj.__doc__))
    return dict(items = items, title = u'Help — Cony')


@route('/')
def do_command():
    """Runs a command"""
    search_string = request.GET.get('s', 'help')

    tokens = search_string.split(' ', 1)
    command_name = tokens[0]
    term = len(tokens) == 2 and tokens[1] or ''

    command = globals().get('cmd_' + command_name, cmd_fallback)

    if command is cmd_fallback:
        term = search_string

    result = command(term)
    if isinstance(result, dict):
        # Command could return a dict
        # in that case, we have to render it first
        name = result.pop('template', command_name)
        kwargs = dict(
            title = None,
        )
        kwargs.update(result)
        return template(name, template_adapter=VerySimpleTemplate, **kwargs)
    else:
        return result


#  "main loop" code
if locals().get('DEBUG'): bottle.debug(DEBUG)
if __name__ == '__main__':
    import sys
    if locals().get('SERVER_STANDALONE'):
        run(reloader = DEBUG, host = SERVER_STANDALONE_HOST,
                port = SERVER_STANDALONE_PORT)
    elif locals().get('SERVER_CGI'):
        run(server = bottle.CGIServer)
    else:
        print 'No SERVER_* defined for running from command-line'
        sys.exit(1)
    sys.exit(0)

if locals().get('SERVER_WSGI'):
    application = bottle.app()
