Python QuadrigaCX
=================

quadrigacx is a Python wrapper for the `QuadrigaCX API (v2)`_.

Install
~~~~~~~

``pip install quadrigacx``

or ``pip install setup.py`` in the repo’s main directory after you
download this repo.

Configuration
~~~~~~~~~~~~~

You will need to create a config file in order to use the authenticated
API actions. Use sample.cfg in the config folder

Usage
~~~~~

Basically, create a QCX object, passing in the path to the config file
[like in ``quadrigacx/config/sample.cfg``], or the config options in a
dict [i.e.
``{client_id:0000, key:yOurKeY, secret:Y0Ur53crr3T142351236}``]

::

    import quadrigacx
    qcx = quadrigacx.QCX('config/auth.cfg')

That QCX object then has a methods called ``methods`` which will tell
you all of the actions available in this format:

::

    qcx.methods()

    {
      'private':
        [
          {
            'name':'name_of_action',
            'requires': {
              'key': [value for key,value in {'maybe':'some', 'example':'data'}]
            },
            'optional': {
              'key': [value for key,value in {'maybe':'some', 'optional':'data'}]
              },
            'returns': {
              'something': {
                  u'details': u'850.99',
                  u'more_details': u'837.51'
              }
            },
          },
        ],
      'public':
        [
          {
            'name':'name_of_action',
            'requires': {
              'key': [value for key,value in {'maybe':'some', 'example':'data'}]
            },
            'optional': {
              'key': [value for key,value in {'maybe':'some', 'optional':'data'}]
              },
            'returns': {
              'something': {
                  u'details': u'850.99',
                  u'more_details': u'837.51'
              }
            },
          }
        ]
      }

You can take that ``name`` and pass it into QCX.api(), along with the
``required`` (and ``optional``, if needed) data *as keyword arguments*,
and you’ll get something like the expected ``returns``.


+------------+------+--------------+------------------+------------------------+-------+
| **Function | **Au | **Required   | **Default**      | **Optional Arguments** | **Def |
| Name**     | th** | Arguments**  |                  |                        | ault* |
|            |      |              |                  |                        | *     |
+============+======+==============+==================+========================+=======+
| ticker     | No   | a or a list  | [btc\_cad,       |                        |       |
|            |      | of valid     | btc\_usd,        |                        |       |
|            |      | books        | eth\_cad,        |                        |       |
|            |      |              | eth\_btc]        |                        |       |
+------------+------+--------------+------------------+------------------------+-------+
| order\_boo | No   | a or a list  | [btc\_cad,       | A boolean to group     | False |
| k          |      | of valid     | btc\_usd,        | orders with the same   |       |
|            |      | books        | eth\_cad,        | price or not           |       |
|            |      |              | eth\_btc]        |                        |       |
+------------+------+--------------+------------------+------------------------+-------+
| transactio | No   | a or a list  | [btc\_cad,       | A time frame; last     | hour  |
| ns         |      | of valid     | btc\_usd,        | ‘minute’, or ‘hour’    |       |
|            |      | books        | eth\_cad,        |                        |       |
|            |      |              | eth\_btc]        |                        |       |
+------------+------+--------------+------------------+------------------------+-------+
| balance    | Yes  |              |                  |                        |       |
+------------+------+--------------+------------------+------------------------+-------+
| user\_tran | Yes  | a or a list  | [btc\_cad,       |                        |       |
| sactions   |      | of valid     | btc\_usd,        |                        |       |
|            |      | books        | eth\_cad,        |                        |       |
|            |      |              | eth\_btc]        |                        |       |
+------------+------+--------------+------------------+------------------------+-------+
| open\_orde | Yes  | open\_orders | [btc\_cad,       |                        |       |
| rs         |      |              | btc\_usd,        |                        |       |
|            |      |              | eth\_cad,        |                        |       |
|            |      |              | eth\_btc]        |                        |       |
+------------+------+--------------+------------------+------------------------+-------+
| lookup\_or | Yes  | order\_id    |                  |                        |       |
| der        |      |              |                  |                        |       |
+------------+------+--------------+------------------+------------------------+-------+
| cancel\_or | Yes  | order\_id    |                  |                        |       |
| der        |      |              |                  |                        |       |
+------------+------+--------------+------------------+------------------------+-------+
| buy        | Yes  | a valid book |                  | a price                |       |
+------------+------+--------------+------------------+------------------------+-------+
|            |      | an amount    |                  |                        |       |
+------------+------+--------------+------------------+------------------------+-------+
| sell       | Yes  | a valid book |                  | a price                |       |
+------------+------+--------------+------------------+------------------------+-------+
|            |      | an amount    |                  |                        |       |
+------------+------+--------------+------------------+------------------------+-------+
| bitcoin\_d | Yes  |              |                  |                        |       |
| eposit\_ad |      |              |                  |                        |       |
| dress      |      |              |                  |                        |       |
+------------+------+--------------+------------------+------------------------+-------+
| ether\_dep | Yes  |              |                  |                        |       |
| osit\_addr |      |              |                  |                        |       |
| ess        |      |              |                  |                        |       |
+------------+------+--------------+------------------+------------------------+-------+
| bitcoin\_w | Yes  | an amount    |                  |                        |       |
| ithdrawal  |      |              |                  |                        |       |
+------------+------+--------------+------------------+------------------------+-------+
|            |      | an address   |                  |                        |       |
+------------+------+--------------+------------------+------------------------+-------+
| ethereum\_ | Yes  | an amount    |                  |                        |       |
| withdrawal |      |              |                  |                        |       |
+------------+------+--------------+------------------+------------------------+-------+
|            |      | an address   |                  |                        |       |
+------------+------+--------------+------------------+------------------------+-------+

