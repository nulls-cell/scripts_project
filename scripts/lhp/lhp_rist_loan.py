import sys
from common_util.psql_util.psql_conn import PsqlUtil
from common_util.mysql_util.mysql_conn import MysqlUtil


# 初始化数据库参数
# psql
post_db = PsqlUtil.get_conn('formal_gpdw')
post_cursor = post_db.cursor()
# mysql
my_db = MysqlUtil.get_conn('formal_rc_prd')
my_cursor = my_db.cursor()

