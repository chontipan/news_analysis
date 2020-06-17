import csv
import requests
from bs4 import BeautifulSoup
import datetime

list_news = []
#row = {}
categories = {
    "sports": "Sports",
    "politics": "Politics",
    "cross-strait": "Cross-Strait",
    "business": "Business",
    "society": "Society",   
    "sci-tech": "Science & Tech",
    "culture": "Culture"

}
#categories = ["Politics", "Cross-Strait",
#              "Business", "Society", "Sports", "Science & Tech", "Culture"]

print("crawing")


for c in categories:
    print(c)
    for m in range(3, 7):
        print(m)
        for d in range(1, 32):
            if(m == 4 and d == 31):
                continue
            if(m == 6 and d >= 7):
                continue
            print(d)
            for p in range(1, 10000):

                date = "2020"+"{:02n}".format(m)+"{:02n}".format(d)
                page = date+"{:04n}".format(p)
                url = "https://focustaiwan.tw/"+c+"/"+page
                page = requests.get(url).text
                soup = BeautifulSoup(page, "lxml")

                if(soup.findAll("div", {"class": "face404"})):
                    continue
                else:
                    text = " ".join([p.text for p in soup.find_all("p")])
                    title = soup.find("span", {"class": "h1t"}).text
                    category = soup.find("a", {"class": "cate-col"}).text
                    #print(categories[c])
                    #print(category)
                    if(category == categories[c] and title != "Taiwan headline news"):
                        #print(category)
                        #print(url)
                        row = {}
                        row["date_mmddyy"] = str(m)+"/"+str(d)+"/2020"
                        row["date_ddmmyy"] = str(d)+"/"+str(m)+"/2020"
                        row["title"] = title
                        row["content"] = text
                        row["url"] = url
                        row["source"] = "focustaiwan"
                        row["section"] = categories[c]
                        list_news.append(row)
                    else:
                        continue

print(len(list_news))
#save to csv
csv_columns = ['date_mmddyy', 'date_ddmmyy', 'title',
               'content', 'url', 'source', 'section']
csv_file = "news_focustaiwan_updated.csv"
print("save to csv")
try:
    with open(csv_file, 'w', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=csv_columns, lineterminator='\n')
        writer.writeheader()
        for data in list_news:
            writer.writerow(data)
except IOError:
    print("I/O error")

print("done")

