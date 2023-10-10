#!/bin/python

from big_thing_py.big_thing import *
from secret import SENDER_EMAIL, EMAIL_PASSWORD_GMAIL, EMAIL_PASSWORD_NAVER


from email.mime.text import MIMEText
import argparse
import smtplib
import ssl


def alert(receiver_email: str, text: str) -> bool:
    title = 'Alert'

    SMTP_SSL_PORT = 465  # SSL connection

    if 'gmail' in SENDER_EMAIL:
        SMTP_SERVER = "smtp.gmail.com"
        SENDER_PASSWORD = EMAIL_PASSWORD_GMAIL
    elif 'naver' in SENDER_EMAIL:
        SMTP_SERVER = "smtp.naver.com"
        SENDER_PASSWORD = EMAIL_PASSWORD_NAVER
    else:
        MXLOG_DEBUG('Not supported email service')
        raise

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_SSL_PORT, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        # msg = MIMEText(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} \n{text}')
        msg = MIMEText(text)
        msg['From'] = SENDER_EMAIL
        msg['Subject'] = title
        msg['To'] = receiver_email
        result = server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())

    if result is not {}:
        return True
    else:
        return False


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--name", '-n', action='store', type=str, required=False, default='alert_big_thing', help="thing name"
    )
    parser.add_argument(
        "--host", '-ip', action='store', type=str, required=False, default='127.0.0.1', help="host name"
    )
    parser.add_argument("--port", '-p', action='store', type=int, required=False, default=1883, help="port")
    parser.add_argument(
        "--alive_cycle", '-ac', action='store', type=int, required=False, default=60, help="alive cycle"
    )
    parser.add_argument("--auto_scan", '-as', action='store_true', required=False, help="middleware auto scan enable")
    parser.add_argument("--log", action='store_true', required=False, help="log enable")
    args, unknown = parser.parse_known_args()

    return args


def generate_thing(args):
    tag_list = [MXTag(name='alert')]
    function_list = [
        MXFunction(
            func=alert,
            return_type=MXType.BOOL,
            exec_time=120,
            timeout=120,
            tag_list=tag_list,
            arg_list=[
                MXArgument(
                    name='receiver_email',
                    type=MXType.STRING,
                    bound=(0, 1000),
                ),
                MXArgument(
                    name='text',
                    type=MXType.STRING,
                    bound=(0, 1000),
                ),
            ],
        )
    ]
    value_list = []

    thing = MXBigThing(
        name=args.name,
        ip=args.host,
        port=args.port,
        alive_cycle=args.alive_cycle,
        service_list=function_list + value_list,
    )
    return thing


if __name__ == '__main__':
    args = arg_parse()
    thing = generate_thing(args)
    thing.setup(avahi_enable=args.auto_scan)
    thing.run()
