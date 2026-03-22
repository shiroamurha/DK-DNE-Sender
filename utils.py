from datetime import datetime
import json



def debug(content):
    time = datetime.now()
    print(f'[{time.strftime("%H:%M:%S")}] > {content}')
    return time



def clear_cookies():

    raw_cookies = json.load(open('./static/session.json', 'r'))
    filtered_session = []

    for item in raw_cookies:
        keys = list(item.keys()).copy()
        for line in keys:
            if line not in ['name', 'value', 'domain', 'path']:
                del item[line]
    filtered_session = raw_cookies

    json.dump(filtered_session, open('./static/session.json', 'w'), indent=4)

    return filtered_session



def padronize(name):
    return name.replace(' ', '').upper()[0:15]



def get_key_by_value(dict, value):

    for key in dict.keys():
        if dict.get(key) == value:
            return key
        


def logger(logs, filenames_list, emails_to_notify):

    for filename in filenames_list:
        if filename not in logs[0]['already_sent_dnes']:
            logs[0]['already_sent_dnes'].append(filename)
    
    single_string_emails = ''
    for email in emails_to_notify:
        single_string_emails += f'{email}, '
        
    logs[0]['emails_to_notify'] = single_string_emails

    update_logs(logs)



def get_logs():
    return json.load(open('./static/logs.json', 'r'))



def update_logs(logs):
    json.dump(logs, open('./static/logs.json', 'w'), indent=4)