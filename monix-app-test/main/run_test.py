import json
import time
from base.sendRequest import RunMain
from monix_data.excel_data import GetData
from utility import encrypt_util
from utility.common_unti import CommonUnit
from monix_data.actual_data import ActualData
from utility.excel_util import OperationExcel


class RunTest:
    def __init__(self):
        self.run = RunMain()
        self.data = GetData()
        self.common_unit = CommonUnit()

    def go_run_main(self):
        """程序执行入口"""

        case_lines = self.data.get_case_lines()
        for i in range(11, case_lines):
            self.encrypt_data = ActualData(i)
            name = self.data.get_case_name(i)
            test_id = self.data.get_case_id(i)
            print("**********" + str(test_id) + ":" + name + "*************")
            url = self.data.get_url(i)
            post_data = self.encrypt_data.get_right_request_data()
            header = self.encrypt_data.get_right_header()
            expect = self.data.get_expect_result(i)
            decrypt = self.data.is_response_decrypt(i)
            res = self.run.send_post(url, post_data, header)
            print("原始返回数据：" + str(res))
            if decrypt:
                res = encrypt_util.decrypt(json.loads(res)["data"])
                self.data.update_header(res)
                print("解密后的数据" + str(res))
            is_contain = self.common_unit.is_contain(expect, res)
            if is_contain == True:
                self.data.wirte_result(i, "pass")
            else:
                self.data.wirte_result(i, "fail")

            depend_case_id = self.data.get_depend_case_id(i)
            if depend_case_id != None:
                self.oper_excel = OperationExcel()
                row = self.oper_excel.get_rows_num(depend_case_id)
                depend_data = self.data.get_depend_data(i)
                for j in list(depend_data):
                    depend_value=self.encrypt_data.get_depend_data(depend_data,json.loads(res))
                    depend_filed = list(self.data.get_depend_filed(j))
                    depend_post_data = self.data.get_request_data(row)
                    self.data.write_header(depend_post_data,depend_filed[j],depend_value)
            print("-------------------------------------")
            time.sleep(2)


if __name__ == "__main__":
    run = RunTest()
    res = run.go_run_main()
