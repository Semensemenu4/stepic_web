from bs4 import BeautifulSoup
from decimal import Decimal


def convert(amount, cur_from, cur_to, date, requests):
    url = f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}'
    response = requests.get(url)  # Использовать переданный requests
    soup = BeautifulSoup(response.content, 'xml')
    tags = soup.find_all('Valute')

    if cur_from == 'RUR':
        for tag in tags:
            if tag.CharCode.text == cur_to:
                rur = Decimal(tag.Value.text.replace(',', '.')) / Decimal(tag.Nominal.text.replace(',', '.'))
                result = Decimal(amount) / Decimal(rur)

                return result.quantize(Decimal("1.0000"))
    else:
        sum_rur_from = 0
        rur_to = 0
        for tag in tags:
            if tag.CharCode.text == cur_from:
                rur = Decimal(tag.Value.text.replace(',', '.')) / Decimal(tag.Nominal.text.replace(',', '.'))
                sum_rur_from = Decimal(amount) * Decimal(rur)
            if tag.CharCode.text == cur_to:
                rur_to = Decimal(tag.Value.text.replace(',', '.')) / Decimal(tag.Nominal.text.replace(',', '.'))
        
        result = Decimal(sum_rur_from) / Decimal(rur_to)
        
        return result.quantize(Decimal("1.0000"))
