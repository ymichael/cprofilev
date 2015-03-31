#!/usr/bin/env python

import argparse
import bottle
import cProfile
import os
import pstats
import re
import sys
import threading

try:
    from cStringIO import StringIO
except ImportError:
    try:
        from StringIO import StringIO
    except ImportError:
        # Python 3 compatibility.
        from io import StringIO


VERSION = '1.0.5'

__doc__ = """\
An easier way to use cProfile.

Outputs a simpler html view of profiled stats.
Able to show stats while the code is still running!

"""


STATS_TEMPLATE = """\
<html>
    <head>
        <title>{{ title }} | cProfile Results</title>
    </head>
    <body>
        <pre>{{ !stats }}</pre>

        % if callers:
            <h2>Called By:</h2>
            <pre>{{ !callers }}</pre>

        % if callees:
            <h2>Called:</h2>
            <pre>{{ !callees }}</pre>
    </body>
</html>"""


SORT_KEY = 'sort'
FUNC_NAME_KEY = 'func_name'


class Stats(object):
    """Wrapper around pstats.Stats class."""

    IGNORE_FUNC_NAMES = ['function', '']
    DEFAULT_SORT_ARG = 'cumulative'
    SORT_ARGS = {
        'ncalls': 'calls',
        'tottime': 'time',
        'cumtime': 'cumulative',
        'filename': 'module',
        'lineno': 'nfl',
    }

    STATS_LINE_REGEX = r'(.*)\((.*)\)$'
    HEADER_LINE_REGEX = r'ncalls|tottime|cumtime'

    def __init__(self, profile_output=None, profile_obj=None):
        self.profile = profile_output or profile_obj
        self.stream = StringIO()
        self.stats = pstats.Stats(self.profile, stream=self.stream)

    def read_stream(self):
        value = self.stream.getvalue()
        self.stream.seek(0)
        self.stream.truncate()
        return value

    def read(self):
        output = self.read_stream()
        lines = output.splitlines(True)
        return "".join(map(self.process_line, lines))

    @classmethod
    def process_line(cls, line):
        # Format header lines (such that clicking on a column header sorts by
        # that column).
        if re.search(cls.HEADER_LINE_REGEX, line):
            for key, val in cls.SORT_ARGS.items():
                url_link = bottle.template(
                    "<a href='{{ url }}'>{{ key }}</a>",
                    url=cls.get_updated_href(SORT_KEY, val),
                    key=key)
                line = line.replace(key, url_link)
        # Format stat lines (such that clicking on the function name drills into
        # the function call).
        match = re.search(cls.STATS_LINE_REGEX, line)
        if match:
            prefix = match.group(1)
            func_name = match.group(2)
            if func_name not in cls.IGNORE_FUNC_NAMES:
                url_link = bottle.template(
                    "<a href='{{ url }}'>{{ func_name }}</a>",
                    url=cls.get_updated_href(FUNC_NAME_KEY, func_name),
                    func_name=func_name)
                line = bottle.template(
                    "{{ prefix }}({{ !url_link }})\n",
                    prefix=prefix, url_link=url_link)
        return line

    @classmethod
    def get_updated_href(cls, key, val):
        href = '?'
        query = dict(bottle.request.query)
        query[key] = val
        for key in query.keys():
            href += '%s=%s&' % (key, query[key])
        return href[:-1]

    def show(self, restriction=''):
        self.stats.print_stats(restriction)
        return self

    def show_callers(self, func_name):
        self.stats.print_callers(func_name)
        return self

    def show_callees(self, func_name):
        self.stats.print_callees(func_name)
        return self

    def sort(self, sort=''):
        sort = sort or self.DEFAULT_SORT_ARG
        self.stats.sort_stats(sort)
        return self


class CProfileV(object):
    def __init__(self, profile, title, address='127.0.0.1', port=4000):
        self.profile = profile
        self.title = title
        self.port = port
        self.address = address

        # Bottle webserver.
        self.app = bottle.Bottle()
        self.app.route('/')(self.route_handler)

    def route_handler(self):
        self.stats = Stats(self.profile)

        func_name = bottle.request.query.get(FUNC_NAME_KEY) or ''
        sort = bottle.request.query.get(SORT_KEY) or ''

        self.stats.sort(sort)
        callers = self.stats.show_callers(func_name).read() if func_name else ''
        callees = self.stats.show_callees(func_name).read() if func_name else ''
        data = {
            'title': self.title,
            'stats': self.stats.sort(sort).show(func_name).read(),
            'callers': callers,
            'callees': callees,
        }
        return bottle.template(STATS_TEMPLATE, **data)

    def start(self):
        self.app.run(host=self.address, port=self.port, quiet=True)


def main():
    parser = argparse.ArgumentParser(
        description='An easier way to use cProfile.',
        usage='%(prog)s [--version] [-a ADDRESS] [-p PORT] scriptfile [arg] ...',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--version', action='version', version=VERSION)
    parser.add_argument('-a', '--address', type=str, default='127.0.0.1',
        help='The address to listen on. (defaults to 127.0.0.1).')
    parser.add_argument('-p', '--port', type=int, default=4000,
        help='The port to listen on. (defaults to 4000).')
    # Preserve v0 functionality using a flag.
    parser.add_argument('-f', '--file', type=str,
        help='cProfile output to view.\nIf specified, the scriptfile provided will be ignored.')
    parser.add_argument('remainder', nargs=argparse.REMAINDER,
        help='The python script file to run and profile.',
        metavar="scriptfile")

    args = parser.parse_args()
    if not sys.argv[1:]:
        parser.print_help()
        sys.exit(2)

    info = '[cProfileV]: cProfile output available at %s:%s' % \
        (args.address, args.port)

    # v0 mode: Render profile output.
    if args.file:
        print(info)
        cprofilev = CProfileV(args.file, title=args.file, address=args.address, port=args.port)
        cprofilev.start()
        return

    # v1 mode: Start script and render profile output.
    sys.argv[:] = args.remainder
    if len(args.remainder) < 0:
        parser.print_help()
        sys.exit(2)

    print(info)
    profile = cProfile.Profile()
    progname = args.remainder[0]
    sys.path.insert(0, os.path.dirname(progname))
    with open(progname, 'rb') as fp:
        code = compile(fp.read(), progname, 'exec')
    globs = {
        '__file__': progname,
        '__name__': '__main__',
        '__package__': None,
    }

    # Start the given program in a separate thread.
    progthread = threading.Thread(target=profile.runctx, args=(code, globs, None))
    progthread.setDaemon(True)
    progthread.start()

    cprofilev = CProfileV(profile, title=progname, address=args.address, port=args.port)
    cprofilev.start()


if __name__ == '__main__':
    main()
