import yfinance as yf
import smtplib

def send_email(user, pwd, recipient, subject, body):
    

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

send_email('', '', '', 'my first test', 'hi works?')
# with open('kospi.txt') as f:
#     lines = [line.strip() for line in f]

# lines.pop(0)

# message = ""
# cnt = 0

# for code in lines:
#     ticker = yf.Ticker(code + ".ks")
#     if (ticker.info['fiftyTwoWeekLowChangePercent'] < 0.05):
        
#         message += ('symbol : {}, shortName : {}, 52w_low_% : {}'.format(
#             ticker.info['symbol'], ticker.info['shortName'], ticker.info['fiftyTwoWeekLowChangePercent'])) + '\n'
#         cnt += 1
#         if(cnt == 2):
#             break

# print(message)
