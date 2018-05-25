# coding: utf-8
from ptml import *
import codecs


# this is an example that reproduces the [bootstrap 'jumbotron' demo](https://getbootstrap.com/docs/4.1/examples/jumbotron/)


def nav_button():
    # bootstrap attributes include dashes, which python does not like as attribute names
    # so we work around that with the **kwargs

    with Button(type='button', cls=('navbar-toggle', 'collapsed'), **{'data-toggle': "collapse", 'data-target': "#navbar", 'aria-expanded': "false", 'aria-controls': "navbar"}):
        Span("Toggle Navigation", cls="sr-only")
        Span(cls="icon-bar")
        Span(cls="icon-bar")
        Span(cls="icon-bar")


# some examples of using the class defaults mechanism to make specific markup classes
class Container(Div):
    DEFAULTS = {'class': ('container', 'example')}

class Row(Div):
    DEFAULTS = {'class': 'row'}

class MD4(Div):
    DEFAULTS = {'class': 'col-md-4'}

with HTML() as doc:
    with Head():
        Title("Example document", escaped_attr = '"hello world"')
        Link(rel="stylesheet",
             href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css",
             integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u",
             crossorigin="anonymous")
        Meta(charset='utf-8')
    with Body():
        with Nav(cls=('navbar', 'navbar-fixed-top')):
            with Div(cls='container'):
                with Div(cls='navbar-header'):
                    nav_button()
                    A("Project Name", cls='navbar-brand', href="#")
                with Div(id='navbar', cls=('navbar-collapse', 'collapse')):
                    with Form(cls=('navbar-form', 'navbar-right')):
                        with Div(cls='form-group'):
                            Input(type='text', placeholder='email', cls='form-control')
                        with Div(cls='form-group'):
                            Input(type='password', placeholder='password', cls='form-control')
                        Button("sign in", type='submit', cls=('btn', 'btn-success'))

        with Div(cls='jumbotron') as jumbo:
            with Container(extra='"hello"'):
                H1("<headline>")
                P("This is a template for a simple marketing or informational website. It includes a large callout called a jumbotron and three supporting pieces of content. Use it as a starting point to create something more unique.This is a template for a simple marketing or informational website. It includes a large callout called a jumbotron and three supporting pieces of content. Use it as a starting point to create something more unique.")
        with Container():
            with Row(id = 'row_1'):
                with MD4(id='column1'):
                    H2("Heading")
                    P("Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui")
                    with P():
                        A("view details»", cls = ('btn', 'btn-default'), href = "#", role='btn')
                with  MD4(id='column2'):
                    H2("Heading")
                    P("Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui")
                    with P():
                        A("view details", cls = ('btn', 'btn-default'), href = "#", role='btn')

                with MD4(id='column3'):
                    H2("Heading")
                    P("Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui")
                    with P():
                        A("view details", cls = ('btn', 'btn-default'), href = "#", role='btn')
        with Footer(cls='container'):
            P("© Company 2017-2018")
with open("./index.html", 'wb') as fh:
    fh.writelines(doc.render())
