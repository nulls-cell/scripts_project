import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formatdate
import traceback


class EmailUitl:

    # 初始化一些类变量
    sender = '270239148@qq.com'
    password = '****'
    receiver_list = None
    msg_root = MIMEMultipart('relate')
    msg_root['From'] = sender
    msg_root['Date'] = formatdate(localtime=True)
    mime_type = {
        'text/css': 'css',
        'html': 'htm,html',
        'text/plain': 'txt,bas',
        'image/gif': 'gif',
        'image/x-icon': 'ico',
        '如果还有找不到的请百度搜索:"MIME type"': ''
        }

    # 添加附件内容
    @classmethod
    def add_attachment(cls, filename):
        att = MIMEText(open(filename, 'rb').read(), 'base64', 'gbk')
        att['Content-Type'] = 'application/octet-stream'
        att.add_header('Content-Disposition', 'attachment', filename=('gbk', '', filename.split('/')[-1]))
        cls.msg_root.attach(att)

    # 添加另一种附件
    @classmethod
    def add_app(cls, filename):
        att = MIMEApplication(open(filename, 'rb').read())
        att.add_header('Content-Disposition', 'attachment', filename=('gbk', '', filename.split('/')[-1]))
        cls.msg_root.attach(att)

    # 获取正文内容
    @classmethod
    def add_content(cls, content, mime_type='html;css', _encode='gbk'):
        message = MIMEText(content, mime_type, 'gbk')
        cls.msg_root.attach(message)

    # 设置邮件头
    @classmethod
    def set_mail_header(cls, subject, receiver_list, cc_list=[], bcc_list=[]):
        cls.msg_root['Subject'] = subject
        cls.msg_root['To'] = ';'.join(receiver_list)
        cls.msg_root['Cc'] = ';'.join(cc_list)
        cls.msg_root['Bcc'] = ';'.join(bcc_list)
        cls.receiver_list = receiver_list + cc_list + bcc_list

    # 所有内容都提前配置好之后调用此方法
    @classmethod
    def send(cls):
        try:
            assert(cls.msg_root['Subject'])
            smtp = smtplib.SMTP()
            print('初始化服务完毕')
            smtp.connect('smtp.hfax.com')
            print('连接到服务')
            smtp.login(cls.sender, cls.password)
            print('登录成功')
            smtp.sendmail(cls.sender, cls.receiver_list, cls.msg_root.as_string())
            print('发送成功')
        except Exception as e:
            print('发送失败，错误原因为：%s' % e)
            print(traceback.format_exc())
        finally:
            cls.msg_root = MIMEMultipart('relate')

    # 发送邮件功能
    @classmethod
    def send_mail_with_allconf(cls, filename, filename2, subject, content, receiver_list, cc_list=[], bcc_list=[]):
        cls.add_attachment(filename)
        cls.add_app(filename2)
        cls.add_content(content=content, mime_type='html;css', _encode='gbk')
        cls.set_mail_header(subject, receiver_list, cc_list, bcc_list)
        print('邮件内容加载完毕')
        cls.send()


if __name__ == '__main__':

    _filename2 = 'C:/Users/Administrator/Desktop/中文——English.xlsx'
    _filename = 'C:/Users/Administrator/Desktop/中文——English2.xlsx'
    _subject = '我的邮件类'
    _content = '<p>第一封邮件<p>'
    _receiver_list = ['']
    EmailUitl.add_app(_filename)
    EmailUitl.add_app(_filename2)
    EmailUitl.add_content(content=_content, mime_type='html')
    EmailUitl.set_mail_header(subject=_subject, receiver_list=_receiver_list)
    EmailUitl.send()
    EmailUitl.send()


