import uuid

from connection import Connection
from utils.forms import *
from utils.datetime_utils import *
from utils.data_table import DataTable

connection = Connection("users.db")
cursor = connection.cursor

class User():
    _all_users = None

    def __init__(self, first_name, last_name, phone, email, password, active = 1, date_created = None, hire_date = None, user_type = 'user'):
        self.user_id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.password = password
        self.active = active
        self.date_created = date_created if date_created else get_current_time()
        self.hire_date = hire_date if hire_date else self.date_created
        self.user_type = user_type

    def __str__(self):
        return f"{self.user_id}, {self.first_name}, {self.last_name}, {self.phone}, {self.email}, {self.password}, {self.active}, {self.date_created}, {self.hire_date}, {self.user_type}"

    def __repr__(self):
        return f"({self.__str__()})"

    def edit(self):
        self.first_name, self.last_name, self.phone, self.email, self.hire_date = edit_form(("First Name", "Last Name", "Phone", "Email", "Hire Date"), (self.first_name, self.last_name, self.phone, self.email, self.hire_date))
        self.update_db()
    
    def save_to_db(self):
        cursor.execute(
            """
            INSERT INTO Users 
            (user_id, first_name, last_name, phone, email, password, active, date_created, hire_date, user_type) 
            VALUES 
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, 
            (self.user_id, self.first_name, self.last_name, self.phone, self.email, self.password, self.active, self.date_created, self.hire_date, self.user_type)
        )
        connection.commit()

    def update_db(self):
        cursor.execute(
            """
            UPDATE Users
            SET first_name = ?, last_name = ?, phone = ?, email = ?, password = ?, active = ?, date_created = ?, hire_date = ?, user_type = ?
            WHERE user_id = ?
            """,
            (self.first_name, self.last_name, self.phone, self.email, self.password, self.active, self.date_created, self.hire_date, self.user_type, self.user_id)
        )

    # def load_from_db(user_id):
    #     _, first_name, last_name, phone, email, password, active, date_created, hire_date, user_type = cursor.execute("SELECT * FROM Users WHERE user_id = ?", (user_id,)).fetchone()
    #     user = User(first_name, last_name, phone, email, password, active, date_created, hire_date, user_type)
    #     user.user_id = user_id
    #     return user

    def _load_all_users_from_db():
        User._all_users = []
        users_db = cursor.execute("SELECT * FROM Users").fetchall()
        for user_db in users_db:
            user_id, first_name, last_name, phone, email, password, active, date_created, hire_date, user_type = user_db
            user = User(first_name, last_name, phone, email, password, active, date_created, hire_date, user_type)
            user.user_id = user_id
            User._all_users.append(user)

    def print_all_users():
        if User._all_users is None:
            User._load_all_users_from_db()
        table = DataTable("Users", ["user_id", "first_name", "last_name", "phone", "email", "password", "active", "date_created", "hire_date", "user_type"], display_names=["User ID", "First Name", "Last Name", "Phone", "Email", "Password", "Active", "Date Created", "Hire Date", "User Type"])
        table.append_rows([user.__str__().split(", ") for user in User._all_users])
        # print(table)
        # table.print(["first_name", "last_name", "phone", "email", "active"])
        user_dict = table.get_user_selection(["first_name", "last_name", "phone", "email", "active"])
        user = User._get_user(user_dict["user_id"])

    def search_users():
        search_term = f"%{input('Enter Search Term: ')}%"
        users = cursor.execute("SELECT * FROM Users WHERE first_name LIKE ? OR last_name LIKE ? OR email LIKE ? OR phone LIKE ?", (search_term, search_term, search_term, search_term)).fetchall()
        table = DataTable("Users", ["user_id", "first_name", "last_name", "phone", "email", "password", "active", "date_created", "hire_date", "user_type"], display_names=["User ID", "First Name", "Last Name", "Phone", "Email", "Password", "Active", "Date Created", "Hire Date", "User Type"])
        table.append_rows(users)
        print(table)

    def create_user():
        first_name, last_name, phone, email, password, hire_date = form("First Name", "Last Name", "Phone", "Email", "Password", "Hire Date")
        user = User(first_name, last_name, phone, email, password, hire_date = hire_date)
        user.save_to_db()
        User._add_user(user)
        return user

    def create_manager():
        first_name, last_name, phone, email, password, hire_date = form("First Name", "Last Name", "Phone", "Email", "Password", "Hire Date")
        manager = User(first_name, last_name, phone, email, password, hire_date = hire_date, user_type = 'manager')
        manager.save_to_db()
        User._add_user(manager)
        return manager

    def _add_user(user):
        if User._all_users is None:
            User._load_all_users_from_db()
            return
        User._all_users.append(user)

    def _get_user(user_id):
        if User._all_users is None:
            User._load_all_users_from_db()
        if any(user for user in User._all_users if user.user_id == user_id):
            return [user for user in User._all_users if user.user_id == user_id][0]