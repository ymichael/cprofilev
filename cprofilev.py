#!/usr/bin/env python

from bottle import route, run, template, request
from pstats import Stats
from StringIO import StringIO
import sys
import re


def read_value(self):
    value = self.stream.getvalue()
    self.stream = StringIO()
    return value


Stats.read_value = read_value


global_obj = {
    'cprofile_output': None,
    'stats_obj': None,
}

stats_template = """\
    <html>
        <head>
            <title>{{ filename }} | cProfile Results</title>
        </head>
        <body>
            <pre>{{ !stats }}</pre>
            <br/>
            <pre>{{ !callers }}</pre>
            <br/>
            <pre>{{ !callees }}</pre>
        </body>
    </html>"""


def get_flag_value(flag):
    try:
        return sys.argv[sys.argv.index(flag) + 1]
    except:
        pass
    return None

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


@route('/')
def index():
    sort = request.query.sort or 'cumulative'
    global_obj['stats_obj'].sort_stats(sort)
    global_obj['stats_obj'].print_stats(request.query.func)
    stats = global_obj['stats_obj'].read_value()

    if request.query.func:
        func = request.query.func
        global_obj['stats_obj'].print_callers(func)
        callers = global_obj['stats_obj'].read_value()

        global_obj['stats_obj'].print_callees(func)
        callees = global_obj['stats_obj'].read_value()
    else:
        callers = ''
        callees = ''

    data = {
        'filename': global_obj['cprofile_output'],
        'stats': process_stats(stats),
        'callers': process_stats(callers),
        'callees': process_stats(callees),
    }
    return template(stats_template, **data)


def usage():
    pass

def main():
    # TODO(michael): Make more robust
    flag = get_flag_value('-p')
    if flag:
        global_obj['cprofile_output'] = flag
        stats_obj = Stats(global_obj['cprofile_output'])
        stats_obj.stream = StringIO()
        global_obj['stats_obj'] = stats_obj
        run(host='localhost', port=8080)
    else:
        usage()

if __name__ == '__main__':
    main()
