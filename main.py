import yfinance as yf
import smtplib
import json
from datetime import date
from prettytable import PrettyTable as pt
import requests
from bs4 import BeautifulSoup
import html
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def per_from_n(code):
    url = "https://finance.naver.com/item/main.nhn?code=" + code

    res = requests.get(url)
    # print(res.text)
    soup = BeautifulSoup(res.text, "lxml")

    rv_per = []

    captions = soup.find("div", {"class": "cop_analysis"}).find_all('tr')
    for caption in captions:
        if (caption.find('th').get_text() == 'PER(배)'):
            per_list = caption.find_all('td')
            for per in per_list:
                rv_per.append(per.get_text().strip())
    return rv_per


def send_email(user, pwd, recipient, subject, body):

    TO = recipient if isinstance(recipient, list) else [recipient]

    # Prepare actual message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = user
    msg['To'] = ", ".join(TO)

    text = "good investment"
    html = "<html><head></head><body>" + body + "</body></html>"

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    if __debug__:
        print('-----mail debug------')
        print('{}\n{}'.format(subject, msg.as_string()))
        print('---------------------')
        return

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(user, TO, msg.as_string())
        server.close()
        print('successfully sent the mail')
    except:
        print("failed to send mail")


if __name__ == '__main__':
    with open('kospi.txt') as f:
        company_codes = [line.strip() for line in f]
    company_codes.pop(0)

    with open('block.txt') as f:
        block_codes = [line.strip() for line in f]

    for block_code in block_codes:
        company_codes.remove(block_code)

    cnt = 0

    tb = pt()
    tb.field_names = ["ID", "Name", "LowP", "NaverInfo", "NaverPER"]

    for code in company_codes:
        try:
            ticker = yf.Ticker(code + ".ks")
            if not 'fiftyTwoWeekLowChangePercent' in ticker.info:
                print(ticker.info)
                continue

            if (ticker.info['fiftyTwoWeekLowChangePercent'] < 0.03):
                n_per_list = per_from_n(code)
                n_stat_link = "https://finance.naver.com/item/main.nhn?code=" + code
                if (float(n_per_list[8]) < 10):  # 2022.12
                    tb.add_row([ticker.info['symbol'][:-3], ticker.info['shortName'],
                                round(ticker.info['fiftyTwoWeekLowChangePercent'], 3), '<a href=' + '"' + n_stat_link + '"' + '>NLink</a>', str(n_per_list)])
                    cnt += 1
        except:
            with open('bug.txt', 'a') as f:
                f.writelines(code)
            continue

        if __debug__ and cnt == 2:
            break

    with open(".secret", "r") as json_file:
        secret_data = json.load(json_file)

    mail_header = "Report " + str(date.today())
    send_email(secret_data['mail_id'], secret_data['mail_key'],
               secret_data['recipient'], mail_header, html.unescape(tb.get_html_string(format=True)))
