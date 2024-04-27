import subprocess
import sys
import logging
import importlib

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_package(package):
    try:
        importlib.import_module(package)
        logging.info(f"{package} is already installed.")
        return True
    except ImportError:
        return False

def install_packages(packages):
    missing_packages = [pkg for pkg in packages if not check_package(pkg.split('==')[0])]
    if missing_packages:
        logging.info(f"Installing packages: {', '.join(missing_packages)}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
    else:
        logging.info("All packages are already installed.")

required_packages = [
    'ansicon==1.89.0',
    'blessed==1.20.0',
    'click==8.1.7',
    'colorama==0.4.6',
    'editor==1.6.6',
    'inquirer==3.2.4',
    'jinxed==1.2.1',
    'markdown-it-py==3.0.0',
    'mdurl==0.1.2',
    'neo4j==5.20.0',
    'pyfiglet==1.0.2',
    'Pygments==2.17.2',
    'PyMySQL==1.1.0',
    'pytz==2024.1',
    'readchar==4.0.6',
    'rich==13.7.1',
    'runs==1.2.2',
    'setuptools==69.5.1',
    'shellingham==1.5.4',
    'six==1.16.0',
    'tabulate==0.9.0',
    'termcolor==2.3.0',
    'typer==0.12.3',
    'typing_extensions==4.11.0',
    'wcwidth==0.2.13',
    'xmod==1.8.1',
    'yaspin==3.0.2',
    'python-dotenv'
]