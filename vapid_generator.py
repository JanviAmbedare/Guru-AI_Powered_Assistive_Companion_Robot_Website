# run in a Python shell
from pywebpush import webpush, WebPushException
from py_vapid import Vapid01 as Vapid
v = Vapid()
v.generate_keys()
print(v.public_key)
print(v.private_key)