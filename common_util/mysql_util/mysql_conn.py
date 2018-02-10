import pymysql
from .mysql_conf import mysql_dic
import traceback


class MysqlUtil:
    # 键值对的形式存储数据库名称和数据库连接对象
    connecting_db_dic = {}

    @classmethod
    # 获取数据库连接，传入数据库配置key名，在psql_conf.py中
    def get_conn(cls, db_name):
        assert (isinstance(db_name, str))
        try:
            if db_name in cls.connecting_db_dic:
                _db = cls.connecting_db_dic[db_name]
            else:
                _db = pymysql.connect(**(mysql_dic[db_name]))
                cls.connecting_db_dic[db_name] = _db
            print('数据库连接成功，参数为：', mysql_dic[db_name])
            return _db
        except Exception as e:
            print('数据库连接失败，原因：' + str(e))
            print(traceback.format_exc())

    @classmethod
    # 关闭单个数据库，掺入数据库名字，进行关闭
    def close_by_name(cls, db_name):
        assert (isinstance(db_name, str))
        try:
            cls.connecting_db_dic[db_name].close()
            del cls.connecting_db_dic[db_name]
        except Exception as e:
            print(db_name + ' 数据库不存在或数据库未连接或数据库关闭失败，具体原因：' + str(e))
            print(traceback.format_exc())

    @classmethod
    # 关闭当前所有连接的数据库
    def close_all(cls):
        for _db_name in list(cls.connecting_db_dic.keys()):
            cls.close_by_name(_db_name)


if __name__ == '__main__':
    db = MysqlUtil.get_conn('test')
