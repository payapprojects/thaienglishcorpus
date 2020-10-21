import re

#cognates ##################################################################
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
    
    num = 0
    en_cogs = {}
    matched = []
    for entext in entexts:
        cog = cognatesEN(entext,all_cogs)
        if len(cog) > 0:
            matched.extend(cog)
            en_cogs[num] = cog
        num = num + 1
    
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
    
    return matches

def tweak(pairs):
    
    A = []
    B = []
    temp = [seq[0] for seq in pairs]
    temp2 = [seq[1] for seq in pairs]
    
    A = []
    for i in range(len(temp)):
        c = temp.count(temp[i])
        if c == 1:
            c2 = temp2.count(temp2[i])
            if c2 == 1:
                A.append(temp[i])     
    
#    #get simple, single pairs - longer list
    B = [seq[1] for seq in pairs if seq[0] in A]
    #print (B)
#    

    for i in range(1,len(A)):
        #print(A[i],A[i-1],B[i],B[i-1])
        x = A[i] - A[i-1]
        y = B[i] - B[i-1]        
        if x > 1 and y == x:
            #print("diff",x)
            for j in range(1,x):
                A.append(A[i]-j)
                B.append(B[i]-j)
    
    A.sort()
    B.sort()  
    
    answer = []
    for i in range(len(A)):
        pair = A[i],B[i]
        if pair not in answer:
            answer.append(pair)
                
    return answer

def find_multiple(ordered,cogs):
    longest = 0        
    for k,v in cogs.items():
        if len(v) > longest:
            longest = len(v)
            
    for i in range(longest,1,-1):
        for k,v in cogs.items():
            if len(v) == i:
                ordered.append(k)
    
    for item in ordered:
        if item in cogs.keys(): 
            cogs.pop(item)

    return ordered,cogs

def find_mixed(ordered,cog):
    
    longest = 0
    temp1 = {}
    temp2 = {}      
    for k,v in cog.items():
        value = v[0]
        if value.isdigit():
            #print (k,v)
            temp1[k] = v
        else:
            #print ("not",k,v)
            temp2[k] = v
            if len(value) > longest:
                longest = len(value)
                
    for i in range(longest,0,-1):
        for k,v in temp2.items():
            if len(v) == i:
                ordered.append(k) 

    longest = 0      
    for k,v in temp1.items():
        value = v[0]
        if len(value) > longest:
            longest = len(value)
            
    for i in range(longest,0,-1):
        for k,v in temp1.items():
            if len(v) == i:
                ordered.append(k)
            
    return ordered

def check_weak(ordered,strong):
     
    ordered = strong + ordered
    strong = []
    num1 = []
    num2 = []
    for pair in ordered:
        num1.append(pair[0])
        num2.append(pair[1])

    duplicates1 = []
    duplicates2 = []

    for value in num1:
      if num1.count(value) > 1:
        if value not in duplicates1:
          duplicates1.append(value)
          
    for value in num2:
      if num2.count(value) > 1:
        if value not in duplicates2:
          duplicates2.append(value)
  
    weak = []
    for pair in ordered:
        if pair[0] in duplicates1 or pair[1] in duplicates2:
            weak.append(pair)
        else:
            strong.append(pair)
       
    return weak,strong

def order_cogs(cogs):
    
    strong = []
    ordered = []
    weak = []
    #find strong
    strong,cogs = find_multiple(strong,cogs)
    ordered = find_mixed(ordered,cogs)
    weak,strong = check_weak(ordered,strong)
    #print(strong)
            
    matches = tweak(strong)
    #return strong,weak
    return strong,matches

# anchor points #############################################################
def find_anchor_point(en,th):
    
    cogs = find_cogs(th,en)
    strong,matches = order_cogs(cogs)
            
    return strong

def get_anchors(th,en):
    #anchors = [(3,2),(6,5)]
    anchors = find_anchor_point(en,th) 
    #print(anchors)
    return anchors 
    
#alignment module ###########################################################
    
def compare_lists(x,y):
    total = 0
    average = 0
    for i in range(len(y)):
        diff = abs(x[i]-y[i])
        total = total + diff
        if total != 0:
            average = total / len(y)
    return average
    
