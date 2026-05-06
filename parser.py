from request_data import *
from lxml import html
import json
import re
import os
import gzip
from model import *
from db import *
from urllib.parse import urljoin


create_db()
if not os.path.exists('C:/Users/meet.vaghasiya/Desktop/bif files/lenscart') :
    os.mkdir('C:/Users/meet.vaghasiya/Desktop/bif files/lenscart')
else:
    None

def add_page_save(page):
    folder_path = 'C:/Users/meet.vaghasiya/Desktop/bif files/lenscart'
    id = page.get('props', {}).get('pageProps', {}).get('data', {}).get('id')

    with gzip.open(f'{folder_path}/{id}.json.gz','wt',encoding='utf-8') as f:
        json.dump(page,f,indent=4,default=str)



def page_json(url):
    page_data = request(url)

    tree=html.fromstring(page_data)
    script=tree.xpath("//script[@type='application/json']/text()")
    for i in script:
        final_script=json.loads(i)
    return final_script



def parser(url):
    pincode = 380001

    product_id = None
    product_name = None
    description = None
    model_number = None
    price = {}
    gallary = {'images': None, 'videos': None}
    specs = []
    review = None
    rating_count = None
    count_reviews = {}
    custome_review_graph = []
    highlight = None
    size_result = None
    color_result = None
    similar_p = []
    stores = None
    lat = None
    lng = None

    page_data = page_json(url)
    add_page_save(page_data)
    if not page_data:
        return

    try:
        main_path = page_data.get('props', {}).get('pageProps', {}).get('data', {})
        product_id = main_path.get('id')
        result = main_path.get('productDetailData', {}).get('result', [])

        for r in result:
            rid = r.get('id')

            if rid == 'gallery':
                data = r.get('data', {})
                gallery_data = data.get('galleryWidget', {}).get('data', [])

                images = [g.get('imageUrl') for g in gallery_data if g.get('type') == 'IMAGE']
                videos = [g.get('videoUrl') for g in gallery_data if g.get('type') == 'VIDEO']

                gallary = {'images': images or None, 'videos': videos or None}

                for s in data.get('specifications', []):
                    specs.append({
                        'key': s.get('name'),
                        'values': [
                            {'key': i.get('name'), 'values': i.get('value')}
                            for i in s.get('items', [])
                        ]
                    })

                review_data = data.get('review', {})
                review = review_data.get('rating')
                rating_count = review_data.get('ratingCount')

                reviews_data_count = review_data.get('reviews',[])

                

                for d in reviews_data_count:
                    stars = d.get("noOfStars")

                    if stars not in count_reviews:
                        count_reviews[stars] = []

                    count_reviews[stars].append({
                        "reviewer": d.get("reviewee"),
                        "title": d.get("reviewTitle"),
                        "comment": d.get("reviewDetail"),
                        "date": d.get("reviewDate")
                    })

                custome_review_graph = [{
                    'rating': c.get('stars'),
                    'review_count': c.get('percentage')
                } for c in review_data.get('reviewGraph', [])]

            if rid == 'feature':
                highlight_data = r.get('data', [])
                highlight = {
                    "key": "features",
                    "value": [
                        {"key": item.get("label"), "value": item.get("imageUrl")}
                        for item in highlight_data
                    ]
                }

            if rid == 'summary':
                data = r.get('data', {})
                product_name = data.get('brandName')
                description = data.get('description')
                model_number = data.get('modelName')
                price = {p.get('name'): p.get('price') for p in data.get('prices', [])}

            if rid == 'additional_options':
                options = r.get('data', {}).get('options', [])

                colors = []
                sizes = []

                for opt in options:
                    if opt.get("label") == "Frame Color":
                        for item in opt.get("optionList", []):
                            colors.append({
                                "key": item.get("title"),
                                "value": item.get("imageUrl")
                            })

                    if opt.get("id") == "framesizeId":
                        for item in opt.get("optionList", []):
                            sizes.append({
                                "key": item.get("title"),
                                "value": item.get("frameWidth")
                            })

                color_result = {"key": "frame_color", "value": colors} if colors else None
                size_result = {"key": "frame_size", "value": sizes} if sizes else None

    except Exception as e:
        print(f'Error-{e}')
        return 

    lat_log = get_lat_log(pincode)

    if lat_log:
        try:
            match = re.search(r'\{[\s\S]*\}', lat_log)
            if match:
                lat_data = json.loads(match.group(0))
                for l in lat_data.get('results', []):
                    loc = l.get('geometry', {}).get('location', {})
                    lat = loc.get('lat')
                    lng = loc.get('lng')
        except Exception as e:
            print(f'error-{e}')
            return

    if lat and lng and product_id:
        try:
            store_api = f'https://api-gateway.juno.lenskart.com/v2/products/product/{product_id}/nearbyStoreInventory'
            params = {'lat': lat, 'lon': lng}
            store_data = request(store_api, params)

            if store_data:
                json_store_data = json.loads(store_data)
                stores = [{
                    'code': s.get('code'),
                    'name': s.get('name'),
                    'open_time': s.get('openingTime'),
                    'close_time': s.get('closingTime'),
                    'phone_number': s.get('telephone'),
                    'url': s.get('url'),
                    'store_distance': s.get('storeDistance')
                } for s in json_store_data.get('result', {}).get('storeList', [])] or None
        except Exception as e:
            print(f'Error-{e}')
            return 

    if product_id:
        try:
            s_product_api = f'https://api-gateway.juno.lenskart.com/v2/products/{product_id}/similar-products'
            params = {'page': '0', 'page-size': '30', 'layout': '1'}
            similar_products = request(s_product_api, params)

            if similar_products:
                sp = json.loads(similar_products)
                similar_p = [{
                    'product_id': p.get('id'),
                    'img': p.get('image_url'),
                    'prices': [
                        {'name': i.get('name'), 'price': i.get('price')}
                        for i in p.get('prices', [])
                    ]
                } for p in sp.get('result', {}).get('product_list', [])]
        except Exception as e:
            print(f'Error-{e}')
            return 
    delivery_api = 'https://api-gateway.juno.lenskart.com/v1/shipping/tat'
    params = {
        'pincode': pincode,
        'productId': product_id,
    }
    avaliblity_check = request(delivery_api,params)

    if avaliblity_check:
        avalible_json_data = json.loads(avaliblity_check)
        with open('1.json','w',encoding='utf-8') as f:
            json.dump(avalible_json_data,f,indent=4,default=str)
        for r in avalible_json_data.get('result'):
            promis = {
                'promis':r.get('promiseTypeLabel'),
                'image':r.get('imageUrl'),
                'benifits':[b.get('label') for b in r.get('benefits')]
                } 
    
    data = {
        'url':url,
        'product_id': product_id,
        'brand': product_name,
        'product_name': description,
        'model_number': model_number,
        'gallary': gallary,
        'price': price,
        'review': review,
        'rating_count': rating_count,
        'customer_reviews': count_reviews or None,
        'custome_review_graph': custome_review_graph,
        'specification': specs,
        'similar_products': similar_p,
        'highlight': highlight,
        'near_by_stores': stores,
        'sizes': size_result,
        'colors': color_result,
        'promis':promis
    }
    vallidate = Product(**data)
    # with open('clean.json','w',encoding='utf-8') as f:
    #     json.dump(vallidate.model_dump(),f,indent=4,default=str)
    print(f'{url} was done!!')  
    return vallidate.model_dump() 




