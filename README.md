# Pregnancy Tracker

Pregnancy Tracker is a Python-based command-line tool that helps you log and monitor your pregnancy progress.It simplifies tracking key milestones, such as weeks, weight, mood, symptoms, and notes, while calculating your estimated due date. All data is stored locally in a JSON file within the project folder.

---

## Features

- Add, view, update, and delete pregnancy entries.  
- Calculate current pregnancy week and estimated due date.  
- Track mood, symptoms, weight, and notes.  
- Display overall pregnancy progress including weight changes.  
- Summarize symptoms across all entries.  
- Supports weight units in kilograms (kg) or pounds (lbs).  
- Stores data locally in JSON format.  

---

## Installation

1. Ensure Python 3.6 or higher is installed.  
2. Run the program with:

```bash
python pregnancy_tracker.py
```

---


## Usage

1. Launch the program.  
2. Enter your name when prompted.  
3. Choose your preferred weight unit (kg or lbs).  
4. Use the menu to:  
   - Add new entries (week, mood, symptoms, weight, notes)  
   - View all entries  
   - Update or delete entries  
   - Calculate current pregnancy week  
   - Show overall progress  
   - Display a symptom summary  
   - Save or load entries  
5. Exit the program when finished.  

---

## Data Storage

All data is saved in `entry.json`. Each entry contains:  

- `id`: Unique identifier  
- `date`: Timestamp of the entry  
- `week`: Pregnancy week  
- `mood`: User mood  
- `symptoms`: List of reported symptoms  
- `weight`: Current weight  
- `notes`: Additional notes  

