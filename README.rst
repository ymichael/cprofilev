=========
cprofilev
=========
An easier way to use `cProfile <https://docs.python.org/2/library/profile.html>`_.
______________________________

about
*****
cprofilev runs and profiles a given python program and outputs a simple html view of the statistics collected.

See: http://ymichael.com/2014/03/08/profiling-python-with-cprofile.html on how to make sense of the profiled statistics.

installation
*****
*on most UNIX-like systems, you'll probably need to run the following `install` command as root or by using sudo*

::

  pip install cprofilev

quickstart
**********

1. Simply run your python program in with the **-m cprofilev** flag.

::

  $ python -m cprofilev /path/to/python/program ...


2. Navigate to http://localhost:4000 to view profile statistics of your python program (even while its still running!)


Alternatively you can output view cprofile output using the **-f flag**:

::

  # NOTE this is cProfile not cprofilev
  $ python -m cProfile -o /path/to/save/output /path/to/python/program ...
  $ cprofilev -f /path/to/save/output

usage
*****

::

  usage: cprofilev.py [--version] [-a ADDRESS] [-p PORT] scriptfile [arg] ...

  An easier way to use cProfile.

  positional arguments:
    scriptfile            The python script file to run and profile.

  optional arguments:
    -h, --help            show this help message and exit
    --version             show program's version number and exit
    -a ADDRESS, --address ADDRESS
                          The address to listen on. (defaults to 127.0.0.1).
    -p PORT, --port PORT  The port to listen on. (defaults to 4000).
    -f FILE, --file FILE  cProfile output to view.
                          If specified, the scriptfile provided will be ignored.


Dependencies
*****
`bottle <http://bottlepy.org>`_: used for serving the html page.
