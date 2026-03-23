from datetime import datetime, timedelta
import json
import os


DATA_FILE = "entry.json"

# -------- Data handling  -------- 


def load_data(filename=DATA_FILE):
    """Load entries from json file"""
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                data= json.load(f)
                if isinstance(data, list):
                    data = {'entries': data, 'unit': None, 'username': None}

                data.setdefault('entries', [])
                data.setdefault('unit', None)
                if not data.get("username"):
                    data['username'] = input("Enter your name: ").strip()
                    save_data(data)
                return data
            except json.JSONDecodeError:
                return {'username': None, 'unit': None, 'entries': []}
    return {'username': None, 'unit': None, 'entries': []}


def save_data(data, filename=DATA_FILE):
    """Save entries to JSON file"""
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# -------- Utilities  -------- 

def generate_entry_id(pregnancy_log):
    if not pregnancy_log:
        return 1
    return max(entry['id'] for entry in pregnancy_log) + 1



def find_entry_by_id(pregnancy_log, entry_id):
    for entry in pregnancy_log:
        if entry["id"] == entry_id:
            return entry
    return None


def get_valid_id():
    while True:
        try:
            entry_id = int(input("Enter entry ID: "))
            return entry_id
        except ValueError:
            print("Invalid input. Please enter a number.")

def format_entry(entry):
    print("=" * 50)
    print(f"Entry ID: {entry['id']}")
    print(f"Date:  {entry['date']}")
    print(f"Week:  {entry['week']}")
    print(f"Mood: {entry['mood']}")
    print(f"Symptoms: {', '.join(entry['symptoms'])}")
    print(f"Weight: {entry['weight']}")
    print(f"Notes:  {entry['notes']}")
    print("=" * 50)

def start_date_pregnancy():
    while True:
        start_date_str = input("Enter start date (DD/MM/YYYY): ")
        try:
            start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
            return start_date
        except ValueError:
            print("Invalid date format. Please try again.")

def format_weight(value, unit):
    return f"{value:.2f} {unit}"

