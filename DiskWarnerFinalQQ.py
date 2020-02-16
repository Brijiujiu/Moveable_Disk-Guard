#import dependency modles.
import socket
import time
import requests
import platform
import re
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from aip import AipFace
import cv2
import base64

# Get PCname local time and device platform information&take photo.
pcname = socket.gethostname()
localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
PCplatform = platform.platform()
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

localip = get_host_ip()

def getip():
    year =  time.strftime("%Y",time.localtime())
    IpGeturl =  str('http://'+year+'.ip138.com/ic.asp')
    response = requests.get(IpGeturl)
    ip = re.search(r"\[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\]",response.content.decode(errors='ignore')).group(0)
    return ip

IPaddress = getip()

def send_email():
    host_server = 'smtp.163.com'

    sender = 'ly9460730472580800@163.com'

    pwd = 'w696919696w'

    sender_mail = 'ly9460730472580800@163.com'

    receiver = open("account.txt", 'r').read()

    mail_content = '您好，您的移动硬盘在陌生设备接入，设备信息如下: ' + '\n' + '接入设备名: '+pcname + '\n' + '设备系统版本： ' + PCplatform + '\n' + '设备公网IP地址： ' + IPaddress + '\n' + '内网IP地址： ' + localip + '\n' + "接入时间： " + localtime + '\n' + '使用者未通过人脸识别验证'+'\n'+'请注意您的数据安全！'
    mail_title = '硬盘接入未知设备预警'

    msg = MIMEMultipart()
    # msg = MIMEText(mail_content, "plain", 'utf-8')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender_mail
    msg["To"] = Header('usr', 'utf-8')

    # 邮件正文内容
    msg.attach(MIMEText(mail_content, 'plain', 'utf-8'))

    fp = open('NowUserFace.jpg', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('invader', '<image1>')
    msg.attach(msgImage)

    smtp = SMTP_SSL(host_server)

    smtp.set_debuglevel(0)
    smtp.ehlo(host_server)
    smtp.login(sender, pwd)

    smtp.sendmail(sender_mail, receiver, msg.as_string())
    smtp.quit()

def Face_Compared():
    APP_ID = '15033725'
    API_KEY = 'he0CtkD7MQUImD8UxVX4Zr4F'
    SECRET_KEY = 'sK97hzEpoRHNlnWNIqa0tHHC8RyNKEj1'
    client = AipFace(APP_ID, API_KEY, SECRET_KEY)

    IMAGE_TYPE = 'BASE64'

    f1 = open('orginal.jpg', 'rb')
    f2 = open('NowUserFace.jpg', 'rb')
    #image parameters
    img1 = base64.b64encode(f1.read())
    img2 = base64.b64encode(f2.read())
    image_1 = str(img1, 'utf-8')
    image_2 = str(img2, 'utf-8')

    ptr = client.match([{'image': image_1, 'image_type': 'BASE64', }, {'image': image_2, 'image_type': 'BASE64', }])
    ptr = ptr['result']

    if ptr['score'] <= 50:
        send_email()

    else:
        pass

def Camera_control():
    if cv2.VideoCapture(0).isOpened():
        cap1 = cv2.VideoCapture(0)
        while True:
            ret, frame = cap1.read()
            if ret:
                file_name = "NowUserFace.jpg"
                cv2.imwrite(file_name, frame)
                break
            else:
                break
            Face_Compared()

    elif cv2.VideoCapture(1).isOpened():
        cap2 = cv2.VideoCapture(1)
        while True:
            ret, frame = cap2.read()
            if ret:
                file_name = "NowUserFace.jpg"
                cv2.imwrite(file_name, frame)
                break
            else:
                break
            Face_Compared()
    else:
        pass

def write_data():
    IPaddress = getip()
    pcinfo = str(pcname + ' ' + IPaddress + ' ' + localtime + '\n')
    # Write to data.txt file.
    Datafile = open('data.txt', 'a')
    Datafile.write(pcinfo)
    Datafile.close()

#Judge whether there have recode in the data.txt file.

def Judge():
    f = ''.join(open('data.txt').readlines())
    if pcname not in f:
        Camera_control()  # Begin to take photo and identify user.
        send_email()
    else:
        pass
Judge()

write_data()

'''完成于戊戌八月廿八未时，2018年10月7日周日下午1：50分。
制作人： 闽清第一中学，高一五班，吴禹荣'''

#2018.12.06.23:04 update to V6.0
#2018.12.08,20:52 update to V7.0
