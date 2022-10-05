class FlatIterator:
    def __init__(self, items: list, depth: int = 1):
        self._items = items
        self._depth = depth

    def __iter__(self):
        self._cursor = 0
        self._nested_iterator = iter([])
        return self

    def __next__(self):
        try:
            return next(self._nested_iterator)
        except StopIteration:
            if self._cursor == len(self._items):
                raise StopIteration
            item = self._items[self._cursor]
            self._cursor += 1
            inf_depth = self._depth == -1
            if isinstance(item, list) and (inf_depth or self._depth):
                self._nested_iterator = iter(FlatIterator(item, depth=-1 if inf_depth else self._depth - 1))
                return next(self._nested_iterator)
            return item


def flat_generator(items: list):
    for item in items:
        if isinstance(item, list):
            yield from item
        else:
            yield item


def deep_flat_generator(item_list: list):
    def recursion(items: list):
        for item in items:
            if isinstance(item, list):
                yield from recursion(item)
            else:
                yield item
    return recursion(item_list)


if __name__ == '__main__':
    nested_list = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None, ['i', 'j', [3, 4, 5]], 'x']
    ]
    result_iterator = list(FlatIterator(nested_list))
    result_generator = list(flat_generator(nested_list))
    assert result_generator == result_iterator
    print(*result_iterator, sep='\n')
    result_deep_iterator = list(FlatIterator(nested_list, depth=-1))
    result_deep_generator = list(deep_flat_generator(nested_list))
    assert result_deep_iterator == result_deep_generator
