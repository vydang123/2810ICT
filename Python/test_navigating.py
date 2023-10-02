import wx
from homepage import MainPage

def test_switch_to_page():
    app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window
    frame = MainPage(None)  # Create a frame

    # Test navigation to "View_Case_Penalty"
    frame.switch_to_page("View_Case_Penalty")
    assert hasattr(frame, 'active_panel'), "Failed to navigate to View_Case_Penalty"

    # Test navigation to "Offence_code"
    frame.switch_to_page("Offence_code")
    assert hasattr(frame, 'active_panel'), "Failed to navigate to Offence_code"

    # Test navigation to "Radar/Camera Cases"
    frame.switch_to_page("Radar/Camera Cases")
    assert hasattr(frame, 'active_panel'), "Failed to navigate to Radar/Camera Cases"

    # Test navigation to "Mobile Phone Usage"
    frame.switch_to_page("Mobile Phone Usage")
    assert hasattr(frame, 'active_panel'), "Failed to navigate to Mobile Phone Usage"

    # Test navigation to "Seatbelt not fastened"
    frame.switch_to_page("Seatbelt not fastened")
    assert hasattr(frame, 'active_panel'), "Failed to navigate to Seatbelt not fastened"

    frame.Destroy()  # Cleanup
