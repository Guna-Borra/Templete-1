import requests
import re
import json
import time
import logging
from fake_useragent import UserAgent
import itertools
import spacy
from googletrans import Translator
#from download_images import *
from each_video_generation import *

#from anim_effects import *

ua = str(UserAgent().random)



#######cool_effects
import numpy as np
from moviepy.editor import *
from moviepy.video.tools.segmenting import findObjects

# WE CREATE THE TEXT THAT IS GOING TO MOVE, WE CENTER IT.


# THE NEXT FOUR FUNCTIONS DEFINE FOUR WAYS OF MOVING THE LETTERS


# helper function
rotMatrix = lambda a: np.array( [[np.cos(a),np.sin(a)], 
                                 [-np.sin(a),np.cos(a)]] )

def vortex(screenpos,i,nletters):
    d = lambda t : 1.0/(0.3+t**16) #damping
    a = i*np.pi/ nletters # angle of the movement
    v = rotMatrix(a).dot([-1,0])
    if i%2 : v[1] = -v[1]
    return lambda t: screenpos+400*d(t)*rotMatrix(0.5*d(t)*a).dot(v)
    
def cascade(screenpos,i,nletters):
    v = np.array([0,-1])
    d = lambda t : 1 if t<0 else abs(np.sinc(t)/(1+t**4))
    return lambda t: screenpos+v*400*d(t-0.15*i)

def arrive(screenpos,i,nletters):
    v = np.array([-1,0])
    d = lambda t : max(0, 3-3*t)
    return lambda t: screenpos-400*v*d(t-0.2*i)
    
def vortexout(screenpos,i,nletters):
    d = lambda t : max(0,t) #damping
    a = i*np.pi/ nletters # angle of the movement
    v = rotMatrix(a).dot([-1,0])
    if i%2 : v[1] = -v[1]
    return lambda t: screenpos+400*d(t-0.1*i)*rotMatrix(-0.2*d(t)*a).dot(v)

def moveLetters(letters, funcpos):
    return [ letter.set_pos(funcpos(letter.screenpos,i,len(letters)))
              for i,letter in enumerate(letters)]
    
def convert_errors(title):
    new_t=[]
    n_t= title.encode('unicode-escape').split(b'\\')
    if n_t[0]== (b'u093f'):
        n_t.insert(0,'\u200c')
    for c,i in enumerate(n_t):
        if i==(b'u093f') : #and n_t[-1] != (b'u093f')
            new_t.append(i)
            new_t[c]=n_t[c-1]
            new_t[c-1]=(b'u093f')
        else:
            new_t.append(i)
            new_string=((b'\\').join(new_t))
            new_string=new_string.decode('unicode-escape')
    
    if n_t[-1] == (b'u093f'):
        new_string=((b'\\').join(new_t))
        new_string=new_string.decode('unicode-escape')
    
    return new_string

screensize = (1920,800)

def text_anim(text,title_number):
    txtClip = TextClip(convert_errors(text),color='white', font="Mangal.ttf",
                       kerning =5, fontsize=100)
    cvc = CompositeVideoClip( [txtClip.set_pos('center')],
                            size=screensize)
    
    # WE USE THE PLUGIN findObjects TO LOCATE AND SEPARATE EACH LETTER
    
    letters = findObjects(cvc) # a list of ImageClips
    
    
    # WE ANIMATE THE LETTERS
    
    
    clips = [ CompositeVideoClip( moveLetters(letters,funcpos),
                                  size = screensize).subclip(0,3)#video duration
              for funcpos in [vortex] ]
    
    # WE CONCATENATE EVERYTHING AND WRITE TO A FILE
    
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile('top'+str(video_number)+'.mp4',fps=25,codec='mpeg4')


# =============================================================================
# all_dict=[{'title':"कॉपर कैन्यन, सिएरा माद्रे, मेक्सिको ।", 'desc':"नॉर्थ अमेरिका की सबसे गहरी घाटियों में से एक यूरीक कैन्यन, अमेरिका के सिएरा माद्रे में स्थित कॉपर कैन्यन का ही हिस्सा है। 1870 मीटर गहराई के साथ ये घाटी अरिजोना की ग्रांड कैन्यन की गहराई के लगभग बराबर है।"},
#           {'title': "ड्रेकेन्सबर्ग, साउथ अफ्रीका ।",  'desc':"अफ्रीका में ड्रैगन्स माउंटेन के नाम से फेमस ड्रेकेन्सबर्ग दुनिया के कुछ सबसे बेहतरीन सीनरी वाली जगहों में शामिल है। चार घाटियों से मिलकर बने इस माउंटेन की कुल ऊंचाई करीब 1500 मीटर है। हर घाटी की कुछ ना कुछ अलग खूबियां हैं जिसे नजरअंदाज करना बेहद मुश्किल है।"},
#           {'title':"एंटीलोप कैनियन, एरिज़ोना ।", 'desc':"एंटेलोप कैनियन अमेरिकी दक्षिण पश्चिम में एक स्लॉट कैनियन (और गंभीर इंस्टाग्राम डार्लिंग) है। इसका नवाजो नाम उस स्थान पर अनुवाद करता है जहां पानी चट्टानों से गुजरता है ।"}]
# 
# 
# video_number =0
# for i in all_dict:
#     text_anim(i['title'],video_number)
#     video_number+= 1
# =============================================================================
    
def proxy():
    response = requests.get("https://www.proxy-list.download/api/v1/get?type=http&a}non=elite&country=ru")
    proxy = (response.text)
    proxt_list = proxy.split('\r\n')
    proxy_dict = dict(itertools.zip_longest(*[iter(proxt_list)] * 2, fillvalue=""))
    return proxy_dict