**Notes:**

-  Not all items in methods() show what the return value is. I will
   eventually update that, but for now just play around.
-  I only show what the positive response should look like, negative
   responses could be (and often are) entirely different.
-  Honestly, you are better off just looking at QuadrigaCX’s API page to
   see what resuts they will provide:
   https://www.quadrigacx.com/api\_info

Examples:
~~~~~~~~~

Basic
^^^^^

::

    print qcx.api('ticker')

    >> {'eth_cad': {u'volume': u'730.00552932', u'last': u'15.00', u'timestamp': u'1467639054', u'bid': u'14.90', u'vwap': u'15.47', u'high': u'16.34', u'low': u'15.00', u'ask': u'16.08'}, 'btc_cad': {u'volume': u'161.49814654', u'last': u'886.00', u'timestamp': u'1467639053', u'bid': u'878.20', u'vwap': u'867.00', u'high': u'886.00', u'low': u'856.79', u'ask': u'887.97'}, 'eth_btc': {u'volume': u'2256.84091030', u'last': u'0.01722000', u'timestamp': u'1467639054', u'bid': u'0.01722000', u'vwap': u'0.01794464', u'high': u'0.01855999', u'low': u'0.01722000', u'ask': u'0.01819999'}, 'btc_usd': {u'volume': u'10.06581000', u'last': u'670.00', u'timestamp': u'1467639053', u'bid': u'663.10', u'vwap': u'666.91', u'high': u'700.26', u'low': u'670.00', u'ask': u'688.00'}}

Optional Parameter as String
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    book = 'btc_cad' # Undocumented ability to send individual values not in a list
    print qcx.api('ticker', book_list=book)

    >> {'btc_cad': {u'volume': u'161.49814654', u'last': u'886.00', u'timestamp': u'1467639054', u'bid': u'878.20', u'vwap': u'867.00', u'high': u'886.00', u'low': u'856.79', u'ask': u'887.97'}}

Optional parameter as List
^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    book_list = ['btc_cad', 'eth_btc']
    print qcx.api('ticker', book_list=book_list)

    >> {'btc_cad': {u'volume': u'161.49814654', u'last': u'886.00', u'timestamp': u'1467639055', u'bid': u'878.20', u'vwap': u'867.00', u'high': u'886.00', u'low': u'856.79', u'ask': u'887.97'}, 'eth_btc': {u'volume': u'2256.84091030', u'last': u'0.01722000', u'timestamp': u'1467639055', u'bid': u'0.01722000', u'vwap': u'0.01794464', u'high': u'0.01855999', u'low': u'0.01722000', u'ask': u'0.01819999'}}

Limit Purchase with unnamed parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    book = 'btc_cad'
    amount = 0.005
    print qcx.api('buy', book, amount)

    >> {u'error': {u'message': u'Incorrect : $7.50CAD exceeds available CAD balance', u'code': 21}}
