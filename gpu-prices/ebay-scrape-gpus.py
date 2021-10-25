import os
import time
# pip install selenium
import selenium.webdriver as webdriver
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup # pip install beautifulsoup4
import pandas as pd # pip install pandas

def gpuPrice(name, link):
    filename = name
    ua = UserAgent()
    user_agent = ua.random
    #FireFoxDriverPath = os.path.join(os.getcwd(), 'Drivers', 'geckodriver.exe')
    FireFoxDriverPath = "D:/gpu-prices/geckodriver.exe"
    FireFoxProfile = webdriver.FirefoxProfile()
    FireFoxProfile.set_preference("general.useragent.override", user_agent)
    url = link
    browser = webdriver.Firefox(executable_path=FireFoxDriverPath)
    browser.implicitly_wait(9)
    browser.get(url)
    time.sleep(15)


    total_result = int(browser.find_element_by_class_name('srp-controls__count-heading').find_element_by_class_name('BOLD').text.replace(',', ''))
    ebay_listings = []

    current_page = 1
    to_continue = True

    while to_continue:
        try:
            print('Processing page {0}'.format(current_page))

            soup = BeautifulSoup(browser.page_source, 'html.parser')
            item_list = soup.find_all('li', 's-item')
            item_list.pop(0)
            len(item_list)
            
            for listing in item_list:
                product_detail = {}

                product_detail['product title'] = listing.h3.text
                product_detail['product url'] = listing.a['href']
                
                listing_subtitles = listing.find_all('div', 's-item__subtitle')
                if len(listing_subtitles) == 2:
                    listing_subtitle_1 = listing_subtitles[0].text
                    listing_subtitle_2 = listing_subtitles[1].text
                elif len(listing_subtitles) == 1:
                    listing_subtitle_1 = listing_subtitles[0].text
                    listing_subtitle_2 = None
                else:
                    listing_subtitle_1 = None
                    listing_subtitle_2 = None

                product_detail['subtitle1'] = listing_subtitle_1
                product_detail['subtitle2'] = listing_subtitle_2

                product_detail['date sold'] = listing.find('div', 's-item__title--tagblock').span.text.replace('Sold ','')


                

                product_detail['price'] = listing.find('span','s-item__price').span.text

                
                    
                ebay_listings.append(product_detail)


            time.sleep(1)
            browser.find_element_by_xpath('//a[@class="pagination__item" and text()="{0}"]'.format(current_page+1)).click()
            current_page +=1

        

        except NoSuchElementException:
            print('Last page {0}'.format(current_page))
            to_continue = False


    df = pd.DataFrame(ebay_listings)
    df.to_excel(f'data/{filename}.xlsx', index=False)

#gpuPrice('amd6800xt','https://www.ebay.com/sch/i.html?_from=R40&_nkw=AMD+Radeon+RX+6800+XT&_sacat=0&LH_Sold=1&LH_Complete=1&rt=nc&Brand=AMD&_dcat=27386')
#gpuPrice('amd6800','https://www.ebay.com/sch/i.html?_from=R40&_nkw=amd+radeon+rx+6800+-xt&_sacat=0&LH_TitleDesc=0&LH_Complete=1&LH_Sold=1&rt=nc&Brand=AMD&_dcat=27386')
#gpuPrice('amd6700xt','https://www.ebay.com/sch/i.html?_from=R40&_nkw=amd+radeon+rx+6700+xt&_sacat=0&LH_TitleDesc=0&LH_Complete=1&LH_Sold=1&rt=nc&Brand=AMD&_dcat=27386')
#gpuPrice('gtx3090', 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=geforce+3090+founders&_sacat=0&LH_TitleDesc=0&LH_Complete=1&LH_Sold=1&_ipg=200')
#gpuPrice('gtx3080ti','https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=geforce+3080+ti+founders&_sacat=0&LH_TitleDesc=0&rt=nc&_odkw=geforce+3090+founders&_osacat=0&LH_Complete=1&_ipg=200&LH_Sold=1')
#gpuPrice('gtx3080','https://www.ebay.com/sch/i.html?_from=R40&_nkw=3080+founders+-ti&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1')
#gpuPrice('gtx3070ti','https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=3070+ti+founders+&_sacat=0&LH_TitleDesc=0&rt=nc&_odkw=3080+founders+-ti&_osacat=0&LH_Complete=1&LH_Sold=1')
#gpuPrice('gtx3070','https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=3070+founders+-ti&_sacat=0&LH_TitleDesc=0&_odkw=3070+ti+founders+&_osacat=0&LH_Complete=1&LH_Sold=1')
#gpuPrice('gtx3060ti','https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=3060+ti+founders&_sacat=0&LH_TitleDesc=0&_odkw=3070+founders+-ti&_osacat=0&LH_Complete=1&LH_Sold=1')