import requests
import json

# import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def collect_data():
    # response = requests.get(
    #     url='https://inventories.cs.money/5.0/load_bots_inventory/730?buyBonus=40&isStore=true&limit=60&maxPrice=10000&minPrice=1&offset=0&type=2&withStack=true',
    #     headers=headers)
    #
    # with open('result.json', 'w', encoding="UTF-8") as file:
    #     json.dump(response.json(), file, indent=4, ensure_ascii=False)
    offset = 0
    batch_size = 60
    result = []
    while True:
        for item in range (offset,offset+batch_size,60):
            url= f'https://inventories.cs.money/5.0/load_bots_inventory/730?buyBonus=40&isStore=true&limit=60&maxPrice=10000&minPrice=1&offset={item}&type=2&withStack=true'
            response = requests.get(
                url = url,
                headers=headers
            )
            offset += batch_size
            data = response.json()
            items = data.get('items')

            for i in items:
                if i.get('overprice') is not None and i.get('overprice') < -10:
                    item_full_name = i.get('fullName')
                    item_3d = i.get('3d')
                    item_price = i.get('price')
                    item_overprice = i.get('overprice')

                    result.append(
                        {
                        'fullName': item_full_name,
                        '3d': item_3d,
                        'price': item_price,
                        'overprice': item_overprice
                        }
                    )
        if len(items)<60:
            break

    result = sorted(result, key=lambda x: x['overprice'], reverse=True)
    with open('result.json', 'w', encoding="UTF-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)


def main():
    collect_data()

if __name__ == '__main__':
    main()



