# conda create -n banchan python=3.10
# pip install icrawler (0.6.9)
from icrawler.builtin import BingImageCrawler


def icrawler():
    # weathers = ["晴れた", "雨の", "曇りの"]
    times = ["朝", "昼", "夕方", "夜"]
    places = ["高速道路", "田舎", "海沿い", "山道"]
    labels = [time + "の" + place for time in times for place in places]
    print(labels)
    for label in labels:
        path = "./images/" + label
        crawler = BingImageCrawler(storage={"root_dir": path})
        crawler.crawl(keyword=label, max_num=50)
