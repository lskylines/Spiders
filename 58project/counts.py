import time
from page_parsing import itemlink
while True:
    print(itemlink.find().count())
    time.sleep(5)