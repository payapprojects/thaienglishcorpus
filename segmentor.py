import segment_english as engseg
import segment_thai as thseg

def segment_en(t):
    sents = engseg.split_into_sentences(t)
    mytext = []
    for sen in sents:
        mytext.append(str(sen))
    return mytext,sents

def segmentS(s_th_text,s_en_text):
    en_text,sents = segment_en(s_en_text)
    total = 0
    for et in en_text:
        total = total + len(et)        
    th_text = thseg.segment_by_spaces(s_th_text,sents,total)
    return th_text,en_text    

def segmentP(th_texts,en_texts):
    en_text = []
    th_text = []
    
    for i in range(len(en_texts)):
        new = []
        new2 = []
        text = en_texts[i]
        new,sents = segment_en(text)
        en_text.extend(new)
                
        if i < len(th_texts):            
            s_th_text = th_texts[i]
            if len(new) == 1:
                new2.append(s_th_text)
            else:
                new2 = thseg.segment_by_spaces(s_th_text,sents,len(text))
            th_text.extend(new2)    
        
    return th_text,en_text

#original Thai segmentation #################################################
#from thai_segmenter import sentence_segment
#
#def split_into_thai_sentences(text):
#    sentences = sentence_segment(text)        
#    return sentences

#def segment_th(text):
#    sents = split_into_thai_sentences(text) 
#    mytext = []
#    for sen in sents:
#        if len(str(sen)) > 2:
#            mytext.append(str(sen))
#    return mytext
    
#def segment(s_th_text,s_en_text):
#    th_text = segment_th(s_th_text)  
#    en_text,_ = segment_en(s_en_text)   
#    return th_text,en_text

#def segmentTH(th_text):
#    ret_text = []
#    new = []
#    for text in th_text:
#        new = segment_th(text)
#        ret_text.extend(new)    
#    return ret_text

#def segmentE(en_text):
#    ret_text = []
#    new = []
#    for text in en_text:
#        new,_ = segment_en(text)
#        ret_text.extend(new)    
#    return ret_text
