import requests
from bs4 import BeautifulSoup
kompas = requests.get('https://www.kompas.com/')
beautify = BeautifulSoup(kompas.content, "html.parser")
berita = beautify.find_all('h3', {'article__title article__title--medium'})

def save_to_txt(judul,link, i):
    with open('url[' + str(i) + '].txt', 'a') as f:
        f.write('\n')
        f.write(str("Judul : " + judul))
        f.write('\n')
        f.write(str("Link: " + link))

jumlah_file = 1
second=0
contents = []
for each in berita:
    link = each.a.get('href')
    requests_link = requests.get(link)
    beautify = BeautifulSoup(requests_link.content, "html.parser")
    judul = beautify.find('title').text

    save_to_txt(judul,link,jumlah_file)
    print(f"waiting : {len(berita)-second:d} more links in progress ")
    second+=1

print("Program Succes")