def get_best_match(cand,y):
    lowest = None
    for c in range(len(cand)):
        score = compare_lists(cand,y)
        if lowest is None or score < lowest:
            lowest = score
    return lowest

def remove_one(x,y):
    cand = []
    for c in range(len(x)):
        temp = x[:]
        temp.pop(c)
        cand.append(temp)

    lowest = None
    
    for c in cand:
        score = get_best_match(c,y)
        if lowest is None or score < lowest:
            lowest = score
            x = c[:] 
            
    return x,y

def calc_best(x,y):
    
    bl_x = x.count("")
    bl_y = y.count("")
    diff = len(x) - bl_x - len(y) - bl_y    
    for d in range(diff):
        x,y = remove_one(x,y)
    return x,y

#dealing with removal
def removals(en,texts,lengths):
    
    want = len(lengths)
    good_text = []
    for t in texts:
        if len(lengths) > 0:
            if len(t) == lengths[0]:
                good_text.append(t)
                lengths.pop(0)
        
    if want != len(good_text):
        print(len(lengths),len(good_text))
    else:
        return en,good_text

#dealing with non-removal
def spaced(en,th,x,y):
    
    new_th = []
    index = 0
    for i in range(len(en)):
        if index < len(x):
            if len(en[i]) == x[index]: 
                new_th.append(th[index])
                index = index+1
            else:           
                new_th.append("")
    return new_th,en
            
#original alignment module   
def align2(th,en):
    longs = []
    shorts = []
    long = len(en)
    short = len(th)
    if len(th) > long:
        long = len(th)
        short = len(en)    
        for i in range(long):
            longs.append(len(th[i]))
            if i < short:
                shorts.append(len(en[i]))
    else:
        for i in range(long):
            longs.append(len(en[i]))
            if i < short:
                shorts.append(len(th[i]))
                
    x,y = calc_best(longs,shorts)              
   
    if len(th) > len(en):
        en,th = removals(en,th,x)
    else:
        th,en = spaced(en,th,x,y)
        
    return th,en

def split(anchors,th,en):

    options = len(anchors)
    #print(options)
    if options == 0:
        new_th,new_en = align2(th,en)
        #print(0)
    elif options == 1:
        pair = anchors[0]
        e_p = pair[0]
        th_p = pair[1]        
        #get before
        en1 = en[:e_p]
        th1 = th[:th_p]
        th1,en1 = align2(th1,en1) 
        #get after
        en2 = en[e_p+1:]
        th2 = th[th_p+1:]
        th2,en2 = align2(th2,en2)  
        
        new_en = []
        new_th = []
        #add before
        new_en.extend(en1)
        new_th.extend(th1)
        #add anchor
        new_en.append(en[e_p])
        new_th.append(th[th_p])
        #add after
        new_en.extend(en2)    
        new_th.extend(th2)
    else:
        pair1 = anchors[0]        
        pair2 = anchors[1]
        e_p = pair1[0]
        th_p = pair1[1]  
        e_p2 = pair2[0]
        th_p2 = pair2[1]

        #print(e_p,e_p2,th_p,th_p2)        
        
        #get before
        en1 = en[:e_p]
        th1 = th[:th_p]
        th1,en1 = align2(th1,en1)         
        #get middle
        en3 = en[e_p+1:e_p2]
        th3 = th[th_p+1:th_p2]
        th3,en3 = align2(th3,en3)  
        #get after
        en2 = en[e_p2+1:]
        th2 = th[th_p2+1:]
        th2,en2 = align2(th2,en2)  
        
        new_en = []
        new_th = []
        #add before
        new_en.extend(en1)
        new_th.extend(th1)
        #add anchor
        new_en.append(en[e_p])
        new_th.append(th[th_p])
        #add middle
        new_en.extend(en3)    
        new_th.extend(th3)
        #add anchor
        new_en.append(en[e_p2])
        new_th.append(th[th_p2])
        #add after
        new_en.extend(en2)    
        new_th.extend(th2)
       
    return new_th,new_en

def alignCogs(th,en):
    anchors = get_anchors(th,en) 
    th,en = split(anchors,th,en)
    return th,en    