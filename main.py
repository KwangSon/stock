import yfinance as yf
import smtplib
import json
from datetime import date


def send_email(user, pwd, recipient, subject, body):

    if __debug__:
        print('-----mail debug------')
        print('{}\n{}'.format(subject, body))
        print('---------------------')
        return

    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail')
    except:
        print("failed to send mail")


with open('kospi.txt') as f:
    lines = [line.strip() for line in f]

lines.pop(0)

message = ""
cnt = 0

for code in lines:
    ticker = yf.Ticker(code + ".ks")
    if not 'fiftyTwoWeekLowChangePercent' in ticker.info:
        print(ticker.info)
        continue

    if (ticker.info['fiftyTwoWeekLowChangePercent'] < 0.03):
        message += ('symbol : {}, shortName : {}, 52w_low_% : {}'.format(
            ticker.info['symbol'], ticker.info['shortName'], ticker.info['fiftyTwoWeekLowChangePercent'])) + '\n'
        cnt += 1
        if (cnt == 10):
            break

with open(".secret", "r") as json_file:
    secret_data = json.load(json_file)

mail_header = "Report " + str(date.today())
send_email(secret_data['mail_id'], secret_data['mail_key'],
           secret_data['recipient'], mail_header, message)
