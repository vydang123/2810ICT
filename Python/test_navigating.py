import pytest
import wx
from homepage import MainPage

# Since we don't have the actual implementations for methods like show_View_Case_Penalty, show_Offence_code, etc.,
# we'll mock them for the purpose of this test. In a real environment, you would not need these mock implementations.

def mock_show_function():
    pass


setattr(MainPage, "show_View_Case_Penalty", mock_show_function)
setattr(MainPage, "show_Offence_code", mock_show_function)
setattr(MainPage, "show_radar_camera_cases", mock_show_function)
setattr(MainPage, "show_Mobile_Offence_code", mock_show_function)
setattr(MainPage, "show_Seatbelt_Offence_code", mock_show_function)


@pytest.mark.parametrize("page_name", ["View_Case_Penalty", "Offence_code", "Radar/Camera Cases", "Mobile Phone Usage",
                                       "Seatbelt not fastened"])
def test_switch_to_page(page_name):
    app = wx.App(False)
    frame = MainPage(None)

    frame.switch_to_page(page_name)

    # For simplicity, we'll just check if the active_panel attribute of MainPage is not None.
    # In a real test, you would check specific components related to the given page_name to ensure they are displayed correctly.
    assert frame.active_panel is not None, f"Failed to switch to {page_name} page"
