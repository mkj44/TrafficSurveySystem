from tkinter import *
from tkinter import ttk
import sqlite3

# Initialize the main window
root = Tk()
root.title("Traffic Survey Monitoring System")
root.geometry("600x700")

# Toggle Dark/Light Mode
def toggle_mode():
    if root["bg"] == "white":
        root.configure(bg="black")
        label_title.config(bg="black", fg="white")
        for widget in frame_entries.winfo_children():
            widget.config(bg="black", fg="white")
        frame_buttons.config(bg="black")
    else:
        root.configure(bg="white")
        label_title.config(bg="white", fg="black")
        for widget in frame_entries.winfo_children():
            widget.config(bg="white", fg="black")
        frame_buttons.config(bg="white")

# Database Connection
def submit_details():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    
    # Insert Data
    cursor.execute("INSERT INTO traffic_survey (location, date, time, vehicle_count, traffic_condition) VALUES (?, ?, ?, ?, ?)",
                   (entry_location.get(), entry_date.get(), entry_time.get(), entry_vehicle_count.get(), entry_traffic_condition.get()))
    
    connection.commit()
    connection.close()
    
    # Clear the fields
    entry_location.delete(0, END)
    entry_date.delete(0, END)
    entry_time.delete(0, END)
    entry_vehicle_count.delete(0, END)
    entry_traffic_condition.delete(0, END)

# View Records Function
def view_records():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM traffic_survey")
    records = cursor.fetchall()
    
    # Display Records
    for i, record in enumerate(records):
        tree.insert('', 'end', values=(record))

    connection.close()

# UI Elements
label_title = Label(root, text="Traffic Survey Monitoring System", font=("Arial", 20))
label_title.pack(pady=20)

frame_entries = Frame(root)
frame_entries.pack(pady=20)

# Entries for Traffic Survey Details
entry_fields = {
    "Location": "",
    "Date (YYYY-MM-DD)": "",
    "Time (HH:MM)": "",
    "Vehicle Count": "",
    "Traffic Condition": ""
}

entries = {}

for field, value in entry_fields.items():
    label = Label(frame_entries, text=field)
    label.pack(pady=5)
    entry = Entry(frame_entries)
    entry.pack(pady=5)
    entries[field] = entry

entry_location = entries["Location"]
entry_date = entries["Date (YYYY-MM-DD)"]
entry_time = entries["Time (HH:MM)"]
entry_vehicle_count = entries["Vehicle Count"]
entry_traffic_condition = entries["Traffic Condition"]

# Buttons
frame_buttons = Frame(root)
frame_buttons.pack(pady=20)

submit_button = Button(frame_buttons, text="Submit", command=submit_details)
submit_button.grid(row=0, column=0, padx=10)

view_button = Button(frame_buttons, text="View Records", command=view_records)
view_button.grid(row=0, column=1, padx=10)

dark_mode_button = Button(frame_buttons, text="Dark Mode", command=toggle_mode)
dark_mode_button.grid(row=0, column=2, padx=10)

# Table to View Records
tree = ttk.Treeview(root, columns=("ID", "Location", "Date", "Time", "Vehicle Count", "Traffic Condition"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Location", text="Location")
tree.heading("Date", text="Date")
tree.heading("Time", text="Time")
tree.heading("Vehicle Count", text="Vehicle Count")
tree.heading("Traffic Condition", text="Traffic Condition")
tree.pack(pady=20)

# Run the application
root.mainloop()