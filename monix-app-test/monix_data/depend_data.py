import json
from utility import encrypt_util
from utility.excel_util import OperationExcel
from base.sendRequest import RunMain
from monix_data.excel_data import GetData
from jsonpath_rw import parse, jsonpath


class DependData:

    def __init__(self):
        self.oper_excel = OperationExcel()
        self.run = RunMain()
        self.data = GetData()

    def get_case_line_data(self, case_id):
        """通过ID，获取该Id的整行数据"""
        rows_data = self.oper_excel.get_rows_data(case_id)
        return rows_data

    def run_dependent(self, case_id):
        """执行依赖数据"""
        row = self.oper_excel.get_rows_num(case_id)
        post_data = self.data.get_request_data(row)
        url = self.data.get_url(row)
        header = self.data.is_header(row)
        decrypt = self.data.is_response_decrypt(row)
        res = self.run.send_post(url, post_data, header)
        print("原始返回数据：" + str(res))
        if decrypt:
            res = encrypt_util.decrypt(json.loads(res)["data"])
        return res

    def get_depend_data(self, row):
        """提取需要的依赖数据"""
        case_id = self.data.get_depend_case_id(row)
        depend_data = self.data.get_depend_data(row)
        res_data = self.run_dependent(case_id)
        json_expr = parse(depend_data)
        male = json_expr.find(res_data)
        return [math.value for math in male]

if __name__=="__main__":
    depend=["data.total"]
    print(len(depend))

