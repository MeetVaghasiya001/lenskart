from parser import *
from db import *
from concurrent.futures import ThreadPoolExecutor
import json


product_url_db()

url = 'https://www.lenskart.com/'

data =get_all_links(url)

uqiue_url = set()


def product_urls(url):
    data=page_json(url)
    id=data.get('props',{}).get('pageProps',{}).get('data',{}).get('id')
    product_url=[]
    params={'page-size':'15','page':'1'}
    api=f'https://api-gateway.juno.lenskart.com/v2/products/category/{id}'
    row=[]
    found=False
    print(f'{url} in process')
    while True:
        page_data=request(api,params)
        if not page_data:
            print('0')
            break
        json_page_data=json.loads(page_data)
        result=json_page_data.get('result') or {}
        product_list=result.get('product_list')
        if not product_list:
            print(f"{url}-{params['page']}-{id} No product!")
            break
        found=True
        for i in product_list:
            if i.get('product_url') not in uqiue_url:
                uqiue_url.add(i.get('product_url'))
                product_url.append(i.get('product_url'))
                row.append((i.get('product_url'),'success'))
                if len(row)==10:
                    insert_url(row)
                    row.clear()
            else:
                print('Url already in db!!')

        params['page']=str(int(params['page'])+1)
    print(f'{url}-{len(product_url)}')
    if not found:
        insert_url([(url,'pending')])
    elif row:
        insert_url(row)
    return product_url


with ThreadPoolExecutor(max_workers=8) as e:
    futures = [e.submit(product_urls, url) for url in data]



