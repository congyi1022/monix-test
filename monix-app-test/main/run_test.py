import json
import time
from base.sendRequest import RunMain
from monix_data.excel_data import GetData
from utility import encrypt_util
from utility.common_unti import CommonUnit
from monix_data.actual_data import ActualData
from utility.excel_util import OperationExcel
from utility.email_unti import SendEmail


class RunTest:
    def __init__(self):
        self.run = RunMain()
        self.data = GetData()
        self.common_unit = CommonUnit()
        self.sendEmail=SendEmail()

    def go_run_main(self):
        """程序执行入口"""
        pass_count=[]
        fail_count=[]
        case_lines = self.data.get_case_lines()
        for i in range(1, case_lines):
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
            print(type(res))
            if decrypt:
                res = encrypt_util.decrypt(json.loads(res)["data"])
                self.data.update_header(res)
                print("解密后的数据" + str(res))
                print(type(res))
            is_contain = self.common_unit.is_contain(expect, res)
            if is_contain == True:
                self.data.wirte_result(i, "pass")
                pass_count.append(i)
            else:
                self.data.wirte_result(i, str(res))
                fail_count.append(i)
            depend_case_id = self.data.get_depend_case_id(i)
            if depend_case_id != None:
                self.oper_excel = OperationExcel()
                row = self.oper_excel.get_rows_num(depend_case_id)  # 获取到依赖的行
                depend_request_data = self.data.get_request_data(row)  # 获取到依赖的请求参数key
                depend_data = self.data.get_depend_data(i)  # 获取到依赖参数到key
                depend_field = self.data.get_depend_filed(i)  # 获取到依赖参数到字段
                is_list = CommonUnit.is_contain(",", depend_data)  # 判断是否是多参数依赖
                if is_list:
                    depend_datas = depend_data.split(",")
                    depend_fields = depend_field.split(",")
                    for j in range(len(depend_datas)):
                        depend_data_key = depend_datas[j]
                        depend_value = self.encrypt_data.get_depend_data(depend_data_key, res)
                        if depend_data_key == "payAmount":
                            depend_value = depend_value / 100
                        self.data.write_header(depend_request_data, depend_fields[j], depend_value)
                else:
                    depend_value = self.encrypt_data.get_depend_data(depend_data, json.loads(res))
                    self.data.write_header(depend_request_data, depend_field, depend_value)

            print("-------------------------------------")
            time.sleep(1)
        self.sendEmail.send_main(pass_count,fail_count)


if __name__ == "__main__":
    run = RunTest()
    res = run.go_run_main()
