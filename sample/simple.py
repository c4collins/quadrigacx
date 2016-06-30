from quadriga import QCX
import random
from pprint import pprint

qcx = QCX()

methods = qcx.methods()

order_books = qcx.enumerations("order_books").keys()

# You can send lists or individual books, api uses honey badger typing
pprint( qcx.api( 'ticker', book_list=[order_books[key] for key in order_books.keys()[:-2]] ) )

# See all the things you can do without authentication
for action in qcx.methods()['public']:
    pprint( qcx.api( action['name'], book_list=order_books[random.choice( order_books.keys() )] ) )
    pprint( action )
