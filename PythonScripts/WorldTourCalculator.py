# Planned features: 
# Have points to next rank stat
# Also have input for player to put how long a match is. Maybe they want to add loading time to calculation.
# Potential additions: projected completion (based on time left and progress so far)
#   Estimated completion date (how many points  you've gotten per day so far, and use days left in season)
# Quick play calculator. Features mostly the same things as world tour, but instead gives data for quick play.

# To build the calculator, run "pyinstaller --onefile --windowed WorldTourCalculator.py"


import tkinter as tk
from tkinter import ttk
import math
from datetime import date


# Setup UI foundation
root = tk.Tk()
root.title("World Tour Points Calculator")

# Create calculator tabs
calc_tabs = ttk.Notebook(root)

world_tour_tab = tk.Frame(calc_tabs)
quick_play_tab = tk.Frame(calc_tabs)
world_tour_tab.pack(fill='both', expand=True)
quick_play_tab.pack(fill='both', expand=True)

calc_tabs.add (world_tour_tab, text='World Tour')
calc_tabs.add (quick_play_tab, text='Quick Play')

calc_tabs.pack(expand=True, fill='both')

def on_tab_changed(event):
    notebook = event.widget
    selected_tab = notebook.select()
    tab_index = notebook.index(selected_tab)
    if tab_index == 0:
        setup_world_tour_ui()
    elif tab_index == 1:
        setup_quick_play_ui()
        
calc_tabs.bind("<<NotebookTabChanged>>", on_tab_changed)


# Estimated time each game will take
# Additional game time includes things like queue time, loading time, and transition time between matches
base_game_time = 10
additional_game_time = 3
game_time = base_game_time + additional_game_time

# Points awarded for each round in world tour
lose_round_one_points = 2
lose_round_two_points = 6
lose_final_round_points = 14
win_final_round_points = 25

# Number of games needed to reach the goal points (default is 1)
round_one_games = 1
round_two_games = 1
lose_final_round_games = 1
win_final_round_games = 1

# Time spent playing for each type of round
round_one_time = game_time
round_two_time = game_time * 2
lose_final_round_time = game_time * 3
win_final_round_time = game_time * 3

# Dates used to determine how much time is left in the season
season_end_date = date(2025, 12, 11)
todays_date = date.today()

