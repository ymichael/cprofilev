=====
cprofilev
=====
A thin wrapper for viewing python's cProfile output.
_____

about
*****
cprofilev is a  thin wrapper for viewing python's cProfile output. It provides
a simple html view of the pstats.Stats object that is generated.

See: http://ymichael.com/2014/03/08/profiling-python-with-cprofile.html

installation
*****
*on most UNIX-like systems, you'll probably need to run the following
`install` command as root or by using sudo*

**pip**

::

  pip install cprofilev

quickstart
*****
1. Simply pass the cprofile output file as an argument to `cprofilev`

::

  $ cprofilev /path/to/cprofile/output


2. Navigate to http://localhost:4000

usage
*****

::

  $ cprofilev --help
  usage: cprofilev.py [-h] [--version] [-v] [-a ADDRESS] [-p PORT] cprofile_output

  Thin wrapper for viewing python cProfile output.

  positional arguments:
    cprofile_output       The cProfile output to view.

    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      -v, --verbose
      -a ADDRESS, --address ADDRESS
                        specify the address to listen on. (defaults to
                        127.0.0.1)
      -p PORT, --port PORT  specify the port to listen on. (defaults to 4000)


Dependencies
*****
`bottle <http://bottlepy.org>`_: used for serving the html page.
