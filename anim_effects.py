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

def text_anim(text,video_number):
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


all_dict=[{'title':"कॉपर कैन्यन, सिएरा माद्रे, मेक्सिको ।", 'desc':"नॉर्थ अमेरिका की सबसे गहरी घाटियों में से एक यूरीक कैन्यन, अमेरिका के सिएरा माद्रे में स्थित कॉपर कैन्यन का ही हिस्सा है। 1870 मीटर गहराई के साथ ये घाटी अरिजोना की ग्रांड कैन्यन की गहराई के लगभग बराबर है।"},
          {'title': "ड्रेकेन्सबर्ग, साउथ अफ्रीका ।",  'desc':"अफ्रीका में ड्रैगन्स माउंटेन के नाम से फेमस ड्रेकेन्सबर्ग दुनिया के कुछ सबसे बेहतरीन सीनरी वाली जगहों में शामिल है। चार घाटियों से मिलकर बने इस माउंटेन की कुल ऊंचाई करीब 1500 मीटर है। हर घाटी की कुछ ना कुछ अलग खूबियां हैं जिसे नजरअंदाज करना बेहद मुश्किल है।"},
          {'title':"एंटीलोप कैनियन, एरिज़ोना ।", 'desc':"एंटेलोप कैनियन अमेरिकी दक्षिण पश्चिम में एक स्लॉट कैनियन (और गंभीर इंस्टाग्राम डार्लिंग) है। इसका नवाजो नाम उस स्थान पर अनुवाद करता है जहां पानी चट्टानों से गुजरता है ।"}]


video_number =0
for i in all_dict:
    text_anim(i['title'],video_number)
    video_number+= 1
    