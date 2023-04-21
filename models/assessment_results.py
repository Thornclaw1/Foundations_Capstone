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

class AssessmentResult():
    _all_results = None

    def __init__(self, user, assessment, score, date_taken = None, manager = None):
        self.result_id = str(uuid.uuid4())
        self.user_id = user.user_id
        self.user = user
        self.assessment_id = assessment.assessment_id
        self.assessment = assessment
        self.score = score
        self.date_taken = date_taken if date_taken else get_current_day()
        self.manager_id = manager.user_id if manager else None
        self.manager = manager

    def __str__(self):
        return f"{self.result_id}, {self.user.first_name} {self.user.last_name}, {self.assessment.name}, {self.score}, {self.date_taken}, " + (f"{self.manager.first_name} {self.manager.last_name}" if self.manager else "")

    __repr__ = __str__

    def edit(self):
        self.score, self.date_taken = edit_form(("Score", "Date Taken"), (self.score, self.date_taken))
        self.update_db()

    def delete(self):
        if strict_input("Are you sure you want to delete this result? (Y/N) ", ["Y", "N"]) == 'y':
            cursor.execute("DELETE FROM AssessmentResults WHERE result_id = ?", (self.result_id,))
            connection.commit()
            AssessmentResult._all_results.remove(self)
            return True

    def save_to_db(self):
        cursor.execute(
            """
            INSERT INTO AssessmentResults
            (result_id, user_id, assessment_id, score, date_taken, manager_id)
            VALUES
            (?, ?, ?, ?, ?, ?)
            """,
            (self.result_id, self.user_id, self.assessment_id, self.score, self.date_taken, self.manager_id)
        )
        connection.commit()

    def update_db(self):
        cursor.execute(
            """
            UPDATE AssessmentResults
            SET score = ?, date_taken = ?
            WHERE result_id = ?
            """,
            (self.score, self.date_taken, self.result_id)
        )
        connection.commit()

    def _load_all_results_from_db():
        AssessmentResult._all_results = []
        results_db = cursor.execute("SELECT * FROM AssessmentResults").fetchall()
        for result_db in results_db:
            result_id, user_id, assessment_id, score, date_taken, manager_id = result_db
            user = models.User._get_user(user_id)
            assessment = models.Assessment._get_assessment(assessment_id)
            manager = models.User._get_user(manager_id)
            result = AssessmentResult(user, assessment, score, date_taken, manager)
            result.result_id = result_id
            AssessmentResult._all_results.append(result)

    def print_all_results():
        if AssessmentResult._all_results is None:
            AssessmentResult._load_all_results_from_db()
        table = DataTable("Assessment Results", ["result_id", "user", "assessment", "score", "date_taken", "manager"], display_names=["Result ID", "User", "Assessment", "Score", "Date Taken", "Manager"])
        table.append_rows([result.__str__().split(", ") for result in AssessmentResult._all_results])
        result_dict = table.get_user_selection(["user", "assessment", "score", "date_taken", "manager"])
        return AssessmentResult._get_result(result_dict["result_id"]) if result_dict else None

    def get_all_results():
        if AssessmentResult._all_results is None:
            AssessmentResult._load_all_results_from_db()
        return AssessmentResult._all_results

    def print_results_for_user(user):
        if AssessmentResult._all_results is None:
            AssessmentResult._load_all_results_from_db()
        table = DataTable("Assessment Results", ["result_id", "user", "assessment", "score", "date_taken", "manager"], display_names=["Result ID", "User", "Assessment", "Score", "Date Taken", "Manager"])
        table.append_rows([result.__str__().split(", ") for result in AssessmentResult._all_results if result.user_id == user.user_id])
        result_dict = table.get_user_selection(["user", "assessment", "score", "date_taken", "manager"])
        return AssessmentResult._get_result(result_dict["result_id"]) if result_dict else None

    def print_results_for_user_unselectable(user):
        if AssessmentResult._all_results is None:
            AssessmentResult._load_all_results_from_db()
        table = DataTable("Assessment Results", ["result_id", "user", "assessment", "score", "date_taken", "manager"], display_names=["Result ID", "User", "Assessment", "Score", "Date Taken", "Manager"])
        table.append_rows([result.__str__().split(", ") for result in AssessmentResult._all_results if result.user_id == user.user_id])
        table.print(["user", "assessment", "score", "date_taken", "manager"])
        input()
        
    def print_result(self):
        table = DataTable(f"{self.user.first_name} {self.user.last_name} : {self.assessment.name}", ["result_id", "user", "assessment", "score", "date_taken", "manager"], display_names=["Result ID", "User", "Assessment", "Score", "Date Taken", "Manager"])
        table.append_rows([result.__str__().split(", ") for result in AssessmentResult._all_results if result.result_id == self.result_id])
        table.print(["score", "date_taken", "manager"])

    def create_result(user):
        assessment = models.Assessment.print_all_assessments()
        if not assessment: return
        score = form("Score")
        manager = None
        if strict_input("Did a manager administer this test? (Y/N) ", ["Y", "N"]) == 'y':
            manager = models.User.print_all_managers()
        result = AssessmentResult(user, assessment, score, manager = manager)
        result.save_to_db()
        AssessmentResult._add_result(result)
        return result

    def create_results_from_list(results_list):
        for result in results_list:
            user = models.User._get_user(result["user_id"])
            assessment = models.Assessment._get_assessment(result["assessment_id"])
            score = result["score"]
            date_taken = result["date_taken"]
            manager = models.User._get_user(result["manager_id"])
            assessment_result = AssessmentResult(user, assessment, score, date_taken, manager)
            assessment_result.save_to_db()
            AssessmentResult._add_result(assessment_result)

    def _add_result(result):
        if AssessmentResult._all_results is None:
            AssessmentResult._load_all_results_from_db()
            return
        AssessmentResult._all_results.append(result)

    def _get_result(result_id):
        if AssessmentResult._all_results is None:
            AssessmentResult._load_all_results_from_db()
        if any(result for result in AssessmentResult._all_results if result.result_id == result_id):
            return [result for result in AssessmentResult._all_results if result.result_id == result_id][0]

    def results_menu():
        def view_all_results():
            result = AssessmentResult.print_all_results()
            if result:
                result.result_menu()
        def export_all_results():
            results = AssessmentResult.get_all_results()
            results_list = [[result.user_id, result.assessment_id, result.score, result.date_taken, result.manager_id] for result in results]
            export_csv("Assessment Results", ["user_id", "assessment_id", "score", "date_taken", "manager_id"], results_list)
            
        full_menu("Assessments Results Menu",
        {
            "1":("View All Results", view_all_results),
            "2":("Export All Results", export_all_results)
        }, quit=("0", "Back"))

    def result_menu(self):
        full_menu("Result Menu",
        {
            "1":("Edit Result", self.edit),
            "2":("Delete Result", self.delete)
        }, quit=("0", "Back"), pre_print_func=self.print_result)