import urllib.request, json 
import wikipedia as w
from random import randint
import sys

pages = []
doc_to_download = int(sys.argv[1])


def save_page(page, ID):
    content = page.content
    html = page.html()
    with open("priv/static/documents/contents/" + str(ID) + '.txt', "w+") as text_file:
        text_file.write(content)
    with open("priv/static/documents/htmls/" + str(ID) + '.html', "w+") as text_file:
        text_file.write(html)

count = 0
i = 1

while count < doc_to_download:
    ID = i+10000
    try:
        print('Downloading...' + str(count + 1) + '/' + sys.argv[1])
        page = w.page(pageid=ID, auto_suggest=True, redirect=True)
        save_page(page, ID)
        count += 1
    except Exception as ex:
        print(ex)
        print("this id does not exist (" + str(ID) + ')')
    i += 1

