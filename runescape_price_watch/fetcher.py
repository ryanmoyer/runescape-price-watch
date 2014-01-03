import requests


def fetch_price(item_id):
    item_url = ('http://services.runescape.com/m=itemdb_rs/api/'
                'catalogue/detail.json?item={0}').format(item_id)
    response = requests.get(item_url)
    response.raise_for_status()
    item_inner = response.json()['item']
    item_price = item_inner['current']['price']
    item_name = item_inner['name']
    # TODO explain why item_prices need to be returned as strings.
    return (item_name, str(item_price))


def fetch_prices(item_ids):
    return [fetch_price(item_id) for item_id in item_ids]
