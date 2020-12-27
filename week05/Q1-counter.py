import redis
import sys

client = redis.Redis(host = '127.0.0.1', port = 6379, password = 'testpasswd', decode_responses = True)  

def counter(video_id):
    if isinstance(video_id, int):
        client.incr(video_id)
        count_number = client.get(video_id)
        return count_number
    else:
        sys.exit('Invalid input')


if __name__ == "__main__":
    print(counter(1001))
    print(counter(1001))
    print(counter(1002))
    print(counter(1001))
    print(counter(1002))