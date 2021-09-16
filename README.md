## cronparser

A Crontab Parser. The parser requires python 3.8 or later. Allowed syntax:

Hour,minute,month and day of the month:

- \*
- \*/3
- 10-13
- 11,22,45

Day of the week (0=sunday):

- 1,2,3
- 1-5
- MON-TUE
- mon,tue
- 1/3
- 1/wed

### installation

Install the package from the repo:

`pip3 install git+https://github.com/albertocalderari/cron-parser`

### Usage

Command: `cronparser -h`

Output:

```
usage: cronparser [-h] cron_expr

A CLI to parse a cron command

positional arguments:
  cron_expr   The cron expression in quotes i.e. */30 0 1,15 * 1-3

optional arguments:
  -h, --help  show this help message and exit
```

Command: `cronparser  "5 1 * * 1 /bin/sh"`

Output:

```
minute:       5
hour:         1
day of month: 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31
month:        1 2 3 4 5 6 7 8 9 10 11 12
day of week:  1
command:      /bin/sh
```

Command: `cronparser  "65 1 * * 1 /bin/sh"`

Output:

```
Traceback (most recent call last):
  File "/Users/alberto/venvs/cron-parser/bin/cronparser", line 33, in <module>
    sys.exit(load_entry_point('cronparser==0.1.0', 'console_scripts', 'cronparser')())
  File "/Users/alberto/venvs/cron-parser/lib/python3.8/site-packages/cronparser/main.py", line 23, in main
    raise InvalidCron(error)
cronparser.models.exceptions.InvalidCron: Errors:
Location: minute Errors: Value must be within 0 and 59
```

### limitations

- Currently, we do not support commands with spaces.
- The crontab elements need to be separated with exactly one space
- The command needs to be separated from the crontab with exactly one space

### To dev

Setup a virtual env and run `pip install -r requirements-dev.txt`.