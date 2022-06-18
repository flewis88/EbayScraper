#! python3
import requests as r
import pandas as pd
import time
from bs4 import BeautifulSoup as bs
from plyer import notification as popup
import webbrowser as w
c = 0 #this is a counter for looping through the URL's in the list
li = []#records links to breville so that no repeats come up
df = pd.DataFrame({'Title':[],'Price':[],'Item Number':[],'Link':[]})


URL = ["https://www.ebay.com.au/sch/i.html?_fsrp=1&rt=nc&_from=R40&_nkw=breville+dual&_sacat=0&LH_PrefLoc=1&LH_ItemCondition=2500%7C3000"]
while True: #Can I make this loop indefinitely?
    c = 0
    print("Scraping")
    for i in URL:#This cycles through the URL's
        page = r.get(URL[c])
        c+=1
        soup = bs(page.content, "html.parser")
        searc = soup.find(id="srp-river-main")#This selects all info on the page
        breville = searc.find_all("div", class_="s-item__info clearfix") #this defines the information for each item on the page
        g = 0 #this is useless but I needed put someting in the if statements below    
        for i in breville:
            itemname = i.find("h3", class_= "s-item__title")
            price = i.find("span", class_= "s-item__price")
            link = i.find("a", class_= "s-item__link")
            ebay_item=link["href"].split("itm/",1)[1].split("?",1)[0]
            x = 'breville' and 'dual'
            y = 'to'
            if ebay_item not in li:          
                if x in itemname.text.lower(): 
                    if price == None:
                        g+=1
                    elif y in price.text.replace('$' ,''):
                        g+=1
                    elif (float(price.text.replace('$','').replace(',','').replace('AU ','')) <= 901) and (float(price.text.replace('$','').replace(',','').replace('AU ','')) >=70):
                        #print (itemname.text, end = "\n")
                        #print (price.text, end = "\n")
                        #print (link["href"], end="\n")
                        li.append(ebay_item)
                        #df2 = pd.DataFrame({'Title':'BES900','Price':'$300','Item Number':'1234','Link':'http://www.ebay.com'})
                        df2 = pd.DataFrame({'Title':[itemname.text],'Price':[price.text],'Item Number':[ebay_item],'Link':[link["href"]]})
                        #print(ebay_item)
                        print("DF2: ",df2)
                        #w.open(link["href"])
                        popup.notify(
                            title = 'New Breville',
                            message = ebay_item,
                            app_icon = None,
                            timeout = 10,
                        )
                        df = pd.concat([df,df2])
                        df.to_excel('./eBay Items.xlsx')
    incr = 0
    while incr <6:
        print("Scraping again in ", (6-incr)*5," minutes")
        time.sleep(300)
        incr +=1
