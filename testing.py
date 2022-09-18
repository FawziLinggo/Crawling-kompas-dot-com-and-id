test = 'https://megapolitan.ayu.com/read/2022/09/18/11494351/2-stasiun-pengisian-kendaraan-listrik-umum-akan-dibangun-di-terminal'

check_link = test.split('.')
if "kompas" in check_link:
    print("cool")
    print(test)
else:
    print("err")