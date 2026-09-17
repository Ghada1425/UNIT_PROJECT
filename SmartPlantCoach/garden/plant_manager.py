import json
import os
from datetime import datetime, timedelta

# Build the path to plants.json so saving works from any terminal location.
DATA_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "plants.json"
)


def load_plants():
    """Load saved plants from JSON."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Warning: plants.json is empty or damaged.")
        return []


def save_plants(plants):
    """Save all plant data to JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(plants, file, indent=4, ensure_ascii=False)


def find_plant(plants, name):
    """Find a plant by name."""
    for plant in plants:
        if plant["name"].lower() == name.lower():
            return plant
    raise ValueError("Plant not found.")


def add_plant(plants, name, location, weather, care):
    """Add a new plant and its AI care plan."""
    for plant in plants:
        if plant["name"].lower() == name.lower():
            raise ValueError("This plant already exists.")

    plants.append({
        "name": name,
        "location": location,
        "weather": weather,
        "watering_days": care["watering_days"],
        "light": care["light"],
        "care_tip": care["care_tip"],
        "last_watered": None
    })
    save_plants(plants)


def display_plants(plants):
    """Display all plants in a simple table."""
    if not plants:
        print("\nYour garden is empty.")
        return

    print("\nMY PLANTS")
    print("-" * 62)
    print(f"{'NAME':<18}{'PLACE':<12}{'WEATHER':<12}{'WATER':<15}")
    print("-" * 62)

    for plant in plants:
        water = f"Every {plant['watering_days']} days"
        print(
            f"{plant['name']:<18}"
            f"{plant['location']:<12}"
            f"{plant['weather']:<12}"
            f"{water:<15}"
        )


def show_plant_details(plants, name):
    """Display the saved care advice for one plant."""

    plant = find_plant(plants, name)

    print(f"\nCARE CARD — {plant['name']}")
    print("-" * 40)

    print(f"Place:   {plant['location']}")
    print(f"Weather: {plant['weather']}")
    print(f"Water:   Every {plant['watering_days']} days")
    print(f"Light:   {plant['light']}")
    print(f"Tip:     {plant['care_tip']}")

    if plant["last_watered"] is None:
        print("Status:  Not watered yet — water it today 💧")

    else:
        last_date = datetime.strptime(
            plant["last_watered"],
            "%Y-%m-%d"
        ).date()

        next_date = last_date + timedelta(
            days=plant["watering_days"]
        )

        print(f"Last watered: {plant['last_watered']}")
        print(f"Next watering: {next_date}")

def water_plant(plants, name):
    """Mark a plant as watered and show the next watering date."""

    plant = find_plant(plants, name)

    today = datetime.now().date()

    if plant["last_watered"] is not None:

        last_date = datetime.strptime(
            plant["last_watered"],
            "%Y-%m-%d"
        ).date()

        if last_date == today:
            print("This plant is already watered today 💧")
            return

    plant["last_watered"] = today.strftime("%Y-%m-%d")

    save_plants(plants)

    next_date = today + timedelta(
        days=plant["watering_days"]
    )

    print(f"Great! {name} was watered today 🌱")
    print(f"Next watering: {next_date}")
    
def mark_watered(plants, name):
    """Mark the plant as watered today."""
    plant = find_plant(plants, name)
    plant["last_watered"] = datetime.now().strftime("%Y-%m-%d")
    save_plants(plants)

def show_schedule(plants):
    """Display the next watering date and status."""
    if not plants:
        print("\nYour garden is empty.")
        return

    today = datetime.now().date()

    print("\nCARE SCHEDULE")
    print("-" * 58)
    print(f"{'NAME':<18}{'NEXT WATERING':<18}{'STATUS':<20}")
    print("-" * 58)

    for plant in plants:
        if plant["last_watered"] is None:
          print(
        f"{plant['name']:<18}"
        f"{'Today':<18}"
        f"{'Not watered yet':<20}"
    )
          continue
        last_date = datetime.strptime(
            plant["last_watered"], "%Y-%m-%d"
        ).date()

        next_date = last_date + timedelta(
            days=plant["watering_days"]
        )

        if next_date < today:
            status = f"Late by {(today - next_date).days} day(s)"
        elif next_date == today:
            status = "Water today"
        else:
            status = f"In {(next_date - today).days} day(s)"

        print(
            f"{plant['name']:<18}"
            f"{str(next_date):<18}"
            f"{status:<20}"
        )


def update_plant(plants, name, location, weather, care):
    """Update conditions and replace the AI care plan."""
    plant = find_plant(plants, name)

    plant["location"] = location
    plant["weather"] = weather
    plant["watering_days"] = care["watering_days"]
    plant["light"] = care["light"]
    plant["care_tip"] = care["care_tip"]

    save_plants(plants)


def garden_mood(plants):
    """Show a mood based on how many plants are overdue."""
    if not plants:
        print("\nGarden Mood: Empty garden 🌱")
        return

    today = datetime.now().date()
    overdue = 0

    for plant in plants:
        if plant["last_watered"] is None:
          overdue += 1
          continue
        last_date = datetime.strptime(
            plant["last_watered"], "%Y-%m-%d"
        ).date()

        due_date = last_date + timedelta(
            days=plant["watering_days"]
        )

        if due_date < today:
            overdue += 1

    # Creative feature: the whole garden gets a care mood.
    if overdue == 0:
        mood = "Thriving 🌿✨"
    elif overdue < len(plants):
        mood = "Needs a little care 🌱"
    else:
        mood = "Rescue mode 🪴"

    print("\nGARDEN MOOD")
    print("-" * 30)
    print(f"Mood: {mood}")
    print(f"Plants on track: {len(plants) - overdue}/{len(plants)}")
