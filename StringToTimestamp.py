from datetime import datetime

string_date='23/09/2022, 22:31 WIB'
string_date=string_date[0:6]+string_date[8:10]+string_date[11:17]+':00'
datetime_object = datetime.strptime(string_date, '%d/%m/%y %H:%M:%S')
print(datetime_object)
