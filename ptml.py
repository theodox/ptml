import datetime


class LayoutFrame:

    CURRENT = None

    def __init__(self, parent, indent):
        self.children = []
        self.indent = indent
        self.parent = parent

    @classmethod
    def open(cls):
        new_frame = LayoutFrame(cls.CURRENT, cls.indent() + 1)
        cls.CURRENT = new_frame
        return new_frame

    @classmethod
    def close(cls):
        cls.CURRENT = cls.CURRENT.parent

    @classmethod
    def append(cls, item):
        if cls.CURRENT:
            cls.CURRENT.children.append(item)

    @classmethod
    def indent(cls):
        return cls.CURRENT.indent if cls.CURRENT else 0


class ElementBase:
    TAG = 'element'

    def __init__(self, content=None, **attribs):
        if 'cls' in attribs:
            attribs['class'] = attribs.pop('cls')
        self.attribs = attribs
        self.content = content
        self.indent = LayoutFrame.indent()
        self.frame = None
        LayoutFrame.append(self)

    def __enter__(self):
        self.frame = LayoutFrame.open()
        return self

    def __exit__(self, *exception_context):
        LayoutFrame.close()

    def render(self):
        inline = self.frame is None

        yield '\n{}<{}'.format('\t' * self.indent, self.TAG)

        # for consistency always yield id, class, then other attribs
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
        yield ">" # close beginning tag

        if not inline:
            for c in self.frame.children:
                for r in c.render():
                    yield r
            yield "\n"
        else:
            yield self.content or ''

        # close tag
        yield "{}</{}>".format('\t' * self.indent if not inline else '', self.TAG)

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


class Title(ElementBase):
    TAG = 'title'


class P (ElementBase):
    TAG = 'p'


class A (ElementBase):
    TAG = 'a'


class Span(ElementBase):
    TAG = 'span'


class Comment(ElementBase):

    def render(self):
        yield "\n{}<!-- {} -->".format('\t' * self.indent, self.content)


class Link(ElementBase):
    TAG = 'link'

class Button(ElementBase):
    TAG = 'button'

class UL(ElementBase):
    TAG = 'ul'

class LI(ElementBase):
    TAG = 'li'

def make_the_button():
    Comment("I'm a comment")
    with Button(cls = ('btn', 'btn-warning'), type='button') as fred:
        Span('go to ')
        A((str(datetime.datetime.now())), href='http://www.theodox.com')
        Span('right now', cls='bold')

with HTML() as doc:
    with Head():
        Title('hello world')
        Link(rel="stylesheet",
             href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css",
             integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u",
             crossorigin="anonymous")
    with Body():
        with Div(cls='container', id = 'main') as d:
            with Div(cls='row') as r:
                make_the_button()
            with Div(cls='row'):
                with UL(cls='list-group'):
                    for n in range(100):
                        LI('number {}'.format(n), cls='list-group-item')


with open("./index.html", 'wt') as fh:
    fh.writelines(doc.render())
