import json


class OperationJson:

    def __init__(self):
        self.file_name = '../requestdata/requestdata.json'
        self.data = self.read_data()

    def read_data(self):
        """读取json文件"""
        with open(self.file_name) as fp:
            data = json.load(fp)
        fp.close()
        return data

    def get_data_from_json(self, id):
        """根据关键字获取数据"""
        return self.data[id]

    def set_json_value(self, id, key, value):
        """设置json的值"""
        self.data[id][key] = value
        new_data = self.data
        self.save(new_data)

    def save(self, data):
        with open(self.file_name, 'w') as file:
            json.dump(data, file, ensure_ascii=False, sort_keys=True, indent=2)
        file.close()


if __name__ == '__main__':
    opers = OperationJson()
    id = "params"
    key = "devicemodel"
    value = "huawei"
    opers.set_json_value(id, key, value)
