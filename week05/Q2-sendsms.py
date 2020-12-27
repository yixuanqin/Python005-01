import re
import redis
import sys
import time
from datetime import timedelta

client = redis.Redis(host = '127.0.0.1', port = 6379, password = 'testpasswd', decode_responses = True)  

def cut(src_string):
    sub_string_len = round(1/2 * len(src_string))
    raw_list = [src_string[i:i + sub_string_len] for i in range(0, len(src_string), sub_string_len)]
    if len(raw_list) > 2:
        result = []
        result.append(raw_list[0])
        result.append("".join(raw_list[1:]))
    else:
        result = raw_list
    return result

def sendsms(telephone_number, content, key = None, limit = 5, period = timedelta(seconds = 60)):
    if not telephone_number or not re.match(r'^\d{11}$', str(telephone_number)):
        sys.exit("Invalid mobile phone number: {}".format(telephone_number))
    if client.setnx(telephone_number, limit):
            client.expire(telephone_number, int(period.total_seconds()))
    bucket_value = client.get(telephone_number)
    if bucket_value and int(bucket_value) > 0:
        client.decrby(telephone_number, 1)
        if len(str(content)) > 70:
            content_list = cut(content)
            for sub_content in content_list:
                    print("发送成功: {}".format(sub_content))
        else:
                print("发送成功: {}".format(content))
    else:
        print("1分钟内发送次数超过5次, 请等待1分钟")


if __name__ == "__main__":
    sendsms(12345654321, content = "Send to phone1: hello world") 
    time.sleep(1)
    sendsms(12345654321, content = "Send to phone1: 青天有月来几时？我今停杯一问之。人攀明月不可得，月行却与人相随。皎如飞镜临丹阙。绿烟灭尽清辉发。但见宵从海上来，宁知晓向云间没？白兔捣药秋复春，嫦娥孤栖与谁邻？")
    time.sleep(1)
    sendsms(12345654321, content = "Send to phone1: 青天有月来几时？我今停杯一问之。人攀明月不可得，月行却与人相随。皎如飞镜临丹阙。绿烟灭尽清辉发。但见宵从海上来，宁知晓向云间没？白兔捣药秋复春，嫦娥孤栖与谁邻？")
    time.sleep(1)
    sendsms(12345654321, content = "Send to phone1: 青天有月来几时？我今停杯一问之。人攀明月不可得，月行却与人相随。皎如飞镜临丹阙。绿烟灭尽清辉发。但见宵从海上来，宁知晓向云间没？白兔捣药秋复春，嫦娥孤栖与谁邻？")
    time.sleep(1)
    sendsms(12345654321, content = "Send to phone1: 青天有月来几时？我今停杯一问之。人攀明月不可得，月行却与人相随。皎如飞镜临丹阙。绿烟灭尽清辉发。但见宵从海上来，宁知晓向云间没？白兔捣药秋复春，嫦娥孤栖与谁邻？")
    time.sleep(1) 
    sendsms(88887777666, content = "Send to phone2: OK") 
    time.sleep(1)
    sendsms(12345654321, content = "Send to phone1: 青天有月来几时？我今停杯一问之。人攀明月不可得，月行却与人相随。皎如飞镜临丹阙。绿烟灭尽清辉发。但见宵从海上来，宁知晓向云间没？白兔捣药秋复春，嫦娥孤栖与谁邻？")
    time.sleep(30) 
    sendsms(88887777666, content = "Send to phone2: OK") 
    time.sleep(1)
    sendsms(12345654321, content = "Send to phone1: 青天有月来几时？我今停杯一问之。人攀明月不可得，月行却与人相随。皎如飞镜临丹阙。绿烟灭尽清辉发。但见宵从海上来，宁知晓向云间没？白兔捣药秋复春，嫦娥孤栖与谁邻？")
    time.sleep(30) 
    sendsms(12345654321, content = "Send to phone1: OK")