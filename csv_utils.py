from os.path import exists
import csv
from utils.datetime_utils import *

from models import *
from utils.box import *

def import_csv():
    file_name = input("Enter file name of csv you'd like to import: ")
    if exists(file_name):
        with open(file_name, 'r') as csvfile:
            csv_dict_reader = csv.DictReader(csvfile)
            models.AssessmentResult.create_results_from_list(list(csv_dict_reader))
        input(f"Successfully Imported {file_name}")
    else:
        input("File does not exist. ")

def export_csv(name, headers, data):
    file_name = f"{name}-{get_current_time()}.csv"
    with open(file_name, 'w') as file:
        wrt = csv.writer(file)
        wrt.writerow(headers)
        wrt.writerows(data)
    input(f"Saved to {file_name}")