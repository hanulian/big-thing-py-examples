#!/bin/python

from big_thing_py.big_thing import *
from secret import *


from email.encoders import encode_base64
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import datetime
import argparse
import smtplib
import ssl


def send(receiver_email: str = '', title: str = '', body: str = '') -> bool:
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = Header(s=title, charset='utf-8')
    body = MIMEText(body, _charset='utf-8')
    msg.attach(body)

    if 'gmail' in SENDER_EMAIL:
        mailServer = smtplib.SMTP_SSL('smtp.gmail.com')
    elif 'naver' in SENDER_EMAIL:
        mailServer = smtplib.SMTP_SSL('smtp.naver.com')
    elif 'daum' in SENDER_EMAIL:
        mailServer = smtplib.SMTP_SSL('smtp.daum.net')

    mailServer.login(SENDER_EMAIL, SENDER_PASSWORD)
    mailServer.send_message(msg)
    mailServer.quit()


def send_with_file(receiver_email: str = '', title: str = '', body: str = '', attachment_path: str = '') -> bool:
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = Header(s=title, charset='utf-8')
    body = MIMEText(body, _charset='utf-8')
    msg.attach(body)

    if attachment_path:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(attachment_path, "rb").read())
        encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment_path)}"')
        msg.attach(part)

    if 'gmail' in SENDER_EMAIL:
        mailServer = smtplib.SMTP_SSL('smtp.gmail.com')
    elif 'naver' in SENDER_EMAIL:
        mailServer = smtplib.SMTP_SSL('smtp.naver.com')
    elif 'daum' in SENDER_EMAIL:
        mailServer = smtplib.SMTP_SSL('smtp.daum.net')

    mailServer.login(SENDER_EMAIL, SENDER_PASSWORD)
    mailServer.send_message(msg)
    mailServer.quit()


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", '-n', action='store', type=str,
                        required=False, default='email_big_thing', help="thing name")
    parser.add_argument("--host", '-ip', action='store', type=str,
                        required=False, default='127.0.0.1', help="host name")
    parser.add_argument("--port", '-p', action='store', type=int,
                        required=False, default=11083, help="port")
    parser.add_argument("--alive_cycle", '-ac', action='store', type=int,
                        required=False, default=60, help="alive cycle")
    parser.add_argument("--auto_scan", '-as', action='store_true',
                        required=False, help="middleware auto scan enable")
    parser.add_argument("--log", action='store_true',
                        required=False, help="log enable")
    args, unknown = parser.parse_known_args()

    return args


def generate_thing(args):
    tag_list = [SoPTag(name='email')]
    function_list = [SoPFunction(func=send,
                                 return_type=SoPType.BOOL,
                                 tag_list=tag_list,
                                 arg_list=[SoPArgument(name='address',
                                                       type=SoPType.STRING,
                                                       bound=(0, 10000)),
                                           SoPArgument(name='title',
                                                       type=SoPType.STRING,
                                                       bound=(0, 10000)),
                                           SoPArgument(name='text',
                                                       type=SoPType.STRING,
                                                       bound=(0, 10000))]),
                     SoPFunction(func=send_with_file,
                                 return_type=SoPType.BOOL,
                                 tag_list=tag_list,
                                 arg_list=[SoPArgument(name='address',
                                                       type=SoPType.STRING,
                                                       bound=(0, 10000)),
                                           SoPArgument(name='title',
                                                       type=SoPType.STRING,
                                                       bound=(0, 10000)),
                                           SoPArgument(name='text',
                                                       type=SoPType.STRING,
                                                       bound=(0, 10000)),
                                           SoPArgument(name='file',
                                                       type=SoPType.STRING,
                                                       bound=(0, 10000))])]
    value_list = []

    thing = SoPBigThing(name=args.name, ip=args.host, port=args.port, alive_cycle=args.alive_cycle,
                        service_list=function_list + value_list)
    return thing


if __name__ == '__main__':
    args = arg_parse()
    thing = generate_thing(args)
    thing.setup(avahi_enable=args.auto_scan)
    thing.run()
