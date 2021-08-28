import argparse
import cpr_calc

parser = argparse.ArgumentParser()
parser.add_argument(
    "--date",
    help="Calculate possible CPR-numbers for this date, must be of format %d%m%Y",
)
parser.add_argument(
    "--gender", help="The gender for which to calculate CPR-numbers for"
)
parser.add_argument(
    "--start_date",
    help="Assigns the start date when calculating CPRs in a daterange, must be of format %d%m%Y",
)
parser.add_argument(
    "--end_date",
    help="Assigns the end date when calculating CPRs in a daterange, must be of format %d%m%Y",
)
parser.add_argument("--output", help="File to output results to, default stdout")

args = parser.parse_args()

if args.start_date and args.end_date:
    cpr_numbers = cpr_calc.possible_cpr_in_date_range(
        args.start_date, args.end_date, args.gender
    )

if args.date:
    cpr_numbers = cpr_calc.possible_cpr(args.date, args.gender)

if args.output:
    try:
        with open(args.output, "w") as f:
            for cpr in cpr_numbers:
                f.write(cpr + "\n")
    except Exception as e:
        print("Couldn't write til file: ", e)
else:
    print("\n".join(cpr_numbers))
