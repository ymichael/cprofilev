#!/usr/bin/env python

from bottle import Bottle, template, request
from pstats import Stats
from StringIO import StringIO
import argparse
import re

VERSION = '0.1.2'

__doc__ = """\
A thin wrapper for viewing python cProfile output.

It provides a simple html view of the pstats.Stats object that is generated
from when a python script is run with the -m cProfile flag.

"""


stats_template = """\
    <html>
        <head>
            <title>{{ filename }} | cProfile Results</title>
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


def get_href(key, val):
    href = '?'
    query = dict(request.query)
    query[key] = val
    for key in query.keys():
        href += '%s=%s&' % (key, query[key])
    return href[:-1]


class CProfileVStats(object):
    """Wrapper around pstats.Stats class."""
    def __init__(self, output_file):
        self.output_file = output_file
        self.obj = Stats(output_file)
        self.reset_stream()

    def reset_stream(self):
        self.obj.stream = StringIO()

    def read(self):
        value = self.obj.stream.getvalue()
        self.reset_stream()

        # process stats output
        value = self._process_header(value)
        value = self._process_lines(value)
        return value

    IGNORE_FUNC_NAMES = ['function', '']
    STATS_LINE_REGEX = r'(.*)\((.*)\)$'
    HEADER_LINE_REGEX = r'ncalls|tottime|cumtime'
    DEFAULT_SORT_ARG = 'cumulative'
    SORT_ARGS = {
        'ncalls': 'calls',
        'tottime': 'time',
        'cumtime': 'cumulative',
        'filename': 'module',
        'lineno': 'nfl',
    }

    @classmethod
    def _process_header(cls, output):
        result = []
        lines = output.splitlines(True)
        for idx, line in enumerate(lines):
            match = re.search(cls.HEADER_LINE_REGEX, line)
            if match:
                for key, val in cls.SORT_ARGS.iteritems():
                    url_link = template(
                        "<a href='{{ url }}'>{{ key }}</a>",
                        url=get_href(SORT_KEY, val),
                        key=key)
                    line = line.replace(key, url_link)
                lines[idx] = line
                break
        return ''.join(lines)

    @classmethod
    def _process_lines(cls, output):
        lines = output.splitlines(True)
        for idx, line in enumerate(lines):
            match = re.search(cls.STATS_LINE_REGEX, line)
            if match:
                prefix = match.group(1)
                func_name = match.group(2)

                if func_name not in cls.IGNORE_FUNC_NAMES:
                    url_link = template(
                        "<a href='{{ url }}'>{{ func_name }}</a>",
                        url=get_href(FUNC_NAME_KEY, func_name),
                        func_name=func_name)

                    lines[idx] = template(
                        "{{ prefix }}({{ !url_link }})\n",
                        prefix=prefix, url_link=url_link)

        return ''.join(lines)

    def show(self, restriction=''):
        self.obj.print_stats(restriction)
        return self

    def show_callers(self, func_name):
        self.obj.print_callers(func_name)
        return self

    def show_callees(self, func_name):
        self.obj.print_callees(func_name)
        return self

    def sort(self, sort=''):
        sort = sort or self.DEFAULT_SORT_ARG
        self.obj.sort_stats(sort)
        return self


class CProfileV(object):
    def __init__(self, cprofile_output, port=4000, quiet=True):
        self.cprofile_output = cprofile_output
        self.port = port
        self.quiet = quiet
        self.app = Bottle()
        self.stats_obj = CProfileVStats(self.cprofile_output)

        # init route.
        self.app.route('/')(self.route_handler)


    def route_handler(self):
        func_name = request.query.get(FUNC_NAME_KEY) or ''
        sort = request.query.get(SORT_KEY) or ''

        stats = self.stats_obj.sort(sort).show(func_name).read()
        if func_name:
            callers = self.stats_obj.sort(sort).show_callers(func_name).read()
            callees = self.stats_obj.sort(sort).show_callees(func_name).read()
        else:
            callers = ''
            callees = ''

        data = {
            'filename': self.cprofile_output,
            'stats': stats,
            'callers': callers,
            'callees': callees,
        }
        return template(stats_template, **data)


    def start(self):
        """Starts bottle server."""
        print 'cprofilev server listening on port %s' % self.port
        self.app.run(host='localhost', port=self.port, quiet=self.quiet)


def main():
    parser = argparse.ArgumentParser(
        description='Thin wrapper for viewing python cProfile output.')

    parser.add_argument('--version', action='version', version=VERSION)

    parser.add_argument('-v', '--verbose', action='store_const', const=True)
    parser.add_argument('-p', '--port', type=int, default=4000,
        help='specify the port to listen on. (defaults to 4000)')
    parser.add_argument('cprofile_output', help='The cProfile output to view.')
    args = vars(parser.parse_args())

    port = args['port']
    cprofile_output = args['cprofile_output']
    quiet = not args['verbose']

    CProfileV(cprofile_output, port, quiet).start()


if __name__ == '__main__':
    main()
