import xlrd
from xlutils.copy import copy


class OperationExcel:
    def __init__(self, filename=None, sheet_id=None):
        if filename:
            self.file_name = filename
            self.sheet_id = sheet_id
        else:
            self.file_name = '../testcase/testcase.xls'
            self.sheet_id = 0

        self.data = self.get_data()

    def get_data(self):
        """获取sheets内容"""
        data = xlrd.open_workbook_xls(self.file_name)
        tables = data.sheets()[self.sheet_id]
        return tables

    def get_lines(self):
        """获取单元格的行数"""
        return self.data.nrows

    def get_cell_value(self, row, col):
        """获取单元格的内容"""
        return self.data.cell_value(row, col)

    def write_value(self, rows, col, value):
        """向excel中写入数据"""
        read_data = xlrd.open_workbook_xls(self.file_name)
        write_data = copy(read_data)
        sheet_data = write_data.get_sheet(0)
        sheet_data.write(rows, col, value)
        write_data.save(self.file_name)

    def get_rows_data(self, case_id):
        """根据caseID,找到对应行号内容"""
        num = self.get_rows_num(case_id)
        rows_data = self.get_rows_values(num)
        return rows_data

    def get_rows_num(self, case_id):
        """根据caseID,找到对应行号"""
        num = 0
        cols = self.get_col_values()
        for col in cols:
            if case_id in col:
                return num
            num = num + 1
        return num

    def get_rows_values(self, row):
        """根据行号，找到该行找到对应内容"""
        tables = self.data
        values = tables.row_values(row)
        return values

    def get_col_values(self, col_id=None):
        """根据列号,找到该列对应的内容"""
        if col_id != None:
            cols = self.data.col_values(col_id)
        else:
            cols = self.data.col_values(0)
        return cols


if __name__ == "__main__":
    o = OperationExcel()
    case_id = 'ID-007'
    print(o.get_rows_data(case_id))