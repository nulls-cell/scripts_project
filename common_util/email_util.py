import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
import traceback


# 发送邮件方法
def send(file_name=None, subject='系统邮件', content='您好，请查收。', sender='发件地址', password='发件邮箱密码',
         _receiver_list=[],
         smtpserver='smtp.hfax.com', cc_list=[], bcc_list=[], mime_type='html;css'):
    # mime_type_list=['html;css','plain']
    if not (isinstance(_receiver_list, list) and isinstance(cc_list, list) and isinstance(bcc_list, list)):
        raise Exception("请将_receiver_list,cc_list,bcc_list以列表的形式传入")
    msg_root = MIMEMultipart('relate')
    if file_name is not None:
        att = MIMEText(open(file_name, 'rb').read(), 'base64', 'gbk')
        att['Content-Type'] = 'application/octet-stream'
        """  此段注释应用于python2版本
        att.add_header('Content-Disposition', 'attachment', filename='=?utf-8?b?' + 
        base64.b64encode(file_name.split('/')[-1].encode('UTF-8')) + '?=')
        """
        att.add_header('Content-Disposition', 'attachment', filename=('gbk', '', file_name.split('/')[-1]))
        msg_root.attach(att)
    message = MIMEText(content, mime_type, 'gbk')
    msg_root.attach(message)
    msg_root['From'] = sender
    msg_root['To'] = ';'.join(_receiver_list)
    msg_root['Date'] = formatdate(localtime=True)
    msg_root['Subject'] = subject
    if cc_list:
        msg_root['Cc'] = ';'.join(cc_list)
    if bcc_list:
        msg_root['Bcc'] = ';'.join(bcc_list)

    receiver = _receiver_list + cc_list + bcc_list
    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)
        print('连接服务器成功')
        # smtp.set_debuglevel(True)
        # smtp.ehlo()
        # smtp.starttls()   //tls加密
        smtp.login(sender, password)
        print('登录成功')
        smtp.sendmail(sender, receiver, msg_root.as_string(), mail_options=['8bitmime'])
        print('发送成功')
    except Exception as e:
        print(traceback.format_exc())
        print(e)
    finally:
        smtp.quit()


if __name__ == '__main__':
    receiver_list = ['']  # , 'zhangjing@hfax.com']
    _content = 'this is English'
    send(file_name='E:/data_2018-01-22.xls', _receiver_list=receiver_list, mime_type='plain', content=_content)
