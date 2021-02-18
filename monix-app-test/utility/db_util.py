import pymysql
from config.monix_conf import global_config


class OperationMysql:
    def __init__(self):
        self.db = pymysql.connect(host=global_config.mysql_host, port=global_config.mysql_port,
                                  user=global_config.mysql_user,
                                  passwd=global_config.mysql_passwd,
                                  db=global_config.mysql_db, charset='utf8', cursorclass=pymysql.cursors.DictCursor,
                                  autocommit=True)
        self.cur = self.db.cursor()

    def search_data(self, sql):
        """根据sql查询数据"""
        self.cur.execute(sql)
        result = self.cur.fetchone()
        return result


if __name__ == "__main__":
    sql="select credit_id from credit_credit_info where customer_id=1090275675033665536 order by created_time desc limit 1"
    o = OperationMysql()
    res = o.search_data(sql)
    print(res)
