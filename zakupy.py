import sys
import csv
from itertools import groupby
from collections import defaultdict
from argparse import ArgumentParser


class Product:

    def __init__(self, name, day, amount):
        self.name = name
        self.day = day
        self.amount = amount

    def __str__(self):
        return "<{} {} - {}>".format(self.name, self.amount, self.day)

    __repr__ = __str__


class ShoppingList:
    days = ['nd', 'pon', 'wt', 'sr', 'czw', 'pt', 'sob']

    def __init__(self, products):
        self.products = products

    def pprint_for_days(self, days):
        products = [p for p in self.products if p.day in days]
        return self.pprint(products)

    def pprint(self, products=None):
        if products is None:
            products = self.products

        key = lambda p: p.name
        for name, objs in groupby(sorted(products, key=key), key=key):
            days = defaultdict(int)
            amount = 0
            info = ""
            for prod in objs:
                days[prod.day] += prod.amount
                amount += prod.amount

            for day, day_amount in sorted(
                    days.items(), key=lambda d: self.days.index(d[0])):
                info += "{} ({}), ".format(day, day_amount)

            print(name, '\t', amount, '\t', info)

    @classmethod
    def from_csv(cls, path):
        current_day = None
        products_objs = []
        with open(path) as f:
            reader = csv.reader(f)
            for products, volumes in reader:
                for prod, vol in zip(products.split('\n'), volumes.split('\n')):
                    key = prod.strip().lower()
                    vol = vol.strip().lower()
                    if key in cls.days:
                        current_day = key
                        continue
                    try:
                        amount = int(vol)
                    except ValueError:
                        if 'ml' in vol:
                            amount = int(vol.split()[0])
                        else:
                            amount = 0
                    products_objs.append(
                        Product(key, current_day, amount))

        return cls(products_objs)

def main(argv):
    parser = ArgumentParser()
    parser.add_argument('csv_path', type=str)
    parser.add_argument('days', type=str, nargs='*', help='like pon wt sr etc')
    args = parser.parse_args()
    slist = ShoppingList.from_csv(args.csv_path)
    if args.days:
        slist.pprint_for_days(args.days)
    else:
        slist.pprint()


if __name__ == '__main__':
    main(sys.argv[1:])
