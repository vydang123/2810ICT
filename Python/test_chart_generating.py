import csv
def get_trend_data(offence_code: str, start_month_year: str, end_month_year: str) -> (list, list):
    with open("penalty_data_set_2.csv", "r") as file:
        reader = csv.reader(file)
        headers = next(reader)
        start_month_year_num = int(start_month_year.split('/')[1] + start_month_year.split('/')[0])
        end_month_year_num = int(end_month_year.split('/')[1] + end_month_year.split('/')[0])
        filtered_data = [row for row in reader if row[2] == offence_code and start_month_year_num <= int(
            row[1].split('/')[-1] + row[1].split('/')[1]) <= end_month_year_num]

    dates = [row[1] for row in filtered_data]
    values = [int(row[24]) for row in filtered_data]  # Assuming 24th column has the trend values

    # Sum values by date (month/year)
    datewise_values = {}
    for date, value in zip(dates, values):
        if date in datewise_values:
            datewise_values[date] += value
        else:
            datewise_values[date] = value

    sorted_dates = sorted(datewise_values.keys(), key=lambda x: (int(x.split('/')[-1]), int(x.split('/')[1])))
    sorted_values = [datewise_values[date] for date in sorted_dates]

    return sorted_dates, sorted_values


def test_get_trend_data():
    offence_code = "74703"  # Replace with an actual valid offense code
    start_month_year = "01/2012"
    end_month_year = "12/2017"

    dates, values = get_trend_data(offence_code, start_month_year, end_month_year)

    # Check if dates and values are non-empty lists
    assert dates, "Dates list is empty"
    assert values, "Values list is empty"

    # Ensure dates and values have the same length
    assert len(dates) == len(values), "Length of dates and values lists differ"

    # Ensure dates are sorted
    assert dates == sorted(dates, key=lambda x: (
    int(x.split('/')[-1]), int(x.split('/')[1]))), "Dates are not sorted correctly"


def test_get_trend_data_failure():
    # Intentionally using an offense code that we know has data
    offence_code = "74703"  # Replace with an actual valid offense code
    start_month_year = "01/2012"
    end_month_year = "12/2017"

    dates, values = get_trend_data(offence_code, start_month_year, end_month_year)

    # Intentionally asserting the opposite of our expectations to force a failure
    assert not dates, "Expected no dates, but got some."
    assert not values, "Expected no values, but got some."