# The different badges the user can choose from to be their goal
world_tour_badge_options = [
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

# Labels for rows in the games table
row_labels = [
    "Round one",
    "Round two",
    "Lose final round",
    "Win final round",
]

# Full table rows in the games table
games_table_rows = [
    [row_labels[0], round_one_games, round_one_time],
    [row_labels[1], round_two_games, round_two_time],
    [row_labels[2], lose_final_round_games, lose_final_round_time],
    [row_labels[3], win_final_round_games, win_final_round_time],
]

# Modified when a calculation occurs
# Number of games and time will be updated and then used to update the data in the games table rows
updated_games_data = [
    (round_one_games, round_one_time),
    (round_two_games, round_two_time),
    (lose_final_round_games, lose_final_round_time),
    (win_final_round_games, win_final_round_time),
]

# Weights for how often a certain type of round will occur
round_one_weight = tk.StringVar(value="50")
round_two_weight = tk.StringVar(value="25")
lose_final_round_weight = tk.StringVar(value="15")
win_final_round_weight = tk.StringVar(value="10")

round_weights_vars = [round_one_weight, round_two_weight, lose_final_round_weight, win_final_round_weight]

for i, var in enumerate(round_weights_vars):
    var.trace_add("write", lambda *args, idx=i: validate_weight(idx))

# Perform a division operation and round up the result
def division_round_up(dividend, divisor):
    return math.ceil(dividend / divisor)
 
 
# Given a time in minutes, calculates the resulting time in days, hours, and minutes format
def convert_time(bulk_minutes):
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
 
 
# Refresh the games table
def refresh_games_table():
    # Clear all existing rows
    for item in tree.get_children():
        tree.delete(item)

    # Insert updated rows
    for row in games_table_rows:
        tree.insert("", "end", values=row)

    
# When a badge is selected, update the goal points and its display 
def on_badge_selected(var_name, index, mode):
    label, points = badge_dict[badge_var.get()]
    global goal_points
    goal_points = points
    goal_label.config(text=f"Goal points: {goal_points} ({label})")


# Validate the inputted weight from the user to make sure it doesn't exceed the combined max of 100
def validate_weight(index, *args):
    vals = []
    for v in round_weights_vars:
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
        round_weights_vars[index].set(str(max_allowed))


# Calculate the different data points that will be shown to the user
def calculate():
    try:
        # The amount of points left to reach the goal points
        current_points = int(points_entry.get())
        points_remaining = goal_points - current_points
        display = f"\n Points remaining: {points_remaining}\n"
        
        # Number of games required in each round to reach the goal points
        # Includes losing first round, losing second round, losing final round, and winning final round
        round_one_games = division_round_up(points_remaining, lose_round_one_points)
        round_two_games = division_round_up(points_remaining, lose_round_two_points)
        lose_final_round_games = division_round_up(points_remaining, lose_final_round_points)
        win_final_round_games = division_round_up(points_remaining, win_final_round_points)
        
        # Playtime to reach goal points if only round type specified is played
        round_one_playtime = round_one_games * round_one_time
        round_two_playtime = round_two_games * round_two_time
        lose_final_round_playtime = lose_final_round_games * lose_final_round_time
        win_final_round_playtime = win_final_round_games * win_final_round_time
        
        # Update the data in the games table and refresh the table to display the updated data
        updated_games_data[0] = (round_one_games, convert_time(round_one_playtime))
        updated_games_data[1] = (round_two_games, convert_time(round_two_playtime))
        updated_games_data[2] = (lose_final_round_games, convert_time(lose_final_round_playtime))
        updated_games_data[3] = (win_final_round_games, convert_time(win_final_round_playtime))
        for i, (games, time) in enumerate(updated_games_data):
            games_table_rows[i][1] = games
            games_table_rows[i][2] = time
        refresh_games_table()
        
        # Calculate playtime based on the chance of each round type occurring
        playtimes  = [round_one_playtime, round_two_playtime, lose_final_round_playtime, win_final_round_playtime]
        round_weights = [float(var.get() or 0) for var in round_weights_vars]
        weighted_playtime = sum((w / 100) * t for w, t in zip(round_weights, playtimes))
        
        # Estimated amount of play time to reach the goal points based on round weights
        display += f"Estimated play time: {convert_time(weighted_playtime)}\n"
        
        # The amount of points needed per day to reach the goal points
        days_remaining = (season_end_date - todays_date).days
        daily_points = points_remaining // days_remaining
        display += f"Days left in season: {days_remaining}\n"
        display += f"Daily points: {daily_points}\n"
        
        # Maximum and weighted time to play each day to reach the goal points
        display += f"Max daily play time: {convert_time(round_one_playtime / days_remaining)}"
        display += f"Weighted daily play time: {convert_time(weighted_playtime / days_remaining)}"
        
        result_label.config(text=display)
    except ValueError:
        result_label.config(text="Please enter a valid points value.")


# Set style for various UI elements
style = ttk.Style(root)
style.theme_use("clam")
style.configure("Treeview", font=("Gadugi", 10))
style.configure("Treeview.Heading", font=("Gadugi", 11))
style.configure("TButton", font=("Gadugi", 10))

# Create the dropdown list of badge options
badge_dict = {f"{label}: {points}": (label, points) for label, points in world_tour_badge_options}
dropdown_options = list(badge_dict.keys())

badge_var = tk.StringVar()
badge_var.set(dropdown_options[-1])  # Default to Emerald 1: 2400

badge_menu = tk.OptionMenu(world_tour_tab, badge_var, *dropdown_options)
badge_menu.config(font=("Gadugi", 11))
badge_menu.pack(pady=(30, 0))

# Whenever badge_var is changed, on_badge_selected will run
badge_var.trace_add("write", on_badge_selected)

# Setup the goal points label
goal_points = badge_dict[badge_var.get()][1]
goal_label = tk.Label(world_tour_tab, text=f"Goal points: {goal_points}", font=("Gadugi", 10))
goal_label.pack(pady=(10, 20))

# Update the goal label text when the game first runs
on_badge_selected("name", 1, "mode")

# Create the points entry box and label for it
tk.Label(world_tour_tab, text="Enter current points:", font=("Gadugi", 12)).pack(pady=5)
points_entry = ttk.Entry(world_tour_tab, font=("Gadugi", 10))
points_entry.pack(pady=(5, 25))
#points_entry.insert(0, 0)

# Create the labels and entry boxes for round weights
tk.Label(world_tour_tab, text="Percent chance of getting each round type (total 100%):", font=("Gadugi", 12)).pack(pady=15)

weight_entry_labels = ["Round One", "Round Two", "Lose Final Round", "Win Final Round"]

# Container frame to hold the two rows
round_weights_frame = tk.Frame(world_tour_tab)
round_weights_frame.pack()

# Create two row frames packed vertically
row_frames = []
for row_index in range(2):
    row_frame = tk.Frame(round_weights_frame)
    row_frame.pack(fill='x')
    row_frames.append(row_frame)

# Loop through each label/entry pair and put them in the appropriate row frame
for i in range(4):
    cell_frame = tk.Frame(row_frames[i // 2])
    cell_frame.pack(side='left', padx=10, pady=5)

    tk.Label(cell_frame, text=weight_entry_labels[i], font=("Gadugi", 11)).pack()
    tk.Entry(cell_frame, textvariable=round_weights_vars[i], font=("Gadugi", 10), width=17).pack(padx=15)

# Calculate button that will perform the calculations and output data when clicked
calc_button = ttk.Button(world_tour_tab, text="Calculate", command=calculate, cursor="question_arrow")
calc_button.pack(pady=(20, 0))

# Label that will be updated with calculated data
result_frame = ttk.Frame(world_tour_tab)
result_frame.pack(padx=10, pady=(30, 0), fill=tk.NONE, expand=True)

result_label = tk.Label(result_frame, text="\n Enter info and press calculate \n", font=("Gadugi", 12))
result_label.pack(pady=15, padx=15)

# Create the games table that will display the type of round,
# the number to play to reach the goal points, and the amount of time it will take
columns = ("round_type", "number_of_rounds", "playtime")
tree = ttk.Treeview(world_tour_tab, columns=columns, show="headings")

tree.heading("round_type", text="Round Type")
tree.heading("number_of_rounds", text="Number of Rounds")
tree.heading("playtime", text="Playtime")

tree.column("round_type", width=145, anchor=tk.W)
tree.column("number_of_rounds", width=145, anchor=tk.CENTER)
tree.column("playtime", width=200, anchor=tk.CENTER)

tree.insert("", "end", values=(row_labels[0], round_one_games, convert_time(round_one_time)))
tree.insert("", "end", values=(row_labels[1], round_two_games, convert_time(round_two_time)))
tree.insert("", "end", values=(row_labels[2], lose_final_round_games, convert_time(lose_final_round_time)))
tree.insert("", "end", values=(row_labels[3], win_final_round_games, convert_time(win_final_round_time)))

tree.pack(padx = 50, pady = (40, 50), fill=tk.NONE)


# Quick Play

# The different badges the user can choose from to be their goal
quick_play_badge_options = [
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

# Awarded point values
# Quick cash
first_place_quick_cash = 10
second_place_quick_cash = 6
third_place_quick_cash = 5

# Team vs Team game modes (TDM, Power Shift, Head 2 Head)
win_tvt = 10
lose_tvt = 5

# When a badge is selected, update the goal points and its display 
def qp_on_badge_selected(var_name, index, mode):
    label, points = qp_badge_dict[qp_badge_var.get()]
    global qp_goal_points
    qp_goal_points = points
    qp_goal_label.config(text=f"Goal points: {qp_goal_points} ({label})")

qp_badge_dict = {f"{label}: {points}": (label, points) for label, points in quick_play_badge_options}
qp_dropdown_options = list(qp_badge_dict.keys())

qp_badge_var = tk.StringVar()
qp_badge_var.set(qp_dropdown_options[-1])  # Default to Gold 1

qp_badge_menu = tk.OptionMenu(quick_play_tab, qp_badge_var, *qp_dropdown_options)
qp_badge_menu.config(font=("Gadugi", 11))
qp_badge_menu.pack(pady=(30, 0))

# Whenever badge_var is changed, on_badge_selected will run
qp_badge_var.trace_add("write", qp_on_badge_selected)

# Setup the goal points label
qp_goal_points = qp_badge_dict[qp_badge_var.get()][1]
qp_goal_label = tk.Label(quick_play_tab, text=f"Goal points: {qp_goal_points}", font=("Gadugi", 10))
qp_goal_label.pack(pady=(10, 20))

def setup_quick_play_ui():
    # badge_dict = {f"{label}: {points}": (label, points) for label, points in quick_play_badge_options}
    # dropdown_options = list(badge_dict.keys())

    # badge_menu['menu'].delete(0, 'end')
    # for opt in dropdown_options:
        # badge_menu['menu'].add_command(label=opt, command=tk._setit(var, opt))
    # badge_var = tk.StringVar()
    # badge_var.set(dropdown_options[-1])  # Default to Gold 1
    # badge_var.trace_add("write", on_badge_selected)
    
    print("Setup quick play")
    
def setup_world_tour_ui():
    # badge_dict = {f"{label}: {points}": (label, points) for label, points in world_tour_badge_options}
    # dropdown_options = list(badge_dict.keys())
    
    # badge_menu['menu'].delete(0, 'end')
    # for opt in dropdown_options:
        # badge_menu['menu'].add_command(label=opt, command=tk._setit(var, opt))
    # badge_var = tk.StringVar()
    # badge_var.set(dropdown_options[-1])  # Default to Emerald 1
    # badge_var.trace_add("write", on_badge_selected)
    
    print("Setup world tour")

#root.geometry("500x450")
root.mainloop()
