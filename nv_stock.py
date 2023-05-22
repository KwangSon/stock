import requests
from bs4 import BeautifulSoup


def get_code_url(code):
    return "https://finance.naver.com/item/main.nhn?code=" + code


def get_code_soup(code):
    url = get_code_url(code)

    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    return soup


def get_company_name(soup):
    corp_scope = soup.find("div", {"class": "wrap_company"})
    return corp_scope.find('a').text


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
                rv_per.append(per.get_text().strip().replace(',', ''))
            break
    if (len(rv_per) != 10):
        return ['', '', '', '', '', '', '', '', '', '']
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
        test_code = '452260'

        def test_per_list(self):
            soup = get_code_soup(self.test_code)
            per_list = get_per_list(soup)
            self.assertEqual(len(per_list), 10)

        def test_52_min_max(self):
            soup = get_code_soup(self.test_code)
            self.assertEqual(len(get_52_min_max(soup)), 2)
            self.assertIsInstance(get_52_min_max(soup)[0], int)
            self.assertIsInstance(get_52_min_max(soup)[1], int)

        def test_current_price(self):
            soup = get_code_soup(self.test_code)
            self.assertIsInstance(current_price(soup), int)

        def test_company_name(self):
            soup = get_code_soup(self.test_code)
            self.assertIsInstance(get_company_name(soup), str)

    unittest.main()
