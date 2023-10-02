import wx
import csv
from unittest.mock import patch
def load_data_from_file(file_path: str) -> list:
    try:
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            data = list(reader)
        return data
    except FileNotFoundError:
        wx.MessageBox(f"The file '{file_path}' was not found.", "Error", wx.OK | wx.ICON_ERROR)
        return []
def test_load_data_invalid_csv():
    invalid_file_path = "/invalid/path.csv"  # Example of an invalid file path
    with patch('wx.MessageBox') as mocked_msgbox:
        data = load_data_from_file(invalid_file_path)
        # Check if wx.MessageBox was called with the expected arguments
        mocked_msgbox.assert_called_once_with(
            f"The file '{invalid_file_path}' was not found.", "Error", wx.OK | wx.ICON_ERROR)
        # Ensure data is an empty list when given an invalid path
        assert data == []
