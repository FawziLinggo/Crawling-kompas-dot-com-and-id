import sys

import requests
from bs4 import BeautifulSoup
import mysql.connector
from jproperties import Properties

configs = Properties()
with open('config.properties', 'rb') as config_file:
    configs.load(config_file)
kompas_domain_com = requests.get(configs.get('url').data)
beautify = BeautifulSoup(kompas_domain_com.content, "html.parser")
berita = beautify.find_all('h3', {'article__title article__title--medium'})

# Check if the link is available? otherwise, the program is forced to stop
if berita == []:
    print("Link Error : " + configs.get('url').data)
    print("Program Stop")
    sys.exit()



judul_halamanutama = []
link_halamanutama = []
total_artikel = 0

db = mysql.connector.connect(user=configs.get('user_db').data,
                             database=configs.get('database').data,
                             host=configs.get('hostname_db').data,
                             port=configs.get('port_db').data,
                             password=configs.get('password').data)
cursor = db.cursor()

######### Count databases #########
count_ = "SELECT COUNT(*) FROM " + configs.get('name_table_db').data
cursor.execute(count_)
nomor_db_terakhir = cursor.fetchone()[0]
nomor_db_terakhir = nomor_db_terakhir + 1
file_ke = nomor_db_terakhir
####################################

add_news = ("INSERT INTO "+configs.get('name_table_db').data +
            "(nomor, url, judul, penulis, waktu_publish,baca,isi_berita) "
            "VALUES (%s, %s, %s, %s, %s, %s , %s)")


def judul_berita_function(judul):
    judul_string = str(judul)
    judulberita = BeautifulSoup(judul_string, "html.parser")
    print(judulberita)


def penulis_berita_function(penulis):
    penulis_string = str(penulis)
    penulisberita = BeautifulSoup(penulis_string, "html.parser").find('a', href=True).contents[0]
    print("Penulis Berita : " + str(penulisberita))


# FIX ME :(
def kompas_domain_id(beautify):
    print("\n=========  WWW.KOMPAS.ID =========  ")
    try:
        judul = beautify.find('h1', {'class', 'ksm-2Y3 ksm-15b'})
        penulis = beautify.find('div', {'class', 'ksm-1w7 ksm-sDo'})
        waktu = beautify.find('div', {'class', 'flex items-center mb-1 md:mb-0 text-sm text-grey-50'})
        baca = beautify.find('span', {'class', 'font-pt-sans'})
        isi = beautify.find_all('p', {'class', 'ksm-GMg ksm-2BC'})
        print("Judul : " + judul.get_text())
        print("Tanggal Artikel : " + waktu.get_text())
        print("Link Artikel : " + link)
        print("Penulis Artikel : " + penulis.get_text())
        print("Isi berita : " + str(isi))
        print("=====================================")
    except:
        judul = 'error'
        penulis = 'error'
        waktu = 'error'
        isi = 'error'

        print("Judul : " + judul)
        print("Tanggal Artikel : " + waktu)
        print("Link Artikel : " + link)
        print("Penulis Artikel : " + penulis)
        print("Isi berita : " + str(isi))
        print("=====================================")


def berita2(link, nomor_db_terakhir):
    try:
        kompas_berita_link = requests.get(link)
        beautify_berita = BeautifulSoup(kompas_berita_link.content, "html.parser")

        content = []
        # try:
        judul__ = beautify_berita.find('a', {'class', 'article__link'}).text

        penulis_ = beautify_berita.find('div', {'class': 'read__credit__item'})
        waktu_publish = beautify_berita.find('meta', attrs={'name': 'content_PublishedDate'}).get('content')
        baca = (beautify_berita.find('div', {'class', 'read__content'}).get_text())

        print("\n=========  WWW.KOMPAS.COM =========  ")
        print("Judul : " + judul__)
        print("Tanggal Artikel : " + waktu_publish)
        print("Link Artikel : " + link)
        penulis_berita_function(penulis_)
        print("Isi berita : " + baca)
        print("=====================================")

        penulis_string = str(penulis_)
        penulisberita = BeautifulSoup(penulis_string, "html.parser").find('a', href=True).contents[0]
        data_news = (str(nomor_db_terakhir), link, judul__, penulisberita, str(waktu_publish), '1 menit baca', str(baca).strip())

        # insertion
        cursor.execute(add_news, data_news)
        db.commit()

        content.append(str(judul__))
        content.append(str(waktu_publish))
        content.append(str(link))
        content.append(str(penulis_.text))
        content.append(str(baca))
        with open('konten[' + str(file_ke) + '].txt', 'a') as f:
            f.write('\n'.join(content))
        content.clear()
    except:
        print("==================  ERROR =====================")
        print("The Kompas.id crawl program is not finished yet")

        # FIX ME :(
        # beautify_berita = BeautifulSoup(kompas_berita_link.content, "html.parser")
        # kompas_domain_id(beautify_berita)



def save_to_txt(content, i):
    with open('konten[' + str(i) + '].txt', 'a') as f:
        f.write('\n'.join(content))


# Get artikel in page home
for each in berita:
    link = each.a.get('href')
    judul = each.find('a', {'class', 'article__link'}).text
    judul_halamanutama.append(judul)
    link_halamanutama.append(link)

print(link_halamanutama)

#### Crawling 20 Link
link_halamanutama_kedua=[]
for link in link_halamanutama:
    file_ke = file_ke + 1
    nomor_db_terakhir = nomor_db_terakhir + 1
    check_link = link.split('.')
    if "kompas" in check_link:
        kompas_artikel_link = requests.get(link)
        beautify_kompas_artikel_link = BeautifulSoup(kompas_artikel_link.content, "html.parser")
        crawl_berita = beautify_kompas_artikel_link.find('h3', {'article__title article__title--medium'})
        berita2(link, nomor_db_terakhir)
        total_artikel += 1

        crawl_berita_link_array=beautify_kompas_artikel_link.find_all('h3', {'article__title article__title--medium'})

        # 1 link x 20 artikel (link)
        for looping_link in crawl_berita_link_array:
            link = looping_link.a.get('href')
            link_halamanutama_kedua.append(link)
    else:
        print("ini bukan link kompas ya ges ya : " + link)

#### Crawling 400 Link
link_halamanutama_ketiga=[]
for link in link_halamanutama_kedua:
    file_ke = file_ke + 1
    nomor_db_terakhir = nomor_db_terakhir + 1
    check_link = link.split('.')
    if "kompas" in check_link:
        kompas_artikel_link = requests.get(link)
        beautify_kompas_artikel_link = BeautifulSoup(kompas_artikel_link.content, "html.parser")
        crawl_berita = beautify_kompas_artikel_link.find('h3', {'article__title article__title--medium'})
        berita2(link, nomor_db_terakhir)
        total_artikel += 1

        crawl_berita_link_array=beautify_kompas_artikel_link.find_all('h3', {'article__title article__title--medium'})

        # 1 link x 20 artikel (link)
        for looping_link in crawl_berita_link_array:
            link = looping_link.a.get('href')
            link_halamanutama_ketiga.append(link)
    else:
        print("ini bukan link kompas ya ges ya : " + link)

print("Program Close")
print(len(link_halamanutama_ketiga))
cursor.close()
db.close()
