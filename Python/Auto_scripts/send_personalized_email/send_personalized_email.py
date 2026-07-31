import os
import smtplib  # 导入smtplib模块，用于发送电子邮件
import ssl
from email.mime.text import MIMEText  # 从email模块导入MIMEText，用于构建电子邮件正文
from email.mime.multipart import MIMEMultipart  # 从email模块导入MIMEMultipart，用于构建多部分邮件

def send_personalized_email(sender_email, sender_password, recipients, subject, body):
    """
    通过Gmail SMTP服务器发送个性化电子邮件给多个收件人。

    参数:
    sender_email (str): 发件人电子邮件地址。
    sender_password (str): 发件人电子邮件密码。
    recipients (list): 收件人电子邮件地址列表。
    subject (str): 电子邮件的主题。
    body (str): 电子邮件的正文内容。
    """
    context = ssl.create_default_context()
    with smtplib.SMTP('smtp.gmail.com', 587, timeout=30) as server:
        server.starttls(context=context)
        server.login(sender_email, sender_password)

        # 遍历每个收件人，发送个性化邮件
        for recipient_email in recipients:
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = recipient_email
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain', 'utf-8'))
            server.send_message(message)

# 使用示例
if __name__ == "__main__":
    # 凭据从环境变量读取，避免误提交明文密码。
    sender_email = os.getenv('SMTP_SENDER')
    sender_password = os.getenv('SMTP_PASSWORD')
    if not sender_email or not sender_password:
        raise SystemExit('请先设置 SMTP_SENDER 和 SMTP_PASSWORD 环境变量。')

    recipients = ['recipient1@example.com', 'recipient2@example.com']  # 收件人电子邮件地址列表
    subject = 'Hello'  # 邮件主题
    body = 'This is a test email.'  # 邮件正文

    # 调用send_personalized_email函数发送邮件
    send_personalized_email(sender_email, sender_password, recipients, subject, body)
