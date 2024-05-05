from setup import install_packages, required_packages
from menu import menu, view_city_by_country, update_city_population, add_new_person, delete_person, view_countries_by_population, show_twinned_cities, twin_with_dublin
import time
from yaspin import yaspin

def main():
    
    install_packages(required_packages)

    choice_to_function = {
        '1': view_city_by_country,
        '2': update_city_population,
        '3': add_new_person,
        '4': delete_person,
        '5': view_countries_by_population,
        '6': show_twinned_cities,
        '7': twin_with_dublin,
        'x': lambda: print("Exiting the application...")
    }
    while True:
        with yaspin(text="Loading main menu...", color="blue"):        
            time.sleep(1)
        choice = menu()
        if choice == 'x':
            break
        if choice in choice_to_function:
            choice_to_function[choice]()
        if choice is None:
            print("No option selected, exiting the application...")
            break

if __name__ == "__main__":
    main()