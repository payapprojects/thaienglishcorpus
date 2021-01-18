import re
from bs4 import BeautifulSoup
#extraction rules for sources ############################################
def check_area(by,source,soup):    
    if source == "bumrungrad" or source == "bum":
        by = soup.find('div',class_='row collapse show')         
    elif source == "intel" or source == "tech":
        by = soup.find('article',class_='article article-long component')
    elif source == "phya":
        by = soup.find("div", {"id": "content"})        
    return by

#extract single ##########################################################

def getEnglishtext(t):   
    extext = ""
    et = re.search(r'English\)</b>\s*</td>\s<td>\s*(.*?)</td>',t)
    if et:
        if et.group(1) is not None:
            extext = et.group(1)
        else:
            extext = "failed extraction"
    else:
        extext = "failed extraction"     
    return extext
    
def getThaitext(t):   
    extext = ""
    et = re.search(r'ไทย\)</b></td>\s*<td>\s*(.*?)</td>',t)
    if et:
        extext = et.group(1)
    else:
        extext = "failed extraction"      
    return extext

def extractor_single(fpath,s):
    
    textE = ""
    textTH = ""
    
    if s == "kmutnb":
        with open(fpath,encoding="utf-8") as hfile:
            soup = BeautifulSoup(hfile, 'lxml')#'html.parser')
        
            by = soup.find("div", {"id": "articleAbstract"})    
            text_elements = []
            
            for p in by.find_all('p'):
                if p.text != "":
                    text_elements.append(p.text)
                    
            if len(text_elements) > 1:
                textTH = text_elements[0]           
                textE = text_elements[1]
                                    
                textTH = re.sub('\s+',' ',textTH)
                textE = re.sub('\s+',' ',textE)

    elif s == "thaithesis" or s == "tt":                
    
        with open(fpath,encoding="tis-620") as hfile: #  "utf-8"
            soup = BeautifulSoup(hfile,'lxml')#html.parser
    
            by = soup.find('body')
            sby = str(by)
            
            if "บทคัดย่อ(ไทย)" in sby and "บทคัดย่อ(English)" in sby:
                textE = getEnglishtext(sby)
                textTH = getThaitext(sby)
                
                textTH = re.sub('\s+',' ',textTH)
                textE = re.sub('\s+',' ',textE)
    
    return(textTH,textE)

#extract pairs ##########################################################
def extractor(f,source,site_repeat_prob):
    by = ""   
    alltext = ""
                        
    with open(f,encoding="utf-8") as hfile:
        soup = BeautifulSoup(hfile, 'lxml')#'html.parser')
        #remove scripts
        [x.extract() for x in soup.findAll('script')]

        #get body
        by = soup.find('body')
        #reduce area if required
        by = check_area(by,source,soup)        
        
        text_elem = []
        text_elements = []
        alltext = ""
                   
        if by:                                
            alltext = by.text            
        text_elem = alltext.split('\n')

        for extext in text_elem:
            extext = re.sub('\s+',' ',extext)
            extext = re.sub('^\s','',extext)
            
            if len(extext)>1:                
                if extext != "" and extext != "," and extext != "|" and extext != " ":                       
                    if extext not in site_repeat_prob:
                        text_elements.append(extext)
                        site_repeat_prob.append(extext)

    return text_elements,site_repeat_prob                              
    

    
