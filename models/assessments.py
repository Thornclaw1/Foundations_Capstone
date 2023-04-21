import uuid

from connection import Connection
from utils.box import *
from utils.forms import *
from utils.datetime_utils import *
from utils.data_table import DataTable

import models

connection = Connection("users.db")
cursor = connection.cursor

class Assessment():
    _all_assessments = None

    def __init__(self, competency, name, date_created = None):
        self.assessment_id = str(uuid.uuid4())
        self.competency_id = competency.competency_id
        self.competency = competency
        self.name = name
        self.date_created = date_created if date_created else get_current_day()

    def __str__(self):
        return f"{self.assessment_id}, {self.competency.name}, {self.name}, {self.date_created}"

    __repr__ = __str__

    def edit(self):
        self.name = edit_form(("Name",), (self.name,))
        self.update_db()
    
    def save_to_db(self):
        cursor.execute(
            """
            INSERT INTO Assessments 
            (assessment_id, competency_id, name, date_created) 
            VALUES 
            (?, ?, ?, ?)
            """, 
            (self.assessment_id, self.competency_id, self.name, self.date_created)
        )
        connection.commit()

    def update_db(self):
        cursor.execute(
            """
            UPDATE Assessments
            SET name = ?, date_created = ?
            WHERE assessment_id = ?
            """,
            (self.name, self.date_created, self.assessment_id)
        )
        connection.commit()

    def _load_all_assessments_from_db():
        Assessment._all_assessments = []
        assessments_db = cursor.execute("SELECT * FROM Assessments").fetchall()
        for assessment_db in assessments_db:
            assessment_id, competency_id, name, date_created = assessment_db
            competency = models.Competency._get_competency(competency_id)
            assessment = Assessment(competency, name, date_created)
            assessment.assessment_id = assessment_id
            Assessment._all_assessments.append(assessment)

    def print_all_assessments():
        if Assessment._all_assessments is None:
            Assessment._load_all_assessments_from_db()
        table = DataTable("Assessments", ["assessment_id", "competency", "name", "date_created"], display_names=["Assessment ID", "Competency", "Name", "Date Created"])
        table.append_rows([assessment.__str__().split(", ") for assessment in Assessment._all_assessments])
        assessment_dict = table.get_user_selection(["competency", "name", "date_created"])
        return Assessment._get_assessment(assessment_dict["assessment_id"]) if assessment_dict else None

    def print_assessment(self):
        table = DataTable(self.name, ["assessment_id", "competency", "name", "date_created"], display_names=["Assessment ID", "Competency", "Name", "Date Created"])
        table.append_rows([assessment.__str__().split(", ") for assessment in Assessment._all_assessments if assessment.assessment_id == self.assessment_id])
        table.print(["competency", "date_created"])

    def create_assessment():
        competency = models.Competency.print_all_competencies()
        if not competency: return
        name = form("Name")
        assessment = Assessment(competency, name)
        assessment.save_to_db()
        Assessment._add_assessment(assessment)
        return assessment

    def _add_assessment(assessment):
        if Assessment._all_assessments is None:
            Assessment._load_all_assessments_from_db()
            return
        Assessment._all_assessments.append(assessment)

    def _get_assessment(assessment_id):
        if Assessment._all_assessments is None:
            Assessment._load_all_assessments_from_db()
        if any(assessment for assessment in Assessment._all_assessments if assessment.assessment_id == assessment_id):
            return [assessment for assessment in Assessment._all_assessments if assessment.assessment_id == assessment_id][0]

    def assessments_menu():
        def view_all_assessments():
            assessment = Assessment.print_all_assessments()
            if assessment:
                assessment.assessment_menu()
        def add_assessment():
            assessment = Assessment.create_assessment()
            if assessment:
                assessment.assessment_menu()
        full_menu("Assessments Menu",
        {
            "1":("View All Assessments",view_all_assessments),
            "2":("Add Assessment",add_assessment),
        },quit=("0", "Back"))

    def assessment_menu(self):
        full_menu("Assessment Menu",
        {
            "1":("Edit Assessment", self.edit),
        }, quit=("0", "Back"), pre_print_func=self.print_assessment)