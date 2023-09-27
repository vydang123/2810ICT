import wx
import wx.grid
import csv
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure

class MainPage(wx.Frame):
    def __init__(self, parent, title="Sample Page", size=(800, 600)):
        super(MainPage, self).__init__(parent, title=title, size=size)
        self.grid_created = False
        self.active_panel = None  # Keep track of the active panel

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
        btn_font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        
        self.sidebar = wx.Panel(self.panel, pos=(10, 60), size=(200, 300))
        self.sidebar.SetBackgroundColour(wx.Colour(50, 50, 50))  # Darker gray for emphasis
        
        self.btn1 = wx.Button(self.sidebar, label="View_Case_Penalty", pos=(10, 10), size=(180, 40))
        self.btn2 = wx.Button(self.sidebar, label="Offence_code", pos=(10, 60), size=(180, 40))
        self.btn3 = wx.Button(self.sidebar, label="Radar/Camera Cases", pos=(10, 110), size=(180, 40))
        self.btn4 = wx.Button(self.sidebar, label="Mobile Phone Usage", pos=(10, 160), size=(180, 40))
        self.btn5 = wx.Button(self.sidebar, label="Seatbelt not fastened", pos=(10, 210), size=(180, 40))

        self.btn1.SetFont(btn_font)
        self.btn2.SetFont(btn_font)
        self.btn3.SetFont(btn_font)
        self.btn4.SetFont(btn_font)
        self.btn5.SetFont(btn_font)

        self.btn1.Bind(wx.EVT_BUTTON, self.on_button_click)
        self.btn2.Bind(wx.EVT_BUTTON, self.on_button_click)
        self.btn3.Bind(wx.EVT_BUTTON, self.on_button_click)
        self.btn4.Bind(wx.EVT_BUTTON, self.on_button_click)
        self.btn5.Bind(wx.EVT_BUTTON, self.on_button_click)

        # Aesthetic elements
        self.panel.SetBackgroundColour(wx.Colour(230, 230, 230))  # Light gray for demonstration
        self.Centre()
        
        self.grid = wx.grid.Grid(self.panel, pos=(230, 60), size=(650, 400))  # Adjusted size
        self.grid.Hide()
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.panel, -1, self.fig)
        self.canvas.Hide()

    def switch_to_page(self, page_name):
        # Hide or destroy components of the old active panel (if any)
        if self.active_panel:
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
            if hasattr(self, 'generate_mobile_phone_trend_btn'):
                self.generate_mobile_phone_trend_btn.Hide()
            if hasattr(self, 'generate_seatbelt_trend_btn'):
                self.generate_seatbelt_trend_btn.Hide()
            if hasattr(self, 'retrieve_cases_btn'):
                self.retrieve_cases_btn.Hide()  # Hide the "Retrieve Cases" button
            self.canvas.Hide()
            self.grid.Hide()
            self.active_panel.Destroy()

        # Show the components of the selected page
        if page_name == "View_Case_Penalty":
            self.show_View_Case_Penalty()
        elif page_name == "Offence_code":
            self.show_Offence_code()
        elif page_name == "Radar/Camera Cases":
            self.show_radar_camera_cases()
        elif page_name == "Mobile Phone Usage":
            self.show_Mobile_Offence_code()
        elif page_name == "Seatbelt not fastened":
            self.show_Seatbelt_Offence_code()
            
    def show_View_Case_Penalty(self):
        # Update the title
        self.active_panel = wx.Panel(self.panel)
        self.hide_trend_components()
        self.title_label.SetLabel("Penalty Details")
        self.intro_label.Hide()  # Hide the introductory text
        
        # Initialize filter components
        self.start_date_label = wx.StaticText(self.panel, label="Start Date:", pos=(230, 80))
        self.end_date_label = wx.StaticText(self.panel, label="End Date:", pos=(410, 80))
        
        with open("penalty_data_set_2.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)
            months_years = sorted(list(set(f"{date.split('/')[1]}/{date.split('/')[2]}" for date in [row[1] for row in reader] if len(date.split('/')) == 3)), key=lambda x: (int(x.split('/')[1]), int(x.split('/')[0])))  # Sort by year first, then month

        self.start_date_dropdown = wx.Choice(self.panel, pos=(310, 75), choices=months_years)
        self.end_date_dropdown = wx.Choice(self.panel, pos=(490, 75), choices=months_years)
        
        self.start_date_dropdown.Bind(wx.EVT_CHOICE, self.on_date_range_selected)
        self.end_date_dropdown.Bind(wx.EVT_CHOICE, self.on_date_range_selected)
        
        # Adjusting the grid position to be lower
        self.grid.SetPosition((230, 120))
        self.grid.Show()
        self.panel.Layout()

    def generate_trend(self, event):
        # Clear any existing plot on the canvas
        self.hide_trend_components()
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
            start_month_year_num = int(start_month_year.split('/')[1] + start_month_year.split('/')[0])
            end_month_year_num = int(end_month_year.split('/')[1] + end_month_year.split('/')[0])
            filtered_data = [row for row in reader if row[2] == offence_code and start_month_year_num <= int(row[1].split('/')[-1] + row[1].split('/')[1]) <= end_month_year_num]


        if not filtered_data:
            wx.MessageBox(f"No data found for offence code: {offence_code} in the selected date range.", "Info", wx.OK | wx.ICON_INFORMATION)
            return

        # Extracting the trend data based on month/year from OFFENCE_MONTH
        dates = [row[1] for row in filtered_data]
        values = [int(row[24]) for row in filtered_data]  # Assuming 24th column has the trend values

        # Sum values by date (month/year)
        datewise_values = {}
        for date, value in zip(dates, values):
            if date in datewise_values:
                datewise_values[date] += value
            else:
                datewise_values[date] = value

        # Sorting dates (month/year) for plotting
        sorted_dates = sorted(datewise_values.keys(), key=lambda x: (int(x.split('/')[-1]), int(x.split('/')[1])))  # Sorting by year first, then month
        sorted_values = [datewise_values[date] for date in sorted_dates]
        ax = self.fig.add_subplot(111)
        ax.plot(sorted_dates, sorted_values, marker='o')
        ax.set_title(f"Trend for Offence Code: {offence_code}")
        ax.set_xlabel("Month/Year")
        ax.set_ylabel("Value")
        ax.set_xticks(sorted_dates)
        ax.set_xticklabels(sorted_dates, rotation=45)

        # Adjust layout and show
        self.fig.tight_layout()
        self.canvas.SetPosition((230, 120))
        self.canvas.Show()
        self.canvas.draw()

        # Update layout of the main page
        self.panel.Layout()

    def generate_trend_for_offense(self, offense_description):
        # Clear any existing plot on the canvas
        self.hide_trend_components()
        self.fig.clear()
        
        start_month_year = self.start_date_dropdown.GetString(self.start_date_dropdown.GetSelection())
        end_month_year = self.end_date_dropdown.GetString(self.end_date_dropdown.GetSelection())

        # Convert MM/YYYY to YYYYMM for comparison
        start_month_year_num = int(start_month_year.split('/')[1] + start_month_year.split('/')[0])
        end_month_year_num = int(end_month_year.split('/')[1] + end_month_year.split('/')[0])

        # Read data and filter based on the offense description and selected date range
        with open("penalty_data_set_2.csv", "r") as file:
            reader = csv.reader(file)
            headers = next(reader)
            filtered_data = [row for row in reader if offense_description in row[3].lower() and start_month_year_num <= int(row[1].split('/')[-1] + row[1].split('/')[1]) <= end_month_year_num]

        if not filtered_data:
            wx.MessageBox(f"No data found for offense description: {offense_description} in the selected date range.", "Info", wx.OK | wx.ICON_INFORMATION)
            return

        # Accumulate (sum) the TOTAL_VALUE for each unique date
        datewise_values = {}
        for row in filtered_data:
            date = row[1]
            value = int(row[24])  # Assuming 24th column has the trend values
            if date in datewise_values:
                datewise_values[date] += value
            else:
                datewise_values[date] = value

        # Sorting dates (month/year) for plotting
        sorted_dates = sorted(datewise_values.keys(), key=lambda x: (datetime.datetime.strptime(x, "%d/%m/%Y").year, datetime.datetime.strptime(x, "%d/%m/%Y").month))  # Sorting by year first, then month
        sorted_values = [datewise_values[date] for date in sorted_dates]
        ax = self.fig.add_subplot(111)
        ax.plot(sorted_dates, sorted_values, marker='o')
        ax.set_title(f"Trend for Offense Description: {offense_description}")
        ax.set_xlabel("Month/Year")
        ax.set_ylabel("Value")
        ax.set_xticks(sorted_dates)
        ax.set_xticklabels(sorted_dates, rotation=45)

        # Adjust layout and show
        self.fig.tight_layout()
        self.canvas.SetPosition((230, 120))
        self.canvas.Show()
        self.canvas.draw()

        # Update layout of the main page
        self.panel.Layout()

    def generate_mobile_phone_trend(self, event):
        self.generate_trend_for_offense("mobile phone")

    def generate_seatbelt_trend(self, event):
        self.generate_trend_for_offense("seatbelt")


    def show_Seatbelt_Offence_code(self):
        self.active_panel = wx.Panel(self.panel)        
        self.hide_trend_components()
        # Update the title
        self.title_label.SetLabel("Seatbelt Not Fastened Trend")
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

        # Button to generate trend
        self.generate_seatbelt_trend_btn = wx.Button(self.panel, label="Generate Mobile Trend", pos=(570, 75), size=(150, 30))
        self.generate_seatbelt_trend_btn.Bind(wx.EVT_BUTTON, self.generate_seatbelt_trend)
        self.panel.Layout()
    
    def show_Mobile_Offence_code(self):
        self.active_panel = wx.Panel(self.panel)        
        self.hide_trend_components()
        # Update the title
        self.title_label.SetLabel("Mobile Phone Usage Trend")
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

        # Button to generate trend
        self.generate_mobile_phone_trend_btn = wx.Button(self.panel, label="Generate Mobile Trend", pos=(570, 75), size=(150, 30))
        self.generate_mobile_phone_trend_btn.Bind(wx.EVT_BUTTON, self.generate_mobile_phone_trend)
        self.panel.Layout()

    def show_Offence_code(self):
        self.active_panel = wx.Panel(self.panel)        
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

    def show_radar_camera_cases(self):
        self.active_panel = wx.Panel(self.panel)
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
        self.hide_trend_components()
        if self.start_date_dropdown.GetSelection() == wx.NOT_FOUND or self.end_date_dropdown.GetSelection() == wx.NOT_FOUND:
            wx.MessageBox("Please select both a start and end date.", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        start_month, start_year = self.start_date_dropdown.GetString(self.start_date_dropdown.GetSelection()).split('/')
        end_month, end_year = self.end_date_dropdown.GetString(self.end_date_dropdown.GetSelection()).split('/')
        
        start_date = datetime.date(int(start_year), int(start_month), 1)
        end_date = datetime.date(int(end_year), int(end_month), 1)

        # Read data and filter based on the selected date range and offense description
        with open("penalty_data_set_2.csv", "r") as file:
            reader = csv.reader(file)
            headers = next(reader)
            # Assuming offense description is in column 3 (index 2)
            filtered_data = [row for row in reader if ("Camera" in row[3] or "Radar" in row[3]) and start_date <= datetime.date(int(row[1].split('/')[2]), int(row[1].split('/')[1]), int(row[1].split('/')[0])) <= end_date]

        # Sort the filtered data by date (oldest to latest)
        filtered_data.sort(key=lambda x: datetime.date(int(x[1].split('/')[2]), int(x[1].split('/')[1]), int(x[1].split('/')[0])))

        print(filtered_data)
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
        
        start_month, start_year = start_month_year.split('/')
        end_month, end_year = end_month_year.split('/')
        
        start_date = datetime.date(int(start_year), int(start_month), 1)
        end_date = datetime.date(int(end_year), int(end_month), 1)

        with open("penalty_data_set_2.csv", "r") as file:
            reader = csv.reader(file)
            headers = next(reader)
            filtered_data = [row for row in reader if start_date <= datetime.date(int(row[1].split('/')[2]), int(row[1].split('/')[1]), int(row[1].split('/')[0])) <= end_date]
            
            # Sort the filtered data by date (oldest to latest)
            filtered_data.sort(key=lambda x: datetime.date(int(x[1].split('/')[2]), int(x[1].split('/')[1]), int(x[1].split('/')[0])))

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
        if self.title_label.GetLabel() != "Radar/Camera Cases":
            if hasattr(self, 'start_date_label') and self.title_label.GetLabel() != "Penalty Details":
                self.start_date_label.Hide()
            if hasattr(self, 'end_date_label') and self.title_label.GetLabel() != "Penalty Details":
                self.end_date_label.Hide()
            if hasattr(self, 'start_date_dropdown') and self.title_label.GetLabel() != "Penalty Details":
                self.start_date_dropdown.Hide()
            if hasattr(self, 'end_date_dropdown') and self.title_label.GetLabel() != "Penalty Details":
                self.end_date_dropdown.Hide()
            if hasattr(self, 'offence_code_label'):
                self.offence_code_label.Hide()
            if hasattr(self, 'offence_code_input'):
                self.offence_code_input.Hide()     
            if hasattr(self, 'generate_trend_btn'):
                self.generate_trend_btn.Hide()
        self.canvas.Hide()

        
    def on_button_click(self, event):
        button_label = event.GetEventObject().GetLabel()
        self.switch_to_page(button_label)

app = wx.App()
frame = MainPage(None)
frame.Show()
app.MainLoop()
