from playwright.sync_api import sync_playwright
import json 
from bs4 import BeautifulSoup



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


def start_driver():
    
    global playwright, browser, context

    session = clear_cookies()

    playwright = sync_playwright().start() 
    browser = playwright.webkit.launch(headless=True)
    context = browser.new_context()
    context.add_cookies(session)

    page = context.new_page()

    # sometimes playwright just cant access for no reason so it has to be done 2 times
    try:
        page.goto("https://admin-meia-entrada.netlify.app/dashboard/carteiras/dce_ifrs_restinga")
    except:
        page.goto("https://admin-meia-entrada.netlify.app/dashboard/carteiras/dce_ifrs_restinga")
    
    return page



def get_info(page):

    section_button = page.locator("button:has(span:has-text('Em Produção'))")
    section_button.click()

    with open('page.html', 'w') as p:  

        soup = BeautifulSoup(page.content(), "html.parser")
        p.write(soup.prettify())



def close_all(page):# aperta agora

        try:
            page.close()
        except:
            pass
        try:
            context.close()
        except:
            pass

        try:
            browser.close()
        except:
            pass
        
        try:
            playwright.dispose()
        except:
            pass



if __name__ == "__main__":
    page = start_driver()
    get_info(page)
    close_all(page)