import yfinance as yf
import smtplib
import json
from datetime import date
from prettytable import PrettyTable as pt


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
    company_codes = [line.strip() for line in f]
company_codes.pop(0)

with open('block.txt') as f:
    block_codes = [line.strip() for line in f]

for block_code in block_codes:
    company_codes.remove(block_code)

cnt = 0

tb = pt()
tb.field_names = ["ID", "Name", "LowP"]

for code in company_codes:
    ticker = yf.Ticker(code + ".ks")
    if not 'fiftyTwoWeekLowChangePercent' in ticker.info:
        print(ticker.info)
        continue

    if (ticker.info['fiftyTwoWeekLowChangePercent'] < 0.03):
        tb.add_row([ticker.info['symbol'][:-3], ticker.info['shortName'],
                   round(ticker.info['fiftyTwoWeekLowChangePercent'], 3)])
        cnt += 1

    if __debug__ and cnt == 2:
        break

with open(".secret", "r") as json_file:
    secret_data = json.load(json_file)

mail_header = "Report " + str(date.today())
send_email(secret_data['mail_id'], secret_data['mail_key'],
           secret_data['recipient'], mail_header, tb.get_string())
