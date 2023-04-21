import sys
import bcrypt

from utils.datetime_utils import *
from utils.forms import *
from utils.box import *
from connection import Connection

from models import *
from csv_utils import *

connection = Connection("users.db")
cursor = connection.cursor

def init_db():
    with open("create_tables.sql") as sql:
        cursor.executescript(sql.read())

def add_default_competencies():
    default_competencies = [
        'Computer Anatomy',
        'Data Types',
        'Variables',
        'Functions',
        'Boolean Logic',
        'Conditionals',
        'Loops',
        'Data Structures',
        'Lists',
        'Dictionaries',
        'Working with Files',
        'Exception Handling',
        'Quality Assurance (QA)',
        'Object-Oriented Programming',
        'Recursion',
        'Databases'
    ]
    current_time = get_current_day()
    for competency in default_competencies:
        competency_id = str(uuid.uuid4())
        cursor.execute("INSERT INTO Competencies (competency_id, name, date_created) VALUES (?, ?, ?)", (competency_id, competency, current_time))
    connection.commit()

main_menu_items = {
    "1":("Users", User.users_menu),
    "2":("Competencies", Competency.competencies_menu),
    "3":("Assessments", Assessment.assessments_menu),
    "4":("Assessment Results", AssessmentResult.results_menu),
    "5":("Import CSV", import_csv)
}

def main_menu():
    menu_selection = full_menu("Main Menu", main_menu_items)

if __name__ == "__main__":
    for arg in sys.argv[1::]:
        if arg == '--init-db':
            init_db()
            add_default_competencies()
            print("Create a Manager\n")
            User.create_manager()
        elif arg == '--adc' or arg == '--add-default-competencies':
            add_default_competencies()

    print("\033c", end="")
    user = User.login()
    if user.user_type == "manager":
        main_menu()
    else:
        user.own_user_menu()