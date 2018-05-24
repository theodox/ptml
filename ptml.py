
CONTEXT = []

import inspect
import datetime

class ElementBase:
    TAG = 'element'

    def __init__(self, **attribs):
        self.attribs = attribs
        self.children = []
        self.content = None
        CONTEXT.append(self)

    def __enter__(self):
        return self

    def __exit__(self, *exception_context):
        start = CONTEXT.index(self)
        if start < len(CONTEXT):
            delenda = range(len(CONTEXT) - 1, start, -1)
            new_children = [CONTEXT.pop(d) for d in delenda]
            new_children.reverse()
            for child in new_children:
                self.children.append(child)

    def __call__(self, c):
        self.content = c

    def render(self):
        yield '\n<{}'.format(self.TAG)
        idval = self.attribs.get('id')
        if idval:
            yield ' id="{}"'.format(idval)

        classval = self.attribs.get('class')
        if classval:
            class_iter = classval if hasattr(classval, '__iter__') else (classval,)
            yield ' class="{}"'.format(' '.join(class_iter))

        for k, v in self.attribs.items():
            if k in ('id', 'class'):
                continue
            yield ' {}="{}"'.format(k, v)
        yield ">"

        if self.content:
            yield self.content
        for c in self.children:
            for r in c.render():
                yield r
        yield "</{}>\n".format(self.TAG)

    def validate(self, item):
        return isinstance(item, ElementBase)


class HTML (ElementBase):
    TAG = 'html'


class Head(ElementBase):
    TAG = 'head'


class Body(ElementBase):
    TAG = 'body'


class Div (ElementBase):
    TAG = 'div'


class P (ElementBase):
    TAG = 'p'

class A (ElementBase):
    TAG = 'a'

class Span(ElementBase):
    TAG = 'span'


with HTML() as doc:
    with Head() as h:
        h.content = "hello world"
    with Body() as b:
        with Div(id='main') as d:
            with P():
                Span()('go to ')
                A(href = 'http://www.theodox.com')(str(datetime.datetime.now()))
                Span(c='bold')('right now')

with open ("./index.html", 'wt') as fh:
    fh.writelines(doc.render())
