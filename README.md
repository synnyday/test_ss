# test_ss
SiteSecure test assignment

Task
-----------
Есть ресурс virustotal, у него есть APIv2. 
Нужно написать пример, который на вход принимает список сайтов, проходит список, 
по каждому сайту отправляет запрос в virustotal, парсит ответ и выводит в итоге список сайтов, у которых вердикт фишинг

Requirements
-----------
* django >= 1.9
* python >= 2.7.3

Usage
-----
* Проверка сайтов, указанных в файле
```
./manage.py check_urls --file ./test_ss/test_file_with_urls
```
* Проверка сайтов, указанных в командной строке
```
./manage.py check_urls --urls http://www.stellarium.org,http://icloud-iosid.win/
```
* Проверка сайтов, указанных в списке
```
./manage.py check_urls
```
* Вызов справки:
```
./manage.py check_urls --help
```

Result
-----------
Данные выводятся в командную строку в виде списка
```
Start to retrieving URLs scan reports
Phishing sites:
http://cheshtainfotech.com/site.html
```
Лог приложения, указан в настройках проекта:
`/tmp/test_ss_debug.log`