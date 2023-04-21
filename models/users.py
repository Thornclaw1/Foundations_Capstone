import uuid
import bcrypt

from connection import Connection
from utils.box import *
from utils.forms import *
from utils.datetime_utils import *
from utils.data_table import DataTable
from utils.input_utils import *
from csv_utils import *

import models

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
        self.date_created = date_created if date_created else get_current_day()
        self.hire_date = hire_date if hire_date else self.date_created
        self.user_type = user_type

    def __str__(self):
        return f"{self.user_id}, {self.first_name}, {self.last_name}, {self.phone}, {self.email}, {self.password}, {self.active}, {self.date_created}, {self.hire_date}, {self.user_type}"

    __repr__ = __str__

    def login():
        print("Login")
        while True:
            email, password = form("Email", "Password")
            user = User._get_user_by_email(email)
            if user:
                pw = password.encode('utf-8')
                if bcrypt.checkpw(pw, user.password):
                    return user
            print("Invalid email or password.")

    def edit(self):
        self.first_name, self.last_name, self.phone, self.email, self.hire_date = edit_form(("First Name", "Last Name", "Phone", "Email", "Hire Date"), (self.first_name, self.last_name, self.phone, self.email, self.hire_date))
        self.update_db()

    def change_password(self):
        old_pw = input("Enter old password: ").encode('utf-8')
        if bcrypt.checkpw(old_pw, self.password):
            new_pw = input("Enter new password: ").encode('utf-8')
            salt = b'$2b$12$2WnZotnPB7rAfIrVIWZuRu'
            self.password = bcrypt.hashpw(new_pw, salt)
            self.update_db()
            return
        print("Incorrect Password..")

    def deactivate(self):
        self.active = 0
        self.update_db()

    def activate(self):
        self.active = 1
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
        connection.commit()

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
        table.append_rows([user.__str__().split(", ") for user in User._all_users if user.active == 1])
        user_dict = table.get_user_selection(["first_name", "last_name", "phone", "email", "active"])
        return User._get_user(user_dict["user_id"]) if user_dict else None

    def print_all_inactive_users():
        if User._all_users is None:
            User._load_all_users_from_db()
        table = DataTable("Users", ["user_id", "first_name", "last_name", "phone", "email", "password", "active", "date_created", "hire_date", "user_type"], display_names=["User ID", "First Name", "Last Name", "Phone", "Email", "Password", "Active", "Date Created", "Hire Date", "User Type"])
        table.append_rows([user.__str__().split(", ") for user in User._all_users if user.active == 0])
        user_dict = table.get_user_selection(["first_name", "last_name", "phone", "email", "active"])
        return User._get_user(user_dict["user_id"]) if user_dict else None

    def print_all_managers():
        if User._all_users is None:
            User._load_all_users_from_db()
        table = DataTable("Users", ["user_id", "first_name", "last_name", "phone", "email", "password", "active", "date_created", "hire_date", "user_type"], display_names=["User ID", "First Name", "Last Name", "Phone", "Email", "Password", "Active", "Date Created", "Hire Date", "User Type"])
        table.append_rows([user.__str__().split(", ") for user in User._all_users if user.user_type == "manager" and user.active == 1])
        user_dict = table.get_user_selection(["first_name", "last_name", "phone", "email", "active"])
        return User._get_user(user_dict["user_id"]) if user_dict else None

    def print_user(self):
        table = DataTable(f"{self.first_name} {self.last_name}", ["user_id", "first_name", "last_name", "phone", "email", "password", "active", "date_created", "hire_date", "user_type"], display_names=["User ID", "First Name", "Last Name", "Phone", "Email", "Password", "Active", "Date Created", "Hire Date", "User Type"])
        table.append_rows([user.__str__().split(", ") for user in User._all_users if user.user_id == self.user_id])
        table.print(["phone", "email", "active", "date_created", "hire_date", "user_type"])

    def print_user_results(self):
        if self.results is None:
            self._load_all_user_results_from_db()
        table = DataTable("Assessment Results", ["result_id", "user", "assessment", "score", "date_taken", "manager"], display_names=["Result ID", "User", "Assessment", "Score", "Date Taken", "Manager"])
        table.append_rows([result.__str__().split(", ") for result in self.results])
        result_dict = table.get_user_selection(["user", "assessment", "score", "date_taken", "manager"])
        return AssessmentResult._get_result(result_dict["result_id"]) if result_dict else None

    def search_users():
        search_term = f"%{input('Enter Search Term: ')}%"
        users = cursor.execute("SELECT * FROM Users WHERE (first_name LIKE ? OR last_name LIKE ? OR email LIKE ? OR phone LIKE ?) AND active = 1", (search_term, search_term, search_term, search_term)).fetchall()
        table = DataTable("Users", ["user_id", "first_name", "last_name", "phone", "email", "password", "active", "date_created", "hire_date", "user_type"], display_names=["User ID", "First Name", "Last Name", "Phone", "Email", "Password", "Active", "Date Created", "Hire Date", "User Type"])
        table.append_rows(users)
        # print(table)
        user_dict = table.get_user_selection(["first_name", "last_name", "phone", "email", "active"])
        return User._get_user(user_dict["user_id"]) if user_dict else None

    def create_user():
        first_name, last_name, phone, email, password, hire_date = form("First Name", "Last Name", "Phone", "Email", "Password", "Hire Date")
        salt = b'$2b$12$2WnZotnPB7rAfIrVIWZuRu'
        byte_pwd = password.encode('utf-8')
        hashed_pwd = bcrypt.hashpw(byte_pwd, salt)
        user = User(first_name, last_name, phone, email, hashed_pwd, hire_date = hire_date)
        user.save_to_db()
        User._add_user(user)
        return user

    def create_manager():
        first_name, last_name, phone, email, password, hire_date = form("First Name", "Last Name", "Phone", "Email", "Password", "Hire Date")
        salt = b'$2b$12$2WnZotnPB7rAfIrVIWZuRu'
        byte_pwd = password.encode('utf-8')
        hashed_pwd = bcrypt.hashpw(byte_pwd, salt)
        manager = User(first_name, last_name, phone, email, hashed_pwd, hire_date = hire_date, user_type = 'manager')
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

    def _get_user_by_email(email):
        if User._all_users is None:
            User._load_all_users_from_db()
        if any(user for user in User._all_users if user.email == email and user.active == 1):
            return [user for user in User._all_users if user.email == email and user.active == 1][0]

    def users_menu():
        def view_all_users():
            user = User.print_all_users()
            if user:
                user.user_menu()
        def search_all_users():
            user = User.search_users()
            if user:
                user.user_menu()
        def add_user():
            user = User.create_user()
            user.user_menu()
        def add_manager():
            manager = User.create_manager()
            manager.user_menu()
        def reactive_user():
            user = User.print_all_inactive_users()
            if user:
                user.activate()

        full_menu("Users Menu",
        {
            "1":("View All Users",view_all_users),
            "2":("Search Users",search_all_users),
            "3":("Add User",add_user),
            "4":("Add Manager",add_manager),
            "5":("Reactivate User",reactive_user)
        },quit=("0", "Back"))

    def user_menu(self):
        def view_report():
            report = cursor.execute(
                """
                SELECT c.name as competency, r.score, a.name, MAX(r.date_taken)
                FROM AssessmentResults r
                JOIN Assessments a ON a.assessment_id = r.assessment_id
                JOIN Competencies c ON a.competency_id = c.competency_id
                JOIN Users u ON u.user_id = r.user_id
                WHERE u.user_id = ?
                GROUP BY c.competency_id
                """,
                (self.user_id,)
            ).fetchall()
            if len(report) < 1:
                input("No assessments have been recorded for this user")
                return
            report_copy = report.copy()
            scores = [int(row[1]) for row in report_copy]
            avg = sum(scores) / len(scores)
            table = DataTable(f"{self.first_name} {self.last_name} Report : Average Score - {avg}", ["competency", "score", "assessment", "date_taken"], display_names=["Competency", "Score", "Assessment", "Date Taken"])
            table.append_rows(report)
            print(table)
            if strict_input("Would you like to export this data? (Y/N) ", ["Y","N"]) == "y":
                export_csv("Competency-Level-Report", ["competency", "score", "assessment", "date_taken"], report)
        def view_results():
            result = models.AssessmentResult.print_results_for_user(self)
            if result:
                result.result_menu()
        def add_result():
            result = models.AssessmentResult.create_result(self)
            if result:
                result.result_menu()
        def deactivate_user():
            if strict_input("Are you sure you want to deactive this user? (Y/N) ", ["Y", "N"]) == "y":
                self.deactivate()
                return True

        full_menu("User Menu",
        {
            "1":("Edit User", self.edit),
            "2":("View Competency Level Report", view_report),
            "3":("View Assessment Results", view_results),
            "4":("Add Assessment Result", add_result),
            "5":("Deactivate User", deactivate_user)
        }, quit=("0", "Back"), pre_print_func=self.print_user)

    def own_user_menu(self):
        def view_report():
            report = cursor.execute(
                """
                SELECT c.name as competency, r.score, a.name, MAX(r.date_taken)
                FROM AssessmentResults r
                JOIN Assessments a ON a.assessment_id = r.assessment_id
                JOIN Competencies c ON a.competency_id = c.competency_id
                JOIN Users u ON u.user_id = r.user_id
                WHERE u.user_id = ?
                GROUP BY c.competency_id
                """,
                (self.user_id,)
            ).fetchall()
            if len(report) < 1:
                input("No assessments have been recorded for this user")
                return
            report_copy = report.copy()
            scores = [int(row[1]) for row in report_copy]
            avg = sum(scores) / len(scores)
            table = DataTable(f"{self.first_name} {self.last_name} Report : Average Score - {avg}", ["competency", "score", "assessment", "date_taken"], display_names=["Competency", "Score", "Assessment", "Date Taken"])
            table.append_rows(report)
            print(table)
            if strict_input("Would you like to export this data? (Y/N) ", ["Y","N"]) == "y":
                export_csv("Competency-Level-Report", ["competency", "score", "assessment", "date_taken"], report)

        def view_results():
            result = models.AssessmentResult.print_results_for_user_unselectable(self)
            if result:
                result.result_menu()

        full_menu("User Menu",
        {
            "1":("View Competency Level Report", view_report),
            "2":("View Assessment Results", view_results),
            "3":("Edit Profile", self.edit),
            "4":("Change Password", self.change_password)
        }, pre_print_func=self.print_user)