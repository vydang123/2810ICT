import wx
import wx.grid
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure

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
        self.btn3 = wx.Button(self.sidebar, label="Radar/Camera Cases", pos=(10, 210), size=(180, 40))
       
        self.btn1.SetFont(btn_font)
        self.btn2.SetFont(btn_font)
        self.btn3.SetFont(btn_font)
        self.btn3.SetFont(btn_font)

        self.btn1.Bind(wx.EVT_BUTTON, self.show_View_Case_Penalty)
        self.btn2.Bind(wx.EVT_BUTTON, self.show_Offence_code)
        self.btn3.Bind(wx.EVT_BUTTON, self.show_radar_camera_cases)

        # Aesthetic elements
        self.panel.SetBackgroundColour(wx.Colour(230, 230, 230))  # Light gray for demonstration
        self.Centre()
        
        self.grid = wx.grid.Grid(self.panel, pos=(230, 60), size=(650, 400))  # Adjusted size
        self.grid.Hide()
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.panel, -1, self.fig)
        self.canvas.Hide()
    def show_View_Case_Penalty(self, event):
        # Update the title
        self.hide_trend_components()
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

    def show_Offence_code(self, event):
        self.hide_trend_components()
        # Update the title
        self.title_label.SetLabel("Offence Code Trend")
        self.intro_label.Hide()  # Hide the introductory text

        # Initialize filter components for date range
        self.start_date_label = wx.StaticText(self.panel, label="Start Date:", pos=(230, 50))
        self.end_date_label = wx.StaticText(self.panel, label="End Date:", pos=(410, 50))

        with open("penalty_data_set_2.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)
            months_years = sorted(list(set(f"{date.split('/')[1]}/{date.split('/')[2]}" for date in [row[1] for row in reader] if len(date.split('/')) == 3)), key=lambda x: (x.split('/')[1], x.split('/')[0]))  # Sort by year first, then month

        self.start_date_dropdown = wx.Choice(self.panel, pos=(310, 45), choices=months_years)
        self.end_date_dropdown = wx.Choice(self.panel, pos=(490, 45), choices=months_years)
        
        # Text input for offence code
        self.offence_code_label = wx.StaticText(self.panel, label="Enter Offence Code:", pos=(230, 80))
        self.offence_code_input = wx.TextCtrl(self.panel, pos=(360, 75), size=(200, 25))

        # Button to generate trend
        self.generate_trend_btn = wx.Button(self.panel, label="Generate Trend", pos=(570, 75), size=(150, 30))
        self.generate_trend_btn.Bind(wx.EVT_BUTTON, self.generate_trend)
        self.panel.Layout()


    def generate_trend(self, event):
        # Clear any existing plot on the canvas
        self.fig.clear()
        
        offence_code = self.offence_code_input.GetValue().strip()
        if not offence_code:
            wx.MessageBox("Please enter an offence code.", "Error", wx.OK | wx.ICON_ERROR)
            return

        # Ensure both dropdowns have a selection before fetching the data
        if self.start_date_dropdown.GetSelection() == wx.NOT_FOUND or self.end_date_dropdown.GetSelection() == wx.NOT_FOUND:
            wx.MessageBox("Please select both a start and end date.", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        start_month_year = self.start_date_dropdown.GetString(self.start_date_dropdown.GetSelection())
        end_month_year = self.end_date_dropdown.GetString(self.end_date_dropdown.GetSelection())

        # Read data and filter based on the offence code and selected date range
        with open("penalty_data_set_2.csv", "r") as file:
            reader = csv.reader(file)
            headers = next(reader)
            filtered_data = [row for row in reader if row[2] == offence_code and start_month_year <= f"{row[1].split('/')[1]}/{row[1].split('/')[2]}" <= end_month_year]

        if not filtered_data:
            wx.MessageBox(f"No data found for offence code: {offence_code} in the selected date range.", "Info", wx.OK | wx.ICON_INFORMATION)
            return

        # Extracting the trend data based on year
        years = [row[1].split('/')[-1] for row in filtered_data]
        values = [int(row[24]) for row in filtered_data]  # Assuming 24th column has the trend values

        # Sum values by year
        yearwise_values = {}
        for year, value in zip(years, values):
            if year in yearwise_values:
                yearwise_values[year] += value
            else:
                yearwise_values[year] = value

        # Sorting years for plotting
        sorted_years = sorted(yearwise_values.keys())
        sorted_values = [yearwise_values[year] for year in sorted_years]
        ax = self.fig.add_subplot(111)
        ax.plot(sorted_years, sorted_values, marker='o')
        ax.set_title(f"Trend for Offence Code: {offence_code}")
        ax.set_xlabel("Year")
        ax.set_ylabel("Value")
        ax.set_xticks(sorted_years)
        ax.set_xticklabels(sorted_years, rotation=45)
        
        # Adjust layout and show
        self.fig.tight_layout()
        self.canvas.SetPosition((230, 120))
        self.canvas.Show()
        self.canvas.draw()

        # Update layout of main page
        self.panel.Layout()

    def show_radar_camera_cases(self, event):
        # Hide components from other pages
        self.hide_trend_components()
        
        # Update the title
        self.title_label.SetLabel("Radar/Camera Cases")
        self.intro_label.Hide()  # Hide the introductory text
        
        # Initialize filter components for date selection
        self.start_date_label = wx.StaticText(self.panel, label="Start Date:", pos=(230, 80))
        self.end_date_label = wx.StaticText(self.panel, label="End Date:", pos=(410, 80))
        
        with open("penalty_data_set_2.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)
            months_years = sorted(list(set(f"{date.split('/')[1]}/{date.split('/')[2]}" for date in [row[1] for row in reader] if len(date.split('/')) == 3)), key=lambda x: (x.split('/')[1], x.split('/')[0]))

        self.start_date_dropdown = wx.Choice(self.panel, pos=(310, 75), choices=months_years)
        self.end_date_dropdown = wx.Choice(self.panel, pos=(490, 75), choices=months_years)
        
        self.retrieve_cases_btn = wx.Button(self.panel, label="Retrieve Cases", pos=(680, 75), size=(150, 30))
        self.retrieve_cases_btn.Bind(wx.EVT_BUTTON, self.retrieve_radar_camera_cases)
        
        # Adjusting the grid position to be lower
        self.grid.SetPosition((230, 120))
        self.panel.Layout()

    def retrieve_radar_camera_cases(self, event):
        # Ensure both dropdowns have a selection before fetching the data
        if self.start_date_dropdown.GetSelection() == wx.NOT_FOUND or self.end_date_dropdown.GetSelection() == wx.NOT_FOUND:
            wx.MessageBox("Please select both a start and end date.", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        start_month_year = self.start_date_dropdown.GetString(self.start_date_dropdown.GetSelection())
        end_month_year = self.end_date_dropdown.GetString(self.end_date_dropdown.GetSelection())

        # Read data and filter based on the selected date range and offense description
        with open("penalty_data_set_2.csv", "r") as file:
            reader = csv.reader(file)
            headers = next(reader)
            # Assuming offense description is in column 3 (index 2)
            filtered_data = [row for row in reader if "Radar" in row[2].lower() or "camera" in row[2].lower() and start_month_year <= f"{row[1].split('/')[1]}/{row[1].split('/')[2]}" <= end_month_year]
        
        self.adjust_grid_size(len(filtered_data), len(headers))
        for col_num, header in enumerate(headers):
            self.grid.SetColLabelValue(col_num, header)

        for row_num, row in enumerate(filtered_data):
            for col_num, cell in enumerate(row):
                self.grid.SetCellValue(row_num, col_num, cell)

        # Auto size columns
        self.grid.AutoSizeColumns()
        self.grid.Show()

    def adjust_grid_size(self, row_count, col_count):
        self.hide_trend_components()
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
        self.hide_trend_components()
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
        self.hide_trend_components()
        # Ensure both dropdowns have a selection before updating the grid
        if self.start_date_dropdown.GetSelection() == wx.NOT_FOUND or self.end_date_dropdown.GetSelection() == wx.NOT_FOUND:
            wx.MessageBox("Please select both a start and end date.", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        start_month_year = self.start_date_dropdown.GetString(self.start_date_dropdown.GetSelection())
        end_month_year = self.end_date_dropdown.GetString(self.end_date_dropdown.GetSelection())
        self.update_grid_with_month_year(start_month_year, end_month_year)

    def hide_trend_components(self):
        if hasattr(self, 'start_date_label'):
            self.start_date_label.Hide()
        if hasattr(self, 'end_date_label'):
            self.end_date_label.Hide()
        if hasattr(self, 'start_date_dropdown'):
            self.start_date_dropdown.Hide()
        if hasattr(self, 'end_date_dropdown'):
            self.end_date_dropdown.Hide()
        if hasattr(self, 'offence_code_label'):
            self.offence_code_label.Hide()
        if hasattr(self, 'offence_code_input'):
            self.offence_code_input.Hide()
        if hasattr(self, 'generate_trend_btn'):
            self.generate_trend_btn.Hide()
        self.canvas.Hide()


app = wx.App()
frame = MainPage(None)
frame.Show()
app.MainLoop()
