from utils.input_utils import *

class DataTable():

    def __init__(self, table_name, headers, display_names = None, header_align = "^", col_formatting = None, divide_rows = False):
        self.table_name = table_name
        self.headers = headers
        self.display_names = display_names if display_names else headers
        self.header_align = header_align
        self.col_formatting = col_formatting if col_formatting else [""] * len(headers)
        self.divide_rows = divide_rows
        self.rows = []

    def __str__(self):
        column_widths = {}
        for idx, header in enumerate(self.headers):
            column_widths[header] = len(self.display_names[idx])

        for row in self.rows:
            for idx, header in enumerate(self.headers):
                if len(f"{row[header]:{self.col_formatting[idx]}}") > column_widths[header]:
                    column_widths[header] = len(f"{row[header]:{self.col_formatting[idx]}}")

        # for key in column_widths.keys():
        #     column_widths[key] += 1

        hori_edge = []
        hori_edge_thick = []
        table_width = 1
        for col_width in column_widths.values():
            hori_edge.append(f"{'─'*(col_width + 2)}")
            hori_edge_thick.append(f"{'━'*(col_width + 2)}")
            table_width += col_width + 3

        table_str = f" {self.table_name} ".center(table_width, '─') + "\n"

        table_str += "┌" + "┬".join(hori_edge) + "┐\n"

        for idx, header in enumerate(self.headers):
            table_str += f"│ {self.display_names[idx]:{self.header_align}{column_widths[header]}} "
        table_str += "│\n"

        table_str += "┝" + "┿".join(hori_edge_thick) + "┥\n"

        row_strs = []
    
        for row in self.rows:
            row_str = ""
            idx = 0
            for header, value in row.items():
                row_str += f"│ {value:{column_widths[header]}{self.col_formatting[idx]}} "
                idx += 1
            row_str += "│\n"
            row_strs.append(row_str)
        if self.divide_rows:
            table_str += ("├" + "┼".join(hori_edge) + "┤\n").join(row_strs)
        else:
            table_str += "".join(row_strs)

        table_str += "└" + "┴".join(hori_edge) + "┘\n"

        return table_str

    def __repr__(self):
        return self.__str__()

    def print(self, columns_to_include = None):
        columns_to_include = columns_to_include if columns_to_include else self.headers

        column_widths = {}
        for idx, header in enumerate(self.headers):
            if header in columns_to_include:
                column_widths[header] = len(self.display_names[idx])

        for row in self.rows:
            for idx, header in enumerate(self.headers):
                if header in columns_to_include:
                    if len(f"{row[header]:{self.col_formatting[idx]}}") > column_widths[header]:
                        column_widths[header] = len(f"{row[header]:{self.col_formatting[idx]}}")

        hori_edge = []
        hori_edge_thick = []
        table_width = 1
        for col_width in column_widths.values():
            hori_edge.append(f"{'─'*(col_width + 2)}")
            hori_edge_thick.append(f"{'━'*(col_width + 2)}")
            table_width += col_width + 3

        table_str = f" {self.table_name} ".center(table_width, '─') + "\n"

        table_str += "┌" + "┬".join(hori_edge) + "┐\n"

        for idx, header in enumerate(self.headers):
            if header in columns_to_include:
                table_str += f"│ {self.display_names[idx]:{self.header_align}{column_widths[header]}} "
        table_str += "│\n"

        table_str += "┝" + "┿".join(hori_edge_thick) + "┥\n"

        row_strs = []
    
        for row in self.rows:
            row_str = ""
            idx = 0
            for header, value in row.items():
                if header in columns_to_include:
                    row_str += f"│ {value:{column_widths[header]}{self.col_formatting[idx]}} "
                    idx += 1
            row_str += "│\n"
            row_strs.append(row_str)
        if self.divide_rows:
            table_str += ("├" + "┼".join(hori_edge) + "┤\n").join(row_strs)
        else:
            table_str += "".join(row_strs)

        table_str += "└" + "┴".join(hori_edge) + "┘\n"

        print(table_str)

    def get_user_selection(self, columns_to_include = None):
        columns_to_include = columns_to_include if columns_to_include else self.headers
        headers = self.headers.copy()
        display_names = self.display_names.copy()
        col_formatting = self.col_formatting.copy()

        headers.insert(0, '_selection_id')
        display_names.insert(0, '')
        col_formatting.insert(0, '')

        column_widths = {}
        for idx, header in enumerate(headers):
            if header in columns_to_include or header == "_selection_id":
                column_widths[header] = len(display_names[idx])

        for id, row in enumerate(self.rows):
            for idx, header in enumerate(headers):
                if header in columns_to_include:
                    if len(f"{row[header]:{col_formatting[idx]}}") > column_widths[header]:
                        column_widths[header] = len(f"{row[header]:{col_formatting[idx]}}")
                elif header == '_selection_id':
                    if len(f"{id:{col_formatting[idx]}}") > column_widths[header]:
                        column_widths[header] = len(f"{id:{col_formatting[idx]}}")

        hori_edge = []
        hori_edge_thick = []
        table_width = 1
        for col_width in column_widths.values():
            hori_edge.append(f"{'─'*(col_width + 2)}")
            hori_edge_thick.append(f"{'━'*(col_width + 2)}")
            table_width += col_width + 3

        table_str = f" {self.table_name} ".center(table_width, '─') + "\n"

        table_str += "┌" + "┬".join(hori_edge) + "┐\n"

        for idx, header in enumerate(headers):
            if header in columns_to_include or header == "_selection_id":
                table_str += f"│ {display_names[idx]:{self.header_align}{column_widths[header]}} "
        table_str += "│\n"

        table_str += "┝" + "┿".join(hori_edge_thick) + "┥\n"

        row_strs = []
    
        for id, row in enumerate(self.rows):
            row_str = f"│ {id:{column_widths['_selection_id']}{col_formatting[0]}} "
            idx = 1
            for header, value in row.items():
                if header in columns_to_include:
                    row_str += f"│ {value:{column_widths[header]}{col_formatting[idx]}} "
                    idx += 1
            row_str += "│\n"
            row_strs.append(row_str)
        if self.divide_rows:
            table_str += ("├" + "┼".join(hori_edge) + "┤\n").join(row_strs)
        else:
            table_str += "".join(row_strs)

        table_str += "└" + "┴".join(hori_edge) + "┘\n"

        print(table_str)
        while True:
            if (user_input := int_input(">>> ")) in range(len(self.rows)):
                return self.rows[user_input]

    def append(self, row):
        if isinstance(row, tuple) or isinstance(row, list):
            self._tuple_append(row)
            return
            
        row_dict = {}
        for header in self.headers:
            if header in row.keys():
                val = row[header]
                row_dict[header] = val if val else ""
            else:
                row_dict[header] = ""
        self.rows.append(row_dict)

    def _tuple_append(self, row):
        row_dict = {}
        for idx, header in enumerate(self.headers):
            try:
                val = row[idx]
                row_dict[header] = val if val else ""
            except:
                row_dict[header] = ""
        self.rows.append(row_dict)

    def append_rows(self, rows):
        for row in rows:
            self.append(row)

    def sort(self, reverse=False, key=None):
        key = key if key else lambda d: d[self.headers[0]]
        self.rows.sort(reverse=reverse, key=key)

    def clear(self):
        self.rows.clear()