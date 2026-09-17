from UNIT_PROJECT.SmartPlantCoach.garden import ai_helper
from UNIT_PROJECT.SmartPlantCoach.garden import plant_manager


def choose_location():
    """Ask whether the plant is indoor or outdoor."""
    while True:
        print("\nWhere is the plant?")
        print("1. Indoor")
        print("2. Outdoor")

        choice = input("Choose 1 or 2: ").strip()

        if choice == "1":
            return "Indoor"

        elif choice == "2":
            return "Outdoor"

        else:
            print("Invalid choice. Please enter 1 or 2.")


def choose_weather():
    """Ask about the current weather."""
    while True:
        print("\nHow is the weather?")
        print("1. Hot")
        print("2. Moderate")
        print("3. Cold")

        choice = input("Choose 1, 2, or 3: ").strip()

        if choice == "1":
            return "Hot"

        elif choice == "2":
            return "Moderate"

        elif choice == "3":
            return "Cold"

        else:
            print("Invalid choice. Please choose from 1 to 3.")


def back_to_menu():
    """Wait until the user presses 0."""
    while input("\nPress 0 to return to the menu: ").strip() != "0":
        print("Please enter 0.")


plants = plant_manager.load_plants()


while True:

    print("\n==============================")
    print("      SMART PLANT COACH")
    print("==============================")
    print("1. Add Plant")
    print("2. View My Plants")
    print("3. Water Plant")
    print("4. Care Schedule")
    print("5. Update Plant")
    print("6. Garden Mood")
    print("7. Exit")

    choice = input("\nChoose an option: ").strip()


    if choice == "1":

        name = input("\nPlant name: ").strip()

        if not name:
            print("Plant name cannot be empty.")
            back_to_menu()
            continue

        location = choose_location()
        weather = choose_weather()

        try:
            print("\nAI is creating your care plan...")

            care = ai_helper.get_care_plan(
                name,
                location,
                weather
            )

            plant_manager.add_plant(
                plants,
                name,
                location,
                weather,
                care
            )

            print("\nPlant added successfully 🌱")

            plant_manager.show_plant_details(
                plants,
                name
            )

            while True:
                watered = input(
                    "\nDid you water this plant now? "
                    "(1 = Yes, 2 = No): "
                ).strip()

                if watered == "1":
                    plant_manager.water_plant(
                        plants,
                        name
                    )
                    break

                elif watered == "2":
                    print(
                        "Okay, this plant will appear as "
                        "'Water today' in your schedule."
                    )
                    break

                else:
                    print("Please enter 1 or 2.")

        except (
            ValueError,
            ConnectionError,
            EnvironmentError
        ) as error:
            print(f"\nError: {error}")

        back_to_menu()


    elif choice == "2":

        plant_manager.display_plants(plants)

        if plants:
            answer = input(
                "\nEnter a plant name for care details "
                "or press Enter to skip: "
            ).strip()

            if answer:
                try:
                    plant_manager.show_plant_details(
                        plants,
                        answer
                    )

                except ValueError as error:
                    print(f"Error: {error}")

        back_to_menu()


    elif choice == "3":

        name = input(
            "\nWhich plant did you water? "
        ).strip()

        try:
            plant_manager.water_plant(
                plants,
                name
            )

        except ValueError as error:
            print(f"Error: {error}")

        back_to_menu()


    elif choice == "4":

        plant_manager.show_schedule(plants)

        back_to_menu()


    elif choice == "5":

        name = input(
            "\nPlant name to update: "
        ).strip()

        try:
            # Check that the plant exists first
            plant_manager.find_plant(
                plants,
                name
            )

            location = choose_location()
            weather = choose_weather()

            print("\nAI is updating the care plan...")

            care = ai_helper.get_care_plan(
                name,
                location,
                weather
            )

            plant_manager.update_plant(
                plants,
                name,
                location,
                weather,
                care
            )

            print("Plant updated successfully.")

        except (
            ValueError,
            ConnectionError,
            EnvironmentError
        ) as error:
            print(f"Error: {error}")

        back_to_menu()


    elif choice == "6":

        plant_manager.garden_mood(plants)

        back_to_menu()


    elif choice == "7":

        print("\nKeep growing 🌿")
        break


    else:

        print(
            "\nInvalid choice. "
            "Please choose from 1 to 7."
        )