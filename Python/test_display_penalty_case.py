import csv
import wx
def load_penalty_data(file_path: str) -> list:

    with open(file_path, "r") as file:
        reader = csv.reader(file)
        next(reader)
        months_years = sorted(list(set(f"{date.split('/')[1]}/{date.split('/')[2]}" for date in [row[1] for row in reader] if len(date.split('/')) == 3)), key=lambda x: (int(x.split('/')[1]), int(x.split('/')[0])))
    return months_years
def test_load_penalty_data():
    file_path = "penalty_data_set_2.csv"
    data = load_penalty_data(file_path)
    assert data is not None, "Data is None"
    assert isinstance(data, list), "Data is not a list"
    assert len(data) > 0, "Data list is empty"

    # Check if the dates are sorted correctly
    sorted_data = sorted(data, key=lambda x: (int(x.split('/')[1]), int(x.split('/')[0])))
    assert data == sorted_data, "Data is not sorted correctly"

