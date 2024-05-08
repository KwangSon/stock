import requests
from bs4 import BeautifulSoup
import datetime as dt

def get_item():
    url = 'https://hsseniorclub.or.kr/bbs/?bid=notice'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    job_list = soup.find_all("li", {"class": "item"})

    new_job_list = []
    today = dt.datetime.now()
    today_format = today.strftime('%Y.%m.%d')


    for job in job_list:
        date_str = job.find('div', {"class":"date"}).text
        if date_str == today_format :
            new_job_list.append(job)
    return new_job_list
