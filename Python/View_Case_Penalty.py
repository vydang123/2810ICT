import wx
import wx.grid

class ViewPenaltyPage(wx.Frame):
    def __init__(self, parent, title="View Penalty", size=(800, 600)):
        super(ViewPenaltyPage, self).__init__(parent, title=title, size=size)
        
        # Setting up the main panel
        self.panel = wx.Panel(self)
        
        # Title
        title_font = wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title_label = wx.StaticText(self.panel, label="Penalty Details", pos=(20, 10))
        title_label.SetFont(title_font)
        
        # Table (Grid) to display penalty details
        self.grid = wx.grid.Grid(self.panel, pos=(20, 50), size=(760, 400))
        
        # Sample data for demonstration
        self.grid.CreateGrid(10, 5)  # 10 rows, 5 columns
        columns = ["Case ID", "Offence Code", "Date", "Fine Amount", "Points"]
        for col_num, col_name in enumerate(columns):
            self.grid.SetColLabelValue(col_num, col_name)
        
        # For demonstration, fill the grid with some dummy data
        for row in range(10):
            self.grid.SetCellValue(row, 0, f"Case {row + 1}")
            self.grid.SetCellValue(row, 1, f"Code {row + 1}")
            self.grid.SetCellValue(row, 2, "2023-09-24")
            self.grid.SetCellValue(row, 3, "$100")
            self.grid.SetCellValue(row, 4, "3")
        
        # Buttons below the table
        self.btn1 = wx.Button(self.panel, label="Button 1", pos=(20, 470))
        self.btn2 = wx.Button(self.panel, label="Button 2", pos=(130, 470))
        
        # Aesthetic elements
        self.panel.SetBackgroundColour(wx.Colour(230, 230, 230))  # Light gray for demonstration
        self.Centre()
        
app = wx.App()
frame = ViewPenaltyPage(None)
frame.Show()
app.MainLoop()
