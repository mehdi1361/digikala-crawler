import urllib2
import json
from bs4 import BeautifulSoup
from DataBase import set_product_detail
from DataBase import get_products_id
products = get_products_id()
for product in products:
    print product
    # id_product = 93349
    url = "http://api.digikala.com/JzNMJGUkc7s=/wxzPbOeaJM2f7qjgetwqKg3HONlZKYBT?aqPI=%s&aqIIO=false&aqIP=false" % product
    req = urllib2.Request(url)
    req.add_header('cookie', 'dk-guid=false; DK-Client=FUUU,26694e3c-28c7-4e57-9cb6-8a01fcb54ba7; _AWXR=YWhuZFIxV2JPSldZelJ6TnpoMVRZdFVPUFZuUTE0a1RXWlVaU0ZrU0tsRFIzQXpScmxGT2lwRmUyRlZidDVrWWhOSE4zTUhXUGgxUzU4VWRDVmpUT1psUmxKVlFLcFVPRWRETUh0V1c0SW1XNFpYVXQxbVRpRjJjMGN6Y1k5RVdMbHpUMUpVTk81a1ZHVm1VQnBrUzVRME53YzBhWmhqWWFobmRSMVdiT0pXWXpSek56aDFUWXRVT1BWblExNGtUV1pVWlNGa1NLbERSM0F6UnJsRk9pcEZlMkZWYnQ1a1loTkhOM01IV1BoMVM1OFVkQ1ZqVE9abFJsSlZRS3BVT0VkRE1IdFdXNEltVzRaWFV0MW1UaUYyYzBjemNZOUVXTGx6VDFKVU5PNWtWR1ZtVUJwa1M1UTBOd2MwYVpoalk%3D; _AWXH=; _ga=GA1.2.1255828712.1450515258; scarab.visitor=%222016CFEEE50471FF%22; __auc=7b4f956e151b9726eea96cfbf7c; scarab.profile=%2297477%7C1451203479%22; scarab.mayAdd=%5B%7B%22i%22%3A%2243024%22%7D%5D; __asc=225dcb6315210a81e481317a5e3; _AWXS=eU1qU001a2FGZEZSUUZFU0pKR1V6ZFVaV1YwUndrMVozRlVUcE5GVzRrVU15a2xVMWxHVnhKek1LeGtUcVYwVkVCVlFJbGtZUU4zUmxaVlJIQlRXbmRYUU5sMlVZaFRTeElUV1NWWGFVRm5Nem9FVE9wV1JYUkVVQmhVU2lCMWNIVm1WRmRFTVpkMmRCMVVhVGhGT0pGak1aSlZkcFJWY3lNalNNNWthRmRGUlFGRVNKSkdVemRVWldWMFJ3azFaM0ZVVHBORlc0a1VNeWtsVTFsR1Z4SnpNS3hrVHFWMFZFQlZRSWxrWVFOM1JsWlZSSEJUV25kWFFObDJVWWhUU3hJVFdTVlhhVUZuTXpvRVRPcFdSWFJFVUJoVVNpQjFjSFZtVkZkRU1aZDJkQjFVYVRoRk9KRmpNWkpWZHBSVmM%3D; _AWUS=S05UYTRkM2FHbG5TVGhrZUxoRVNNZDFONVlETnJSMmJsSjFkTlZUV0hOR09PbFdRbGxGUzVwME1waDNkclpVZUtORlM2dEVTSXgwVjNrak4wc0dadlZtVTMxVU5aZDBZNDRVYUJWV1dJbG5TemtHZTN0bVI1cDBVSXAzU0loRVRYZFRPMlF6YWs5V1pTZFhUMWsxUmpoalRwRlVaWmhVZUtOVGE0ZDNhR2xuU1Roa2VMaEVTTWQxTjVZRE5yUjJibEoxZE5WVFdITkdPT2xXUWxsRlM1cDBNcGgzZHJaVWVLTkZTNnRFU0l4MFYza2pOMHNHWnZWbVUzMVVOWmQwWTQ0VWFCVldXSWxuU3prR2UzdG1SNXAwVUlwM1NJaEVUWGRUTzJRemFrOVdaU2RYVDFrMVJqaGpUcEZVWlpoVWU%3D; _AWUR=a2xtY2xOR2RrbG1jbE5HZGtsbWNsTkdka2xtY2xOR2RrbG1jbE5HZGtsbWNsTkdk; _gat=1')
    resp = urllib2.urlopen(req)
    text = resp.read().decode('utf-8')
    json_data = json.loads(text)
    html_doc = json_data['Data']
    soup = BeautifulSoup(html_doc, 'html.parser')
    for li in soup.find_all(attrs={'class': 'clearfix'}):

            cells = li.findChildren('span')
            item = {'id_product': product}
            wiki = ''
            for cell in cells:
                    # if cell.has_attr('class=technicalspecs-title'):
                    #         print cell.get_text()
                    # print cell['class'][0]
                    if cell['class'][0] == u'technicalspecs-title':
                            item['specs_title'] = cell.text
                    if cell['class'][0] == u'technicalspecs-value':
                            item['specs_value'] = cell.text
                    if cell['class'][0] == u'wiki':
                            wiki += ',' + cell.text

            item['wiki'] = wiki
            # print item
            set_product_detail.delay(**item)
