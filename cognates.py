import file_handling as fhand
import re

def convert_thai_nums(num):
    
    num = re.sub('๐','0',num)
    num = re.sub('๑','1',num)
    num = re.sub('๒','2',num)
    num = re.sub('๓','3',num)
    num = re.sub('๔','4',num)
    num = re.sub('๕','5',num)
    num = re.sub('๖','6',num)
    num = re.sub('๗','7',num)
    num = re.sub('๘','8',num)
    num = re.sub('๙','9',num)
    return num

def cognatesTH(text):
    cognates = []   
    all_nums = re.findall('\d+[\-\_\.\,]*\d*',text)
    for num in all_nums:
        if len(num) > 1:            
            num = convert_thai_nums(num)
            cognates.append(num)      
    return cognates

def cognatesEN(text,cogs):
    
    text = text.lower()
    cog  = []
    for y in cogs:        
        if y in text:
            cog.append(y)
            i = text.find(y)
            text = text[i:]
                                       
    return cog

def find_cogs(thtexts,entexts):
    all_cogs = []
    cognates = {}
    no = 0
    for thtext in thtexts: 
        cogs = cognatesTH(thtext)
        if len(cogs) > 0:
            all_cogs.extend(cogs)
            cognates[no] = cogs
        no = no + 1
    
    #for k,v in cognates.items():
    #    print(k,v)
    #for c in all_cogs:
    #    print(c)    
    
    num = 0
    en_cogs = {}
    matched = []
    for entext in entexts:
        cog = cognatesEN(entext,all_cogs)
        if len(cog) > 0:
            matched.extend(cog)
            en_cogs[num] = cog
        num = num + 1
    
    #for k,v in en_cogs.items():
    #    print(k,v)
    
    #    th_in = [k for k, v in cognates.items() if v == c]
    #    en_in = [k for k, v in en_cogs.items() if v == c]
    
    th_in = [] 
    en_in = [] 
    matches = {} 
     
    for c in matched:
        en_key = -1
        th_key = -1
        for k1,vs in cognates.items():
            for v in vs:
                if v == c:
                    th_key = k1
                    th_in.append(k1) 
                    
        for k2,vs in en_cogs.items():
            for v in vs:
                if v == c:
                    en_key = k2
                    en_in.append(k2) 
                    
        #print(c,en_key,th_key)
        if en_key != -1 and th_key != -1:        
            pair = en_key,th_key
            matches[pair] = c
    
#    for k,v in matches.items():
#        print(k,v) 
    return matches
        
def check_in_both(th1,en1,th2,en2):   
    new_en1 = []
    new_en2 = []
    new_th1 = []
    new_th2 = []
    
    #compare en
    for paths in en1:
        path = re.sub('text','sent',paths)
        if path in en2:
            #print (paths,path)
            new_en1.append(paths)
            new_en2.append(path)
            
    #compare th
    for paths in th1:
        path = re.sub('text','sent',paths)
        if path in th2:
            #print (paths,path)
            new_th1.append(paths)
            new_th2.append(path)        
    
    return new_th1,new_en1,new_th2,new_en2

def get_text(f): 
    
    count = 1 
    text = {}       
    with open(f,encoding="utf-8") as nwfp: 
        for line in nwfp:
            line = line.strip()
            if len(line) > 0:
                text[count] = line
                count = count + 1                                     
    return text

def calc_with_text(en1,th1):
       
    for i in range(len(en1)):
        en_textO = get_text(en1[i])   
        th_textO = get_text(th1[i])
        
        entexts = en_textO.values()
        thtexts = th_textO.values()
        print(en1[i],th1[i])
        matches = find_cogs(thtexts,entexts)       
        
def test_cogs():
    file_folder = "corpus_files" 
    th1,en1,_ = fhand.get_files(file_folder)
        
#    file_folder2 = "correct_files"
#    th2,en2,_ = fhand.get_files(file_folder2)
#    th1,en1,th2,en2 = check_in_both(th1,en1,th2,en2)
    
    for i in range(len(th1)):
        th1[i] = file_folder + "\\" + th1[i]
    for i in range(len(en1)):
        en1[i] = file_folder + "\\" + en1[i]
#    for i in range(len(th2)):
#        th2[i] = file_folder2 + "\\" + th2[i]
#    for i in range(len(en2)):
#        en2[i] = file_folder2 + "\\" + en2[i]
    
    #print(en1,en2,th1,th2)
    calc_with_text(en1,th1)  
    
test_cogs()