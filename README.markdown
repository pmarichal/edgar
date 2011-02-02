Shared Smart Bookmarks Server
=============================

"Cony" is a tool to write [smart bookmarks][smart-bm] in the python and
to share them across all your browsers and with other developers
on GitHub. This project is inspired by Facebook's [bunny1][].

What the difference between Cony and Bunny1?
--------------------------------------------

* Cony has no dependencies other than Bottle, which itself is a
  micro web framework without dependencies.
* Cony could be easily extended. You have no need to inherit any classes like
  you do with Bunny1. With Cony, you place your commands in a separate
  file and fire `./cony.py`.

Introduction
------------

Smart bookmarks are a fast way to retrive information from the web.
For example, you could type `w smart bookmarks` in the browser's
location bar and it will open the Wikipedia article about
[smart bookmarks][smart-bm].

If you use more than one browser or device, then you are in trouble,
because you have to sync the smart bookmarks of the various browsers.

Cony not only solves this problem, creating one place were you store your
smart bookmarks, but also, it makes your bookmarks **much** **much**
**smarter**.

For example, you could create this bookmark which will choose the
text translation mode depending on language:

    def cmd_tr(term):
        """Translates the text using Google Translate."""
        if len(term.decode('utf-8')) < len(term):
            direction = 'ru|en'
        else:
            direction = 'en|ru'
        redirect('http://translate.google.com/#%s|%s' % (direction, term))

This bookmark converts from English to Russian if it contains only ASCII
characters.  Otherwise it translates in other direction.

There are many other applications of this small webserver.


Installation
------------

Ways to install Cony:

* Just clone the repository and to run `./cony.py`.
* `easy_install cony; cony.py`
* `pip install cony; cony.py`

Now you have server up and running. It binds to the localhost:8080 by
default. Open the <http://localhost:8080> in your browser to see the help.

Browser Configuration
---------------------

### Firefox

* Type `about:config` into your location bar in Firefox.
* Set the value of `keyword.URL` to be `http://localhost/?s=`
* Now, type `pypi cony` into your location bar and press ENTER.

### Google Chromium

* Click the "Wrench" to the right of the URL bar.
* Click "Preferences".
* Click "Search:", click on "Manage Search Engines".
* Click "Add".
   * Name: Cony
   * Keyword: c
   * URL: http://localhost:8080/?s=%s
   * OK.
* Select the "Cony" line.
* Click "Make Default" in the upper right.
* Close the window.
* Type "pypi cony" in the URL bar and press ENTER.


### Google Chrome

* Choose `Options` from the wrench menu to the right of the
location bar in Chrome.
* Under the section `Default Search`.
* Click the `Manage` button.
* Click the `Add` button and then fill in the fields:
   * Name: Cony
   * Keyword: c
   * URL: http://localhost:8080/?s=%s
   * OK.
* Select the "Cony" line.
* Click "Make Default" in the upper right.
* Close the window.
* Type "pypi cony" in the URL bar and press ENTER.

### Safari

For Safari you could try to install [Keywurl][] plugin. And add a `Cony`
as default search.


[smart-bm]: http://en.wikipedia.org/wiki/Smart_bookmark
[bunny1]: https://github.com/facebook/bunny1
[Keywurl]: http://alexstaubo.github.com/keywurl/
