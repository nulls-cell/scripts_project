from common_util.mysql_util.mysql_conn import MysqlUtil
from common_util.email_util import send
from common_util.datetime_unit import add_date
from common_util.log_util import get_logger
from common_util.excel_util import ExcelUtil
import traceback
import os


# 初始化日志
logger = get_logger()
logger.info('日志初始化完毕')

try:
    # 初始化数据库参数
    # mysql
    my_db = MysqlUtil.get_conn('formal_rc_prd')
    my_cursor = my_db.cursor()
    logger.info('数据库初始化完毕')
    # 初始化10天之前的日志
    ten_days_ago = add_date(-80).strftime('%Y-%m-%d')
    to_date = add_date(0).strftime('%Y-%m-%d')
    logger.info('日期等参数初始化完毕')

    # 初始化excel表
    wb = ExcelUtil()
    # 初始化存储分产品字典
    dic_pro_data = {}
    logger.info('储存数据的xlsx文件和字典初始化完毕')

    # ###################################分产品数据写入#########################################
    # 分产品数据
    my_cursor.execute("select date(lend_date),product_id,product_name,loan_ent,loan_amount,loan_ent_tot,loan_amount_tot\
        from rpt_risk_loan_statistics_report where date(lend_date)>='%s' \
        order by product_id asc,lend_date desc" % ten_days_ago)
    logger.info('分产品sql执行完毕')

    # 分产品存入字典
    result = my_cursor.fetchall()
    for row in result:
        pro_name = str(row[2])
        if pro_name not in dic_pro_data:
            dic_pro_data[pro_name] = [row]
        else:
            dic_pro_data[pro_name].append(row)
    logger.info('分产品书记写入到字典完毕')

    # 写入到excel并释放字典内存
    for pro_name in dic_pro_data:
        head_data = ['日期', '产品id', '产品名称', '报告期放款笔数', '报告期放款金额', '累计放款笔数', '累计放款金额']
        result_data = dic_pro_data[pro_name]
        wb.write_excel(pro_name, head_data, result_data)
    logger.info('分产品数据字典写入到excel完毕')

    # 释放内存
    dic_pro_data.clear()
    logger.info('字典释放内存完毕')

    # ####################################汇总数据库写入########################################
    # 汇总数据
    my_cursor.execute("select date(lend_date),loan_ent,loan_amount,loan_ent_tot,loan_amount_tot\
        from rpt_risk_loan_statistics_report where date(lend_date)>='%s' \
        group by date(lend_date)\
        order by product_id asc,lend_date desc" % ten_days_ago)
    logger.info('汇总数据sql执行完毕')

    # 汇总数据写入excel
    result = my_cursor.fetchall()
    head_data = ['日期', '报告期放款笔数', '报告期放款金额', '累计放款笔数', '累计放款金额']
    wb.write_excel('汇总数据', head_data, result)
    wb.set_fit()
    _file_name = os.path.dirname(os.path.abspath(__file__))+'发放贷款统计数据_%s.xlsx' % to_date
    logger.info('汇总数据写入到excel完毕')

    # 保存excel
    wb.save(filename=_file_name)
    logger.info('xlsx文件保存完毕')

    # 发送邮件参数初始化
    _subject = '发放贷款统计数据——%s' % to_date
    _content = '您好:\n\t附件为%s的发放贷款统计数据，汇总数据在名为“汇总数据”的sheet中，请查收。' % to_date
    receiver_list = ['lirui-pbj@hfax.com']
    logger.info('发送邮件函数初始化完毕')

    # 发送邮件
    logger.info('开始发送邮件')
    send(file_name=_file_name, subject=_subject, content=_content, _receiver_list=receiver_list, mime_type='plain')
    logger.info('邮件发送完毕')

except Exception as e:
    print('错误原因：' + str(e))
    print(traceback.format_exc())
finally:
    MysqlUtil.close_all()


