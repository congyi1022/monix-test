import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import datetime
import time
from config.monix_conf import global_config


class SendEmail:
    """发送邮件"""
    # global sender
    # global my_pass
    # sender = '997296384@qq.com'  # 发件人邮箱账号
    # my_pass = 'ucrwmxkbvqycbcjd'  # 使用qq邮件作为发送服务器获得的授权码

    def send_test_mail(self, receiveList, sub, content):
        # 设置邮件基本内容
        # msg = MIMEMultipart()  # 创建一个带附件的实例
        # msg['Subject'] = sub  # 设置邮件标题
        # msg['From'] = formataddr(["licongyi", sender])  # 发件人名称
        # msg['To'] = ";".join(receiveList)  # 收件人列表
        # msg.attach(MIMEText(content, "plain", "utf-8"))  # 邮件正文内容

        # # 邮件携带附件
        # filename = "../report/" + now + "-report.html"  # 保存的报告路径和名称
        # att1 = MIMEText(open(filename, 'rb').read(), 'base64', 'utf-8')
        # att1["Content-Type"] = 'application/octet-stream'
        # att1["Content-Disposition"] = 'attachment; filename="result.html"'  # 这里的filename可以任意写，是邮件中附件显示的名字
        # msg.attach(att1)  # 添加附件，如果有多个附件，同理添加

        user = "licongyi" + "<" + str(global_config.sender) + ">"
        message = MIMEText(content, _subtype='plain', _charset="utf8")
        message['Subject'] = sub
        message['From'] = user
        message['To'] = ";".join(receiveList)

        # 发送邮件
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(global_config.sender, global_config.my_pass)
        server.sendmail(user, receiveList, message.as_string())
        print("邮件发送成功" + str(receiveList))
        server.quit()

    def send_main(self, pass_list, fail_list):
        sub = "monix app主流程接口自动化测试结果"
        pass_num = float(len(pass_list))
        fail_num = float(len(fail_list))
        count_num = pass_num + fail_num
        pass_result = "%.2f%%" % (pass_num / count_num * 100)
        fail_result = "%.2f%%" % (fail_num / count_num * 100)

        content = "运行结果个数为%s个\n通过个数为%s个\n失败个数为%s个\n通过率为%s\n失败率为%s\n\n详情请参考附件测试结果:" % (
            count_num, pass_num, fail_num, pass_result, fail_result)
        self.send_attach_mail(global_config.receiver, sub, content)

    def send_attach_mail(self, receiveList, sub, content):
        # 设置邮件基本内容
        msg = MIMEMultipart()  # 创建一个带附件的实例
        msg['Subject'] = sub  # 设置邮件标题
        msg['From'] = formataddr(["licongyi", global_config.sender])  # 发件人名称
        msg['To'] = ";".join(receiveList)  # 收件人列表
        msg.attach(MIMEText(content, "plain", "utf-8"))  # 邮件正文内容

        # 邮件携带附件
        filename = "../testcase/testcase.xls"  # 保存的报告路径和名称
        att1 = MIMEText(open(filename, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename="testcase.xls"'  # 这里的filename可以任意写，是邮件中附件显示的名字
        msg.attach(att1)  # 添加附件，如果有多个附件，同理添加

        # 发送邮件
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(global_config.sender, global_config.my_pass)
        server.sendmail(global_config.sender, receiveList, msg.as_string())
        print("邮件发送成功" + str(receiveList))
        server.quit()


if __name__ == '__main__':
    s = SendEmail()
    content="测试报告见附件"
    sub="report"
    # s.send_attach_mail(global_config.receiver,sub,content)
    pass_list = [1, 1, 1, 1, 1, 1, 1, 1]
    fail_list = [1, 1]
    s.send_main(pass_list, fail_list)
