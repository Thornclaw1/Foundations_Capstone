import uuid

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

class Competency():
    _all_competencies = None

    def __init__(self, name, date_created = None):
        self.competency_id = str(uuid.uuid4())
        self.name = name
        self.date_created = date_created if date_created else get_current_day()

    def __str__(self):
        return f"{self.competency_id}, {self.name}, {self.date_created}"

    __repr__ = __str__
    
    def edit(self):
        self.name = edit_form(("Name",), (self.name,))
        self.update_db()
    
    def save_to_db(self):
        cursor.execute(
            """
            INSERT INTO Competencies 
            (competency_id, name, date_created) 
            VALUES 
            (?, ?, ?)
            """, 
            (self.competency_id, self.name, self.date_created)
        )
        connection.commit()

    def update_db(self):
        cursor.execute(
            """
            UPDATE Competencies
            SET name = ?, date_created = ?
            WHERE competency_id = ?
            """,
            (self.name, self.date_created, self.competency_id)
        )
        connection.commit()

    def _load_all_competencies_from_db():
        Competency._all_competencies = []
        competencies_db = cursor.execute("SELECT * FROM Competencies").fetchall()
        for competency_db in competencies_db:
            competency_id, name, date_created = competency_db
            competency = Competency(name, date_created)
            competency.competency_id = competency_id
            Competency._all_competencies.append(competency)

    def print_all_competencies():
        if Competency._all_competencies is None:
            Competency._load_all_competencies_from_db()
        table = DataTable("Competencies", ["competency_id", "name", "date_created"], display_names=["Competency ID", "Name", "Date Created"])
        table.append_rows([competency.__str__().split(", ") for competency in Competency._all_competencies])
        competency_dict = table.get_user_selection(["name", "date_created"])
        return Competency._get_competency(competency_dict["competency_id"]) if competency_dict else None

    def print_competency(self):
        table = DataTable(self.name, ["competency_id", "name", "date_created"], display_names=["Competency ID", "Name", "Date Created"])
        table.append_rows([competency.__str__().split(", ") for competency in Competency._all_competencies if competency.competency_id == self.competency_id])
        table.print(["date_created"])

    def search_competencies():
        search_term = f"%{input('Enter Search Term: ')}%"
        competencies = cursor.execute("SELECT * FROM Competencies WHERE name LIKE ?", (search_term,)).fetchall()
        table = DataTable("Competencies", ["competency_id", "name", "date_created"], display_names=["Competency ID", "Name", "Date Created"])
        table.append_rows(competencies)
        # print(table)
        competency_dict = table.get_user_selection(["name", "date_created"])
        return Competency._get_competency(competency_dict["competency_id"]) if competency_dict else None

    def create_competency():
        name = form("Name")
        competency = Competency(name)
        competency.save_to_db()
        Competency._add_competency(competency)
        return competency

    def _add_competency(competency):
        if Competency._all_competencies is None:
            Competency._load_all_competencies_from_db()
            return
        Competency._all_competencies.append(competency)

    def _get_competency(competency_id):
        if Competency._all_competencies is None:
            Competency._load_all_competencies_from_db()
        if any(competency for competency in Competency._all_competencies if competency.competency_id == competency_id):
            return [competency for competency in Competency._all_competencies if competency.competency_id == competency_id][0]

    def competencies_menu():
        def view_all_competencies():
            competency = Competency.print_all_competencies()
            if competency:
                competency.competency_menu()
        def add_competency():
            competency = Competency.create_competency()
            competency.competency_menu()
        full_menu("Competencies Menu",
        {
            "1":("View All Competencies",view_all_competencies),
            "2":("Add Competency",add_competency),
        },quit=("0", "Back"))

    def competency_menu(self):
        def view_report():
            report = cursor.execute(
                """
                SELECT u.first_name || " " || u.last_name, r.score, a.name, MAX(r.date_taken)
                FROM AssessmentResults r 
                JOIN Assessments a ON a.assessment_id = r.assessment_id 
                JOIN Competencies c ON a.competency_id = c.competency_id 
                JOIN Users u ON u.user_id = r.user_id 
                WHERE c.competency_id = ? 
                GROUP BY u.user_id
                """,
                (self.competency_id,)
            ).fetchall()
            if len(report) < 1:
                input("No assessments have been recorded for this competency")
                return
            report_copy = report.copy()
            scores = [int(row[1]) for row in report_copy]
            avg = sum(scores) / len(scores)
            table = DataTable(f"{self.name} Report : Average Score - {avg}", ["user", "score", "assessment", "date_taken"], display_names=["User", "Score", "Assessment", "Date Taken"])
            table.append_rows(report)
            print(table)
            if strict_input("Would you like to export this data? (Y/N) ", ["Y","N"]) == "y":
                export_csv(f"{self.name} Report", ["user", "score", "assessment", "date_taken"], report)
        full_menu("Competency Menu",
        {
            "1":("Edit Competency", self.edit),
            "2":("View Report of All Users For Competency", view_report)
        }, quit=("0", "Back"), pre_print_func=self.print_competency)