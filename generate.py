from datetime import datetime, timedelta
from random import choice, randint, random
from typing import Tuple

products = [
    ('Люстра', 2000),
    ('Лампочка', 200),
    ('Газонокосилка', 18000),
    ('Камин', 20000),
    ('Перфоратор', 7000),
    ('Отвертка', 250),
    ('Шпатель', 300),
    ('Швабра', 1500)
]

stocks = {
    product_name: randint(0, 100)
    for product_name, _ in products
}

orders = dict()


def product() -> str:
    index = randint(0, len(products) - 1)
    return products[index][0]


def shift(timestamp: datetime) -> datetime:
    return timestamp - timedelta(seconds=randint(0, 30))


def generate_order_id(timestamp: datetime) -> str:
    return str(abs(hash(str(timestamp))))


def sales(product_name: str) -> Tuple[int, int]:
    s = stocks[product_name]
    delta = min(randint(1, 15), s)
    s -= delta
    stocks[product_name] = s
    return s, delta


def returns(order_id: int) -> Tuple[int, int]:
    product_name = orders[order_id]['product_name']
    s = stocks[product_name]
    delta = orders[order_id]['qty']
    s += delta
    return s, delta


def deliveries(product_name: str) -> int:
    s = stocks[product_name]
    s += randint(5, 100)
    stocks[product_name] = s
    return s


def time(ts):
    return ts + timedelta(minutes=randint(1, 15))


start_date = datetime(2021, 7, 19, 8)
end_date = datetime(2021, 7, 25, 22)

script = """
create table products (
    product text,
    price numeric,
    constraint pk_products primary key (product)
);

create table stocks (
    product text,
    stock numeric,
    ts timestamp,
    constraint pk_stocks primary key (product, ts)
);

create table orders (
    order_id text,
    product text,
    qty numeric,
    ts timestamp,
    constraint pk_orders primary key (order_id)
);

create table orders_history (
    order_id text,
    status text,
    ts timestamp,
    constraint pk_orders_history primary key (order_id, ts)
);
"""

insert_product_template = (
    "\ninsert into products (product, price)"
    + " values ('{product}', {price});"
)

insert_stock_template = (
    "\ninsert into stocks (product, stock, ts)"
    + " values ('{product}', {stock}, '{ts}'::timestamp);"
)

insert_order_template = (
    "\ninsert into orders (order_id, product, qty, ts)"
    + " values ('{order_id}', '{product}', {qty}, '{ts}'::timestamp);"
)

insert_order_history_template = (
    "\ninsert into orders_history (order_id, status, ts)"
    + " values ('{order_id}', '{status}', '{ts}'::timestamp);"
)

if __name__ == '__main__':
    for product_name, price in products:
        script += insert_product_template.format(
            product=product_name,
            price=price
        )

        script += insert_stock_template.format(
            product=product_name,
            stock=stocks[product_name],
            ts=start_date
        )

    start_date = time(start_date)

    while start_date < end_date:

        if start_date.hour > 22:
            start_date += timedelta(hours=10)

        else:
            start_date = time(start_date)

        if orders:
            if random() < 0.1:
                order_id = choice(list(orders.keys()))
                s, delta = returns(order_id)
                product_name = orders[order_id]['product_name']
                del orders[order_id]

                script += insert_order_history_template.format(
                    order_id=order_id,
                    status='CANCELLED',
                    ts=shift(start_date)
                )

                script += insert_stock_template.format(
                    product=product_name,
                    stock=s,
                    ts=start_date
                )

                continue

            delete_order_id = None
            for order_id in orders:
                interval_hours = (
                    (start_date - orders[order_id]['ts'])
                    .total_seconds() // 3600
                )

                if random() < interval_hours / 72:
                    delete_order_id = order_id

                    script += insert_order_history_template.format(
                        order_id=order_id,
                        status='COMPLETED',
                        ts=start_date
                    )

                    break

            if delete_order_id is not None:
                del orders[delete_order_id]
                continue

        product_name = product()
        s = stocks[product_name]
        if stocks[product_name] == 0:
            if random() < 0.33:
                s = deliveries(product_name)

            else:
                continue

        else:
            if random() < 0.1:
                s = deliveries(product_name)

            else:
                if random() < 0.5:
                    order_id = generate_order_id(start_date)
                    s, delta = sales(product_name)
                    ts = shift(start_date)

                    orders[order_id] = {
                        'product_name': product_name,
                        'qty': delta,
                        'ts': ts
                    }

                    script += insert_order_template.format(
                        order_id=order_id,
                        product=product_name,
                        qty=delta,
                        ts=ts
                    )

                    script += insert_order_history_template.format(
                        order_id=order_id,
                        status='CREATED',
                        ts=ts
                    )

                else:
                    s, delta = sales(product_name)

        script += insert_stock_template.format(
            product=product_name,
            stock=s,
            ts=start_date
        )

    with open('scripts/stocks.sql', 'w', encoding='utf-8') as f:
        f.write(script)
