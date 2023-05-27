import smtplib
import json
from datetime import date
from prettytable import PrettyTable as pt
import html
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import nv_stock


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
        print('{}\n{}'.format(subject, body))
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


def contain_negative(per_list):
    for per in per_list:
        if (per and float(per) < 0):
            return True
    return False


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
        soup = nv_stock.get_code_soup(code)
        cp = nv_stock.current_price(soup)
        min_52 = nv_stock.get_52_min_max(soup)[0]
        change_52 = min_52 / cp

        print('code: {}, current_price: {}, min_52: {}, change_52: {}'.format(
            code, cp, min_52, change_52))
        try:
            if (change_52 > 0.9):
                n_per_list = nv_stock.get_per_list(soup)
                n_stat_link = nv_stock.get_code_url(code)
                if (contain_negative(n_per_list)):
                    continue
                if (n_per_list[8] and float(n_per_list[8]) < 10 and
                    n_per_list[2] and float(n_per_list[2]) < 10): # prev quater and year PER
                    tb.add_row([code, nv_stock.get_company_name(soup),
                                round(change_52, 3), '<a href=' + '"' + n_stat_link + '"' + '>NLink</a>', str(n_per_list)])
                    cnt += 1
        except Exception as e:
            with open('bug.txt', 'a') as f:
                f.writelines('{} : {}\n'.format(code, e))
            continue

        if __debug__ and cnt == 2:
            break

    with open(".secret", "r") as json_file:
        secret_data = json.load(json_file)

    mail_header = "Report " + str(date.today())
    send_email(secret_data['mail_id'], secret_data['mail_key'],
               secret_data['recipient'], mail_header, html.unescape(tb.get_html_string(format=True)))
