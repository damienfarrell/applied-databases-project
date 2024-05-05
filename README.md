![Banner Image](./markdown-images/APPLIED_DATABASES.png)
---
![GitHub last commit](https://img.shields.io/github/last-commit/damienfarrell/applied-databases-project)
![GitHub contributors](https://img.shields.io/github/contributors/damienfarrell/applied-databases-project)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/damienfarrell/applied-databases-project)

# **Application Overview**

This Python application provides a menu-driven interface CLI, using MySQL and Neo4j databases.

## **Features**

- **View Cities by Country**: Allows users to list cities in a specified country.
- **Update City Population**: Users can increase or decrease the population of a specified city.
- **Add New Person**: Add a new person's details to the database.
- **Delete Person**: Remove a person's details from the database based on their ID.
- **View Countries by Population**: Display countries that meet certain population criteria (less than, greater than, or equal to a specified number).
- **Show Twinned Cities**: List all pairs of twinned cities from the database.
- **Twin with Dublin**: Establish a new twinning relationship between any city and Dublin.

## **Setup and Installation**

The application requires several Python packages to function, which can be installed using the `install_packages` function that reads from a predefined list of `required_packages`. 

## **Main Menu**

Upon execution, the main menu is presented where users can choose an action by selection a menu option with the up and down arrows. The application provides feedback and prompts through a CLI interface powered by libraries such as `inquirer` for interactive prompts and `yaspin` for spinners during operations, enhancing user experience.

## **Database Connection**

The application connects to MySQL and Neo4j databases to perform operations. Ensure that database credentials and access details are configured correctly in your environment.

## **Dependencies**

Some of the key external libraries used in this application include:

- `inquirer`: For creating interactive command line user interfaces.
- `yaspin`: Provides a spinner for command line applications indicating progress.
- `pyfiglet`: Used for ASCII art headers.
- `tabulate`: To format tables for display in command line.
- `PyMySQL`: A MySQL database connector for Python.
- `neo4j`: Neo4j driver for Python for connecting to Neo4j database.

Ensure all dependencies are installed using the provided `install_packages` script which checks for missing packages and installs them.