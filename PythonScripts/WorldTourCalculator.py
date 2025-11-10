# Planned features: 
# Have points to next rank stat
# Also have input for player to put how long a match is. Maybe they want to add loading time to calculation.
# Weighted calculations for game time. Maybe 60% of time player gets round 1, so that time will be used more.
# Inputs for player to vary weight on rounds
# Potential additions: projected completion (based on time left and progress so far)
#   Estimated completion date (how many points  you've gotten per day so far, and use days left in season)


import tkinter as tk
import math
from datetime import date
from tkinter import ttk


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
badge_options = [
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


# Calculate the different data points that will be shown to the user
def calculate():
    try:
        # The amount of points left to reach the goal points
        current_points = int(entry.get())
        points_remaining = goal_points - current_points
        display = f"Points remaining: {points_remaining}\n"
        
        # Number of games required in each round to reach the goal points
        # Includes losing first round, losing second round, losing final round, and winning final round
        round_one_games = division_round_up(points_remaining, lose_round_one_points)
        round_two_games = division_round_up(points_remaining, lose_round_two_points)
        lose_final_round_games = division_round_up(points_remaining, lose_final_round_points)
        win_final_round_games = division_round_up(points_remaining, win_final_round_points)
        
        # Update the data in the games table and refresh the table to display the updated data
        updated_games_data[0] = (round_one_games, convert_time(round_one_games * round_one_time))
        updated_games_data[1] = (round_two_games, convert_time(round_two_games * round_two_time))
        updated_games_data[2] = (lose_final_round_games, convert_time(lose_final_round_games * lose_final_round_time))
        updated_games_data[3] = (win_final_round_games, convert_time(win_final_round_games * win_final_round_time))
        for i, (games, time) in enumerate(updated_games_data):
            games_table_rows[i][1] = games
            games_table_rows[i][2] = time
        refresh_games_table()
        
        # Estimated amount of play time to reach the goal points
        total_minutes = (points_remaining / 2) * game_time
        display += f"Estimated play time: {convert_time(total_minutes)}\n"
        
        # The amount of points needed per day to reach the goal points
        days_remaining = (season_end_date - todays_date).days
        daily_points = points_remaining // days_remaining
        display += f"Days left in season: {days_remaining}\n"
        display += f"Daily points: {daily_points}\n"
        
        # Maximum time to play each day to reach the goal points (all round 1 games)
        display += f"Daily play time: {convert_time(total_minutes / days_remaining)}"
        
        result_label.config(text=display)
    except ValueError:
        result_label.config(text="Please enter a valid number.")


# Setup UI foundation
root = tk.Tk()
root.title("World Tour Points Calculator")

# Set style for various UI elements
style = ttk.Style(root)
style.theme_use("clam")
style.configure("Treeview", font=("Gadugi", 10))
style.configure("Treeview.Heading", font=("Gadugi", 11))

# Create the dropdown list of badge options
badge_dict = {f"{label}: {points}": (label, points) for label, points in badge_options}
dropdown_options = list(badge_dict.keys())

badge_var = tk.StringVar()
badge_var.set(dropdown_options[-1])  # Default to Emerald 1: 2400

badge_menu = tk.OptionMenu(root, badge_var, *dropdown_options)
badge_menu.config(font=("Gadugi", 11))
badge_menu.pack(pady=(30, 0))

# Whenever badge_var is changed, on_badge_selected will run
badge_var.trace_add("write", on_badge_selected)

# Setup the goal points label
goal_points = badge_dict[badge_var.get()][1]
goal_label = tk.Label(root, text=f"Goal points: {goal_points}", font=("Gadugi", 10))
goal_label.pack(pady=(10, 20))

# Update the goal label text when the game first runs
on_badge_selected("name", 1, "mode")

# Create the entry box and label for it
tk.Label(root, text="Enter current points:", font=("Gadugi", 12)).pack(pady=5)
entry = ttk.Entry(root, font=("Gadugi", 10))
entry.pack(pady=5)
#entry.insert(0, 0)

# Calculate button that will perform the calculations and output data when clicked
calc_button = tk.Button(root, text="Calculate", font=("Gadugi", 10), command=calculate)
calc_button.pack(pady=5)

# Label that will be updated with calculated data
result_label = tk.Label(root, text="", font=("Gadugi", 12))
result_label.pack(pady=(25, 0))

# Create the games table that will display the type of round,
# the number to play to reach the goal points, and the amount of time it will take
columns = ("round_type", "number_of_games", "playtime")
tree = ttk.Treeview(root, columns=columns, show="headings")

tree.heading("round_type", text="Round Type")
tree.heading("number_of_games", text="Number of Games")
tree.heading("playtime", text="Playtime")

tree.column("round_type", width=145, anchor=tk.W)
tree.column("number_of_games", width=145, anchor=tk.CENTER)
tree.column("playtime", width=200, anchor=tk.CENTER)

tree.insert("", "end", values=(row_labels[0], round_one_games, convert_time(round_one_time)))
tree.insert("", "end", values=(row_labels[1], round_two_games, convert_time(round_two_time)))
tree.insert("", "end", values=(row_labels[2], lose_final_round_games, convert_time(lose_final_round_time)))
tree.insert("", "end", values=(row_labels[3], win_final_round_games, convert_time(win_final_round_time)))

tree.pack(padx = 50, pady = (40, 50))

#root.geometry("500x450")
root.mainloop()
