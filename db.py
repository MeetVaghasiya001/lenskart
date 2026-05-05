import mysql.connector


def connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Actowiz",
        database="lenskart"
    )

    cur = conn.cursor()

    return conn,cur 


def create_db():
    conn,cur = connection()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS lenskart(
                p_id INT AUTO_INCREMENT PRIMARY KEY,
                product_id INT,
                brand VARCHAR(255),
                product_name VARCHAR(255),
                model_number VARCHAR(255),
                gallary JSON,
                price JSON,
                review VARCHAR(255),
                review_count VARCHAR(255),
                customer_reviews JSON,
                custome_review_graph JSON,
                specification JSON,
                similar_products JSON,
                highlight JSON,
                near_by_stores JSON,
                sizes JSON,
                colors JSON,
                promis JSON
            )

    """)

    conn.commit()
    conn.close()


def insert_in_db(data):
    conn,cur = connection()
    query="INSERT INTO lenskart (product_id,brand,product_name,model_number,gallary,price,review,review_count,customer_reviews,custome_review_graph,specification,similar_products,highlight,near_by_stores,sizes,colors,promis) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    print('data was add!')
    cur.executemany(query,data)
    conn.commit()
    conn.close()