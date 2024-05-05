from database import connect_mysql, connect_neo4j
from rich import print
import inquirer
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
    questions = [inquirer.Text('country', message="Enter Country")]
    answers = inquirer.prompt(questions)
    if not answers:
        print("No country entered, exiting...")
        return
    country = answers['country']
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
                with yaspin(text="Fetching cities...", color="green") as spinner:
                    time.sleep(.5)
                    cursor.execute(query, (country, page_size, current_offset))
                    result = cursor.fetchall()
                spinner.ok("✔")
                if not result:
                    print("No more cities to display.")
                    print("\n")
                    break

                table = tabulate(result, headers="keys", tablefmt="fancy_grid")
                print(table)

                current_offset += page_size
                user_input = input("\n-- Quit (q) --\n")
                with yaspin(text="quitting...", color="green"):
                    if user_input.lower() == 'q':
                        time.sleep(1)
                        break
                
    except pymysql.MySQLError as e:
        print(f"An error occurred while trying to query the database: {e}")
    finally:
        conn.close()

def update_city_population():
    conn = connect_mysql()
    try:
        while True:
            questions = [inquirer.Text('city', message="Enter City ID")]
            answers = inquirer.prompt(questions)
            if not answers:
                print("No city entered, exiting...")
                break
            city_id = answers['city']

            with conn.cursor() as cursor:
                    read_query = """
                        SELECT id, name, countrycode, population, district, latitude, longitude
                        FROM city
                        WHERE id = %s
                    """
                    with yaspin(text="Fetching city...", color="green") as spinner:
                        time.sleep(1)
                        cursor.execute(read_query, (city_id,))
                    spinner.ok("✔")
                    result = cursor.fetchone()
                    if not result:
                        print(f"No city found with ID = {city_id}.")
                        continue
                    pop_option_question = [
                        inquirer.List('choice',
                                    message="Increase or Decrease Population",
                                    choices=[('Increase', 'increase'), ('Decrease', 'decrease')]
                                    )
                    ]
                    pop_option_answer = inquirer.prompt(pop_option_question)
                    choice = pop_option_answer['choice']
                    amount_question = [inquirer.Text('amount', message="Enter population adjustment amount")]
                    amount_answer = inquirer.prompt(amount_question)
                    adjustment = int(amount_answer['amount'])
                    if choice == 'increase':
                        new_population = result['population'] + adjustment
                    elif choice == 'decrease':
                        new_population = result['population'] - adjustment
                        if new_population < 0:
                            print("Population decrease would result in a negative value, which is not allowed.")
                            break
                    update_query = """
                        UPDATE city
                        SET population = %s
                        WHERE id = %s
                    """
                    with yaspin(text="Updating city population...", color="green"):
                        time.sleep(1)
                        cursor.execute(update_query, (new_population, city_id))
                    conn.commit()
                    cursor.execute(read_query, (city_id,))
                    updated_result = cursor.fetchone()
                    table = tabulate([updated_result], headers="keys", tablefmt="fancy_grid")
                    print("\n")
                    print(table)
                    print("\n")
                    print(f"{result['name']} has changed its population from {result['population']} to {updated_result['population']}")
                    print("\n")
                    time.sleep(2)
                    break
    except pymysql.MySQLError as e:
        print(f"An error occurred while trying to query the database: {e}")
    finally:
        conn.close()

def add_new_person():
    conn = connect_mysql()
    try:
        questions = [
            inquirer.Text('id', message="ID"),
            inquirer.Text('name', message="Name"),
            inquirer.Text('age', message="Age"),
            inquirer.Text('salary', message="Salary"),
            inquirer.Text('city_id', message="City ID")
        ]
        answers = inquirer.prompt(questions)
        if not answers:
            print("No data entered, exiting...")
            return  

        id = answers['id']
        name = answers['name']
        age = answers['age']
        salary = answers['salary']
        cid = answers['city_id']

        with conn.cursor() as cursor:
            check_id_query = "SELECT personid FROM person WHERE personid = %s"           
            cursor.execute(check_id_query, (id,))
            if cursor.fetchone():
                print(f"Error: Person ID: {id} already exists")
                return  

            check_city_query = "SELECT id FROM city WHERE id = %s"
            cursor.execute(check_city_query, (cid,))
            if not cursor.fetchone():
                print(f"Error: City ID: {cid} does not exist")
                return

            try:
                insert_query = """
                    INSERT INTO person (personid, personname, age, salary, city)
                    VALUES (%s, %s, %s, %s, %s)
                """
                with yaspin(text="Adding new person...", color="green") as spinner:
                    time.sleep(2)
                    cursor.execute(insert_query, (id, name, age, salary, cid))
                spinner.ok("✔")
                conn.commit()
                print("New person added successfully.")
            except pymysql.MySQLError as e:
                print(f"An error occurred: {e}")
                conn.rollback()
                return 

    except pymysql.MySQLError as e:
        print(f"An error occurred while trying to query the database: {e}")
    finally:
        conn.close()

