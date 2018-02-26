from common_util.mysql_util.mysql_conn import MysqlUtil

if __name__ == '__main__':
    db1 = MysqlUtil.get_conn('formal_rc_prd')
    db2 = MysqlUtil.get_conn('formal_application_db')
    db3 = MysqlUtil.get_conn('formal_application_db')
    print(id(db2))
    print(id(db3))
    MysqlUtil.close_by_name('formal_rc_prd')
    MysqlUtil.close_all()
