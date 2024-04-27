from setup import install_packages, required_packages
from database import connect_mysql, connect_neo4j
from rich import print
import typer
from typing import List
from pyfiglet import Figlet
import inquirer
from tabulate import tabulate
from yaspin import yaspin
import time

app = typer.Typer()

def display_menu() -> str:
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
    return answers['choice']

@yaspin(text="Retrieving Cities by Country...")
@app.command()
def view_cities_by_country():
    time.sleep(5)
    print("ASDF")

@app.command()
def update_city_population():
    print("Updating City Population")

@app.command()
def add_new_person():
    print("Adding New Person")

@app.command()
def delete_person():
    print("Deleting Person")

@app.command()
def view_countries_by_population():
    print("Viewing Countries by Population")

@app.command()
def show_twinned_cities():
    print("Showing Twinned Cities")

@app.command()
def twin_with_dublin():
    print("Twinning with Dublin")

if __name__ == "__main__":

    # install_packages(required_packages)

    connect_mysql()
    connect_neo4j()
    print("Running main application")


    choice_to_function = {
        '1': view_cities_by_country,
        '2': update_city_population,
        '3': add_new_person,
        '4': delete_person,
        '5': view_countries_by_population,
        '6': show_twinned_cities,
        '7': twin_with_dublin,
    }

    choice = display_menu()
    if choice == 'x':
        typer.echo("Exiting the application...")
        raise typer.Exit()
    else:
        choice_to_function[choice]()