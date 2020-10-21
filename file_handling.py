import os
import re

def get_files(fn):
    enfiles = []
    thfiles = []
    singles = []    
    for filname in os.listdir(fn):
        if "_en_" in filname:   enfiles.append(filname)
        elif "_th_" in filname: thfiles.append(filname)
        else:   singles.append(filname)             
    return thfiles,enfiles,singles

def print_results(filname,source,th_text,en_text):
           
    ytemp = re.findall("\d+",filname)
    fnum = ytemp[0]    
    th_filename = source + "_th_" + fnum + ".txt"
    en_filename = source + "_en_" + fnum + ".txt"
    
    mypath1 = "corpus_files/" + th_filename
    with open(mypath1,'a',encoding="utf-8") as fh1:
    #print(len(th_text))
        for st in th_text:
            st = st + "\n"
            fh1.write(st)
            
    mypath2 = "corpus_files/" + en_filename
    with open(mypath2,'a',encoding="utf-8") as fh2:
        for st in en_text:
            st = st + "\n"
            fh2.write(st)
        
def print_resultsTH(filname,source,th_text):
           
    filename = re.sub('.html$','.txt',filname)           
    mypath1 = "corpus_files/" + filename
    with open(mypath1,'a',encoding="utf-8") as fh1:
        for text in th_text:
            text = re.sub('\s+',' ',text)
            if len(text) > 2:
                text = str(text) + "\n"  
                fh1.write(text)
                
def print_resultsE(filname,source,en_text):
           
    filename = re.sub('.html$','.txt',filname)           
    mypath2 = "corpus_files/" + filename
    with open(mypath2,'a',encoding="utf-8") as fh2:
        for text in en_text: 
            text = re.sub('\s+',' ',text)
            if len(text) > 2:
                text = str(text) + "\n"  
                fh2.write(text)
                
#fn = 'html_files'
#th,en,singles = get_files(fn)
#print(singles)
