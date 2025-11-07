# Planned features: 
# Let player select goal badge from drop down. Include number of points for that tier.
# Input box for current number of points.
# Display number of days remaining in the season. Season 8 ends December 11 2025
# Have points to next rank stat
# List number of daily points needed. Points needed / days left = daily points
# Include estimate for time to play as well as daily play time. 
# Also have input for player to put how long a match is. Maybe they want to add loading time to calculation.
# Daily playtime: minimum amount of time needed to play each day.
# Estimate play time for each type of round. For example, how much play time if player won final round each time.
# Potential additions: projected completion (based on time left and progress so far)
#   Estimated completion date (how many points  you've gotten per day so far, and use days left in season)

import tkinter as tk
import math
from datetime import date
from tkinter import ttk

# Estimated time each game will take
game_time = 10

# Points awarded for each round in world tour
lose_round_one_points = 2
lose_round_two_points = 6
lose_final_round_points = 14
win_final_round_points = 25

# Number of games needed to reach the goal points (default is 0)
round_one_games = 0
round_two_games = 0
lose_final_round_games = 0
win_final_round_games = 0

# Time spent playing for each type of round
round_one_time = game_time
round_two_time = game_time * 2
lose_final_round_time = game_time * 3
win_final_round_time = game_time * 3

# Dates used to determine how much time is left in the season
season_end_date = date(2025, 12, 11)
today_date = date.today()


# Options in "Label: value" format
rank_options = [
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
    "Round one games",
    "Round two games",
    "Lose final round games",
    "Win final round games",
]

# Full table rows in the games table
updated_table_rows = [
    [row_labels[0], round_one_games, round_one_time],
    [row_labels[1], round_two_games, round_two_time],
    [row_labels[2], lose_final_round_games, lose_final_round_time],
    [row_labels[3], win_final_round_games, win_final_round_time],
]

# Updated data used to update the data in table rows
new_data = [
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
    
    if days > 0:
        return f"{days} days, {hours%24} hours, {minutes} minutes\n"
    elif hours > 0:
        return f"{hours} hours, {minutes} minutes\n"
    else:
        return f"{minutes} minutes\n"
 
 
# Refresh the table that contains number of games and estimated play time for each round type
def refresh_games_table():
    # Clear all existing rows
    for item in tree.get_children():
        tree.delete(item)

    # Insert updated rows
    for row in updated_table_rows:
        tree.insert("", "end", values=row)

    
def on_rank_selected(var_name, index, mode):
    # When user selects, update goal_points
    label, points = rank_dict[rank_var.get()]
    global goal_points
    goal_points = points
    goal_label.config(text=f"Goal points: {goal_points} ({label})")


def calculate():
    try:
        # The amount of points left to reach the goal points
        current_points = int(entry.get())
        points_remaining = goal_points - current_points
        
        # The number of games needed to reach the goal points
        # Includes losing first round, losing second round, losing final round, and winning final round
        round_one_games = division_round_up(points_remaining, lose_round_one_points)
        round_two_games = division_round_up(points_remaining, lose_round_two_points)
        lose_final_round_games = division_round_up(points_remaining, lose_final_round_points)
        win_final_round_games = division_round_up(points_remaining, win_final_round_points)
        
        display = f"Points remaining: {points_remaining}\n"
        
        # Estimated amount of play time to reach the goal points
        total_minutes = (points_remaining / 2) * game_time
        display += f"Estimated play time: {convert_time(total_minutes)}"
        
        # Estimated number of games required in each round to reach the goal points
        new_data[0] = (round_one_games, convert_time(round_one_games * round_one_time))
        new_data[1] = (round_two_games, convert_time(round_two_games * round_two_time))
        new_data[2] = (lose_final_round_games, convert_time(lose_final_round_games * lose_final_round_time))
        new_data[3] = (win_final_round_games, convert_time(win_final_round_games * win_final_round_time))
        for i, (games, time) in enumerate(new_data):
            updated_table_rows[i][1] = games
            updated_table_rows[i][2] = time
        
        # The amount of points needed per day to reach the goal points
        days_remaining = (season_end_date - today_date).days
        daily_points = points_remaining / days_remaining
        display += f"Days left in the season: {days_remaining}\n"
        display += f"Points needed per day: {daily_points}\n"
        
        # Update the table that shows info on the games
        refresh_games_table()
        
        result_label.config(text=display)
    except ValueError:
        result_label.config(text="Please enter a valid number.")


root = tk.Tk()
root.title("World Tour Points Calculator")

rank_dict = {f"{label}: {points}": (label, points) for label, points in rank_options}
dropdown_options = list(rank_dict.keys())

rank_var = tk.StringVar()
rank_var.set(dropdown_options[-1])  # Default to Emerald 1: 2400

goal_points = rank_dict[rank_var.get()][1]

rank_menu = tk.OptionMenu(root, rank_var, *dropdown_options)
rank_menu.pack(pady=8)

# Whenever rank_var is changed, on_rank_selected will run
rank_var.trace_add("write", on_rank_selected)

goal_label = tk.Label(root, text=f"Goal points: {goal_points}")
goal_label.pack(pady=8)

# Update the goal label text when the game first runs
on_rank_selected("name", 1, "mode")

tk.Label(root, text="Enter current points:").pack(pady=5)
entry = tk.Entry(root)
entry.pack(pady=5)

calc_button = tk.Button(root, text="Calculate", command=calculate)
calc_button.pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=30)

# Define columns in the table
columns = ("round_type", "number_of_games", "playtime")

# Create Treeview with these columns, show="headings" hides the default first column
tree = ttk.Treeview(root, columns=columns, show="headings")

# Define headings and their display text
tree.heading("round_type", text="Round Type")
tree.heading("number_of_games", text="Number of Games")
tree.heading("playtime", text="Playtime")

# Define column widths and alignment
tree.column("round_type", width=150, anchor=tk.W)
tree.column("number_of_games", width=120, anchor=tk.CENTER)
tree.column("playtime", width=150, anchor=tk.CENTER)

# Insert rows
tree.insert("", "end", values=("Round one games", round_one_games, round_one_time))
tree.insert("", "end", values=("Round two games", round_two_games, round_two_time))
tree.insert("", "end", values=("Lose final round games", lose_final_round_games, lose_final_round_time))
tree.insert("", "end", values=("Win final round games", win_final_round_games, win_final_round_time))

tree.pack(expand=True, fill=tk.BOTH)

#root.geometry("500x450")
root.mainloop()
