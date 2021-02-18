from utility.json_util import OperationJson


class global_var:
    id = '0'
    name = '1'
    url = '2'
    header = '3'
    depend_case_id = '4'
    depend_data = '5'
    depend_field = '6'
    request_data = '7'
    header_encrypt = '8'
    post_data_encrypt = '9'
    response_decrypt = '10'
    need_db_data = '11'
    expect_result = '12'
    actual_result = '13'


def get_id():
    return global_var.id


def get_name():
    return global_var.name


def get_url():
    return global_var.url


def get_header():
    return global_var.header


def get_depend_case_id():
    return global_var.depend_case_id


def get_depend_data():
    return global_var.depend_data


def get_depend_field():
    return global_var.depend_field


def get_header_encrypt():
    return global_var.header_encrypt


def get_post_data_encrypt():
    return global_var.post_data_encrypt


def get_response_decrypt():
    return global_var.response_decrypt


def get_expect_result():
    return global_var.expect_result


def get_actual_result():
    return global_var.actual_result


def get_request_data():
    return global_var.request_data


def get_need_db_data():
    return global_var.need_db_data


def get_header_val():
    oper = OperationJson()
    headers = oper.get_data_from_json("params")
    return headers


def get_mysql_callback_header():
    header = {"content-type": "application/json"}
    return header


if __name__ == "__main__":
    print(get_mysql_callback_header())
