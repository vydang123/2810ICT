import csv
import datetime


# Replicating the provided generate_trend_for_offense function
def generate_trend_for_offense(file_path, offense_description, start_month_year, end_month_year):
    # Convert MM/YYYY to YYYYMM for comparison
    start_month_year_num = int(start_month_year.split('/')[1] + start_month_year.split('/')[0])
    end_month_year_num = int(end_month_year.split('/')[1] + end_month_year.split('/')[0])

    # Read data and filter based on the offense description and selected date range
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        headers = next(reader)
        filtered_data = [row for row in reader if offense_description in row[3].lower() and start_month_year_num <= int(
            row[1].split('/')[-1] + row[1].split('/')[1]) <= end_month_year_num]

    # Accumulate (sum) the TOTAL_VALUE for each unique date
    datewise_values = {}
    for row in filtered_data:
        date = row[1]
        value = int(row[24])  # Assuming 24th column has the trend values
        if date in datewise_values:
            datewise_values[date] += value
        else:
            datewise_values[date] = value

    # Sorting dates (month/year) for return
    sorted_dates = sorted(datewise_values.keys(), key=lambda x: (datetime.datetime.strptime(x, "%d/%m/%Y").year,
                                                                 datetime.datetime.strptime(x,
                                                                                            "%d/%m/%Y").month))  # Sorting by year first, then month
    sorted_values = [datewise_values[date] for date in sorted_dates]

    return sorted_dates, sorted_values


# Test case
def test_generate_mobile_phone_trend():
    file_path = "penalty_data_set_2.csv"  # Path to the sample data file
    start_month_year = "01/2013"
    end_month_year = "02/2015"

    sorted_dates, sorted_values = generate_trend_for_offense(file_path, "seatbelt", start_month_year,
                                                             end_month_year)

    # Assert that the function processes the data correctly
    assert sorted_dates and sorted_values, "Failed to generate the trend"
