import mysql.connector
from jproperties import Properties

configs = Properties()
with open('config.properties', 'rb') as config_file:
    configs.load(config_file)

link='https://www.kompas.id/baca/ekonomi/2022/06/29/pedagang-donggala-jual-minyak-goreng-curah-pakai-botol-plastik'
judul='Pedagang Donggala Jual Minyak Goreng Curah Pakai Botol Plastik'
penulis='Hendriyo Widi'
date='2022-06-29 16:50:08'
isi='1 menit baca'
berita='AKARTA, KOMPAS — Pedagang Pasar Toaya, Kabupaten Donggala, Sulawesi Tengah, menjual minyak goreng curah memakai kemasan botol plastik. '

db = mysql.connector.connect(user=configs.get('user_db').data,
                             database=configs.get('database').data,
                             host=configs.get('hostname_db').data,
                             port=configs.get('port_db').data,
                             password=configs.get('password').data)

cursor = db.cursor()

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

print(configs.get('url').data)