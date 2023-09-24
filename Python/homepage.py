import wx
import wx.grid
import subprocess
import csv

class MainPage(wx.Frame):
    def __init__(self, parent, title="Sample Page", size=(800, 600)):
        super(MainPage, self).__init__(parent, title=title, size=size)
        self.grid_created = False  

        # Setting up the main panel
        self.panel = wx.Panel(self)
        
        # Menu Bar
        self.menuBar = wx.MenuBar()
        self.fileMenu = wx.Menu()
        self.fileMenu.Append(wx.ID_EXIT, "Exit", "Exit the application")
        self.menuBar.Append(self.fileMenu, "&File")
        self.SetMenuBar(self.menuBar)
        
        # Title
        self.title_font = wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.title_label = wx.StaticText(self.panel, label="NSW Traffic Penalty", pos=(20, 10))
        self.title_label.SetFont(self.title_font)
        
        # Introduction
        self.intro_font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.intro_text = (
            "Welcome to the NSW Traffic Penalty application.\n\n"
            "Here, you can view details about traffic penalties, "
            "understand offense codes, and gain insights into related data. "
            "Use the navigation buttons on the left to explore the application."
        )
        self.intro_label = wx.StaticText(self.panel, label=self.intro_text, pos=(230, 60))
        self.intro_label.Wrap(540)  # Wrap text to fit the window width
        self.intro_label.SetFont(self.intro_font)
        
        # Sidebar with buttons
        self.sidebar = wx.Panel(self.panel, pos=(10, 60), size=(200, 300))
        self.sidebar.SetBackgroundColour(wx.Colour(50, 50, 50))  # Darker gray for emphasis
        
        btn_font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        
        self.btn1 = wx.Button(self.sidebar, label="View_Case_Penalty", pos=(10, 10), size=(180, 40))
        self.btn2 = wx.Button(self.sidebar, label="Offence_code", pos=(10, 60), size=(180, 40))
        self.btn3 = wx.Button(self.sidebar, label="Page 3", pos=(10, 110), size=(180, 40))
        self.btn4 = wx.Button(self.sidebar, label="Page 4", pos=(10, 160), size=(180, 40))
        
        self.btn1.SetFont(btn_font)
        self.btn2.SetFont(btn_font)
        self.btn3.SetFont(btn_font)
        self.btn4.SetFont(btn_font)
        
        self.btn1.Bind(wx.EVT_BUTTON, self.show_View_Case_Penalty)
        self.btn2.Bind(wx.EVT_BUTTON, self.show_Offence_code)
        
        # Aesthetic elements
        self.panel.SetBackgroundColour(wx.Colour(230, 230, 230))  # Light gray for demonstration
        self.Centre()
        
        self.grid = wx.grid.Grid(self.panel, pos=(230, 60), size=(650, 400))  # Adjusted size
        self.grid.Hide()
    def show_View_Case_Penalty(self, event):
        # Update the title
        self.title_label.SetLabel("Penalty Details")
        self.intro_label.Hide()  # Hide the introductory text
        
        # Initialize filter components
        self.start_date_label = wx.StaticText(self.panel, label="Start Date:", pos=(230, 80))
        self.end_date_label = wx.StaticText(self.panel, label="End Date:", pos=(410, 80))
        
        with open("penalty_data_set_2.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)
            months_years = sorted(list(set(f"{date.split('/')[1]}/{date.split('/')[2]}" for date in [row[1] for row in reader] if len(date.split('/')) == 3)), key=lambda x: (x.split('/')[1], x.split('/')[0]))  # Sort by year first, then month

        self.start_date_dropdown = wx.Choice(self.panel, pos=(310, 75), choices=months_years)
        self.end_date_dropdown = wx.Choice(self.panel, pos=(490, 75), choices=months_years)
        
        self.start_date_dropdown.Bind(wx.EVT_CHOICE, self.on_date_range_selected)
        self.end_date_dropdown.Bind(wx.EVT_CHOICE, self.on_date_range_selected)
        
        # Adjusting the grid position to be lower
        self.grid.SetPosition((230, 120))
        self.grid.Show()
        self.panel.Layout()

    def adjust_grid_size(self, row_count, col_count):
        if not hasattr(self, "grid_created"):
            self.grid_created = False

        if not self.grid_created:
            self.grid.CreateGrid(row_count, col_count)
            self.grid_created = True
        else:
            if self.grid.GetNumberRows() > 0:
                self.grid.DeleteRows(0, self.grid.GetNumberRows())
            if self.grid.GetNumberCols() > 0:
                self.grid.DeleteCols(0, self.grid.GetNumberCols())

            self.grid.AppendRows(row_count)
            self.grid.AppendCols(col_count)

    def update_grid_with_month_year(self, start_month_year, end_month_year):
        # Extract month and year from the date string
        start_month, start_year = start_month_year.split('/')
        end_month, end_year = end_month_year.split('/')
        
        # Load data from CSV
        with open("penalty_data_set_2.csv", "r") as file:
            reader = csv.reader(file)
            headers = next(reader)
            # Filter the data based on the selected month/year range
            filtered_data = [row for row in reader if start_month_year <= f"{row[1].split('/')[1]}/{row[1].split('/')[2]}" <= end_month_year]
 
            print(f"Filtered data from {start_month}/{start_year} to {end_month}/{end_year}:")
            print(filtered_data)
            self.adjust_grid_size(len(filtered_data), len(headers))
            for col_num, header in enumerate(headers):
                self.grid.SetColLabelValue(col_num, header)

            for row_num, row in enumerate(filtered_data):
                for col_num, cell in enumerate(row):
                    self.grid.SetCellValue(row_num, col_num, cell)

            # Auto size columns
            self.grid.AutoSizeColumns()

    def on_date_range_selected(self, event):
        # Ensure both dropdowns have a selection before updating the grid
        if self.start_date_dropdown.GetSelection() == wx.NOT_FOUND or self.end_date_dropdown.GetSelection() == wx.NOT_FOUND:
            wx.MessageBox("Please select both a start and end date.", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        start_month_year = self.start_date_dropdown.GetString(self.start_date_dropdown.GetSelection())
        end_month_year = self.end_date_dropdown.GetString(self.end_date_dropdown.GetSelection())
        self.update_grid_with_month_year(start_month_year, end_month_year)

    def show_Offence_code(self, event):
        self.Hide()  # Hide the main page
        subprocess.run(['python', 'Offence_code.py'])
        self.Show()  # Show the main page again after closing Offence_code.py window


app = wx.App()
frame = MainPage(None)
frame.Show()
app.MainLoop()
