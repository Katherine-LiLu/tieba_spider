# 百度贴吧爬虫

## 用法
`
#爬取帖子
python3 tieba_spider_to_xlsx.py 柯南 kenan 100
#整合成一个文件
python3 each_xlsx_to_one.py kenan
`

## 参数
|argv[1]|argv[2]|argv[3]|
|-------|-------|-------|
|贴吧名字|保存路径|每贴的页数限制|

## 数据
爬取min(pages,200)页帖子，每一贴保存成一个xlsx，按帖子内容、楼层与时间戳、用户名保存
