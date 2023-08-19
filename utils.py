import csv


def books_generator(batch_size=100):
    lines = list()
    with open('books.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter=',')
        line = next(reader)
        count = 0
        while line:
            lines.append(line)
            line = next(reader)
            count += 1
            if count == batch_size:
                yield lines
                count = 0
                lines = list()


def to_dict(book, exclude_attrs=['_sa_instance_state']):
    _dict = book.__dict__.copy()

    for attr in exclude_attrs:
        _dict.pop(attr, None)

    return _dict
