from django.db import connection
from contextlib import closing

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns,row)) for row in cursor.fetchall()
    ]

def dictfetchone(cursor):
    row = cursor.fetchone()
    if row is None:
        return False
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns,row))

def get_order_by_user(id):
    with closing(connection.cursor()) as cursor:
        cursor.execute(""" SELECT mahsulotlar_order.id, mahsulotlar_customer.first_name,mahsulotlar_customer.last_name, mahsulotlar_order.address, mahsulotlar_order.payment_type,mahsulotlar_order.status,mahsulotlar_order.created_at from mahsulotlar_order 
                            INNER JOIN mahsulotlar_customer on mahsulotlar_customer.id=mahsulotlar_order.customer_id 
                            where mahsulotlar_order.customer_id =%s""",[id])
        order = dictfetchall(cursor)
        return order

def get_product_by_order(id):
    with closing(connection.cursor()) as cursor:
        cursor.execute(""" SELECT mahsulotlar_orderproduct.count,mahsulotlar_orderproduct.price,
        mahsulotlar_orderproduct.created_at, mahsulotlar_product.title from mahsulotlar_orderproduct 
         INNER JOIN mahsulotlar_product ON mahsulotlar_orderproduct.product_id=mahsulotlar_product.id  where order_id=%s""",[id])
        orderproduct = dictfetchall(cursor)
        return orderproduct

def get_table():
    with closing(connection.cursor()) as cursor:
        cursor.execute(""" 
        SELECT mahsulotlar_orderproduct.product_id, 
COUNT(mahsulotlar_orderproduct.product_id),mahsulotlar_product.title 
FROM mahsulotlar_orderproduct 
INNER JOIN mahsulotlar_product ON mahsulotlar_product.id=mahsulotlar_orderproduct.product_id 
GROUP BY mahsulotlar_orderproduct.product_id ,mahsulotlar_product.title 
order by count desc limit 10

        """)
        table = dictfetchall(cursor)
        return table