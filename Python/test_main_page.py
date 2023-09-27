import test_main_page
from unittest.mock import Mock
from homepage import MainPage  # Replace 'your_module' with the actual module name

class TestMainPage:
    def setup_method(self, method):
        self.parent = Mock()
        self.main_page = MainPage.__new__(MainPage)
        # Initialize only the attributes you need for testing
        self.main_page.parent = self.parent
        # ... any other necessary attributes ...

    def test_init(self):
        # Ensure attributes are initialized correctly
        self.assertFalse(self.main_page.grid_created)
        self.assertIsNone(self.main_page.active_panel)

        # Check if the title and size are set correctly
        self.assertEqual(self.main_page.GetTitle(), "Sample Page")
        self.assertEqual(self.main_page.GetSize(), (800, 600))

        # Ensure that the panel, menu bar, and other UI elements are created
        self.assertIsInstance(self.main_page.panel, wx.Panel)
        self.assertIsInstance(self.main_page.menuBar, wx.MenuBar)
        self.assertIsInstance(self.main_page.title_label, wx.StaticText)
        self.assertIsInstance(self.main_page.intro_label, wx.StaticText)
        self.assertIsInstance(self.main_page.sidebar, wx.Panel)
        self.assertIsInstance(self.main_page.btn1, wx.Button)
        self.assertIsInstance(self.main_page.btn2, wx.Button)
        self.assertIsInstance(self.main_page.btn3, wx.Button)
        self.assertIsInstance(self.main_page.btn4, wx.Button)
        self.assertIsInstance(self.main_page.grid, wx.grid.Grid)
        self.assertIsInstance(self.main_page.fig, wx.lib.mpl.Figure)
        self.assertIsInstance(self.main_page.canvas, wx.lib.mpl.FigureCanvas)

        # Ensure event bindings are set up correctly
        self.assertEqual(len(self.main_page.btn1.GetEvents()), 1)
        self.assertEqual(len(self.main_page.btn2.GetEvents()), 1)
        self.assertEqual(len(self.main_page.btn3.GetEvents()), 1)
        self.assertEqual(len(self.main_page.btn4.GetEvents()), 1)

    def test_show_View_Case_Penalty(self):
        # Mock components for view case penalty page
        self.main_page.panel = Mock()
        self.main_page.title_label = Mock()
        self.main_page.intro_label = Mock()
        self.main_page.grid = Mock()
        self.main_page.start_date_label = None
        self.main_page.end_date_label = None
        self.main_page.start_date_dropdown = None
        self.main_page.end_date_dropdown = None
        self.main_page.offence_code_label = None
        self.main_page.offence_code_input = None
        self.main_page.generate_trend_btn = None
        self.main_page.generate_mobile_phone_trend_btn = None
        self.main_page.retrieve_cases_btn = None
        self.main_page.canvas = Mock()
        # Simulate show_View_Case_Penalty
        self.main_page.show_View_Case_Penalty()
        self.assertTrue(self.main_page.start_date_label)
        self.assertTrue(self.main_page.end_date_label)
        
    def test_on_button_click(self):
        # Create a mock event
        event = Mock()

        # Simulate button click for each button
        self.main_page.on_button_click(event)
        self.assertEqual(self.main_page.active_panel, "View_Case_Penalty")

        self.main_page.on_button_click(event)
        self.assertEqual(self.main_page.active_panel, "Offence_code")

        self.main_page.on_button_click(event)
        self.assertEqual(self.main_page.active_panel, "Radar/Camera Cases")

        self.main_page.on_button_click(event)
        self.assertEqual(self.main_page.active_panel, "Mobile Phone Usage")

if __name__ == '__main__':
    test_main_page.main()
