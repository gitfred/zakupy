import sys
import csv
from collections import defaultdict


def parse_csv(path):
    with open(path) as f:
        reader = csv.reader(f)
        data = defaultdict(int)
        for products, volumes in reader:
            for prod, vol in zip(products.split('\n'), volumes.split('\n')):
                key = prod.strip().lower()
                try:
                    data[key] += int(vol)
                except ValueError:
                    data[key] += 0

    return data


def main(args):
    data = parse_csv(args[0])
    for product, volume in sorted(data.items()):
        print "{}: {}g".format(product, volume)


if __name__ == '__main__':
    main(args=sys.argv[1:])