from quadriga import QCX
import random
from pprint import pprint

config_filepath = "../../flask_application/config/auth.cfg"
qcx = QCX(config_filepath)

## Harmless Functions

pprint( qcx.api('balance') )

book_list = [value for key,value in qcx.enumerations("order_books").iteritems()]
pprint( qcx.api('transactions', book_list=book_list) )

open_order_result = qcx.api('open_orders', book_list=book_list )
pprint( open_order_result )

order_id = None
for book in open_order_result:
    if len(open_order_result[book]) > 0:
        order_id = open_order_result[book][0]['id']

if order_id:
    print order_id

    pprint( qcx.api('lookup_order', order_id=order_id) )

    pprint( qcx.api('cancel_order', order_id=order_id) )
