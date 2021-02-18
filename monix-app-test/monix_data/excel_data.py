from utility.excel_util import OperationExcel
from config import data_conf
from utility.json_util import OperationJson
from utility import encrypt_util
from utility.common_unti import CommonUnit
from utility.db_util import OperationMysql
import time


class GetData:
    def __init__(self):
        self.open_excel = OperationExcel()
        self.open_json = OperationJson()
        self.common = CommonUnit()
        self.oper_mysql = OperationMysql()

    def get_case_lines(self):
        """获取数据的行数"""
        return self.open_excel.get_lines()

    def get_case_id(self, x):
        """获取case id"""
        y = data_conf.get_id()
        id = self.open_excel.get_cell_value(x, int(y))
        return id

    def get_case_name(self, x):
        """获取case name"""
        y = data_conf.get_name()
        id = self.open_excel.get_cell_value(x, int(y))
        return id

    def get_url(self, x):
        """获取url"""
        y = data_conf.get_url()
        url = self.open_excel.get_cell_value(x, int(y))
        return url

    def get_depend_case_id(self, x):
        """获取依赖case_ID"""
        y = data_conf.get_depend_case_id()
        case_id = self.open_excel.get_cell_value(x, int(y))
        if case_id=='':
            return None
        return case_id

    def get_depend_data(self, x):
        """获取依赖的数据"""
        y = data_conf.get_depend_data()
        data = self.open_excel.get_cell_value(x, int(y))
        if data == "":
            return None
        return data

    def get_depend_filed(self, x):
        """依赖的数据的字段"""
        y = data_conf.get_depend_field()
        fileds = self.open_excel.get_cell_value(x, int(y))
        return fileds

    def is_header(self, x):
        """是否携带header"""
        y = data_conf.get_header()
        header = self.open_excel.get_cell_value(x, int(y))
        return header

    def get_request_data(self, x):
        """获取请求数据"""
        y = data_conf.get_request_data()
        request_data = self.open_excel.get_cell_value(x, int(y))
        if request_data == '':
            return None
        else:
            return request_data

    # def get_encrypt_header(self):
    #     """获得加密后的header"""
    #     header = {"content-type": "application/json"}
    #     param = encrypt_util.encrypt(self.get_data_from_json("params"))
    #     header["params"] = param
    #     return header

    def get_expect_result(self, x):
        """获取预期结果"""
        y = data_conf.get_expect_result()
        expect_result = self.open_excel.get_cell_value(x, int(y))
        return expect_result

    def is_header_encrypt(self, x):
        """header是否加密"""
        is_encrypt = None
        y = data_conf.get_header_encrypt()
        result = self.open_excel.get_cell_value(x, int(y))
        if result == 'yes':
            is_encrypt = True
        else:
            is_encrypt = False
        return is_encrypt

    def is_post_data_encrypt(self, x):
        """请求数据是否加密"""
        is_encrypt = None
        y = data_conf.get_post_data_encrypt()
        result = self.open_excel.get_cell_value(x, int(y))
        if result == 'yes':
            is_encrypt = True
        else:
            is_encrypt = False
        return is_encrypt

    def is_need_db_data(self, x):
        """是否是回调接口"""
        is_callback = None
        y = data_conf.get_need_db_data()
        result = self.open_excel.get_cell_value(x, int(y))
        if result == 'yes':
            is_callback = True
        else:
            is_callback = False
        return is_callback

    def is_response_decrypt(self, x):
        """返回数据是否需要解密"""
        is_decrypt = None
        y = data_conf.get_response_decrypt()
        result = self.open_excel.get_cell_value(x, int(y))
        if result == 'yes':
            is_decrypt = True
        else:
            is_decrypt = False
        return is_decrypt

    def wirte_result(self, x, value):
        y = int(data_conf.get_actual_result())
        self.open_excel.write_value(x, y, value)

    def write_header(self, id, key, value):
        """更新header"""
        self.open_json.set_json_value(id, key, value)

    def update_header(self, res):
        """更新header"""
        header_filed = {"customerId": "customerid", "refreshToken": "refresh-token", "accessToken": "access-token"}
        for i in header_filed.keys():
            result = self.common.is_has_key(i, res)
            if result:
                self.write_header("params", header_filed[i], res[i])

    def update_request_data(self, id, res):
        """更新请求数据"""
        fileds = {"credit_apply_id": "apply_id", "customer_id": "customer_id", "credit_id": "creditId",
                  'loan_invoice_id': "order_sn", "loan_apply_id": "loanApplyId"}
        for i in fileds.keys():
            result = self.common.is_has_key(i, res)
            if result:
                is_exists = self.common.is_has_key(fileds[i], self.open_json.get_data_from_json(id))
                if is_exists:
                    self.write_header(id, fileds[i], res[i])
                    print(id + ":" + fileds[i] + "更新成功")

    def get_customerid(self):
        """获取customerID"""
        customerID = self.open_json.get_data_from_json("params")["customerid"]
        return customerID

    def get_sql(self, id):
        """根据不同的接口，获取不同的sql语句"""
        customer_id = self.get_customerid()
        sql = ""
        if id == "creditPass":
            sql = "select credit_apply_id,customer_id from credit_credit_apply where customer_id=" + str(
                customer_id) + " order by created_time desc limit 1"
        elif id == "riskPass":
            sql = "SELECT loan_apply_id,loan_invoice_id,customer_id from loan_apply_record where customer_id=" + str(
                customer_id) + " order by created_time desc limit 1"
        elif id == "loanPass":
            sql = "SELECT loan_apply_id from loan_apply_record where customer_id=" + str(
                customer_id) + " order by created_time desc limit 1"
        elif id == "payPass":
            sql = "select PAY_APPLY_NO,PAY_AMOUNT from pay_apply_record where customer_id=" + str(
                customer_id) + " order by created_time desc limit 1"
        elif id == "applyLoan":
            sql = "select credit_id from credit_credit_info where customer_id=" + str(
                customer_id) + " order by created_time desc limit 1"
        return sql

    def clear_header(self):
        """还原header"""
        keys = ["refresh-token", "customerid", "access-token"]
        for i in keys:
            self.open_json.set_json_value("params", i, None)
        print("header还原成功")

    def clear_data_from_mysql(self):
        """还原数据库"""
        customerid = self.get_customerid()
        sqls = ["DELETE  FROM repay_receipt_record where CUSTOMER_ID =",
                "DELETE  FROM repay_plan where CUSTOMER_ID =",
                "DELETE  FROM repay_plan_history where CUSTOMER_ID =",
                "DELETE  FROM repay_billing_record where CUSTOMER_ID =",
                "DELETE  FROM repay_billing_detail where CUSTOMER_ID =",
                "DELETE  FROM repay_billing where CUSTOMER_ID =",
                "DELETE  FROM repay_apply_record where CUSTOMER_ID =",
                "DELETE  FROM pay_apply_record where CUSTOMER_ID =",
                "DELETE  FROM loan_invoice_info where CUSTOMER_ID =",
                "DELETE  FROM loan_customer_product where CUSTOMER_ID =",
                "DELETE  FROM loan_apply_record where CUSTOMER_ID =",
                "DELETE  FROM credit_credit_apply where CUSTOMER_ID =",
                "DELETE  FROM credit_credit_info where CUSTOMER_ID =",
                "DELETE  FROM credit_credit_history where CUSTOMER_ID =",
                "DELETE  FROM product_activate where CUSTOMER_ID ="]
        for i in sqls:
            self.oper_mysql.search_data(i + customerid)
        print("数据库清除成功")

    def clear_actual_result(self):
        """还原excel中的实际结果列"""
        lines = self.get_case_lines()
        for i in range(1, lines):
            y = int(data_conf.get_actual_result())
            self.open_excel.write_value(i, y, None)
        print("excel中，实际结果清除成功")

    def clear_all_data(self):
        """还原所有数据"""
        self.clear_header()
        self.clear_actual_result()

    def is_depend(self, x):
        """判断是否有case依赖"""
        depend_case_id = None
        y = data_conf.get_depend_case_id()
        result = self.open_excel.get_cell_value(x, int(y))
        if result == "":
            return None
        return result


if __name__ == "__main__":
    getdata = GetData()
    # print(getdata.get_depend_case_id(12))
    getdata.clear_all_data()
