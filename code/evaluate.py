import file_handling as fhand
import re

out_file = "results.csv" 

def get_source(text):
    
    sources = ['apple','bc','bum', 'intel','kmutnb','krungthai', 'phya','scb','thaithesis','tt']
    for s in sources:
        if s in text:
            source = s
    return source

def compare(A,B):

    answer = []
    gap = abs(len(A) - len(B))
    if gap < 2: gap = 2
    #print(gap)
    begin = -1
    for i in range(len(A)):
        found = 0
        for j in range(-gap,gap+1): 
            if i+j > begin and i+j < len(B) and found == 0:
                z = 1
                if A[i] == B[i+j]:
                    begin = i + j
                    found = 1
                    pair = (i,i+j,z)
                    if j > gap/2:
                        gap = gap + 1
                    answer.append(pair)
                    continue  
    return answer        

def compareT(A,B,cor_pair):

    answer = []
    gap = abs(len(A) - len(B))
    if gap < 2: gap = 2
    begin = -1
    for i in range(len(A)):
        found = 0
        for j in range(-gap,gap+1): 
            if i+j > begin and i+j < len(B) and found == 0:

                texts = A[i],B[i+j]
                if texts in cor_pair:
                    begin = i + j
                    found = 1
                    pair = (i,i+j)
                    if j > gap/2:
                        gap = gap + 1
                    answer.append(pair)
                    continue  
    return answer

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
    texts = []       
    with open(f,encoding="utf-8") as nwfp: 
        for line in nwfp:
            line = line.strip()
            if len(line) > 0:
                text[count] = line
                texts.append(line)
                count = count + 1                                     
    return text,texts
        
def calc_with_text(en1,en2,th1,th2,out_file):
       
    for i in range(len(en1)):
        en_textO,Xen = get_text(en1[i])   
        en_textC,Yen = get_text(en2[i])
        th_textO,Xth = get_text(th1[i])
        th_textC,Yth = get_text(th2[i])
        s = get_source(en1[i])
        temp = re.search('\d+',en1[i])
        ref =temp.group(0)
        
        aligned = []        
        match = []
        posE = {}
        for key,value in en_textO.items():
            #print(key,value)
            for k,v in en_textC.items():
                #print(k,v)
                if value == v:
                    match.append(key)
                    posE[key] = k
                    if k==key:
                        aligned.append(key)
                    break
        ans = []
        ans = compare(Xen,Yen)
        
        matchTH = []
        alignedTH = []
        posTH = {}
        for key,value in th_textO.items():
            for k,v in th_textC.items():
                #print("text",value)
                if value == v:
                    matchTH.append(key)
                    posTH[key] = k
                    if k==key:
                        alignedTH.append(key)
                    break      
        ans1 = []
        ans1 = compare(Xth,Yth)

        if len(Yen) != len(Yth):
            if len(Yen) > len(Yth):
                diff = len(Yen) - len(Yth)
                for i in range(diff):
                    Yth.append(Yth[-1])
            else:
                diff = len(Yth) - len(Yen)
                for i in range(diff):
                    Yen.append(Yen[-1])                                
                    
        cor_pair = []
        for i in range(len(Yen)):
                pair = (Yen[i],Yth[i])
                cor_pair.append(pair)  
        pairs = compareT(Xen,Xth,cor_pair)
        
        #print(len(Yen),len(match),len(matchTH),len(ans),len(ans1),len(pairs))                
       
        towrite = ""
        #print(s,ref,len(en_textO),len(en_textO),len(match),len(aligned),len(th_textO),len(th_textO),len(matchTH),len(alignedTH))
        towrite = s + ',' + str(ref) + ',' + str(len(en_textO)) + ',' + str(len(en_textC)) + ',' + str(len(match)) + ',' + str(len(ans))
        towrite = towrite + ',' + str(len(th_textO)) + ',' + str(len(th_textC)) + ',' + str(len(matchTH)) + ',' + str(len(ans1))
        towrite = towrite + ',' + str(len(pairs))  + "\n"
        
        #out_file = "new_results.csv"
        with open(out_file,'a',encoding="utf-8") as fh2:
            fh2.write(towrite)
            
#evaluate 
def evaluate(out_file):
    file_folder = "corpus_files" 
    th1,en1,_ = fhand.get_files(file_folder)
        
    file_folder2 = "correct_files"
    th2,en2,_ = fhand.get_files(file_folder2)
    th1,en1,th2,en2 = check_in_both(th1,en1,th2,en2)
    for i in range(len(th1)):
        th1[i] = file_folder + "\\" + th1[i]
    for i in range(len(en1)):
        en1[i] = file_folder + "\\" + en1[i]
    for i in range(len(th2)):
        th2[i] = file_folder2 + "\\" + th2[i]
    for i in range(len(en2)):
        en2[i] = file_folder2 + "\\" + en2[i]
     
    calc_with_text(en1,en2,th1,th2,out_file)

evaluate(out_file)

