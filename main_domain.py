import sys
from time import time
import requests
from bs4 import BeautifulSoup
import mysql.connector
from jproperties import Properties

configs = Properties()
with open('config.properties', 'rb') as config_file:
    configs.load(config_file)

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

add_news = ("INSERT INTO " + configs.get('name_table_db').data +
            "(nomor, url, judul, penulis, waktu_publish,isi_berita) "
            "VALUES (%s, %s, %s, %s, %s, %s )")


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
        data_news = (
        str(nomor_db_terakhir), link, judul__, penulisberita, str(waktu_publish), '1 menit baca', str(baca).strip())

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


def get_link_compas(array_link, link_halaman_n, duplicate_link):
    for link in array_link:
        check_link = link.split('.')
        if "kompas" in check_link:
            kompas_artikel_link = requests.get(link)
            beautify_kompas_artikel_link = BeautifulSoup(kompas_artikel_link.content, "html.parser")
            crawl_berita = beautify_kompas_artikel_link.find_all('h3', {'article__title article__title--medium'})
            for looping_link in crawl_berita:
                link = looping_link.a.get('href')
                link_halaman_n.append(link)
        else:
            print("ini bukan link kompas ya ges ya : " + link)

    for item in link_halaman_n:
        if not item in duplicate_link:
            duplicate_link.append(item)
            print(item)


# kompas_domain_com = requests.get(configs.get('url').data)
# beautify = BeautifulSoup(kompas_domain_com.content, "html.parser")
# berita = beautify.find_all('h3', {'article__title article__title--medium'})
#
# # Check if the link is available? otherwise, the program is forced to stop
# if berita == []:
#     print("Link Error : " + configs.get('url').data)
#     print("Program Stop")
#     sys.exit()
link_utama = []
kompas_domain_com = requests.get('https://www.kompas.com/')
beautify = BeautifulSoup(kompas_domain_com.content, "html.parser")
berita = beautify.find_all('ul', {'discover__menu'})
for each in berita:
    ulList = each.find_all('a', href=True)
    for a in ulList:
        # print(a.get('href'))
        link_utama.append(a.get('href'))

# Remove Index 0 as : www.kompas.com
del link_utama[0]

link_crawling = []
link_crawling_error = []
for link_each in link_utama:
    kompas_subdomain_com = requests.get(link_each)
    beautify = BeautifulSoup(kompas_subdomain_com.content, "html.parser")
    berita = beautify.find_all('h3', {'article__title article__title--medium'})
    # Check if the link is available? otherwise, the program is forced to stop
    if berita == []:
        link_crawling_error.append(link_each)
    for each in berita:
        link = each.a.get('href')
        link_crawling.append(link)

# Get artikel in page home
# for each in link_crawling:
#     link = each.a.get('href')
#     link_halamanutama.append(link)
#
# print(link_halamanutama)

#### Crawling 20 Link
time1 = time()
link_halamanutama_duplicate_1 = []
link_halamanutama_duplicate_2 = []
link_halamanutama_duplicate_3 = []
check_duplicat_link = []
get_link_compas(link_crawling, link_halamanutama_duplicate_1, check_duplicat_link)
print("looping 1x : %d" % len(link_halamanutama_duplicate_1))
get_link_compas(link_halamanutama_duplicate_1, link_halamanutama_duplicate_2, check_duplicat_link)
print("looping 2x : %d" % len(link_halamanutama_duplicate_2))
get_link_compas(check_duplicat_link, link_halamanutama_duplicate_3, check_duplicat_link)
print("looping 3x : %d" % len(link_halamanutama_duplicate_3))
# print(len(check_duplicat_link))
time2 = time()
time_calculation = time2 - time1
print("lama waktu: %d" % time_calculation)

# Array save to file
# Array = numpy.array(check_duplicat_link)
# file = open("file1.txt", "w+")
# content = str(Array)
# file.write(content)
# file.close()

# for link in link_halamanutama:
#     check_link = link.split('.')
#     if "kompas" in check_link:
#         kompas_artikel_link = requests.get(link)
#         beautify_kompas_artikel_link = BeautifulSoup(kompas_artikel_link.content, "html.parser")
#         crawl_berita = beautify_kompas_artikel_link.find_all('h3', {'article__title article__title--medium'})
#         for looping_link in crawl_berita:
#             link = looping_link.a.get('href')
#             link_halamanutama_kedua.append(link)
#     else:
#         print("ini bukan link kompas ya ges ya : " + link)
#
# check_duplicat_link_halaman_keuda=[]
# for item_2 in link_halamanutama_kedua:
#     if not item_2 in check_duplicat_link_halaman_keuda:
#         check_duplicat_link_halaman_keuda.append(item_2)
#
# print("Link duplicate (halaman_kedua): %d" %len(link_halamanutama_kedua))
# print("Link tidak duplicate (halaman_kedua) : %d"  %len(check_duplicat_link_halaman_keuda))
#
# #### Crawling 400 Link
# link_halamanutama_ketiga=[]
# link_halamanutama_ketiga.append(check_duplicat_link_halaman_keuda)
# for link in check_duplicat_link_halaman_keuda:
#     check_link = link.split('.')
#     if "kompas" in check_link:
#         kompas_artikel_link = requests.get(link)
#         beautify_kompas_artikel_link = BeautifulSoup(kompas_artikel_link.content, "html.parser")
#         crawl_berita = beautify_kompas_artikel_link.find_all('h3', {'article__title article__title--medium'})
#         for looping_link in crawl_berita:
#             link = looping_link.a.get('href')
#             link_halamanutama_ketiga.append(link)
#     else:
#         print("ini bukan link kompas : " + link)
#
# check_duplicat_link_halaman_ketiga=[]
# for item_3 in link_halamanutama_ketiga:
#     if not item_3 in check_duplicat_link_halaman_ketiga:
#         check_duplicat_link_halaman_ketiga.append(item_3)
#
# print("Link duplicate (halaman_kedua): %d" %len(link_halamanutama_ketiga))
# print("Link tidak duplicate (halaman_kedua) : %d"  %len(check_duplicat_link_halaman_ketiga))
#
#
#
# print("Program Close")
# print(len(link_halamanutama_ketiga))
cursor.close()
db.close()
