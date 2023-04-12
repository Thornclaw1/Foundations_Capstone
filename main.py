import sys

from utils.datetime_utils import *
from utils.forms import *
from connection import Connection

from users import *

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
    current_time = get_current_time()
    for competency in default_competencies:
        cursor.execute("INSERT INTO Competencies (name, date_created) VALUES (?, ?)", (competency, current_time))
    connection.commit()



if __name__ == "__main__":
    for arg in sys.argv[1::]:
        if arg == '--init-db':
            init_db()
            add_default_competencies()
        elif arg == '--adc' or arg == '--add-default-competencies':
            add_default_competencies()

    # User.create_user()
    # rlinput("First Name : ", "Cameron")
    # first_name, last_name, phone, email, password, hire_date = edit_form(("First Name", "Last Name", "Phone", "Email", "Password", "Hire Date"), ("Cameron", "Fletcher", "382088259", "camfletcher02@gmail.com", "123", "2023-04-03"))
    # print(first_name, last_name, phone, email, password, hire_date)
    # User.print_all_users()
    # User.search_users()