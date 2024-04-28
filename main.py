from setup import install_packages, required_packages
from database import connect_mysql, connect_neo4j
from rich import print
import inquirer
from typing import List
from pyfiglet import Figlet
from tabulate import tabulate
from yaspin import yaspin
import time
import pymysql

def menu() -> str:
    f = Figlet(font='slant')
    print(f.renderText('Main Menu'))

    choices = [
        ("1 - View Cities by Country", "1"),
        ("2 - Update City Population", "2"),
        ("3 - Add New Person", "3"),
        ("4 - Delete Person", "4"),
        ("5 - View Countries by Population", "5"),
        ("6 - Show Twinned Cities", "6"),
        ("7 - Twin with Dublin", "7"),
        ("x - Exit application", "x")
    ]

    questions = [
        inquirer.List('choice',
                      message="What do you want to do?",
                      choices=choices
                      ),
    ]
    answers = inquirer.prompt(questions)
    if answers is None:
        return None
    else:
        return answers['choice']

def view_city_by_country():
    questions = [inquirer.Text('country', message="Enter the country to view its cities")]
    answers = inquirer.prompt(questions)
    if not answers:
        print("No country entered, exiting...")
        return
    country = answers['country']
    if not country:
        print("No country entered, exiting...")
        return
    page_size = 2
    current_offset = 0
    conn = connect_mysql()
    try:
        while True:
            with conn.cursor() as cursor:
                query = """
                    SELECT country.name AS country, city.name AS city, city.district, city.population
                    FROM city
                    LEFT JOIN country ON country.code = city.countrycode
                    WHERE country.name LIKE CONCAT('%%', %s, '%%')
                    ORDER BY country.name
                    LIMIT %s OFFSET %s;
                """
                cursor.execute(query, (country, page_size, current_offset))
                result = cursor.fetchall()

                if not result:
                    print("No more cities to display.")
                    print("\n")
                    break

                headers = ["Country", "City", "District", "Population"]
                table = tabulate(result, headers="keys", tablefmt="fancy_grid")
                print(table)

                current_offset += page_size
                user_input = input("\n-- Quit (q) --\n")
                if user_input.lower() == 'q':
                    print("\n")
                    break
    except pymysql.MySQLError as e:
        print(f"An error occurred while trying to query the database: {e}")
    finally:
        conn.close()

def update_city_population():
    print("Updating City Population")

def add_new_person():
    print("Adding New Person")

def delete_person():
    print("Deleting Person")

def view_countries_by_population():
    print("Viewing Countries by Population")

def show_twinned_cities():
    print("Showing Twinned Cities")

def twin_with_dublin():
    print("Twinning with Dublin")

def main():
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
        time.sleep(2)
        choice = menu()
        if choice == 'x':
            break
        if choice in choice_to_function:
            choice_to_function[choice]()
        if choice is None:
            print("No option selected, exiting the application...")
            break


    # install_packages(required_packages)
    # connect_neo4j()

if __name__ == "__main__":
    main()

