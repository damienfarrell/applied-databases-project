from setup import install_packages, required_packages
import time
import importlib

def main():
    install_packages(required_packages)

    menu_module = importlib.import_module("menu")
    yaspin_module = importlib.import_module("yaspin")
    
    choice_to_function = {
        '1': menu_module.view_city_by_country,
        '2': menu_module.update_city_population,
        '3': menu_module.add_new_person,
        '4': menu_module.delete_person,
        '5': menu_module.view_countries_by_population,
        '6': menu_module.show_twinned_cities,
        '7': menu_module.twin_with_dublin,
        'x': lambda: print("Exiting the application...")
    }

    while True:
        with yaspin_module.yaspin(text="Loading main menu...", color="blue"):
            time.sleep(1)
        choice = menu_module.menu()
        if choice == 'x':
            break
        if choice in choice_to_function:
            choice_to_function[choice]()
        if choice is None:
            print("No option selected, exiting the application...")
            break

if __name__ == "__main__":
    main()