import requests
import pandas as pd
from bs4 import BeautifulSoup

URL = "https://kreyol.com/dictionary/"
pages = ["Aa.html", "Bb.html", "Cc.html", "Dd.html", "Ee.html", 
        "Ff.html", "Gg.html", "Hh.html", "Ii.html", "Jj.html", 
        "Kk.html","Ll.html", "Mm.html", "Nn.html", "Oo.html",
        "Pp.html", "Qq.html", "Rr.html", "Ss.html", "Tt.html"
        "Uu.html", "Vv.html", "Ww.html", "Xx.html", "Yy.html",
        "Zz.html"]



x = URL + pages[0]
print(x)
page = requests.get(URL + pages[0])
# print(page.text)

soup = BeautifulSoup(page.content, "html.parser")

y = soup.find_all("p")
# print(y)
words = []
count = 0
for element in y:
    # print(type(element))
    # print(type(element.text))
    if "/" in element.text and "href" not in element.text:
        # print(count, "-", element)
        words.append(element.text)
    count += 1

print(words[0])
print(len(words))

a = words[0].split("\n")
print(ord(a[0]))
# print(a)