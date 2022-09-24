import requests
from bs4 import BeautifulSoup

# test = 'https://megapolitan.ayu.com/read/2022/09/18/11494351/2-stasiun-pengisian-kendaraan-listrik-umum-akan-dibangun-di-terminal'
#
# check_link = test.split('.')
# if "kompas" in check_link:
#     print("cool")
#     print(test)
# else:
#     print("err")


kompas_domain_com = requests.get(
    'https://www.kompas.com/edu/read/2022/09/22/114238371/ruu-sisdiknas-tak-masuk-prolegnas-nadiem-yang-penting-hati-tulus-kinerja')
beautify = BeautifulSoup(kompas_domain_com.content, "html.parser")
# print(beautify.find('div', {'class', 'read__time'}).contents[1].text)
print(beautify.find('meta',attrs={'name':'content_PublishedDate'}).get('content'))