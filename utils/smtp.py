from bson.objectid import ObjectId
import datetime
from pymongo.errors import AutoReconnect
import platform, os, sys
if platform.system() == 'Linux':
    sys.path.append('/app/project/AutoDeploy')

import smtplib, sys
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutoDeploy.settings")
django.setup()

from omtools import models as OMTOOLS_MODELS


def sendMail(username,password, send_to, subject, text, files={},server="smtp.gmail.com",port=587):
    assert isinstance(send_to, list)
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text, 'html'))
    for i in files:
        part = MIMEApplication(
                files[i],
                Name=i
            )
        part['Content-Disposition'] = 'attachment; filename="%s"' % i
        msg.attach(part)
    smtp = smtplib.SMTP()
    smtp.connect(server,port)
    smtp.starttls()
    smtp.login(username,password)
    smtp.sendmail(username,send_to,msg.as_string())
    smtp.close()
    return True

if __name__ == '__main__':
    mission_id = sys.argv[1]
    template_id = sys.argv[2]
    mission_obj = OMTOOLS_MODELS.MongodbMission.objects.get(id=mission_id)
    template_obj = OMTOOLS_MODELS.MongodbMissionTemplate.objects.get(id=template_id)

    approval_email = template_obj.approve_mail
    mail_title = 'MongoDB自助任务审核 - %s' % template_obj.title
    approval_url = "http://cmdb.omtools.me/omtools/mongodb-approval.html?id=%s" % mission_obj.approval_md5
    mail_content = "申请执行以下语句：<br><br>%s<br><br>审批地址：<a href='%s'>%s</a>" % (mission_obj.op_exec, approval_url, approval_url)

    sendMail("noreply@m1om.me", "bananaballs123!", [approval_email], mail_title, mail_content)