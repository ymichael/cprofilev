# cprofilev
Thin wrapper for viewing python cProfile output

__Super flaky implementation.__

## Dependencies
- bottle (`pip install bottle`)

## Usage
1. run python script with `-m cProfile -o output_file` flags

```
# -o out.profile specifies where the output of cprofile will be saved.
$ python -m cProfile -o /path/to/out.profile your_script.py ...
```

2. run cprofilev on the output file.

```
$ ./cprofilev.py -p /path/to/out.profile
```

3. navigate to http://localhost:8080

## TODO
- Clean up code
- Write tests
- Publish as a python package
