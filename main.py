import requests
from bs4 import BeautifulSoup


kompas_domain_com=requests.get('https://kompas.com/')
beautify=BeautifulSoup(kompas_domain_com.content, "html.parser" )
berita=beautify.find_all('h3',{'article__title article__title--medium'})

judul_halamanutama=[]
link_halamanutama=[]
total_artikel=0

def judul_berita_function(judul):
    judul_string = str(judul)
    judulberita = BeautifulSoup(judul_string, "html.parser")
    print(judulberita)

def penulis_berita_function(penulis):
    penulis_string = str(penulis)
    penulisberita = BeautifulSoup(penulis_string, "html.parser").find('a', href=True).contents[0]
    print("Penulis Berita : "+ penulisberita)


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
        judul='error'
        penulis='error'
        waktu='error'
        isi='error'

        print("Judul : " + judul)
        print("Tanggal Artikel : " + waktu)
        print("Link Artikel : " + link)
        print("Penulis Artikel : " + penulis)
        print("Isi berita : " + str(isi))
        print("=====================================")

def berita2(link):
    kompas_berita_link = requests.get(link)
    beautify_berita = BeautifulSoup(kompas_berita_link.content, "html.parser")
    try:
        judul__ = beautify_berita.find('a', {'class', 'article__link'}).text

        penulis_ = beautify_berita.find('div', {'class': 'read__credit__item'})
        waktu_publish = beautify_berita.find('div', {'class', 'article__date'}).contents[0].text
        baca = (beautify_berita.find('div', {'class', 'read__content'}).get_text())

        print("\n=========  WWW.KOMPAS.COM =========  ")
        print("Judul : " + judul__)
        print("Tanggal Artikel : " + waktu_publish)
        print("Link Artikel : " + link)
        penulis_berita_function(penulis_)
        print("Isi berita : " + baca)
        print("=====================================")
    except:
        beautify_berita = BeautifulSoup(kompas_berita_link.content, "html.parser")
        kompas_domain_id(beautify_berita)



# Get artikel in page home
for each in berita:
    link=each.a.get('href')
    judul=each.find('a',{'class','article__link'}).text
    judul_halamanutama.append(judul)
    link_halamanutama.append(link)

print(link_halamanutama)
for link in link_halamanutama:
    check_link= link.split('.')
    if "kompas" in check_link:
        kompas_artikel_link = requests.get(link)
        beautify_kompas_artikel_link = BeautifulSoup(kompas_artikel_link.content, "html.parser")
        crawl_berita = beautify_kompas_artikel_link.find('h3', {'article__title article__title--medium'})

        # link_to_db = crawl_berita.a.get('href')
        # judul_to_db = crawl_berita.find('a', {'class', 'article__link'}).text
        berita2(link)
        total_artikel += 1
    else:
        print("ini bukan link kompas ya ges ya : " + link)
    # for looping in crawl_berita:
    #     link_to_db = looping.a.get('href')
    #     judul_to_db = looping.find('a', {'class', 'article__link'}).text
    #     berita2(link_to_db,judul_to_db)
    #     total_artikel+=1

print(total_artikel)