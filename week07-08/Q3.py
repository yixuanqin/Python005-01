from functools import wraps
import time


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            _duration = round(time.time() - start, 6)
            print(f"Total execution time: {_duration if _duration > 0 else 0} s")
    return wrapper

@timer
def count_sum(input_list):
    sum = 0
    for item in input_list:
        sum += item
        time.sleep(1)
    return sum

@timer
def display_item(input_list):
    for item in input_list:
        print(item)
        time.sleep(1)


if __name__ == "__main__":
    input_list = [x * 10 for x in range(5)]
    print(count_sum(input_list))
    display_item(input_list)