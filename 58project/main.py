from multiprocessing import Pool
from chanenel_extract import channel_list
from page_parsing import get_links

def get_all_links(channel):
    for num in range(2, 30):
        get_links(channel, num)
if __name__ == "__main__":
    pool = Pool()
    pool.map(get_all_links, channel_list.split())

# if __name__ == "__main__":
#     for channel in channel_list.split():
#         print(channel)