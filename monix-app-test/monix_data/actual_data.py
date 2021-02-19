from config import data_conf
from monix_data.depend_data import DependData
from monix_data.excel_data import GetData
import base64
import json
from utility import encrypt_util
from config.monix_conf import global_config
from utility.json_util import OperationJson
from utility.db_util import OperationMysql
from jsonpath_rw import parse, jsonpath
from utility.common_unti import CommonUnit


class ActualData:

    def __init__(self, row):
        self.getData = GetData()
        self.oper_json = OperationJson()
        self.oper_sql = OperationMysql()
        self.row = row

    def get_right_header(self):
        """正确的header"""
        header = self.getData.is_header(self.row)
        if header == 'yes':
            encrypt = self.getData.is_header_encrypt(self.row)
            if encrypt == True:
                return self.get_encrypt_header()
            else:
                return data_conf.get_header_val()
        elif header == "normal":
            return data_conf.get_mysql_callback_header()
        else:
            return None

    def get_right_request_data(self):
        """返回正确的请求数据"""
        request_data = self.getData.get_request_data(self.row)
        encrypt = self.getData.is_post_data_encrypt(self.row)
        case_id = self.getData.get_case_id(self.row)
        is_need_db_data = self.getData.is_need_db_data(self.row)
        is_depend = self.getData.is_depend(self.row)
        if request_data == None:
            return None
        if is_need_db_data == True:
            sql = self.getData.get_sql(request_data)
            print("------开始查询sql---------" + sql)
            res = self.oper_sql.search_data(sql)
            print("sql查询结果:" + str(res))
            self.getData.update_request_data(request_data, res)
            print("更新成功")

        post_data = self.oper_json.get_data_from_json(request_data)
        if request_data == "creditPass":
            post_data["apply_id"] = res['credit_apply_id']
            post_data["customer_id"] = res['customer_id']
        elif request_data == "riskPass":
            post_data["post_data"] = res["loan_invoice_id"]
            post_data["customer_id"] = res['customer_id']
        elif request_data == "loanPass":
            post_data["loanApplyId"] = res['loan_apply_id']
        print("请求数据" + str(post_data))

        if encrypt == True:
            return encrypt_util.encrypt(post_data)
        else:
            return post_data

    def get_encrypt_header(self):
        """获得加密后的header"""
        header = {"content-type": "application/json"}
        param = encrypt_util.encrypt(self.oper_json.get_data_from_json("params"))
        header["params"] = param
        return header

    def get_depend_data(self, depend_data, res_data):
        """提取需要的依赖数据"""

        json_expr = parse(depend_data)
        male = json_expr.find(res_data)
        return [math.value for math in male][0]
