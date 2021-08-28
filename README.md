# CPR wordlist generator

CPR wordlist generator is a simple CLI tool made for generating valid CPR-numbers for a given date or a given date range.

## Getting Started

Getting started requires nothing more than downloading the repository:
```
git clone git@github.com:emil-muller/CPR-wordlist-generator.git
```

## Flags
`--date` - Generates all valid CPR-numbers for the given date. Note that the date must be of the format `%d%m%Y`.

`--gender` - If this flag is set, only CPR-numbers for that specific gender is calculated. Possible values are `m` and `f`

`--start_date` - Sets the start date of the date range when generating CPRs within a given range. Note that the date must be of the format `%d%m%Y`.

`--end_date` - Sets the end date of the date range when generating CPRs within a given range. Note that the end date is not included in the date range. Note that the date must be of the format `%d%m%Y`.

`--output` - The name of file to save the output to. If no output flag is set, the output is printed to stdout.

### Examples
```
python3 CPR.py --date 01071997
```
Generates all valid CPR-numbers for the day 1st of July, 1997.

```
python3 CPR.py --start_date 20072001 --end_date 05122002 --gender m
```
Generates all valid CPR-numbers for males in the date range 20th of July 2001 to 5th of December 2002.
