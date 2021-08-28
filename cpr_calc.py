import datetime

"""
# The numbers are calculated in accordance with the modulo 11 method
# Note however that after 2007, there exists valid CPR-numbers that
# doesn't pass this check.
# https://en.wikipedia.org/wiki/Personal_identification_number_(Denmark)
"""


def _daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


def parse_date(date):
    """Get a date on the format %d%m%Y and returns a date object for that date."""
    date = str(date)
    day = date[:2]
    month = date[2:4]
    year = date[4:]
    return datetime.date(int(year), int(month), int(day))


def possible_cpr_in_date_range(start_date, end_date, gender=None):
    """Take two dates of the format %d%m%Y and returns a list of valid CPR-numbers for that given date range.

    Keyword arguments:
    start_date -- string -- the first day from which to generate CPR-numbers
    end_date -- string -- the last day from which to generate CPR-numbers
    gender -- char -- the gender of the person which CPR-number should be generated for
    """
    start_date = parse_date(start_date)
    end_date = parse_date(end_date)
    possible_cprs = []
    for single_date in _daterange(start_date, end_date):
        possible_cprs.extend(possible_cpr(single_date.strftime("%d%m%Y"), gender))
    return possible_cprs


def possible_cpr(date, gender=None):
    """Take a date of the format %d%m%Y and returns a list of valid CPR-numbers for that given date.

    Keyword arguments:
    date -- string -- the day to generate valid CPR-numbers for, must be of format %d%m%Y
    gender -- char -- the gender of the person which CPR-number should be generated for, possible options are 'm' and 'f'
    """
    checksum_coeff = [4, 3, 2, 7, 6, 5]
    date = str(date)
    year = date[4:]
    date = date[:4] + date[6:]
    datesum = 0
    for i, num in enumerate(date):
        datesum += checksum_coeff[i] * int(num)
    possible_control_numbers = generate_control_numbers(datesum, gender)
    possible_control_numbers = filter_controls(year, possible_control_numbers)
    return [date + str(x) for x in possible_control_numbers]


def generate_control_numbers(datesum, gender=None):
    """Generate a list of possible control numbers using the modulo 11 method.

    https://da.wikipedia.org/wiki/CPR-nummer#Kontrol_af_personnummer

    Keyword arguments:
    datesum -- int -- the calculated checksum for the date
    gender -- char -- the gender of the person which CPR-number should be generated for, possible options are 'm' and 'f'
    """
    increment = 2
    if gender == "m":
        start_pos = 1
    elif gender == "f":
        start_pos = 0
    else:
        # If no gender if passed generate CPR-number for both men and women
        increment = 1
        start_pos = 0

    checksum_coeff = [4, 3, 2, 1]
    possible_control_numbers = []
    for control_num in range(start_pos, 10000, increment):
        controlsum = sum(
            [
                int(x) * checksum_coeff[i]
                for i, x in enumerate("{:04d}".format(control_num))
            ]
        )
        if (controlsum + datesum) % 11 == 0:
            possible_control_numbers.append("{:04d}".format(control_num))
    return possible_control_numbers


def filter_controls(year, control_nums):
    """Filter out control numbers given the full year.

    https://da.wikipedia.org/wiki/CPR-nummer#Under_eller_over_100_%C3%A5r

    Keyword arguments:
    year -- int -- the year to filter control numbers for
    control_nums -- list[string] -- a list of control numbers to be filtered
    """
    year = int(year)
    filtered_controls = []
    possible_controls = []
    if year >= 1900 and year <= 1999:
        possible_controls.extend([0, 1, 2, 3])
    if year >= 1937 and year <= 2036:
        possible_controls.append(4)
    if year >= 2000 and year <= 2057:
        possible_controls.extend([5, 6, 7, 8])
    if year >= 1858 and year <= 1899:
        possible_controls.extend([5, 6, 7, 8])
    if year >= 1937 and year <= 2036:
        possible_controls.append(9)
    if len(possible_controls) == 0:
        raise Exception("Year wasn't recognized, must be between 1858 and 2057")
    for control_num in control_nums:
        control = int(control_num[1])
        if control in possible_controls:
            filtered_controls.append(control_num)
    return filtered_controls
