# Planned features: 
# Have points to next rank stat
# Also have input for player to put how long a match is. Maybe they want to add loading time to calculation.
# Potential additions: projected completion (based on time left and progress so far)
#   Estimated completion date (how many points  you've gotten per day so far, and use days left in season)
# Quick play calculator. Features mostly the same things as world tour, but instead gives data for quick play.
# Game time and additional game time input fields for quick play
# Maybe dropdown for which gamemode in quick play as well. Game modes can vary in how long they are.
# Additionally, special event game modes can give the player different amounts of points.

# To build the calculator, run "pyinstaller --onefile --windowed WorldTourCalculator.py"


import tkinter as tk
from tkinter import ttk
import math
from datetime import date


class WorldTourCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Set application title
        self.title("World Tour Points Calculator")

        # Set style for various UI elements
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", font=("Gadugi", 10))
        style.configure("Treeview.Heading", font=("Gadugi", 11))
        style.configure("TButton", font=("Gadugi", 10))
        
        # Styling for notebook
        style.configure(
            "TNotebook",
            #background="gray",   # box around the tabs
            tabmargins=[0, 0, 0, 0]   # space on the left, up, down, and right
        )

        # All tabs
        style.configure(
            "TNotebook.Tab",
            #background="gray",  # tab background color
            foreground="black",  # text color
            padding=[15, 5],   # horizontal, vertical padding
            font=("Gadugi", 11)
        )

        # Selected tab state
        style.map(
            "TNotebook.Tab",
            #background=[("selected", "light gray")],
            foreground=[("selected", "green")],
            font=[("selected", ("Gadugi", 13))],
            padding=[("selected", [15, 10])]
        )

        # --- World Tour Data ---
        # Estimated time each game will take
        # Additional game time includes things like queue time, loading time, and transition time between matches
        self.base_game_time = 10
        self.additional_game_time = 3
        self.game_time = self.base_game_time + self.additional_game_time

        # Points awarded for each round in world tour
        self.lose_round_one_points = 2
        self.lose_round_two_points = 6
        self.lose_final_round_points = 14
        self.win_final_round_points = 25

        # Number of games needed to reach the goal points (default is 1)
        self.round_one_games = 1
        self.round_two_games = 1
        self.lose_final_round_games = 1
        self.win_final_round_games = 1

        # Time spent playing for each type of round
        self.round_one_time = self.game_time
        self.round_two_time = self.game_time * 2
        self.lose_final_round_time = self.game_time * 3
        self.win_final_round_time = self.game_time * 3

        # Dates used to determine how much time is left in the season
        self.season_end_date = date(2025, 12, 10)
        self.todays_date = date.today()

        # The different badges in world tour
        self.world_tour_badge_options = [
            ("Bronze 4", 25),
            ("Bronze 3", 50),
            ("Bronze 2", 75),
            ("Bronze 1", 100),
            ("Silver 4", 150),
            ("Silver 3", 200),
            ("Silver 2", 250),
            ("Silver 1", 300),
            ("Gold 4", 375),
            ("Gold 3", 450),
            ("Gold 2", 525),
            ("Gold 1", 600),
            ("Platinum 4", 700),
            ("Platinum 3", 800),
            ("Platinum 2", 900),
            ("Platinum 1", 1000),
            ("Diamond 4", 1150),
            ("Diamond 3", 1300),
            ("Diamond 2", 1450),
            ("Diamond 1", 1600),
            ("Emerald 4", 1800),
            ("Emerald 3", 2000),
            ("Emerald 2", 2200),
            ("Emerald 1", 2400),
        ]

        # Labels for rows in the world tour games table
        self.row_labels = [
            "Round one",
            "Round two",
            "Lose final round",
            "Win final round",
        ]

        # Full table rows in the world tour games table
        self.games_table_rows = [
            [self.row_labels[0], self.round_one_games, self.round_one_time],
            [self.row_labels[1], self.round_two_games, self.round_two_time],
            [self.row_labels[2], self.lose_final_round_games, self.lose_final_round_time],
            [self.row_labels[3], self.win_final_round_games, self.win_final_round_time],
        ]

        # Modified when a calculation occurs
        # Number of games and time will be updated and then used to update the data in the games table rows
        self.updated_games_data = [
            (self.round_one_games, self.round_one_time),
            (self.round_two_games, self.round_two_time),
            (self.lose_final_round_games, self.lose_final_round_time),
            (self.win_final_round_games, self.win_final_round_time),
        ]
        
        # Weights for how often a certain type of round will occur
        self.round_one_weight = tk.StringVar(value="50")
        self.round_two_weight = tk.StringVar(value="25")
        self.lose_final_round_weight = tk.StringVar(value="15")
        self.win_final_round_weight = tk.StringVar(value="10")

        self.round_weights_vars = [
            self.round_one_weight,
            self.round_two_weight,
            self.lose_final_round_weight,
            self.win_final_round_weight,
        ]

        for i, var in enumerate(self.round_weights_vars):
            var.trace_add("write", lambda *args, idx=i: self.validate_weight(idx))

        # --- Quick Play Data ---
        # Base quick cash variables for wins and playtime
        self.win_games = 1
        self.lose_games = 1
        self.second_place_qc_games = 1

        self.win_playtime = self.game_time
        self.lose_playtime = self.game_time
        self.second_place_qc_playtime = self.game_time

        # Labels for rows in the quick play games table
        self.qp_row_labels = [
            "Win",
            "Lose",
            "Second Place",
        ]

        # Full table rows in the quick play games table
        self.qp_games_table_rows = [
            [self.qp_row_labels[0], self.win_games, self.win_playtime],
            [self.qp_row_labels[1], self.lose_games, self.lose_playtime],
            [self.qp_row_labels[2], self.second_place_qc_games, self.second_place_qc_playtime],
        ]

        # Modified when a calculation occurs
        # Number of games and time will be updated and then used to update the data in the games table rows
        self.qp_updated_games_data = [
            (self.win_games, self.win_playtime),
            (self.lose_games, self.lose_playtime),
            (self.second_place_qc_games, self.second_place_qc_playtime),
        ]

        # The different badges the user can choose from to be their goal
        self.quick_play_badge_options = [
            ("Bronze 4", 50),
            ("Bronze 3", 100),
            ("Bronze 2", 150),
            ("Bronze 1", 200),
            ("Silver 4", 300),
            ("Silver 3", 400),
            ("Silver 2", 500),
            ("Silver 1", 600),
            ("Gold 4", 775),
            ("Gold 3", 950),
            ("Gold 2", 1125),
            ("Gold 1", 1300),
        ]

        # Quick Cash awarded point values
        self.first_place_quick_cash = 10
        self.second_place_quick_cash = 6
        self.third_place_quick_cash = 5

        # Team vs Team game modes (TDM, Power Shift, Head 2 Head)
        self.win_tvt = 10
        self.lose_tvt = 5

        # --- General Data --- 
        self.base_result_label_text = "\n Enter info and press calculate \n"

        self.tab_data = {
            "World Tour Tab": {
                "name": "World Tour",
                "dropdown_options": self.world_tour_badge_options,
                "selected_option": "Emerald 1: 2400",
                "result_label_text": self.base_result_label_text,
                "tree_data": self.games_table_rows,
            },
            "Quick Play Tab": {
                "name": "Quick Play",
                "dropdown_options": self.quick_play_badge_options,
                "selected_option": "Gold 1: 1300",
                "result_label_text": self.base_result_label_text,
                "tree_data": self.qp_games_table_rows,
            },
        }
        
        # Currently active tab key
        self.current_tab = "World Tour Tab"
        self.goal_points = self.world_tour_badge_options[-1][1]

        # Create widgets here and populate them later
        self.badge_dict = {}
        self.badge_var = tk.StringVar()

        self.goal_label = None
        self.badge_menu = None
        self.points_entry = None
        self.round_weights_frame = None
        self.qp_weight_frame = None
        self.calc_button = None
        self.result_label = None
        self.tree = None

        # Setup the UI
        self.setup_ui()
    
    
    # --- Math Utility Methods ---
    # Perform a division operation and round up the result
    def division_round_up(self, dividend, divisor):
        return math.ceil(dividend / divisor)
     
     
    # Given a time in minutes, calculates the resulting time in days, hours, and minutes format
    def convert_time(self, bulk_minutes):
        hours = int(bulk_minutes // 60)
        minutes = int(bulk_minutes % 60)
        days = hours // 24
        
        # Format differently if the result contains days, hours, or only minutes
        if days > 0:
            return f"{days} days, {hours%24} hours, {minutes} minutes\n"
        elif hours > 0:
            return f"{hours} hours, {minutes} minutes\n"
        else:
            return f"{minutes} minutes\n"
            

    
    # --- UI Data Management Methods ---
    def on_tab_changed(self, event):
        notebook = event.widget
        selected_tab = notebook.select()
        tab_index = notebook.index(selected_tab)

        if tab_index == 0:
            self.current_tab = "World Tour Tab"
            self.setup_world_tour_ui()
        elif tab_index == 1:
            self.current_tab = "Quick Play Tab"
            self.setup_quick_play_ui()
           
           
    # When a badge is selected, update the goal points and its display 
    def on_badge_selected(self, *args):
        label, points = self.badge_dict[self.badge_var.get()]
        self.goal_points = points
        self.goal_label.config(text=f"Goal: {self.goal_points} ({label})")

        # Save selected badge
        data = self.tab_data[self.current_tab]
        data["selected_option"] = self.badge_var.get()
     
     
    # Refresh the games table
    def refresh_games_table(self):
        # Reference to the saved table data
        data = self.tab_data[self.current_tab]
        
        # Clear all existing rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert updated rows
        for row in data["tree_data"]:
            self.tree.insert("", "end", values=row)
            
            
    # Validate the inputted weight from the user to make sure it doesn't exceed the combined max of 100
    def validate_weight(self, index, *args):
        vals = []
        for v in self.round_weights_vars:
            try:
                vals.append(int(v.get()))
            except ValueError:
                vals.append(0)
        
        # Calculate total minus value from this entry
        other_sum = sum(vals) - vals[index]
        # The max value to allow in this box
        max_allowed = max(0, 100 - other_sum)

        # If value entered is above max, set to the maximum allowed value
        if vals[index] > max_allowed:
            self.round_weights_vars[index].set(str(max_allowed))


    # --- Main Calculations ---
    # Calculate the different data points that will be shown to the user
    def calculate(self):
        try:
            # Reference to the saved data for world tour tab
            data = self.tab_data["World Tour Tab"]
            
            # The amount of points left to reach the goal points
            current_points = int(self.points_entry.get())
            points_remaining = self.goal_points - current_points
            display = f"\n Points remaining: {points_remaining}\n"
            
            # Number of games required in each round to reach the goal points
            # Includes losing first round, losing second round, losing final round, and winning final round
            round_one_games = self.division_round_up(points_remaining, self.lose_round_one_points)
            round_two_games = self.division_round_up(points_remaining, self.lose_round_two_points)
            lose_final_round_games = self.division_round_up(points_remaining, self.lose_final_round_points)
            win_final_round_games = self.division_round_up(points_remaining, self.win_final_round_points)
            
            # Playtime to reach goal points if only round type specified is played
            round_one_playtime = round_one_games * self.round_one_time
            round_two_playtime = round_two_games * self.round_two_time
            lose_final_round_playtime = lose_final_round_games * self.lose_final_round_time
            win_final_round_playtime = win_final_round_games * self.win_final_round_time
            
            # Update the data in the games table and refresh the table to display the updated data
            self.updated_games_data[0] = (round_one_games, self.convert_time(round_one_playtime))
            self.updated_games_data[1] = (round_two_games, self.convert_time(round_two_playtime))
            self.updated_games_data[2] = (lose_final_round_games, self.convert_time(lose_final_round_playtime))
            self.updated_games_data[3] = (win_final_round_games, self.convert_time(win_final_round_playtime))

            for i, (games, time_str) in enumerate(self.updated_games_data):
                self.games_table_rows[i][1] = games
                self.games_table_rows[i][2] = time_str

            self.refresh_games_table()
            
            # Calculate playtime based on the chance of each round type occurring
            playtimes = [
            round_one_playtime,
            round_two_playtime,
            lose_final_round_playtime,
            win_final_round_playtime,
            ]
            round_weights = [float(var.get() or 0) for var in self.round_weights_vars]
            weighted_playtime = sum((w / 100) * t for w, t in zip(round_weights, playtimes))
            
            # Estimated amount of play time to reach the goal points based on round weights
            display += f"Estimated play time: {self.convert_time(weighted_playtime)}\n"
            
            # The amount of points needed per day to reach the goal points
            days_remaining = (self.season_end_date - self.todays_date).days
            daily_points = points_remaining // days_remaining
            display += f"Days left in season: {days_remaining}\n"
            display += f"Daily points: {daily_points}\n"
            
            # Maximum and weighted time to play each day to reach the goal points
            display += f"Max daily play time: {self.convert_time(round_one_playtime / days_remaining)}"
            display += f"Weighted daily play time: {self.convert_time(weighted_playtime / days_remaining)}"
            
            # Set and save the result label text
            self.result_label.config(text=display)
            data["result_label_text"] = display
            
        except ValueError:
            self.result_label.config(text="Please enter a valid points value.")
            
        
    # Calculate the different data points that will be shown to the user
    def qp_calculate(self):
        try:
            # Reference to the saved data for quiick play tab
            data = self.tab_data["Quick Play Tab"]
            
            # The amount of points left to reach the goal points
            current_points = int(self.points_entry.get())
            points_remaining = self.goal_points - current_points
            display = f"\n Points remaining: {points_remaining}\n"
            
            # Number of games required for each amount of rewared points to reach the goal points
            # Win tvt and 1st place quick cash are same value. 
            # Lose tvt and 3rd place quick cash also same value.
            win_games = self.division_round_up(points_remaining, self.win_tvt)
            lose_games = self.division_round_up(points_remaining, self.lose_tvt)
            second_place_qc_games = self.division_round_up(points_remaining, self.second_place_quick_cash)
            
            # Playtime to reach goal points if only type specified is played
            win_playtime = win_games * self.game_time
            lose_playtime = lose_games * self.game_time
            second_place_qc_playtime = second_place_qc_games * self.game_time
            
            # Update the data in the games table and refresh the table to display the updated data
            self.qp_updated_games_data[0] = (win_games, self.convert_time(win_playtime))
            self.qp_updated_games_data[1] = (lose_games, self.convert_time(lose_playtime))
            self.qp_updated_games_data[2] = (second_place_qc_games, self.convert_time(second_place_qc_playtime))

            for i, (games, time_str) in enumerate(self.qp_updated_games_data):
                self.qp_games_table_rows[i][1] = games
                self.qp_games_table_rows[i][2] = time_str

            self.refresh_games_table()
            
            # Calculate playtime based on the chance of each round type occurring
            playtimes = [win_playtime, lose_playtime, second_place_qc_playtime]
            round_weights = [float(var.get() or 0) for var in self.round_weights_vars[:3]]
            weighted_playtime = sum((w / 100) * t for w, t in zip(round_weights, playtimes))
            
            # Estimated amount of play time to reach the goal points based on round weights
            display += f"Estimated play time: {self.convert_time(lose_playtime)}\n"
            
            # The amount of points needed per day to reach the goal points
            days_remaining = (self.season_end_date - self.todays_date).days
            daily_points = points_remaining // days_remaining
            display += f"Days left in season: {days_remaining}\n"
            display += f"Daily points: {daily_points}\n"
            
            # Maximum and weighted time to play each day to reach the goal points
            display += f"Max daily play time: {self.convert_time(lose_playtime / days_remaining)}"
            
            # Set and save the result label text
            self.result_label.config(text=display)
            data["result_label_text"] = display
            
        except ValueError:
            self.result_label.config(text="Please enter a valid points value.")


    # --- Tab-Specific UI Setup ---
    def setup_world_tour_ui(self):
        self.calc_button.config(command=self.calculate)
        self.round_weights_frame.grid()
        self.qp_weight_frame.grid_remove()
        self.load_tab_data("World Tour Tab")
        
    def setup_quick_play_ui(self):
        self.calc_button.config(command=self.qp_calculate)
        self.round_weights_frame.grid_remove()
        self.qp_weight_frame.grid()
        self.load_tab_data("Quick Play Tab")


    def load_tab_data(self, tab_name):
        data = self.tab_data[tab_name]

        # Remove dropdown options
        dropdown_menu = self.badge_menu["menu"]
        dropdown_menu.delete(0, "end")

        # Add new dropdown options for this specific tab
        self.badge_dict = {
            f"{label}: {points}": (label, points)
            for label, points in data["dropdown_options"]
        }
        dropdown_options = list(self.badge_dict.keys())

        for option in dropdown_options:
            dropdown_menu.add_command(
                label=option,
                command=lambda v=option: self.badge_var.set(v),
            )

        # Set selected option from saved data
        self.badge_var.set(data["selected_option"])
        
        # Set result label text from saved data
        self.result_label.config(text=data["result_label_text"])
        
        # Refresh the games table to show the saved table data
        self.refresh_games_table()
        
    
    # Initial setup of UI
    def setup_ui(self):
        # Create calculator tabs
        calc_tabs = ttk.Notebook(self)
        calc_tabs.grid(row=0, column=0, columnspan=3, sticky='nsew', padx=5, pady=5)

        world_tour_tab = tk.Frame(calc_tabs)
        quick_play_tab = tk.Frame(calc_tabs)
        calc_tabs.add(world_tour_tab, text='World Tour')
        calc_tabs.add(quick_play_tab, text='Quick Play')

        calc_tabs.bind("<<NotebookTabChanged>>", self.on_tab_changed)

        # Setup the goal points label
        self.goal_label = tk.Label(self, text="Select your goal", font=("Gadugi", 11))
        self.goal_label.grid(row=1, column=0, columnspan=3, pady=(10, 8))

        # Create the dropdown list of badge options
        self.badge_dict = {
            f"{label}: {points}": (label, points)
            for label, points in self.world_tour_badge_options
        }
        dropdown_options = list(self.badge_dict.keys())

        self.badge_var.set(dropdown_options[-1])
        self.badge_var.trace_add("write", self.on_badge_selected)

        # Style the option menu
        self.optionmenu_style = ttk.Style(self)
        self.optionmenu_style.configure("My.TMenubutton", font=("Gadugi", 11))

        self.badge_menu = ttk.OptionMenu(
            self,
            self.badge_var,
            dropdown_options[-1],
            *dropdown_options,
            style="My.TMenubutton",
        )
        self.badge_menu.grid(row=2, column=0, columnspan=3, pady=(0, 30))
        
        # Points entry
        points_entry_frame = tk.Frame(self)
        points_entry_frame.grid(row=3, column=0, columnspan=3, pady=(5, 25))

        points_entry_label = tk.Label(points_entry_frame, text="Enter current points:", font=("Gadugi", 12))
        points_entry_label.grid(row=0, column=0, padx=5)

        self.points_entry = ttk.Entry(points_entry_frame, font=("Gadugi", 10))
        self.points_entry.grid(row=0, column=1, padx=5)

        # Round weights label
        tk.Label(
            self,
            text="Percent chance of getting each round type (total 100%):",
            font=("Gadugi", 12),
        ).grid(row=4, column=0, columnspan=3, pady=15)

        # World tour weights frame
        self.round_weights_frame = tk.Frame(self)
        self.round_weights_frame.grid(row=5, column=0, columnspan=3)

        weight_entry_labels = ["Round One", "Round Two", "Lose Final Round", "Win Final Round"]

        # World Tour weight entries
        for i in range(4):
            r, c = divmod(i, 2)
            tk.Label(self.round_weights_frame, text=weight_entry_labels[i], font=("Gadugi", 11)).grid(
                row=r * 2, column=c, padx=10, pady=5
            )
            tk.Entry(self.round_weights_frame, textvariable=self.round_weights_vars[i], font=("Gadugi", 10), width=17).grid(
                row=r * 2 + 1, column=c, padx=15, pady=5
            )
            
        # Quick play weights frame
        self.qp_weight_frame = tk.Frame(self)
        self.qp_weight_frame.grid(row=6, column=0, columnspan=3, pady=10)
        
        qp_weight_entry_labels = ["Win", "Lose", "Second Place"]
        
        # Quick play weight entries
        for i in range(3):
            tk.Label(self.qp_weight_frame, text=qp_weight_entry_labels[i], font=("Gadugi", 11)).grid(
                row=0, column=i, padx=10, pady=5
            )
            tk.Entry(self.qp_weight_frame, textvariable=self.round_weights_vars[i], font=("Gadugi", 10), width=17).grid(
                row=1, column=i, padx=15, pady=5
            )

        # Calculate button
        self.calc_button = ttk.Button(self, text="Calculate", command=self.calculate, cursor="question_arrow")
        self.calc_button.grid(row=7, column=0, columnspan=3, pady=(20, 0))

        # Results section
        result_frame = ttk.Frame(self)
        result_frame.grid(row=8, column=0, columnspan=3, pady=(30, 0))

        self.result_label = tk.Label(result_frame, text=self.base_result_label_text, font=("Gadugi", 12))
        self.result_label.grid(row=0, column=0, padx=15, pady=15)

        # Games table
        columns = ("round_type", "number_of_rounds", "playtime")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.heading("round_type", text="Round Type")
        self.tree.heading("number_of_rounds", text="Number of Rounds")
        self.tree.heading("playtime", text="Playtime")

        self.tree.column("round_type", width=145, anchor=tk.W)
        self.tree.column("number_of_rounds", width=145, anchor=tk.CENTER)
        self.tree.column("playtime", width=200, anchor=tk.CENTER)

        # Initial tree rows for World Tour
        self.tree.insert("", "end", values=(self.row_labels[0], self.round_one_games, self.convert_time(self.round_one_time)))
        self.tree.insert("", "end", values=(self.row_labels[1], self.round_two_games, self.convert_time(self.round_two_time)))
        self.tree.insert("", "end", values=(self.row_labels[2], self.lose_final_round_games, self.convert_time(self.lose_final_round_time)))
        self.tree.insert("", "end", values=(self.row_labels[3], self.win_final_round_games, self.convert_time(self.win_final_round_time)))

        self.tree.grid(row=9, column=0, columnspan=3, padx=50, pady=(40, 50))

        # Start with World Tour tab layout
        self.setup_world_tour_ui()
    
if __name__ == "__main__":
    app = WorldTourCalculator()
    app.mainloop()
