import requests
import json


class RunMain:
    def send_get(self, url, data, header=None):
        response = None
        if header != None:
            response = requests.get(url=url, params=data, headers=header).json()
        else:
            response = requests.get(url=url, params=data).json()
        return response

    def send_post(self, url, data=None, header=None):
        response = None
        if header != None:
            response = requests.post(url=url, data=json.dumps(data), headers=header).json()
        else:
            response = requests.post(url=url, data=json.dumps(data)).json()
        return json.dumps(response, ensure_ascii=False, sort_keys=True, indent=2)

    def run_main(self, url, method, data=None, header=None):
        res = None
        if method == "GET":
            res = self.send_get(url, data, header)
        else:
            res = self.send_post(url, data, header)
        return res
