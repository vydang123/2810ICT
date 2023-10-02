import csv
def load_data_from_csv(file_path: str) -> list:
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    return data

def test_load_data_from_csv():
    file_path = "penalty_data_set_2.csv" # Example valid file path
    data = load_data_from_csv(file_path)
    assert data is not None # Ensure data is loaded
    assert isinstance(data, list) # Ensure data is a list of rows from cvs
    assert len(data) > 0 # Ensure data is not empty

def test_load_data_from_csv_failed():
    file_path = "penalty_data_set_2.csv"  # Example valid file path
    data = load_data_from_csv(file_path)
    assert len(data) == 0, f"Expected an empty list, but got a list of length {len(data)}."


