#!/usr/bin/env python

from bottle import Bottle, template, request
from pstats import Stats
from StringIO import StringIO
import argparse
import re


stats_template = """\
    <html>
        <head>
            <title>cProfile Results</title>
        </head>
        <body>
            <pre>{{ !stats }}</pre>
            <br/>
            <pre>{{ !callers }}</pre>
            <br/>
            <pre>{{ !callees }}</pre>
        </body>
    </html>"""

SORT_ARGS = ['ncalls', 'cumtime', 'tottime', 'filename']


def get_href(key, val):
    href = '?'
    request.query[key] = val
    for key in request.query.keys():
        href += '%s=%s&' % (key, request.query.get(key))
    return href[:-1]


def process_stats(stats):
    result = []
    pattern = r'(.*)\((.*)\)$'
    for line in stats.split('\n'):
        if 'ncalls' in line:
            for sort_arg in SORT_ARGS:
                line = line.replace(sort_arg,
                    '<a href="%s">%s</a>' %
                    (get_href('sort', sort_arg), sort_arg))
        match = re.search(pattern, line)
        if match and match.group(2) not in ['function', '']:
            line = match.group(1) + \
                '(<a href="%s">%s</a>)' % \
                (get_href('func', match.group(2)), match.group(2))
        result.append(line)
    return '\n'.join(result)

# @route('/')
# def index():
#     sort = request.query.sort or 'cumulative'
#     global_obj['stats_obj'].sort_stats(sort)
#     global_obj['stats_obj'].print_stats(request.query.func)
#     stats = global_obj['stats_obj'].read_value()
#
#     if request.query.func:
#         func = request.query.func
#         global_obj['stats_obj'].print_callers(func)
#         callers = global_obj['stats_obj'].read_value()
#
#         global_obj['stats_obj'].print_callees(func)
#         callees = global_obj['stats_obj'].read_value()
#     else:
#         callers = ''
#         callees = ''
#
#     data = {
#         'filename': global_obj['cprofile_output'],
#         'stats': process_stats(stats),
#         'callers': process_stats(callers),
#         'callees': process_stats(callees),
#     }
#     return template(stats_template, **data)


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
        return value

    def show(self, restriction=''):
        self.obj.print_stats(restriction)
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
        stats = self.stats_obj.show().read()
        callers = ''
        callees = ''
        data = {
            'stats': process_stats(stats),
            'callers': process_stats(callers),
            'callees': process_stats(callees),
        }
        return template(stats_template, **data)


    def start(self):
        """Starts bottle server."""
        self.app.run(host='localhost', port=self.port, quiet=self.quiet)


def main():
    parser = argparse.ArgumentParser(
        description='Thin wrapper for viewing python cProfile output.')
    # TODO(michael): Read version from some config file.
    parser.add_argument('--version', action='version', version='0.0.1')
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
