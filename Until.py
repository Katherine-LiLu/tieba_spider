#  来自Android客户端21楼2020-01-26 07:17
import re

timePattern = '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}'
floorPattern = '[0-9]{1,3}楼'

def getTimeAndFloor(info):
    timeresult = re.search(timePattern, info)
    flooresult = re.search(floorPattern, info)

    timeresult = timeresult.group()
    flooresult = flooresult.group()
    
    if timeresult is None:
        timeresult = ' '
    if flooresult is None:
        flooresult = ' '
    else:
        flooresult = flooresult.replace('楼', '')
    return timeresult, flooresult



if __name__ == "__main__":
    test = '来自Android客户端21楼2020-01-26 07:17'
    print(getTimeAndFloor(test))