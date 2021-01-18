import re

#Thai text space analysis ###################################################
def get_terms():
    civil = ['นายอำเภอ','นอภ.','นายกเทศมนตรี','รองเทศมนตรี','ปลัดเทศบาล','กำนัน']#'ผู้ใหญ่บ้าน',
    air = ['จ่าอากาศตรี','จ่าอากาศโท','จ่าอากาศเอก','พันจ่าอากาศตรี','พันจ่าอากาศโท','พันจ่าอากาศเอก','เรืออากาศตรี','เรืออากาศโท','เรืออากาศเอก','นาวาอากาศตรี','นาวาอากาศโท','พลอากาศตรี','นาวาอากาศเอก','พลอากาศโท','พลอากาศเอก','จอมพลอากาศ','ผู้บัญชาการทหารอากาศ']
    navy = ['พลทหาร','จ่าตรี','จ่าโท','จ่าเอก','พันจ่าตรี','พันจ่าโท','พันจ่าเอก','เรือตรี','เรือโท','เรือเอก','นาวาตรี','นาวาโท','นาวาเอก','พลเรือตรี','พลเรือโท','พลเรือเอก','จอมพลเรือ','ผู้บัญชาการทหารเรือ']
    police = ['พลตำรวจ','สิบตำรวจโท','สิบตำรวจเอก','สิบตำรวจตรี','จ่าสิบตำรวจ','ดาบตำรวจ','ร้อยตำรวจตรี','ร้อยตำรวจโท','ร้อยตำรวจเอก','พันตำรวจตรี','พันตำรวจโท','พันตำรวจเอก','พลตำรวจตรี','พลตำรวจโท','พลตำรวจเอก','ผู้นำสีกากี']	
    army = ['พลทหาร','สิบตรี','สิบโท','สิบเอก','จ่าสิบตรี','จ่าสิบโท','จ่าสิบเอก','ร้อยตรี','ร้อยโท','ร้อยเอก','พันตรี','พันโท','พันเอก','พลตรี','พลโท','พลเอก','จอมพล','ผู้บัญชาการทหารบก']
    other = ['นาย','น.ส.','นางสาว','พ.ต.อ.','พันตำรวจเอก','พล.ต.อ.','พลตำรวจเอก','พ.ต.ท.','พันตำรวจโท','พล.ต.ต.','พลตำรวจตรี','พล.อ.','พลเอก','จ.ท.','จ่าอากาศโท','จ.อ.','จ่าอากาศเอก','ผบ.สส.','ผู้บัญชาการทหารสูงสุด','นายทหารพระธรรมนูญ','นายกฯ','นายกรัฐมนตรี','รมว.','รัฐมนตรีว่าการ','รมช.','รัฐมนตรีช่วยว่าการ']
    terms = police + army + navy + air + civil + other
    return terms

def check_space(pos,text2):
    ans = 0
    afternum = ['น.','บาท','เวลา','ล้านคน','คน','ปี']
    months = ['ม.ค.','มกราคม','ก.พ.','กุมภาฯ','กุมภาพันธ์','มี.ค.','มีนาคม','เม.ย.','เมษายน''พฤษภา','พฤษภาคม','พ.ค.','มิ.ย.','มิถุนายน','กรกฎาคม','สิงหาคม','กันยายน','ตุลาคม','พฤศจิกายน','ธันวาคม','ก.ค.','ส.ค.','ราชสีห์','ก.ย.','ต.ค.','พ.ย.','ธ.ค.']
    #terms = get_terms()
    after = text2[pos:]
    before = text2[:pos+1]
    if pos < len(text2)-1:
        #print (text2[pos+1],after)
        if text2[pos+1] == 'ๆ':
            #print(text2[pos],text2[pos+1])
            ans = 1
#        elif text2[pos-1] == "-" or text2[pos-1] == ")":
#            ans = 1
        elif text2[pos-1].isdigit():
            #print(text2[pos-1],text2[pos],text2[pos+1],after[:7])
            for pat in afternum:
                if pat in after[:7]:
                    #print("found",text2[pos-1],pat)
                    ans = 1
                    break  
            for pat in months:
                if pat in after[:12]:
                    #print("found",text2[pos-1],pat)
                    ans = 1
                    break  
        elif text2[pos+1].isdigit():
#            if text2[pos+2] != "." and text2[pos+3] != " ":
#                ans = 1
            for pat in months:
                if pat in before[12:]:
                    #print("found",text2[pos+1],pat)
                    ans = 1
                    break
#        else:
#            for pat in terms:
#                if pat in before[20:]:
#                    #print("found",pat)
#                    ans = 1
#                    break                               
    return ans

def closest(alist, Number):
    aux = []
    for valor in alist:
        aux.append(abs(Number-valor))
        
    ret_value = int(Number)
    if aux.index(min(aux)):
        ret_value = aux.index(min(aux))
    return ret_value

def segment_by_spaces(th_text,sents,total):
    
    percs = []
    #total = len(en)
    sb = 0
    
    for sen in sents:
        sb = sb + len(str(sen))
        perc = sb / total
        #print(total,sb,perc)
        percs.append(perc)
    
    #print(percs)    
    #get spaces in thai text
    #chars = 0
    spaces = []
#    for ch in th_text:
#        if ch == " ":
#            cont = check_space(char+1,th_text)
#            if cont != 1:            
#                spaces.append(chars+1)                  
#        chars +=1
        
    cont = 0        
    for m in re.finditer(' ', th_text):
        cont = check_space(m.start(),th_text)
        if cont != 1:
            spaces.append(m.start()) 
    
    #print(len(spaces))                    
    #calcualte candidate breaks
    total_th = len(th_text)
    cand = []
    for p in percs:
        cand.append(p*total_th)
    #print(len(sents),len(cand),len(spaces))  
    
    mytext = []
    if len(spaces) < len(sents) - 1:
        mytext.append(th_text)
    elif len(spaces) == len(sents)-1:
        mytext = th_text.split()
    elif len(spaces) == len(sents):
        mytext = th_text.split()        
    else:        
    #get closest space to candidate
        seg_points = []
        
        for c in cand:
            if len(spaces) > 0:
                seg_p = closest(spaces, c)
                if seg_p < len(spaces):
                    seg_points.append(spaces[seg_p])
     
        #print(len(spaces),len(sents),seg_points)
        if len(seg_points) > 0:
        #put Thai text into sentences by seg_point
            if seg_points[-1] != len(th_text):
                seg_points.append(len(th_text))
                
            sentTH = []
            start = 0
            for p in seg_points:
                end = int(p)
                temp = th_text[start:end]
                sentTH.append(temp)
                start = int(p)
                
            mytext  = []
            for sen in sentTH:
                if len(str(sen)) > 0:
                    sent = str(sen)
                    sent = re.sub('^\s+','',sent)
                    if sent:
                        mytext.append(sent)        
        #print (len(sents),len(mysents))
    
    return mytext

#Thai text space analysis ###################################################
