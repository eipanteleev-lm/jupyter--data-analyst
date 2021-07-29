from datetime import datetime, timedelta
from random import randint, random

products = [
    'Люстра',
    'Лампочка',
    'Газонокосилка',
    'Камин',
    'Перфоратор',
    'Отвертка',
    'Шпатель',
    'Швабра'
]

stocks = {
    product_name: randint(0, 100)
    for product_name in products
}


def product():
    index = randint(0, len(products) - 1)
    return products[index]


def stock(product_name, action):
    s = stocks[product_name]

    if action == 'sale':
        s = max(0, s - randint(1, 15))

    if action == 'delivery':
        s += randint(5, 100)

    stocks[product_name] = s
    return s


def time(ts):
    return ts + timedelta(minutes=randint(1, 15))


start_date = datetime(2021, 7, 19, 8)
end_date = datetime(2021, 7, 25, 22)

script = """
create table stocks (
    product text,
    stock numeric,
    ts timestamp,
    constraint pk_stocks primary key (product, ts)
);
"""

insert_template = (
    "\ninsert into stocks (product, stock, ts)"
    + " values ('{product}', {stock}, '{ts}'::timestamp);"
)

if __name__ == '__main__':
    while start_date < end_date:

        if start_date.hour > 22:
            start_date += timedelta(hours=10)

        else:
            start_date = time(start_date)

        product_name = product()

        s = stocks[product_name]
        if stocks[product_name] == 0:
            if random() < 0.33:
                s = stock(product_name, action='delivery')

            else:
                continue

        else:
            if random() < 0.1:
                s = stock(product_name, action='delivery')

            else:
                s = stock(product_name, action='sale')

        script += insert_template.format(
            product=product_name,
            stock=s,
            ts=start_date
        )

    with open('scripts/stocks.sql', 'w', encoding='utf-8') as f:
        f.write(script)
