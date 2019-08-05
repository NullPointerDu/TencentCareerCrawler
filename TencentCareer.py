import requests
import time


class RequestFailedException(Exception):
    def __init__(self):
        self.args = ('Request Code is not 200',)
        self.message = 'Request Code is not 200'


def getTimeStamp():
    return int(round(time.time() * 1000))

def getMainJSON():
    mainUrl = "https://careers.tencent.com/tencentcareer/api/post/Query"
    pageSize = "10000000"
    params = {
        "timestamp": getTimeStamp(),
        "countryId": "",
        "cityId": "",
        "bgIds": "",
        "productId": "",
        "categoryId": "",
        "parentCategoryId": "",
        "attrId": "",
        "keyword": "",
        "pageIndex": "1",
        "pageSize": pageSize,
        "language": "zh-cn",
        "area": "ca"
    }

    json = requests.get(mainUrl, params=params).json()
    if json['Code'] != 200:
        raise RequestFailedException()
    if len(json['Data']['Posts']) < int(json['Data']['Count']):
        params["pageSize"] = json['Data']['Count']
        json = requests.get(mainUrl, params=params).json()
        if json['Code'] != 200:
            raise RequestFailedException()
    result = []
    for i in json['Data']['Posts']:
        result.append(i['PostId'])
    return result

def getDetails(postId, lang="zh-cn"):
    try:
        url = "https://careers.tencent.com/tencentcareer/api/post/ByPostId"
        params = {
            "timestamp": getTimeStamp(),
            "postId": postId,
            "language": lang
        }

        json = requests.get(url, params=params).json()
        if json['Code'] != 200:
            raise RequestFailedException()
        else:
            info = json['Data']
            return info
    except Exception:
        return None


if __name__ == "__main__":
    jobs = getMainJSON()
    for i in jobs:
        print(getDetails(i))
