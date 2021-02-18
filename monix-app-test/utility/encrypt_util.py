# coding:utf-8
import base64
import json
from utility.database_kms import DatabaseKms
from config.monix_conf import global_config


key = global_config.key
keys = base64.b64decode(key)
databaseKms = DatabaseKms()


def encrypt(content):
    contents = json.dumps(content, separators=(',', ':'))
    data = databaseKms.aes_encrypt(contents, keys, keys[0:16])
    return data


def decrypt(content):
    data = databaseKms.aes_decrypt(content, keys, keys[0:16])
    return json.loads(data)

