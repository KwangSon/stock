import requests
from bs4 import BeautifulSoup


def get_code_url(code):
    return "https://finance.naver.com/item/main.nhn?code=" + code


def get_code_soup(code):
    url = get_code_url(code)

    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    return soup


def get_per_list(soup):
    rv_per = []

    cop_anal = soup.find("div", {"class": "cop_analysis"})
    if (cop_anal is None):
        return ['', '', '', '', '', '', '', '', '', '']

    captions = cop_anal.find_all('tr')
    for caption in captions:
        if (caption.find('th').get_text() == 'PER(배)'):
            per_list = caption.find_all('td')
            for per in per_list:
                rv_per.append(per.get_text().strip())
    return rv_per


def get_52_min_max(soup):
    table = soup.find('table', summary="투자의견 정보")
    price_list = table.find_all('em')
    # nv make [<em>N/A</em>, <em>N/A</em>, <em>2,650</em>, <em>1,627</em>]
    # or [<em>5,450</em>, <em>4,305</em>]
    int_max = int(price_list[-2].text.replace(',', ''))
    int_min = int(price_list[-1].text.replace(',', ''))
    return (int_min, int_max)


def current_price(soup):
    str_price = soup.find('div', {"class": "rate_info"}).find(
        'span', {"class": "blind"}).text
    return int(str_price.replace(',', ''))


if __name__ == '__main__':
    import unittest

    class TestStringMethods(unittest.TestCase):
        def test_per_list(self):
            soup = get_code_soup('089860')
            per_list = get_per_list(soup)
            self.assertEqual(len(per_list), 10)

        def test_52_min_max(self):
            soup = get_code_soup('089860')
            print(get_52_min_max(soup))

        def test_current_price(self):
            soup = get_code_soup('089860')
            print(current_price(soup))

    unittest.main()
