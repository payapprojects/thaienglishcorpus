import re
import file_handling as fhand
import extract as ex
import segmentor as seg
import aligner as ali

file_folder = 'html_files'            
#################################################
def get_source(filname):
    
    source = "unfound"
    temp = re.findall('(^.+?)\_',filname)
    if len(temp) > 0:
        source = temp[0]
    path = file_folder + "/" + filname
    return source,path
       
#################################################
def process_singles(singles):
    
    for filename in singles:   
        source,path = get_source(filename)
        #extraction
        s_th_text,s_en_text = ex.extractor_single(path,source)
        #deal with files without both languages
        if s_th_text != "failed extraction" and s_en_text != "failed extraction":
            #segment  into sentences
            th_text,en_text = seg.segmentS(s_th_text,s_en_text)
            #align with sign posts
            th_text,en_text = ali.alignCogs(th_text,en_text)
            #print results to individual files
            fhand.print_results(filename,source,th_text,en_text)            
            print(filename,source,',',len(en_text),',',len(th_text))

def process_pairs(th,en):    
                    
    rep = []
    #get English files first for segmentation reasons
    for i in range(len(en)):
        filename = en[i]
        source,path = get_source(filename)
        #extraction
        en_text,rep = ex.extractor(path,source,rep) 
         
        #Thai files
        filename2 = th[i]   
        source2,path2 = get_source(filename2)
        #extraction
        th_text,rep = ex.extractor(path2,source2,rep)
        #align segments
        th_text,en_text = ali.alignCogs(th_text,en_text)
        #segment into sentences       
        th_texts,en_texts = seg.segmentP(th_text,en_text)                     
        #align sentences with sign posts
        th_texts,en_texts = ali.alignCogs(th_texts,en_texts)
        #print results to individual files
        fhand.print_resultsE(filename,source,en_texts)
        fhand.print_resultsTH(filename2,source2,th_texts)        
        print(filename,',',len(en_text),',',len(th_text),',',len(en_texts),',',len(th_texts))

#########################################################################
def main():
    if __name__== "__main__" :
        th,en,singles = fhand.get_files(file_folder)
        process_singles(singles)
        process_pairs(th,en)
    
main()