def delete_person():
    conn = connect_mysql()
    try:
        questions = [
            inquirer.Text('person_id', message="Enter ID of Person to Delete"),
        ]
        answers = inquirer.prompt(questions)
        if not answers:
            print("No data entered, exiting...")
            return  
        person_id = answers['person_id']
        with conn.cursor() as cursor:
            hvc_query = """
                        SELECT person.*, hvc.cityid
                        FROM person
                        INNER JOIN hasvisitedcity hvc ON person.personID = hvc.personID
                        WHERE person.personID = %s
                        """
            cursor.execute(hvc_query, (person_id,))
            if cursor.fetchone() is not None:
                print("\n")
                print(f"Can't delete Person ID: {person_id}. He/she has visited cities.")
                print("\n")
                time.sleep(1)
                return
            try:
                delete_query = "DELETE FROM person WHERE personID = %s"
                with yaspin(text="Deleting person...", color="green") as spinner:
                    time.sleep(2)
                    cursor.execute(delete_query, (person_id,))
                spinner.ok("✔")
                conn.commit()
                print(f"Person ID: {person_id} deleted")
            except pymysql.MySQLError as e:
                print(f"An error occurred: {e}")
                conn.rollback()
    except pymysql.MySQLError as e:
        print(f"An error occurred while trying to query the database: {e}")
    finally:
        conn.close()

def view_countries_by_population():
    questions = [
        inquirer.List('option', message="Choose comparison (<, >, =)", choices=['<', '>', '=']),
        inquirer.Text('population', message="Enter population", validate=lambda _, x: x.isdigit())
    ]
    answers = inquirer.prompt(questions)
    
    if not answers:
        print("No input provided, exiting...")
        return
    
    option = answers['option']
    population = int(answers['population'])
    
    conn = connect_mysql()
    if conn is None:
        print("Failed to connect to the database.")
        return

    try:
        with conn.cursor() as cursor:
            query = f"""
                SELECT code, name, continent, population
                FROM country
                WHERE population {option} %s
                ORDER BY population
            """
            cursor.execute(query, (population,))
            result = cursor.fetchall()

            if not result:
                print("No countries to display.")
                return

            table = tabulate(result, headers="keys", tablefmt="fancy_grid")
            with yaspin(text="Fetching cities...", color="green"):
                time.sleep(2)
                print("\n")
                print(table)
                print("\n")
    except pymysql.MySQLError as e:
        print(f"An error occurred while trying to query the database: {e}")
    finally:
        conn.close()

def show_twinned_cities():
    driver = connect_neo4j()
    try:
        with driver.session() as session:
            with yaspin(text="Fetching twinned cities...", color="green"):
                result = session.run("MATCH (city)-[:TWINNED_WITH]-(partner_city) RETURN city.name AS City, partner_city.name AS PartnerCity ORDER BY city.name")
            print("\n")     
            for record in result:
                print(f"{record['City']} <-> {record['PartnerCity']}")
            print("\n")   
            time.sleep(2)
    except Exception as e:
        print(f"An error occurred while fetching twinned cities: {e}")

def twin_with_dublin():
    driver = connect_neo4j()
    conn = connect_mysql()
    
    while True:
        try:
            with driver.session() as session:
                with yaspin(text="Loading...", color="green"):
                    dublin_exists = session.run("MATCH (city:City {name: 'Dublin'}) RETURN city").single()
                    if not dublin_exists:
                        print("Error: Dublin does not exist in Neo4j database")
                        break
        except Exception as e:
            print(f"An error occurred while checking for Dublin: {e}")
            break

        questions = [
            inquirer.Text('cid', message="Enter ID of City to twin with Dublin", validate=lambda _, x: x.isdigit())
        ]
        answers = inquirer.prompt(questions)
        if not answers:
            print("No input provided.")
            break
        partner_cid = int(answers['cid'])
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT name FROM city WHERE id = %s", (partner_cid,))
                result = cursor.fetchone()
                if result:
                    city_name = result['name']
                    with driver.session() as session:
                        with yaspin(text="Loading...", color="green") as spinner:
                            city_check = session.run(
                                "MATCH (city:City) WHERE city.cid = $cid RETURN exists((city)-[:TWINNED_WITH]->(:City {name: 'Dublin'})) AS isTwinned",
                                parameters={'cid': partner_cid}).single()
                        spinner.ok("✔")
                        if city_check and city_check['isTwinned']:
                            print(f"{city_name} is already twinned with Dublin.")
                        else:
                            with yaspin(text="Creating relationship...", color="green"):
                                session.run("MATCH (dublin:City {name: 'Dublin'}), (city:City {cid: $cid}) MERGE (city)-[:TWINNED_WITH]->(dublin)",
                                            parameters={'cid': partner_cid}) 
                                print(f"{city_name} is now twinned with Dublin.")
                            break
                else:
                    print(f"{partner_cid} does not exist in MySQL database")
                    continue
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if not conn.open:
                conn = connect_mysql()
            if not driver.session():
                driver = connect_neo4j()

    conn.close()
    driver.close()