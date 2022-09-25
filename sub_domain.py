import sys

import requests
from bs4 import BeautifulSoup
from jproperties import Properties
import mysql.connector

configs = Properties()
with open('config.properties', 'rb') as config_file:
    configs.load(config_file)

link_utama = []
kompas_domain_com = requests.get(configs.get('url').data)
beautify = BeautifulSoup(kompas_domain_com.content, "html.parser")
berita = beautify.find_all('ul', {'discover__menu'})
for each in berita:
    ulList = each.find_all('a', href=True)
    for a in ulList:
        link_utama.append(a.get('href'))

# Remove Index 0 as : www.kompas.com
del link_utama[0]

# remove subdomains that don't have articles
# print(link_utama[0:12])

# Start Crawling since ?
# must String (januari  == '01', Desember ==
# why don't convert to datetime.strptime ? I just implement  KISS principle
# get artikel link since 2022
tahun = '2022'
bulan = '08'
# start from 1 end 28
tanggal_terakhir = '28'

def penulis_berita_function(penulis):
    penulis_string = str(penulis)
    penulisberita = BeautifulSoup(penulis_string, "html.parser").find('a', href=True).contents[0]
    print("Penulis Berita : " + str(penulisberita))


def berita2(link, nomor_db_terakhir):
        kompas_berita_link = requests.get(link)
        beautify_berita = BeautifulSoup(kompas_berita_link.content, "html.parser")

        # try:
        judul__ = beautify_berita.find('title').text

        penulis_ = beautify_berita.find('div', {'class': 'read__credit__item'})
        waktu_publish = beautify_berita.find('meta', attrs={'name': 'content_PublishedDate'}).get('content')
        baca = (beautify_berita.find('div', {'class', 'read__content'}).get_text())

        # print("\n=========  WWW.KOMPAS.COM =========  ")
        # print("Judul : " + judul__)
        # print("Tanggal Artikel : " + waktu_publish)
        # print("Link Artikel : " + link)
        # penulis_berita_function(penulis_)
        # print("Isi berita : " + baca)
        # print("=====================================")

        penulis_string = str(penulis_)
        penulisberita = BeautifulSoup(penulis_string, "html.parser").find('a', href=True).contents[0]
        data_news = (
            str(nomor_db_terakhir), link, judul__, penulisberita, str(waktu_publish), str(baca).strip())

        # insertion
        cursor.execute(add_news, data_news)
        db.commit()

        # To Text
        # content.append(str(judul__))
        # content.append(str(waktu_publish))
        # content.append(str(link))
        # content.append(str(penulis_.text))
        # content.append(str(baca))
        # with open('konten[' + str(file_ke) + '].txt', 'a') as f:
        #     f.write('\n'.join(content))
        # content.clear()
        print('success row : %d' % nomor_db_terakhir)



# print(int(bulan))


configs = Properties()
with open('config.properties', 'rb') as config_file:
    configs.load(config_file)
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
file_ke = nomor_db_terakhir + 1
####################################
add_news = ("INSERT INTO " + configs.get('name_table_db').data +
            "(nomor, url, judul, penulis, waktu_publish,isi_berita) "
            "VALUES (%s, %s, %s, %s, %s, %s )")

print(" Link sub-domain : " + str(link_utama[0:12]))
# print("waiting for the crawl link, it takes about 30 minutes")
artikel_subdomain_kompas_com = []
for sub_domain in link_utama[0:12]:
    for tanggal in range(int(tanggal_terakhir)):
        tanggal += 1
        for pages in range(10):
            pages += 1
            # tanggal start from 1
            url = sub_domain + 'search/' + tahun + '-' + bulan + '-' + str(tanggal) + "/" + str(pages)
            kompas_subdomain_com = requests.get(url)
            beautify = BeautifulSoup(kompas_subdomain_com.content, "html.parser")
            artikel = beautify.find_all('h3', {'article__title article__title--medium'})
            if artikel == []:
                break
            for each in artikel:
                link = each.a.get('href')
                check_link = link.split('.')
                if "kompas" in check_link:
                    kompas_artikel_link = requests.get(link)
                    try:
                        berita2(link, file_ke)
                        file_ke += 1
                    except:
                        print("Failed in row data : %d" % file_ke + ", skip process")
                else:
                    print("this is not a compass link, geez : " + link)
                artikel_subdomain_kompas_com.append(link)

# TEMPLATE
# for link in artikel_subdomain_kompas_com:
#     check_link = link.split('.')
#     if "kompas" in check_link:
#         kompas_artikel_link = requests.get(link)
#         beautify_kompas_artikel_link = BeautifulSoup(kompas_artikel_link.content, "html.parser")
#         crawl_berita = beautify_kompas_artikel_link.find('h3', {'article__title article__title--medium'})
#         berita2(link, nomor_db_terakhir)
#     else:
#         print("ini bukan link kompas ya ges ya : " + link)

print(len(artikel_subdomain_kompas_com))
