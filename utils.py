from datetime import datetime



def debug(content):
    print(f'[{datetime.now().strftime("%H:%M:%S")}] > {content}')

