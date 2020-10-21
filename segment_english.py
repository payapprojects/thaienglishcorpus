import re

def split_into_sentences(text):
    
    alphabets= "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov)"
    
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    
    if re.search('\d+\.\d+',text): #12.183
        result = re.sub('(\d+)\.(\d+)',r'\1<STP>\2',text)
        text = result
    if re.search('\s\.\d+',text): #12.183
        result = re.sub('\s\.(\d+)',r' <STP>\1',text)
        text = result
    if re.search('\d+\.\s',text): #12.183
        result = re.sub('(\d+)\.\s',r'\1<STP> ',text)
        text = result
    #print (text)
    #or re.search('(\d+)\.\s',text):
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
#    text = text.replace(":",":<stop>")  #colon for sinlge docs
    text = text.replace("<prd>",".")
    text = text.replace("<STP>",".")
    sentences = text.split("<stop>")
    #sentences = sentences[:-1]
    sentences2 = []
    for s in sentences:
        s = re.sub('\s+',' ',s)
        s = s.strip()
        if len(s) > 2:
            sentences2.append(s)  
    return sentences2