proxy_dict = proxy()

def get_transalation(text1):
    final_text=[]
    try:
        text1= text1.replace('।','.')
        text1=text1.split('.')
        translator = Translator(service_urls=['translate.google.co.in', 'translate.google.com'], user_agent=ua, proxies=proxy_dict)
        for txt in text1:
            transalation1= translator.translate(txt, dest="en" )
            eng_text= transalation1.text
            final_text.append(eng_text)

        final_text=('. '.join(final_text))
        
        return final_text

    except Exception as e:
        print(e)
        pass


def urlfinder(keywords):
    keywords=keywords
    logging.basicConfig(level=logging.DEBUG);
    logger = logging.getLogger(__name__)
   
    def search(keywords, max_results=None):
        url = 'https://duckduckgo.com/';
        params = {
        'q': keywords
        };
   
        logger.debug("Hitting DuckDuckGo for Token");
   
        #   First make a request to above URL, and parse out the 'vqd'
        #   This is a special token, which should be used in the subsequent request
        res = requests.post(url, data=params)
        searchObj = re.search(r'vqd=([\d-]+)\&', res.text, re.M|re.I);
   
        if not searchObj:
            logger.error("Token Parsing Failed !");
            return -1;
   
        logger.debug("Obtained Token");    
        headers = {
            'dnt': '1',
            #'accept-encoding': 'gzip, deflate, sdch, br',
            'x-requested-with': 'XMLHttpRequest',
            'accept-language': '*',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'referer': 'https://duckduckgo.com/',
            'authority': 'duckduckgo.com',
        }
   
        params = (
        ('l', 'wt-wt'),
        ('o', 'json'),
        ('q', keywords),
        ('vqd', searchObj.group(1)),
        ('f', ',,,'),
        ('p', '2')
        )
   
        requestUrl = url + "i.js";
   
        logger.debug("Hitting Url : %s", requestUrl);
        i=0
        while i<10:
            j=0
            while j<10:
                try:
                    res = requests.get(requestUrl, headers=headers, params=params);
                    data = json.loads(res.text);
                    break;
                except ValueError as e:
                    logger.debug("Hitting Url Failure - Sleep and Retry: %s", requestUrl);
                    time.sleep(0.7);
                    continue;
                j=j+1  
            logger.debug("Hitting Url Success : %s", requestUrl);
            printJson(data["results"]);
           
            i=i+1
   
            #requestUrl = url + data["next"];
    imageurl=[]
    specs=[]
    title=[]
    def printJson(objs):
        for obj in objs:
            specs.append(("Width {0}, Height {1}".format(obj["width"], obj["height"])))
            #print("Thumbnail {0}".format(obj["thumbnail"]))
            #print("Url {0}".format(obj["url"]))
            title.append( ("Title {0}".format(obj["title"].encode('utf-8'))))
            #print ("Image {0}".format(obj["image"]))
            imageurl.append((obj["image"]))          
   
    #print(search("अजित पवार के इस्तीफा देने के बाद"))
    search(keywords)
    print(imageurl)
    return imageurl[:10],specs[:10],title[:10]

def multiple_video(title,desc):
    eng_text= get_transalation(title)
    get_urls =urlfinder(eng_text)
    result_links = get_urls[0]
    req_video = Video_Processing(result_links,title,desc)


all_sent ={}
  
   
video_Title= "दुनिया में top 3 sceneries ।"

all_dict=[{'title':"कॉपर कैन्यन, सिएरा माद्रे, मेक्सिको ।", 'desc':"नॉर्थ अमेरिका की सबसे गहरी घाटियों में से एक यूरीक कैन्यन, अमेरिका के सिएरा माद्रे में स्थित कॉपर कैन्यन का ही हिस्सा है। 1870 मीटर गहराई के साथ ये घाटी अरिजोना की ग्रांड कैन्यन की गहराई के लगभग बराबर है।"},
          {'title': "ड्रेकेन्सबर्ग, साउथ अफ्रीका ।",  'desc':"अफ्रीका में ड्रैगन्स माउंटेन के नाम से फेमस ड्रेकेन्सबर्ग दुनिया के कुछ सबसे बेहतरीन सीनरी वाली जगहों में शामिल है। चार घाटियों से मिलकर बने इस माउंटेन की कुल ऊंचाई करीब 1500 मीटर है। हर घाटी की कुछ ना कुछ अलग खूबियां हैं जिसे नजरअंदाज करना बेहद मुश्किल है।"},
          {'title':"एंटीलोप कैनियन, एरिज़ोना ।", 'desc':"एंटेलोप कैनियन अमेरिकी दक्षिण पश्चिम में एक स्लॉट कैनियन (और गंभीर इंस्टाग्राम डार्लिंग) है। इसका नवाजो नाम उस स्थान पर अनुवाद करता है जहां पानी चट्टानों से गुजरता है ।"}]


all_video_names = []
title_number = 0
for each_dict in all_dict:
    video_title = each_dict['title']
    video_desc = each_dict['desc']
    #print('\n'+post_text+'\n')
    eng_text= get_transalation(video_title)
    get_urls=[]
    get_urls =urlfinder(eng_text)
    result_links = get_urls[0]
    if len(result_links)>0:
        file_name = Video_Processing(result_links,video_title,video_title)
        title_anim =text_anim(video_title,title_number)
        all_video_names.append(file_name)
        
        
        
        split_name = file_name.split('.')[0]+ '_int.ts'
        intermediate_names.append(split_name)
        convert_command = convert_command + split_name + '|'
        command = 'ffmpeg -i '+ file_name + ' -c copy -bsf:v h264_mp4toannexb -f mpegts '+ split_name
        os.system(command)
        
        