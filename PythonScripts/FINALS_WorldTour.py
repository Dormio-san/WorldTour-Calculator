# Planned features: 
# Let player select goal badge from drop down. Include number of points for that tier.
# Input box for current number of points.
# Display number of days remaining in the season. Season 8 ends December 11 2025
# Have points to next rank stat
# List number of daily points needed. Points needed / days left = daily points
# Include estimate for time to play as well as daily play time. 
# Also have input for player to put how long a match is. Maybe they want to add loading time to calculation.
# Potential additions: projected completion (based on time left and progress so far)
#   Estimated completion date (how many points  you've gotten per day so far, and use days left in season)

import tkinter as tk

def calculate():
    try:
        current_points = int(entry.get())
        points_left = 2400 - current_points
        total_minutes = (points_left / 2) * 10

        hours = int(total_minutes // 60)
        minutes = int(total_minutes % 60)
        days = hours // 24
        display = f"Points to target: {points_left}\n"
        if days > 0:
            display += f"Estimated time: {days} days, {hours%24} hours, {minutes} minutes"
        elif hours > 0:
            display += f"Estimated time: {hours} hours, {minutes} minutes"
        else:
            display += f"Estimated time: {minutes} minutes"
        result_label.config(text=display)
    except ValueError:
        result_label.config(text="Please enter a valid number.")

root = tk.Tk()
root.title("World Tour Points Calculator")

tk.Label(root, text="Enter current points:").pack(pady=5)
entry = tk.Entry(root)
entry.pack(pady=5)

calc_button = tk.Button(root, text="Calculate", command=calculate)
calc_button.pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

root.geometry("350x180")
root.mainloop()
