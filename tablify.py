#!/usr/bin/python
__author__ = "Mike Ross"

import sys, os, struct, fcntl, termios, tempfile, shlex, argparse, logging
import re, time
import sys, os

class Color:
    NORMAL = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    INVERSE = '\033[7m'
    FG_BLACK = '\033[30m'
    FG_BLUE = '\033[34m'
    FG_CYAN = '\033[36m'
    FG_GREEN = '\033[32m'
    FG_MAGENTA = '\033[35m'
    FG_RED = '\033[31m'
    FG_WHITE = '\033[37m'
    FG_YELLOW = '\033[33m'
    BG_BLACK = '\033[40m'
    BG_BLUE = '\033[44m'
    BG_CYAN = '\033[46m'
    BG_GREEN = '\033[42m'
    BG_MAGENTA = '\033[45m'
    BG_RED = '\033[41m'
    BG_WHITE = '\033[47m'
    BG_YELLOW = '\033[43m'
    

class App(object):
    """
    Tabularizes the given input based on whitespace.
    """

    def parseOpts(self, args):
        """Adds command line flags to the application.
        Parameters cl
                Instance of an studio.utils.cmdline object.
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('-html', help='convert to html')
        parser.add_argument(
            '--tabs',
            help='convert to tab-separated table.  This can be '
            'pasted into most spreadsheets easily.',
            action='store_true',
        )
        parser.add_argument(
            '--jira',
            help='convert to jira format',
            action='store_true',
        )
        parser.add_argument(
            '--slice',
            help='The lines to tablify.  First line is 0.  Syntax is '
            'like python slice syntax, '
            'e.g. -lines 0, -lines 1:, -lines 2:4, -lines :5, -lines -1',
        )
        parser.add_argument(
            '--inner_slice',
            help='The tokens per line to tablify.',
        )
        parser.add_argument(
            '--file',
            help='Tablify contents of the given file instead of stdin.',
        )
        parser.add_argument(
            '--shlex',
            help='Split with shlex split, not regular split',
            action='store_true',
        )
        parser.add_argument(
            '--delim',
            help='Delimiter to split lines by.',
        )
        return parser.parse_args(args=args)

    def configureOptions(self, optsNs):
        """Configures the application options.
        """
        opts = dict([(attr, getattr(optsNs, attr)) for attr in dir(optsNs)
                     if not attr.startswith("_")])
        
        return opts

    def __init__(self):
        super(App, self).__init__()
        self.log = logging.getLogger(__name__)
        self.log.addHandler(logging.StreamHandler())

    def run(self, args):
        self.opts = self.parseOpts(args)
        self.opts = self.configureOptions(self.opts)
        self.main()

    def main(self):
        """Application entry point."""

        if self.opts['file']:
            stream = open(self.opts['file'], 'r')
        else:
            stream = sys.stdin
        preLines,tableLines,postLines = self.getLines(stream)
        if self.opts['file']:
            stream.close()

        rows = self.splitPreservingColors(tableLines,
                                          delimiter=self.opts['delim'])
        if self.opts['html']:
            format = EmailFormat()
        elif self.opts['jira']:
            format = WikiFormat()
        elif self.opts['tabs']:
            format = TabSeparatedTableFormat()
        else:
            format = TerminalFormat()
        if preLines:
            print ("".join(preLines).rstrip())
        if rows:
            table = Table(rows)
            text = table.formatted(format)
            text = "\n".join([line.rstrip() for line in text.split("\n")])
            print (text)
        if postLines:
            print ("".join(postLines).rstrip())

    def getLines(self, stream):
        """
        Get all the lines from stream.
        :Parameters:
            stream : `file`
                An open file like obj.
        :Returns:
            Three string lists: lines before the table,
                                lines in the table,
                                lines after the table.
        :Rtype:
            `tuple`
        """
        lines = [line for line in stream]
        preLines = []
        postLines = []
        if self.opts['slice']:
            preLines, tableLines, postLines = self.sliceByArg(
                lines, self.opts['slice'])
        else:
            tableLines = lines
        return preLines, tableLines, postLines

    def sliceByArg(self, iterable, sliceArgString):
        """
        :Parameters:
            iterable : `iterable` 
                An iterable sequence of elements.
            sliceArgString : `str`
                A string version of a slice, e.g.
                "1", "1:", "4:6", ":-3"
        :Returns:
            Three lists:
                elements of iterables appearing before the slice.
                elements of iterables appearing within the slice.
                elements of iterables appearing beyond the slice.
        :Rtype:
            `tuple`
        """
        sliceArgs = [0, len(iterable), 1]
        for i,arg in enumerate(sliceArgString.split(":")):
            try:
                sliceArgs[i] = int(arg)
            except ValueError:
                pass
        innerElements = iterable[slice(*sliceArgs)]
        preElements   = iterable[:sliceArgs[0]]
        postElements  = iterable[sliceArgs[1]:]
        return preElements, innerElements, postElements

    def splitPreservingColors(self, lines, delimiter=None):
        """
        :Parameters:
            lines : `str list`
                A list of lines to split.
        :Returns:
            A list of lists of strings.  Each inner list is a list of
            lines split by the delimiter
        :Rtype:
            `str list list`
        """
        color = Color.NORMAL
        if self.opts['shlex']:
            splitLines = [shlex.split(line) for line in lines]
        else:
            splitLines = [line.split(delimiter) for line in lines]
        for splitLine in splitLines:
            if self.opts['inner_slice']:
                preTokens, innerTokens, postTokens = self.sliceByArg(
                    splitLine, self.opts['inner_slice'])
                innerTokens.insert(0, " ".join(preTokens))
                innerTokens.append(" ".join(postTokens))
                splitLine = innerTokens
            for i,token in enumerate(splitLine):
                if color != Color.NORMAL:
                    splitLine[i] = "%s%s" % (color, token)
                matches = re.findall("(\x1b\\[\\d+m)", token)
                if matches:
                    color = matches[-1]
        return splitLines

class Format(object):
    """
    Message objects store the data that will be reported without committing to
    an output format.  Once the data is ready to be reported, a Format class
    parses Message objects and returns a string that will present the data
    nicely in some particular format (e.g. email, wiki, terminal, etc.).
    """

    newline = NotImplementedError

    def formatMessage(self, message):
        """
        Format the given message with this format type.
        Use this when you don't know if something is a Message, str, int, or
        whatever.  If you know it's a message, you can use
        <message>.formatted(format)

        :Parameters:
            message : `Message`
                Accepts a Message or applies str() to non-Messages.
            format : `Format`
        :Returns:
            Formatted message
        :Rtype:
            `str`
        """
        if isinstance(message, Message):
            return str(message.formatted(self))
        if isinstance(message, list):
            return self.formatMessages(message)
        else:
            return str(message)

    def formatMessages(self, messages):
        """
        Convenience method to format a list of messages and return a list
        :Parameters:
            messages : `Message`
                Accepts a Message or apples str() to non-Messages.
            format : `Format`
        :Returns:
            List of formatted messages
        :Rtype:
            `str list`
        """
        return [self.formatMessage(msg) for msg in messages]

    def join(self, messages):
        """
        :Parameters:
            messages : `Message list`
        :Returns:
            Formatted list of messages, joined with the newline separator.
        :Rtype:
            `str`
        """
        return self.newline.join(self.formatMessages(messages))

    @classmethod
    def maxWidth(cls):
        """
        :Returns:
            The agreed upon maximum width of the window this will be displayed
            in, or 0 if not applicable
        :Rtype:
            `int`
        """
        return 0

class TerminalFormat(Format):
    newline = "\n"

    @classmethod
    def maxWidth(cls):
        return terminalWidth()

    @classmethod
    def bar(cls):
        return "-"*terminalWidth()

    @classmethod
    def webLink(cls, text, url):
        return text

    @classmethod
    def anchorLink(cls, text, url):
        return text

    @classmethod
    def anchor(cls, text, name):
        return text

    @classmethod
    def bold(cls, text):
        return cls.colorize(text, Color.BOLD)

    @classmethod
    def header(cls, text, level=1):
        return cls.colorize(text, Color.BOLD)

    @classmethod
    def colorize(cls, text, color):
        return "%s%s%s" % (color, text, Color.NORMAL)

    @classmethod
    def date(cls, seconds):
        """
        :Parameters:
            seconds : `int`
                posixTime
        :Returns:
            A date string in the format e.g. Wed Aug 24 12:23 format.
        :Rtype:
            `str`
        """
        timeTuple = time.localtime(seconds)
        return time.strftime("%a %b %d %H:%M", timeTuple)

class PlaintextFormat(Format):
    newline = "\n"

    def formatMessage(self, message):
        msg = super(PlaintextFormat, self).formatMessage(message)
        return decolorize(msg)

    @classmethod
    def maxWidth(cls):
        return 160

    @classmethod
    def bar(cls):
        return "-" * cls.plaintextWidth

    @classmethod
    def webLink(cls, text, url):
        return text

    @classmethod
    def anchorLink(cls, text, url):
        return text

    @classmethod
    def anchor(cls, text, name):
        return text

    @classmethod
    def bold(cls, text):
        return text

    @classmethod
    def header(cls, text, level=1):
        return text

    @classmethod
    def colorize(cls, text, color):
        return text

    @classmethod
    def date(cls, seconds):
        """
        :Parameters:
            seconds : `int`
                posixTime
        :Returns:
            A date string in the format e.g. Wed Aug 24 12:23 format.
        :Rtype:
            `str`
        """
        timeTuple = time.localtime(seconds)
        return time.strftime("%a %b %d %H:%M", timeTuple)

class TabSeparatedTableFormat(PlaintextFormat):
    pass

class EmailFormat(Format):
    newline = "<br>"

    def __init__(self):
        super(EmailFormat, self).__init__()

        # Image paths that will need to be attached to the email.
        # Keys image names, values are paths to the image on disk.
        # 
        self.imagePaths = {}
        
    def addImage(self, cid, imgPath):
        """
        :Parameters:
            cid : `str`
                Content id used to retrieve the image.
            imgPath : `str`
                Path to the image on disk
        """
        self.imagePaths[cid] = imgPath

    @classmethod
    def webLink(cls, text, url):
        return '<a href="%s">%s</a>' % (url, text)

    @classmethod
    def anchorLink(cls, text, anchor):
        return text
        # return '<a href="#%s">%s</a>' % (anchor, text)

    @classmethod
    def anchor(cls, text, anchor):
        return text
        # return '<a anchor="%s">%s</a>' % (anchor, text)

    @classmethod
    def bar(cls):
        return "<hr>"

    @classmethod
    def bold(cls, text):
        return "<b>%s</b>" % text

    @classmethod
    def header(cls, text, level=1):
        levelToFontSize = {1: 6,
                           2: 4,
                           3: 2,
                           4: 1,
                           }
            
        return '<font size="%d">%s</font>' % (levelToFontSize[level], text)

    @classmethod
    def colorize(cls, text, color):
        return "%s%s%s" % (color, text, Color.NORMAL)

    @classmethod
    def date(cls, seconds):
        """
        :Parameters:
            seconds : `int`
                posixTime
        :Returns:
            A date string in the format e.g. Wed Aug 24 12:23 format.
        :Rtype:
            `str`
        """
        timeTuple = time.localtime(seconds)
        return time.strftime("%a %b %d %H:%M", timeTuple)


class WikiFormat(Format):
    newline = "\n"

    @classmethod
    def webLink(cls, text, url):
        return "[%s|%s]" % (text, url)

    @classmethod
    def anchorLink(cls, text, anchor):
        return '[%s|#%s]' % (text, anchor)

    @classmethod
    def anchor(cls, text, anchor):
        return '{anchor:%s}%s' % (anchor, text)

    @classmethod
    def bar(cls):
        return "----"

    @classmethod
    def bold(cls, text):
        return "*%s*" % text

    @classmethod
    def header(cls, text, level=1):
        return 'h%s. %s' % (level, text)

    @classmethod
    def colorize(cls, text, color):
        return "%s%s%s" % (color, text, Color.NORMAL)

    @classmethod
    def date(cls, seconds):
        """
        :Parameters:
            seconds : `int`
                posixTime
        :Returns:
            A sortable date string, e.g. 2012-08-17 12:23:45 (Wed Aug 24) format.
        :Rtype:
            `str`
        """
        timeTuple = time.localtime(seconds)
        return time.strftime("%m-%d %H:%M:%S (%a %b %d)", timeTuple)


class Message(object):
    """
    Class to describe a basic frmt object.  All subclasses should
    support these methods.
    """
    def formatted(self, format):
        """
        format : `Format`
            A Format object that determines how this message is formatted.
        """
        raise NotImplementedError("%s has not implemented formatted" % 
                                  (self.__class__.__name__))

class WebLink(Message):
    """Link to an external webpage"""
    def __init__(self, message, url):
        super(WebLink, self).__init__()
        self.message = message
        self.url = url
        
    def formatted(self, format):
        contents = format.formatMessage(self.message)
        return format.webLink(contents, self.url)        


class Line(Message):
    """A string line with Message objects embedded."""
    def __init__(self, *args):
        self.messageList = args

    def formatted(self, format):
        msg = ""
        for message in self.messageList:
            msg += format.formatMessage(message)
        return msg

class AnchorLink(WebLink):
    """Link to another spot on the same page."""
    def formatted(self, format):
        contents = format.formatMessage(self.message)
        return format.anchorLink(contents, self.url)


class Anchor(WebLink):
    """Link to another spot on the same page."""
    def formatted(self, format):
        contents = format.formatMessage(self.message)
        return format.anchor(contents, self.url)


class Date(Message):
    """Date that will be converted to a calendar day."""
    def __init__(self, posixTime):
        """
        :Parameters:
            posixTime : `int|float`
                UTC date in seconds since epic.
        """
        self.posixTime = posixTime

    def formatted(self, format):
        return format.date(self.posixTime)


class Newline(Message):
    """Newline/break symbol"""
    def formatted(self, format):
        return format.newline


class Bar(Message):
    """Horizontal bar for headers or dividers."""
    def formatted(self, format):
        return format.bar()


class Header(Message):
    """A major header for a new section."""
    def __init__(self, message, level=1, bar=False):
        self.message = message
        self.level = level
        self.bar = bar

    def formatted(self, format):
        text = format.formatMessage(self.message)
        text = format.header(text, level=self.level)
        if self.bar:
            text = format.newline + format.bar()
        return text


class Bold(Message):
    def __init__(self, message):
        self.message = message

    def formatted(self, format):
        text = format.formatMessage(self.message)
        return format.bold(text)


def timeString(seconds):
    """
    :Parameters:
        seconds : `int`
    :Returns:
        A string in <hour>:<minute>:<second> format, or <minute>:<second>
        if less than 1 hour.
    :Rtype:
        `str`
    """
    sec     = seconds %  60
    hours   = seconds // 3600
    minutes = (seconds // 60) - (hours * 60)
    if hours:
        return "%d:%.2d:%.2d" % (hours, minutes, sec)
    return "%d:%.2d" % (minutes, sec)

def dateString(seconds):
    """
    :Parameters:
        seconds : `int`
            posixTime
    :Returns:
        A sortable date string, e.g. 2012-08-17 12:23:45 (Wed Aug 24) format.
    :Rtype:
        `str`
    """
    timeTuple = time.localtime(seconds)
    return time.strftime("%m-%d %H:%M:%S (%a %b %d)", timeTuple)

def terminalWidth(default=70):
    """
    :Returns:
        The width of the terminal, or default if not in a terminal
    :Rtype:
        `int`
    """
    try:
        return struct.unpack("HHHH", 
                             fcntl.ioctl(sys.stdout.fileno(),
                                         termios.TIOCGWINSZ,
                                         struct.pack("HHHH", 0, 0, 0, 0)))[1]
    except IOError, e:
        return default

colors = [Color.BG_BLUE,    Color.BG_CYAN, Color.BG_GREEN, 
          Color.BG_MAGENTA, Color.BG_RED,  Color.BG_WHITE,
          Color.BG_YELLOW,  Color.BOLD,    Color.FG_BLACK,
          Color.FG_BLUE,    Color.FG_CYAN, Color.FG_GREEN,
          Color.FG_MAGENTA, Color.FG_RED,  Color.FG_WHITE,
          Color.FG_YELLOW,  Color.INVERSE, Color.NORMAL,
          Color.UNDERLINE]

def colorize(text, color):
    """Wrap the text in the given color, leaving following text normal.
    :Parameters:
        text : `str`
    :Returns:
        Text color frmt
    :Rtype:
        `str`
    """
    return "%s%s%s" % (color, text, Color.NORMAL)


def decolorize(text):
    """Strip color codes from text.
    :Parameters:
        text : `str`

    :Returns:
        Text without color frmt
    :Rtype:
        `str`
    """
    return re.sub("\x1b\\[\\d+m", "", text)
    
def emphasizeNumbers(string):
    """
    :Parameters:
        string : `str`
            A string to emphasize numbers in
    :Returns:
        The string with all numbers emphasized for wiki markup.
    :Rtype:
        `str`
    """
    return re.sub(r"(\d+)", r"*\1*", string)

def wrap(message, columns):
    """
    :Parameters:
        message : `str`
            The message to wrap
        columns : `int`
            The number of columns to wrap to.
    :Returns:
        The original message wrapped at the given column width split
        into a list of lines that wrap at the given column.  Attempts
        to leave any special formatting intact, and does not count those
        characters in your column count.
    :Rtype:
        `str list`
    """
    # Some constants
    # 
    normal     = Color.NORMAL
    formatting = ""
    whiteSpace = (' ', '\n', '\r', '\t')
    newLines   = ('\n', '\r')

    # State within the loop.
    # 
    lines  = []
    line   = ""
    word   = ""
    curCol = 0
    i      = 0

    while i < len(message):
        char = message[i]

        # If the char is a formatting char, record it and continue.
        # 
        if char == '\x1b':
            tmpWord = message[i:i+12]
            clr = [clr for clr in colors if tmpWord.startswith(clr)]
            match = re.search("(\x1b\\[\\d+m)", tmpWord)
            if match:
                clr = match.groups()[0]
                formatting += clr
                word += clr
                i += len(clr)
                continue

        # Whitespace
        # 
        elif char in whiteSpace:
            if char in newLines:
                line += word
                if formatting:
                    line += normal
                lines.append(line)
                line = "" + formatting
                curCol = 0
            else:
                line += word + char
                curCol += 1
            word = ""

        # Regular char
        # 
        else:
            curCol += 1
            if curCol > columns:
                if formatting:
                    line += normal
                lines.append(line)
                line = "" + formatting       
                curCol = 0
            word += char

        i += 1

    # Finish
    # 
    if word:
        line += word
    if line:
        if formatting:
            line += normal
        lines.append(line)
    return lines
        
class Table(Message):
    """
    An abstraction for a table, so that tables can be output to wiki, email,
    html, or terminal format more easily.
    """
    def __init__(self, rows=[], header=None, title=None,  colWidths=[], sortable=True):
        """
        :Parameters:
            rows : `str list`
            header : `str list`
            colWidths : `int list`
                If colWidths is given, plainText columns will use these widths
        """
        self.rows = rows
        self.header = header
        self.title = title
        self._colWidths = colWidths
        self.sortable = sortable

    def formatted(self, format):
        """
        :Parameters:
            format : `FORMAT_*`
                The format type from frmt
        :Returns:
            This table formatted in the given format.
        :Rtype:
            `str`
        """
        if isinstance(format, EmailFormat):
            return self.getEmail(format)
        elif isinstance(format, WikiFormat):
            return self.getWiki(format)
        elif isinstance(format, (TabSeparatedTableFormat)):
            return self.getTabSeparated(format)
        elif isinstance(format, (TerminalFormat,PlaintextFormat)):
            return self.getText(format)
        raise ValueError("Unrecognized Format: %s" % (str(format)))

    def getWiki(self, format):
        """
        :Parameters:
            format : `Format`
        :Returns:
            The markup for a wiki table.
        :Rtype:
            `str`
        """
        messages = []
        colWidths = self.colWidths()
        if self.title:
            messages.append("h3. %s" % format.formatMessage(self.title))
        # messages.append(self._getWikiTableInit())
        if self.header:
            headerCells = format.formatMessages(self.header)
            headerCells = [cell.ljust(colWidths[i])
                           for i,cell in enumerate(headerCells)]
            messages.append("||%s||" % "||".join(headerCells))
        for row in self.rows:
            cells = format.formatMessages(row)
            cells = [cell.ljust(colWidths[i]) for i,cell in enumerate(cells)]
            messages.append("|%s|" % ("|".join(cells)))
        # messages.append("{table-plus}")
        message = "\n".join(messages)
        return message

    def _getWikiTableInit(self):
        """
        :Returns:
            Line to initialize a wiki table based on this table's action.s
        :Rtype:
            `str`
        """
        options = [
            "border=1",
            "enableHighlighting=false",
            "columnTypes=S,S,S,S,S,S,S",
            ]
        if self.sortable:
            options.append("sortIcon=true")
        else:
            options.append("enableSorting=false")
        line = "{table-plus:%s}" % "|".join(options)
        return line

    def getEmail(self, format):
        """
        :Parameters:
            format : `Format`
        """
        messages = []

        if self.title:
            messages.append("<b>%s</b><br>" % format.formatMessage(self.title))

        # messages.append('<table collapse="1">')
        messages.append('<table frame="VOID" rules="NONE" border="1" cellspacing="0">')
        headerTag = '<th style="border-top:1px solid #707070;border-bottom:1px solid #707070;border-left:1px solid #707070;border-right:0px solid #707070" height="19" align="LEFT" bgcolor="#D0D0D0"><font size="3">'
        joiner = "</font></th>%s" % headerTag
        if self.header:
            headerCells = format.formatMessages(self.header)
            messages.append("<tr>%s%s</font></th></tr>" % 
                            (headerTag, joiner.join(headerCells)))

        # tdTag = "<td style='border: thin solid #cccccc'>"
        tdTag = '<td style="border-top:0px solid #707070;border-bottom:1px solid #707070;border-left:1px solid #707070;border-right:0px solid #707070" height="19">'
        # tdTag = "<td>"
        joiner = "</td>\n%s" % tdTag
        for row in self.rows:
            cells = format.formatMessages(row)
            messages.append("<tr>%s%s</td></td></tr>\n" % 
                            (tdTag, (joiner.join(cells))))

        messages.append("</table>")
        message = "\n".join(messages)
        return message

    def getTabSeparated(self, format, colored=False):
        messages = []
        if self.title:
            messages.append(format.formatMessage(self.title))
        for row in self.allRows():
            cells = [format.formatMessage(c).replace("\t", "") for c in row]
            messages.append("\t".join(cells))
        message = format.newline.join(messages)
        return message

    def getText(self, format, colored=True):
        """
        :Parameters:
            format : `Format`
            colored : `bool`
                If colored is False, return without ansi colors.
        """
        
        messages = []

        colWidths = self.colWidths()
        
        if self.title:
            messages.append(format.bold(format.formatMessage(self.title)))

        # Preformat all cells to allow wrapping.
        # 
        wrappedRows = []
        allRows = self.allRows()
        for ri,row in enumerate(allRows):
            wrappedRow = []
            for ci,cell in enumerate(row):
                wrappedRow.append(self.wrapCell(ri, ci, format))
            wrappedRows.append(wrappedRow)

        # Header Row
        # 
        if self.header:
            ri = 0
            row = wrappedRows[0]
            numCols = len(row)
            numLines = max([len(row[i]) for i in range(numCols)])
            for lineNum in range(numLines):
                line = ""
                for ci in range(numCols):
                    contents = wrappedRows[ri][ci]
                    if lineNum < len(contents):
                        colWidth = colWidths[ci]
                        cellContents = contents[lineNum]
                        extraWidth = (len(cellContents) -
                                      len(decolorize(cellContents)))
                        colWidth = colWidths[ci] + extraWidth
                        line += "%s " % contents[lineNum].ljust(colWidth)
                    else:
                        line += "%s " % ("".ljust(colWidths[ci]))
                messages.append(line)

        # Data Rows
        # 
        ri = 1 if self.header else 0
        for row in self.rows:
            row = wrappedRows[ri]
            numCols = len(row)
            numLines = max([len(row[i]) for i in range(numCols)] or [1])
            for lineNum in range(numLines):
                line = ""
                for ci in range(numCols):
                    contents = wrappedRows[ri][ci]
                    if lineNum < len(contents):
                        colWidth = colWidths[ci]
                        cellContents = contents[lineNum]
                        extraWidth = (len(cellContents) -
                                      len(decolorize(cellContents)))
                        colWidth = colWidths[ci] + extraWidth
                        line += "%s " % contents[lineNum].ljust(colWidth)
                    else:
                        line += "%s " % ("".ljust(colWidths[ci]))
                messages.append(line)
            ri += 1

        # # Data Rows
        # # 
        # for row in self.rows:
        #     rowMessage = ""
        #     for i,cell in enumerate(row):
        #         cellMessage = format.formatMessage(cell)
        #         rowMessage += "%s " % cellMessage.ljust(colWidths[i])
        #     messages.append(rowMessage)

        message = format.newline.join(messages)
        return message
        
    def wrapCell(self, row, col, format):
        """
        :Parameters:
            row : `int`
                Row of the cell.  0 is the header if it exists and the first
                data row otherwise.
            col : `int`
                Column of the cell.  0 is the first column.
            format : `Format`
        :Returns:
            The message in the specified cell, split into lines wrapped to
            a desired width.
        :Rtype:
            `str list`
        """
        allRows = self.allRows()
        cell = allRows[row][col]
        width = self.colWidth(col)
        message = format.formatMessage(cell)
        if self.header and row == 0:
            message = format.bold(message)
        return wrap(message, width)

    def colWidths(self):
        """
        :Returns:
            A list of the column widths for this table.
        :Rtype:
            `int list`
        """
        numCols = self.numCols()
        return [self.colWidth(i) for i in range(numCols)]

    def setColWidth(self, col, width):
        """Set the $column to the max width of $width
        :Parameters:
            col : `int`
            width : `int`
        """
        # Expand the list of explicit column widths if necessary.
        # 
        difference = col - len(self._colWidths) + 1
        if difference > 0:
            self._colWidths += [0] * (difference + 1)
        self._colWidths[col] = width

    def numCols(self):
        """
        :Returns:
            The number of columns in this table.
        :Rtype:
            `int`
        """
        rowLengths = [len(row) for row in self.allRows()]
        if not rowLengths:
            return 0
        return max(rowLengths)

    def rowHeight(self, rowIndex):
        """
        :Returns:
            The number of lines a column spans.  If the text in any cells
            span more than that row's width, wrap the text.
            0 is the header row if it exists and the first data row
            otherwise.
        :Rtype:
            `int`
        """
        maxHeight = 1
        for row in self.allRows():
            for colIndex,cell in enumerate(row):
                maxWidth = self.colWidth(colIndex)
                contents = decolorize(cell)
                if len(contents) > maxWidth:
                    wrapped = wrap(contents, maxWidth)
                    maxHeight = max(maxHeight,len(wrapped.split('\n')))
        return maxHeight

    def colWidth(self, index):
        """
        :Parameters:
            index : `int`
                The index of this column
        :Returns:
            The width of this column in characters.
        :Rtype:
            `int`
        """

        # If a nonzero columnWidth is listed in self._colWidths, use that.
        # Otherwise, determine the width of the longest element.
        # 
        if index < len(self._colWidths) and self._colWidths[index]:
            return self._colWidths[index]
            
        rows = self.allRows()
        cellWidths = []

        # If we're looking up colWidth, we assume we're using a
        # terminal.
        # 
        format = TerminalFormat()

        for row in rows:
            if index < len(row):
                # Format the cell as a terminal string and decolorize it
                # to avoid counting ansi coloring.
                # 
                cellString = format.formatMessage(row[index])
                size = len(decolorize(cellString))
                cellWidths.append(size)
            else:
                cellWidths.append(0)

        if not cellWidths:
            maxWidth = 0
        else:
            maxWidth = max(cellWidths)

        # Cache so we don't do this insane lookup everytime.
        self.setColWidth(index, maxWidth)

        return maxWidth

    def allRows(self):
        if self.header:
            return [self.header] + self.rows
        return self.rows[:]


# Globally defined formats.
# 
FORMAT_DEFAULT = TerminalFormat
# FORMAT_WIKI      = WikiFormat()
# FORMAT_TERM      = TerminalFormat()
# FORMAT_EMAIL     = EmailFormat()
# FORMAT_PLAINTEXT = PlaintextFormat()
# FORMAT_DEFAULT   = FORMAT_TERM

if __name__ == '__main__':
    App().run(sys.argv[1:])

