import unittest
import wx
from unittest.mock import Mock

# Import the class you want to test
from homepage import MainPage  # Replace 'your_module' with the actual module name

class TestMainPage(unittest.TestCase):
    def setUp(self):
        # Create a mock parent window
        self.parent = Mock()

        # Create an instance of MainPage
        self.main_page = MainPage(self.parent)

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
    unittest.main()