def get_valid_number(prompt, number_type=float):
    while True:
        try:
            return number_type(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")


# -------- Entry Operations --------


def add_entry(pregnancy_log, unit):
    entry_id = generate_entry_id(pregnancy_log)
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    week = get_valid_number("Enter pregnancy week: ", int)
    mood = input("Enter mood: ")
    symptoms = [s.strip().lower() for s in input("Enter symptoms (comma separated): ").split(",") if s.strip()]
    weight = get_valid_number(f"Enter weight ({unit}): ", float)
    notes = input("Enter notes: ")

    entry = {
        "id": entry_id,
        "date": date,
        "week": week,
        "mood": mood,
        "symptoms": symptoms,
        "weight": weight,
        "notes": notes
    }
    pregnancy_log.append(entry)
    print("\n✅ Entry added successfully!\n")


def view_entries(pregnancy_log): 
    if not pregnancy_log:
        print("\n⚠️  No entries yet. Add a new entry!")
        return
    print("\n📋 All Entries:")
    for entry in pregnancy_log:
        format_entry(entry)


def update_entry(pregnancy_log):
    if not pregnancy_log:
        print("\n⚠️ No entries available to update.")
        return

    entry_id = get_valid_id()
    entry = find_entry_by_id(pregnancy_log, entry_id)
    if not entry:
        print("⚠️ Entry not found.")
        return

    print("\nLeave blank to keep the current value.\n")
    new_week = input(f"Enter new week ({entry['week']}): ")
    new_mood = input(f"Enter new mood ({entry['mood']}): ")
    new_symptoms = input(f"Enter new symptoms ({','.join(entry['symptoms'])}): ")
    new_weight = input(f"Enter new weight ({entry['weight']}): ")
    new_notes = input(f"Enter new notes ({entry['notes']}): ")

    if new_week:
        try:
            entry["week"] = int(new_week)
        except ValueError:
            print("Invalid week. Keeping previous value.")
    if new_mood: entry["mood"] = new_mood
    if new_symptoms: entry["symptoms"] = [s.strip().lower() for s in new_symptoms.split(",") if s.strip()]
    if new_weight:
        try:
            entry["weight"] = float(new_weight)
        except ValueError:
            print("Invalid weight. Keeping previous value.")
    if new_notes: entry["notes"] = new_notes

    print("\n✅ Entry updated successfully!")


def delete_entry(pregnancy_log):
    if not pregnancy_log:
        print("\n⚠️ No entries to delete.")
        return
    entry_id = get_valid_id()
    entry = find_entry_by_id(pregnancy_log, entry_id)
    if entry:
        pregnancy_log.remove(entry)
        print("✅ Entry deleted successfully!")
    else:
        print("⚠️ Entry not found.")

# -------- Calculations & Summaries  -------- 

def calculate_week():
    start_date = start_date_pregnancy()
    today=datetime.now()
    difference = today - start_date
    days_pregnant = difference.days
    week = days_pregnant // 7
    print(f"\n⏳ You are approximately in week {week} of pregnancy.")

def estimate_due_date():
    start_date = start_date_pregnancy()
    due_date = start_date + timedelta(days=280)
    print(f"\n📅 Estimated due date: {due_date.strftime('%d/%m/%Y')}")


def show_progress(pregnancy_log, unit):
    if not pregnancy_log:
        print("\n⚠️ No entries available to show.")
        return

    total_entries = len(pregnancy_log)
    latest_entry = pregnancy_log[-1]
    latest_week = latest_entry['week']

   
    weights= [entry['weight']for entry in pregnancy_log]
    avg = sum(weights)/len(weights)
    first_weight = pregnancy_log[0]['weight']
    latest_weight = pregnancy_log[-1]['weight']
    difference_weight = latest_weight - first_weight

    print("\n📊 Pregnancy Progress:")
    print(f"Total entries: {total_entries}")
    print(f"Latest week: {latest_week}")
    print(f"Average weight: {format_weight(avg, unit)}")

    if difference_weight > 0:
        print(f"Weight increased by {difference_weight:.2f} {unit}")
    elif difference_weight < 0:
        print(f"Weight decreased by {-difference_weight:.2f} {unit}")
    else:
        print("No weight change.")


def symptom_summary(pregnancy_log):
    if not pregnancy_log:
        print("\n⚠️ No entries available to display.")
        return

    symptoms_count= {}
    for entry in pregnancy_log:
        for symptom in entry["symptoms"]:
            clean_symptom = symptom.strip().lower()
            if clean_symptom in symptoms_count:
                symptoms_count[clean_symptom] += 1
            else:
                symptoms_count[clean_symptom] = 1

    print("\n🩺  Symptom Summary:\n")
    for symptom, count in symptoms_count.items():
        print(f"{symptom.capitalize()}: {count} time(s)")

# -------- Menu --------

def display_start_menu():
    """This will display the list of options"""
    print("\n" + "="*50)
    print("Pregnancy Tracker")
    print(" 1. Add new entry")
    print(" 2. View entries")
    print(" 3. Update entry")
    print(" 4. Delete entry")
    print(" 5. Calculate pregnancy week")
    print(" 6. Show pregnancy progress")
    print(" 7. Symptom summary")
    print(" 8. Save entries")
    print(" 9. Load entries")
    print("10. Change unit")
    print("11. Exit")
    print("="*50)

# -------- Main --------

def main():
    data = load_data()
    pregnancy_log = data['entries']
    unit = data.get('unit')
    username = data['username']

    print(f"\n👋 Welcome {username}!\n")

    while unit not in ['kg', 'lbs']:
        unit = input("Choose weight unit (kg/lbs): ").lower()
        data['unit'] = unit
        save_data(data)

    while True:
        display_start_menu()
        choice = input("\n Enter your choice: (1 - 11)" )

        if choice == "1": add_entry(pregnancy_log, unit)
        elif choice == "2": view_entries(pregnancy_log)
        elif choice == "3": update_entry(pregnancy_log)
        elif choice == "4": delete_entry(pregnancy_log)
        elif choice == "5": calculate_week()
        elif choice == "6": show_progress(pregnancy_log, unit)
        elif choice == "7": symptom_summary(pregnancy_log)
        elif choice == "8": save_data({'username':username, 'unit': unit, 'entries': pregnancy_log})
        elif choice == "9":
            data = load_data()
            username = data['username']
            pregnancy_log = data['entries']
            unit = data.get('unit')
            print("\n✅ Entries loaded successfully!\n")
        elif choice == "10":
            unit = input("Choose weight unit (kg/lbs): ").lower()
            data = {'username': username, 'unit': unit, 'entries': pregnancy_log}
            save_data(data)
        elif choice == "11":
            print("\n🙏  Thank you for using Pregnancy Tracker. Goodbye!")
            break
        else:
            print("⚠️  Invalid choice. Please enter a number from 1 to 11.")


if __name__ == "__main__":
    main()

