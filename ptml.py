import datetime
import sys

if (sys.version_info[0] == 2):
    from cgi import escape
else:
    from html import escape


class LayoutFrame:
    """manages the layout stack"""
    CURRENT = None

    def __init__(self, parent, indent):
        self.children = []
        self.indent = indent
        self.parent = parent

    @classmethod
    def open(cls):
        """begin tracking a new layout frame"""
        new_frame = LayoutFrame(cls.CURRENT, cls.indent() + 1)
        cls.CURRENT = new_frame
        return new_frame

    @classmethod
    def close(cls):
        """revert to the previous layout frame"""
        cls.CURRENT = cls.CURRENT.parent

    @classmethod
    def append(cls, item):
        """add <item> to the active layout frame"""
        if cls.CURRENT:
            cls.CURRENT.children.append(item)

    @classmethod
    def indent(cls):
        """get's the current indent level"""
        return cls.CURRENT.indent if cls.CURRENT else 0


class ElementBase:
    """base for all tag elements"""
    TAG = 'element'
    DEFAULTS = {}
    __slots__ = 'attribs', 'content', 'indent', 'frame'

    def __init__(self, content=None, **attribs):

        if 'cls' in attribs:
            attribs['class'] = attribs.pop('cls')

        instance_attribs = self.DEFAULTS.copy()
        instance_attribs.update(attribs)

        self.attribs = instance_attribs
        self.content = content
        self.indent = LayoutFrame.indent()
        self.frame = None
        LayoutFrame.append(self)

    def __enter__(self):
        self.frame = LayoutFrame.open()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        LayoutFrame.close()
        return exc_type is None

    def render(self):
        """yield this element as a stream of strings"""
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
            yield ' {}="{}"'.format(k, escape(v, quote=True))
        yield ">"
        # ends beginning tab

        # contents
        if not inline:
            for c in self.frame.children:
                for r in c.render():
                    yield r
            yield "\n"
        else:
            yield escape(self.content or '')
        # end contents

        # closing tag
        yield "{}</{}>".format('\t' * self.indent if not inline else '', self.TAG)


# HTML class tags -------------------

class A (ElementBase):
    TAG = "a"


class Abbr (ElementBase):
    TAG = "abbr"


class Acronym (ElementBase):
    TAG = "acronym"


class Address (ElementBase):
    TAG = "address"


class Area (ElementBase):
    TAG = "area"


class Base (ElementBase):
    TAG = "base"


class Blockquote (ElementBase):
    TAG = "blockquote"


class Body (ElementBase):
    TAG = "body"


class Br (ElementBase):
    TAG = "br"


class Button (ElementBase):
    TAG = "button"


class Caption (ElementBase):
    TAG = "caption"


class Cite (ElementBase):
    TAG = "cite"


class Code (ElementBase):
    TAG = "code"


class Col (ElementBase):
    TAG = "col"


class Dfn (ElementBase):
    TAG = "dfn"


class Dir (ElementBase):
    TAG = "dir"


class Div (ElementBase):
    TAG = "div"


class Dl (ElementBase):
    TAG = "dl"


class Dt (ElementBase):
    TAG = "dt"


class Dd (ElementBase):
    TAG = "dd"


class Em (ElementBase):
    TAG = "em"


class Form (ElementBase):
    TAG = "form"

class Footer(ElementBase):
    TAG = 'footer'


class H1 (ElementBase):
    TAG = "h1"


class H2 (ElementBase):
    TAG = "h2"


class H3 (ElementBase):
    TAG = "h3"


class H4 (ElementBase):
    TAG = "h4"


class H5 (ElementBase):
    TAG = "h5"


class H6 (ElementBase):
    TAG = "h6"


class Head (ElementBase):
    TAG = "head"


class HTML (ElementBase):
    TAG = "html"


class Img (ElementBase):
    TAG = "img"


class Input (ElementBase):
    TAG = "input"


class Link (ElementBase):
    TAG = "link"


class Li (ElementBase):
    TAG = "li"


class Map (ElementBase):
    TAG = "map"


class Marquee (ElementBase):
    TAG = "marquee"


class Menu (ElementBase):
    TAG = "menu"


class Meta (ElementBase):
    TAG = "meta"


class Ol (ElementBase):
    TAG = "ol"


class Option (ElementBase):
    TAG = "option"


class Param (ElementBase):
    TAG = "param"


class Pre (ElementBase):
    TAG = "pre"


class P (ElementBase):
    TAG = "p"


class Q (ElementBase):
    TAG = "q"


class Script (ElementBase):
    TAG = "script"


class Select (ElementBase):
    TAG = "select"


class Span (ElementBase):
    TAG = "span"


class Strong (ElementBase):
    TAG = "strong"


class Style (ElementBase):
    TAG = "style"


class Sub (ElementBase):
    TAG = "sub"


class Sup (ElementBase):
    TAG = "sup"


class Table (ElementBase):
    TAG = "table"


class Td (ElementBase):
    TAG = "td"


class Textarea (ElementBase):
    TAG = "textarea"


class Th (ElementBase):
    TAG = "th"


class TBody (ElementBase):
    TAG = "tbody"


class THead (ElementBase):
    TAG = "thead"


class TFoot (ElementBase):
    TAG = "tfoot"


class Title (ElementBase):
    TAG = "title"


class Tr (ElementBase):
    TAG = "tr"


class Ul (ElementBase):
    TAG = "ul"

class Nav(ElementBase):
    TAG = "nav"


class Comment(ElementBase):
    """
    Explicit HTML comment
    """
    def render(self):
        yield "\n{}<!-- {} -->".format('\t' * self.indent, self.content)


class H (ElementBase):
    """
    An alternative to explicit H1... H2... etc tags.

        H(1, "Headline")

    is equivalent to 

        H1("Headline")
    """
    def __init__(self, level, content, **kwargs):
        self.TAG = "h{}".format(level)
        ElementBase.__init__(self, content, **kwargs)


#-------------------- deprecated elements ----------------------

class IsIndex (ElementBase):
    TAG = "isindex"


class Applet (ElementBase):
    TAG = "applet"


class Blink (ElementBase):
    TAG = "blink"


class Small (ElementBase):
    TAG = "small"


class Strikeout (ElementBase):
    TAG = "strikeout"


class Tt (ElementBase):
    TAG = "tt"


class U (ElementBase):
    TAG = "u"


class Var (ElementBase):
    TAG = "var"


class I (ElementBase):
    TAG = "i"


class Kbd (ElementBase):
    TAG = "kbd"


class Font (ElementBase):
    TAG = "font"


class Hr (ElementBase):
    TAG = "hr"


class Center (ElementBase):
    TAG = "center"


class B (ElementBase):
    TAG = "b"


class Basefont (ElementBase):
    TAG = "basefont"


class Big (ElementBase):
    TAG = "big"
