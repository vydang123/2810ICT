import datetime
import csv

def get_radar_camera_cases(start_month_year: str, end_month_year: str) -> list:
    start_month, start_year = start_month_year.split('/')
    end_month, end_year = end_month_year.split('/')

    start_date = datetime.date(int(start_year), int(start_month), 1)
    end_date = datetime.date(int(end_year), int(end_month), 1)

    with open("penalty_data_set_2.csv", "r") as file:
        reader = csv.reader(file)
        headers = next(reader)
        filtered_data = [row for row in reader if
                         ("Camera" in row[3] or "Radar" in row[3]) and start_date <= datetime.date(
                             int(row[1].split('/')[2]), int(row[1].split('/')[1]),
                             int(row[1].split('/')[0])) <= end_date]

    # Sort the filtered data by date (oldest to latest)
    filtered_data.sort(
        key=lambda x: datetime.date(int(x[1].split('/')[2]), int(x[1].split('/')[1]), int(x[1].split('/')[0])))

    return filtered_data


def test_get_radar_camera_cases():
    start_month_year = "01/2012"
    end_month_year = "12/2017"

    start_month, start_year = start_month_year.split('/')
    end_month, end_year = end_month_year.split('/')

    start_date = datetime.date(int(start_year), int(start_month), 1)
    end_date = datetime.date(int(end_year), int(end_month), 1)

    data = get_radar_camera_cases(start_month_year, end_month_year)

    # Ensure that data is non-empty
    assert data, "Data list is empty"

    # Ensure that each row in data contains either "Camera" or "Radar" in the offense description (assuming it's in column index 2)
    for row in data:
        assert "Camera" in row[3] or "Radar" in row[3], f"Unexpected offense description in row: {row}"

    # Ensure that each row's date falls within the specified range
    for row in data:
        date = datetime.date(int(row[1].split('/')[2]), int(row[1].split('/')[1]), int(row[1].split('/')[0]))
        assert start_date <= date <= end_date, f"Date out of range in row: {row}"

