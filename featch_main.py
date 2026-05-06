from parser import *
from db import *
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

conn, cur = connection()
create_db()

cur.execute("SELECT * FROM urls WHERE url_status=%s", ('success',))
data = [d[1] for d in cur.fetchall()]

row = []
status = []

with ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(parser, url) for url in data]

    for future in as_completed(futures):
        r = future.result()

        if not r:
            continue

        row.append((
            r.get('product_id'),
            r.get('brand'),
            r.get('product_name'),
            r.get('model_number'),
            json.dumps(r.get('gallary')),
            json.dumps(r.get('price')),
            r.get('review'),
            r.get('rating_count'),
            json.dumps(r.get('customer_reviews')),
            json.dumps(r.get('custome_review_graph')),
            json.dumps(r.get('specification')),
            json.dumps(r.get('similar_products')),
            json.dumps(r.get('highlight')),
            json.dumps(r.get('near_by_stores')),
            json.dumps(r.get('sizes')),
            json.dumps(r.get('colors')),
            json.dumps(r.get('promis'))
        ))

        status.append(('success',r.get('url')))

        if len(row) >= 20:
            insert_in_db(row, status)
            row.clear()
            status.clear()

if row:
    insert_in_db(row, status)