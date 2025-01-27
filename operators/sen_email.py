import smtplib
from email.mime.text import MIMEText
from email.header import Header
from ..nodes.BASE.node_tree import RenderStackNode
from ..preferences import get_pref

import bpy
from bpy.props import *


class RSN_OT_SendEmail(bpy.types.Operator):
    bl_idname = "rsn.send_email"
    bl_label = "Send Email (Not ready)"

    smtp_server: StringProperty(
        name="SMTP Server",
        description="Something Like 'smtp.qq.com' or 'smtp.gmail.com'",
        default="")

    smtp_pass: StringProperty(
        name="SMTP Password",
        description="The SMTP Password for your receiver email", )

    content: StringProperty(
        name="Content", default="Write you want to reamain yourself")
    subject: StringProperty(
        name="Subject", default="Write your subject here")

    sender_name: StringProperty(name="Name", default="")

    email: StringProperty(
        name="Email",
        description="Your sender email as well as your receiver email")

    def __init__(self):
        pref = get_pref()

        self.smtp_server = pref.node_smtp.server
        self.smtp_pass = pref.node_smtp.password

        self.mail_host = self.smtp_server
        self.mail_pass = self.smtp_pass
        self.sender = self.email
        self.receivers = self.email

    def send(self):

        message = MIMEText(self.content, 'plain', 'utf-8')

        message['From'] = Header(f"{self.sender_name}<{self.email}>", 'utf-8')
        message['To'] = Header(f"Atticus<{self.sender}>", 'utf-8')

        subject = self.subject  # 发送的主题，可自由填写
        message['Subject'] = Header(subject, 'utf-8')
        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, 465)
            smtpObj.login(self.sender, self.mail_pass)
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            smtpObj.quit()
            return True
        except smtplib.SMTPException as e:
            print(f"Mail sent failed!!! \n{e}")
            return False

    def execute(self, context):
        if self.send():
            self.report({"INFO"}, "Mail sent successfully!")
        else:
            self.report({"INFO"}, "Mail sent failed!")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(RSN_OT_SendEmail)


def unregister():
    bpy.utils.unregister_class(RSN_OT_SendEmail)
