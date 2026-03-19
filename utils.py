from datetime import datetime
import json



def debug(content):
    print(f'[{datetime.now().strftime("%H:%M:%S")}] > {content}')



def clear_cookies():

    raw_cookies = json.load(open('../dk_dne_session.json', 'r'))
    filtered_session = []

    for item in raw_cookies:
        keys = list(item.keys()).copy()
        for line in keys:
            if line not in ['name', 'value', 'domain', 'path']:
                del item[line]
    filtered_session = raw_cookies

    json.dump(filtered_session, open('../dk_dne_session.json', 'w'), indent=4)

    return filtered_session



def padronize(name):
    return name.replace(' ', '').upper()[0:15]



def get_key_by_value(dict, value):

    for key in dict.keys():
        if dict.get(key) == value:
            return key
        


def log_what_was_done(dict):
    pass # todo: set all info of the dnes sent