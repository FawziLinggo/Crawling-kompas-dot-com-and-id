import requests
from bs4 import BeautifulSoup

url='https://megapolitan.kompas.com/read/2015/09/08/11340571/Alasan.Ahok.Larang.Potong.Hewan.Kurban.di.Sembarang.Tempat'
kompas_berita_link = requests.get(url)
beautify_berita = BeautifulSoup(kompas_berita_link.content, "html.parser")
penulis_ = beautify_berita.find('div', {'class': 'read__credit__item'})
penulis_string = str(penulis_)
penulisberita = BeautifulSoup(penulis_string, "html.parser").find('a', href=True).contents[0]
judul__ = beautify_berita.find('title').text


waktu_publish = beautify_berita.find('meta', attrs={'name': 'content_PublishedDate'}).get('content')
baca = (beautify_berita.find('div', {'class', 'read__content'}).get_text())

print("\n=========  WWW.KOMPAS.COM =========  ")
print("Judul : " + judul__)
print("Penulis : " + penulisberita.text)
print("Tanggal Artikel : " + waktu_publish)
print("Link Artikel : " + url)
print("Isi berita : " + baca)
print("=====================================")

file_ke=1
content=[]
# To Text
content.append(str(judul__))
content.append(str(waktu_publish))
content.append(str(url))
content.append(str(penulisberita.text))
content.append(str(baca))
with open('konten[' + str(file_ke) + '].txt', 'a') as f:
    f.write('\n'.join(content))
content.clear()