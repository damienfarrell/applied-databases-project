from setup import install_packages, required_packages
from database import connect_mysql, connect_neo4j

def main():
    connect_mysql()
    connect_neo4j()
    print("Running main application")

if __name__ == "__main__":

    # install_packages(required_packages)
    
    main()