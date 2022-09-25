import json

import requests
from bs4 import BeautifulSoup
from jproperties import Properties

configs = Properties()
with open('config.properties', 'rb') as config_file:
    configs.load(config_file)

# link='https://www.kompas.id/baca/ekonomi/2022/06/29/pedagang-donggala-jual-minyak-goreng-curah-pakai-botol-plastik'
# judul='Pedagang Donggala Jual Minyak Goreng Curah Pakai Botol Plastik'
# penulis='Hendriyo Widi'
# date='2022-06-29 16:50:08'
# isi='1 menit baca'
# berita='AKARTA, KOMPAS — Pedagang Pasar Toaya, Kabupaten Donggala, Sulawesi Tengah, menjual minyak goreng curah memakai kemasan botol plastik. '

# db = mysql.connector.connect(user=configs.get('user_db').data,
#                              database=configs.get('database').data,
#                              host=configs.get('hostname_db').data,
#                              port=configs.get('port_db').data,
#                              password=configs.get('password').data)
#
# cursor = db.cursor()

# add_news = ("INSERT INTO " + configs.get('name_table_db').data
#             "(nomor, url, judul, penulis, waktu_publish,baca,isi_berita) "
#                 "VALUES (%s, %s, %s, %s, %s, %s , %s)"
#             )
#
# number=1141
# data_news = (str(number), link, judul, penulis, date, isi, berita)
# #insertion
# cursor.execute(add_news,data_news)
#
# db.commit()

# count_ ="SELECT COUNT(*) FROM " + + configs.get('name_table_db').data
# cursor.execute(count_)
# number_row=cursor.fetchone()
# print(number_row[0])

# print(configs.get('url').data)

# myarray=['aba','bac','koni']
# k = ['aba','bac']
# for item in myarray:
#     if not item in k:
#         print("Item is in array already.")
#         k.append(item)
#
# print(k)

# TEMPLATE
# for link in check_duplicat_link_halaman_keuda:
#     check_link = link.split('.')
#     if "kompas" in check_link:
#         kompas_artikel_link = requests.get(link)
#         beautify_kompas_artikel_link = BeautifulSoup(kompas_artikel_link.content, "html.parser")
#         crawl_berita = beautify_kompas_artikel_link.find('h3', {'article__title article__title--medium'})
#         # berita2(link, nomor_db_terakhir)
#         crawl_berita_link_array=beautify_kompas_artikel_link.find_all('h3', {'article__title article__title--medium'})
#
#         # 1 link x 20 artikel (link)
#         for looping_link in crawl_berita_link_array:
#             link = looping_link.a.get('href')
#             link_halamanutama_ketiga.append(link)
#     else:
#         print("ini bukan link kompas ya ges ya : " + link)
# link_utama=[]
# kompas_domain_com = requests.get('https://bola.kompas.com/search/2022-09-14')
# beautify = BeautifulSoup(kompas_domain_com.content, "html.parser")
# berita = beautify.find_all('ul', {'discover__menu'})
# for each in berita:
#     ulList = each.find_all('a',href=True)
#     for a in ulList:
#         # print(a.get('href'))
#         link_utama.append(a.get('href'))
#
# # Remove Index 0 as : www.kompas.com
# del link_utama[0]
#
#
# link_crawling=[]
# link_crawling_error=[]
# for link_each in link_utama:
#     kompas_subdomain_com=requests.get(link_each)
#     beautify = BeautifulSoup(kompas_subdomain_com.content, "html.parser")
#     berita = beautify.find_all('h3', {'article__title article__title--medium'})
#     # Check if the link is available? otherwise, the program is forced to stop
#     if berita == []:
#         link_crawling_error.append(link_each)
#     for each in berita:
#         link = each.a.get('href')
#         link_crawling.append(link)
#
# print(len(link_crawling))
# print(link_crawling_error)

# berita_array=[]
# # mean 01 - 12
# bulan = '01'
# # range tanggal 1 - 28
# for tanggal in range(28):
#     tanggal += 1
#     for pages in range (10):
#         pages += 1
#         url='https://bola.kompas.com/search/2022-'+bulan+'-'+str(tanggal)+'/'+str(pages)
#         kompas_domain_com = requests.get(url)
#         beautify = BeautifulSoup(kompas_domain_com.content, "html.parser")
#         artikel = beautify.find_all('h3', {'article__title article__title--medium'})
#         if artikel == []:
#             break
#         for each in artikel:
#             link = each.a.get('href')
#             berita_array.append(link)
#
# print('url : %s ' %url )
# print(len(berita_array))
# print(berita_array)

link = 'https://bola.kompas.com/read/2022/08/20/01284768/persita-vs-persikabo-drama-delapan-gol-di-tangerang'
kompas_berita_link = requests.get(link)
beautify_berita = BeautifulSoup(kompas_berita_link.content, "html.parser")

print(beautify_berita.find('title').text)