def get_all_links(url):
    main_url = 'https://www.lenskart.com/'
    data = page_json(url)
    with open('clean2.json','w',encoding='utf-8') as f:
        json.dump(data,f,indent=4,default=str)
    main_path = data.get('props').get('pageProps').get('data').get('headerData').get('menu1')

    def extract_urls(obj, result=None):
        if result is None:
            result = []

        if isinstance(obj, list):
            for item in obj:
                extract_urls(item, result)

        elif isinstance(obj, dict):
            for k, v in obj.items():
                if k == "url" and isinstance(v, str):
                    result.append(urljoin(main_url,v))
                else:
                    extract_urls(v, result)

        return result

    return extract_urls(main_path)

params = {
        'page-size': '15',
        'page': '15',
    }
data = request(f'https://api-gateway.juno.lenskart.com/v2/products/category/29361',params)

with open('lense.json','w',encoding='utf-8') as f:
    json.dump(json.loads(data),f,indent=4,default=str)









# data = parser('https://www.lenskart.com/aquacolor-dusky-brown-n-candy-pack-color-lenses-2-lens-box-plano.html')

# row = []
# row.append((
#     data.get('product_id'),
#     data.get('brand'),
#     data.get('product_name'),
#     data.get('model_number'),
#     json.dumps(data.get('gallary')),
#     json.dumps(data.get('price')),
#     data.get('review'),
#     data.get('rating_count'),
#     json.dumps(data.get('customer_reviews')),
#     json.dumps(data.get('custome_review_graph')),
#     json.dumps(data.get('specification')),
#     json.dumps(data.get('similar_products')),
#     json.dumps(data.get('highlight')),
#     json.dumps(data.get('near_by_stores')),
#     json.dumps(data.get('sizes')),
#     json.dumps(data.get('colors')),
#     json.dumps(data.get('promis'))

# ))


# insert_in_db(row)
