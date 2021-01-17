def mapper(func, *sequences):
    if not sequences:
        raise TypeError('Mapper should have at least two parameters')
    iters = [iter(seq) for seq in sequences]
    while True:
        yield func(*[next(it) for it in iters])


def testFunc(n):
    return n * 10


if __name__ == "__main__":
    my_list = [x for x in range(4)]
    list_mapper = mapper(testFunc, my_list)
    
