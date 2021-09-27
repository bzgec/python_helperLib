#!/usr/bin/python

"""
https://geekflare.com/send-gmail-in-python/
"""
import sys
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
import traceback


def displayHelp():
    print("""\
Send emails through Gmail.

Tested with python 3.9.7.

How to use:
  python mailSender.py [OPTIONS]

""")
    fileStr = os.path.join(os.path.dirname(__file__), "helpOptionsMailSender.txt")
    with open(fileStr, "r") as file:
        print(file.read())


# https://www.tutorialspoint.com/python/python_command_line_arguments.htm
# Ignore "C901 'checkArgs' is too complex" - I don't think that it is too complex, also
# I don't know how mccabe's complexity could be reduced for this function
def checkArgs(handle, argv):  # noqa: C901
    import getopt

    shortopts = "hf:p:r:x:c:a:"
    longopts = [
        "help",
        "sender=",
        "password=",
        "port=",
        "server=",
        "receiver=",
        "subject=",
        "content=",
        "attachment=",
    ]

    try:
        opts, args = getopt.getopt(argv, shortopts, longopts)
    except getopt.GetoptError:
        displayHelp()
        sys.exit(1)

    for opt, arg in opts:
        if opt in ('-h', "--help"):
            displayHelp()
            sys.exit(0)
        elif opt in ("-f", "--sender"):
            handle["senderMail"] = arg
        elif opt in ("-p", "--password"):
            handle["pass"] = arg
        elif opt in ("--port"):
            handle["port"] = arg
        elif opt in ("--server"):
            handle["smtpServer"] = arg
        elif opt in ("-r", "--receiver"):
            handle["receiverMail"] = arg
        elif opt in ("-x", "--subject"):
            handle["subject"] = arg
        elif opt in ("-c", "--content"):
            handle["content"] = arg
        elif opt in ("-a", "--attachment"):
            handle["attachments"].append(arg)


class Mail:
    def __init__(self, senderMail, password, port=None, smtpServer=None):
        if port is None:
            port = self.getDefault_port()

        if smtpServer is None:
            smtpServer = self.getDefault_smtpServer()

        self.port = port
        self.smtpServer = smtpServer
        self.senderMail = senderMail
        self.password = password

    def getDefault_port(self):
        return 465

    def getDefault_smtpServer(self):
        return "smtp.gmail.com"

    def send(self, email, subject, content, attachments=None):
        mailSendStatus = 1

        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self.smtpServer, self.port, context=ssl_context)
        service.login(self.senderMail, self.password)

        try:
            mail = MIMEMultipart('alternative')
            mail['Subject'] = subject
            mail['From'] = self.senderMail
            mail['To'] = email

            text_mail = "Your mail reader does not support the report format."

            html_content = MIMEText(content.format(email.split("@")[0]), 'html')
            text_content = MIMEText(text_mail.format(email.split("@")[0]), 'plain')

            # Attaching messages to MIMEMultipart
            mail.attach(text_content)
            mail.attach(html_content)

            if attachments is not None:
                # Attaching an attachment
                for attachment in attachments:
                    file_path = attachment
                    mimeBase = MIMEBase("application", "octet-stream")
                    with open(file_path, "rb") as file:
                        mimeBase.set_payload(file.read())
                    encoders.encode_base64(mimeBase)
                    mimeBase.add_header("Content-Disposition", f"attachment; filename={Path(file_path).name}")
                    mail.attach(mimeBase)

            service.sendmail(self.senderMail, email, mail.as_string())
            service.quit()
            mailSendStatus = 0

        except Exception:
            tracebackStr = traceback.format_exc()
            print(tracebackStr)

        return mailSendStatus


def checkScriptParams(handle):
    if handle["senderMail"] is None:
        print("Missing sender email!")
        sys.exit(2)

    if handle["pass"] is None:
        print("Missing sender email password!")
        sys.exit(2)

    if handle["receiverMail"] is None:
        print("Missing receiver email!")
        sys.exit(2)

    if handle["subject"] is None:
        print("Missing email subject!")
        sys.exit(2)


def main():
    handle = {
        "senderMail": None,
        "pass": None,
        "port": None,
        "smtpServer": None,
        "receiverMail": None,
        "subject": None,
        "content": "",
        "attachments": [],
        "mailHandle": None,
    }

    if len(sys.argv) > 1:
        checkArgs(handle, sys.argv[1:])
    else:
        displayHelp()
        sys.exit(1)

    # Check if script parameters are OK
    checkScriptParams(handle)

    # Initialise Mail module
    handle["mailHandle"] = Mail(handle["senderMail"],
                                handle["pass"],
                                handle["port"],
                                handle["smtpServer"])

    # Send email
    mailSendStatus = handle["mailHandle"].send(handle["receiverMail"],
                                               handle["subject"],
                                               handle["content"],
                                               handle["attachments"])

    sys.exit(mailSendStatus)


if __name__ == "__main__":
    main()
