from bs4 import BeautifulSoup
import unittest


def parse(path_to_file):    
    # Поместите ваш код здесь.
    # ВАЖНО!!!
    # При открытии файла, добавьте в функцию open необязательный параметр
    # encoding='utf-8', его отсутствие в коде будет вызвать падение вашего
    # решения на грейдере с ошибкой UnicodeDecodeError
    with open( path_to_file, 'r', encoding='utf-8' ) as f:
        resp = f.read()
    soup = BeautifulSoup(resp, 'lxml')

    def image(soup):
        bodyContent = soup.select('#bodyContent img')
        result = 0
        
        for img in bodyContent:
            if 'width' not in img.attrs:
                continue
            if int(img.attrs['width']) > 199:
                result+=1
        
        return result

    def first_letter(soup):
        list_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        list_letters = ['E', 'T', 'C']

        result = 0
        for h in list_tags:
            bodyContent = soup.select(f'div#bodyContent {h}')
            for tag in bodyContent:
                if tag.text[0] in list_letters:
                    result+=1

        return result

    def links(soup):
        bodyContent = soup.select('div#bodyContent a')
        max_link = 0
        for tag in bodyContent:
            long = 0
            all_tags = tag.find_next_siblings(True)
            for tag in all_tags:
                if tag.name != 'a':
                    break
                else: long+=1

            if long > max_link:
                max_link = long

        return max_link + 1    

    def li(soup):
        l = ['ul', 'ol']
        result = 0
        for li in l:
            bodyContent = soup.select(f'div#bodyContent {li}')
            for tag in bodyContent:
                ol = tag.find_parents('ol')
                ul = tag.find_parents('ul')
                if len(ol) + len(ul) != 0:
                    continue
                result+=1
        
        return result

    return [image(soup), first_letter(soup), links(soup), li(soup)]



class TestParse(unittest.TestCase):
    def test_parse(self):
        test_cases = (
            ('wiki/Stone_Age', [13, 10, 12, 40]),
            ('wiki/Brain', [19, 5, 25, 11]),
            ('wiki/Artificial_intelligence', [8, 19, 13, 198]),
            ('wiki/Python_(programming_language)', [2, 5, 17, 41]),
            ('wiki/Spectrogram', [1, 2, 4, 7]),)

        for path, expected in test_cases:
            with self.subTest(path=path, expected=expected):
                self.assertEqual(parse(path), expected)


if __name__ == '__main__':
    unittest.main()