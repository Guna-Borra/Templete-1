from imageai.Detection import ObjectDetection #https://anaconda.org/powerai/imageai
import os
from PIL import Image 
import requests
import re
import math
import shutil
import numpy as np
from pydub import AudioSegment
import natsort
from collections import Counter
import textwrap
from math import floor
from keras.preprocessing import image
import imquality.brisque as brisque
from urllib.parse import urlparse
from os.path import splitext
from google.cloud import texttospeech
from scipy.spatial import distance
#https://anaconda.org/conda-forge/ffmpeg

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/home/Downloads/Video_Generation_Complete/service_account.json"
#client = texttospeech.TextToSpeechClient()

image_dest   =  "1_old_test_1.jpg"
detection_length  = 2 
video_number  = 0 

###########
#Step 1 : 
###########
#Download the images from the result_links list one by one saving the image 
#as 1_old_test_1.jpg and crop them if it is single image and finally delete the image

execution_path = os.getcwd()
detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(execution_path , "yolo.h5"))
detector.loadModel()
custom = detector.CustomObjects(person=True)

def change_position(pos_list11,imag_h):
    final_list= pos_list11
    w=  final_list[2]-final_list[0]
    h=  imag_h
    a_r = w/h
   
    if a_r != 0.56:
        n_width= 0.56*h
        diff= n_width-w
        final_list[0] = final_list[0]- (diff/2)
        final_list[0]=int(final_list[0])
        final_list[2] =final_list[2] +(diff/2)
        final_list[2]=int(final_list[2])
        final_list[1]=0        
        final_list[3]=h
    else:
        pass
    return final_list

def crop(image_dest,pos,image_name):
    im = Image.open(image_dest) 
    left = pos[0]
    top = pos[1]
    right = pos[2]
    bottom = pos[3]
    im1 = im.crop((left, top, right, bottom)) 
    im1.save(image_name)

def image_analysis(image_dest,custom,imag_h):
    global detection_length
    global video_number
    
    detections = detector.detectCustomObjectsFromImage(custom_objects=custom, input_image=os.path.join(execution_path,image_dest), output_image_path=os.path.join(execution_path,"custom2.jpg") ,minimum_percentage_probability=99) 
    
    if len(detections) ==2:  
        a=detections[0]["box_points"][:2]
        b=detections[1]["box_points"][:2]
        distance_two_Objects = distance.euclidean(a, b)   
        if round(distance_two_Objects) >= 250: #Existing logic to crop
            for eachObject in detections:
                pos_list=eachObject["box_points"]
                image_name = str(detection_length) + '.jpg'
                new_pos= change_position(pos_list,imag_h)
                crop(image_dest,new_pos,image_name)
                detection_length = detection_length + 1
                #print("--- Image Cropped Successfully---")
            return detection_length            
        else: #Using center cropping
            img     = Image.open(image_dest) 
            width   = img.width
            height  = img.height
            
            if width >500 and height >500:
                new_width   = min(width, height)    
                new_height  = min(width, height)
            else:
                new_width   = min(width, height)+100    
                new_height  = min(width, height)+100                
            
            left = int(np.ceil((width - new_width) / 2))
            right = width - int(np.floor((width - new_width) / 2))
            top = int(np.ceil((height - new_height) / 2))
            bottom = height - int(np.floor((height - new_height) / 2))
            
            img2 = img.crop((left, top, right, bottom))
            image_name = str(detection_length) + '.jpg'
            img2.save(image_name)
            detection_length = detection_length + 1
            
            return detection_length            
        
    elif len(detections) ==1: 
        for eachObject in detections:
            pos_list=eachObject["box_points"]
            image_name = str(detection_length) + '.jpg'
            new_pos= change_position(pos_list,imag_h)
            crop(image_dest,new_pos,image_name)
            detection_length = detection_length + 1
            #print("--- Image Cropped Successfully---")
        return detection_length
    else:        
        img     = Image.open(image_dest) 
        width   = img.width
        height  = img.height 
        
        new_width   = min(width, height)    
        new_height  = min(width, height)
        
        left = int(np.ceil((width - new_width) / 2))
        right = width - int(np.floor((width - new_width) / 2))
        top = int(np.ceil((height - new_height) / 2))
        bottom = height - int(np.floor((height - new_height) / 2))
        
        img2 = img.crop((left, top, right, bottom))
        #crop(image_dest,new_pos,image_name)
        
        image_name = str(detection_length) + '.jpg'
        img2.save(image_name)
        detection_length = detection_length + 1
        
        return detection_length

def DownloadImages(result_links):
    global detection_length
    global video_number

    for url in result_links: 
        try:
            requests.get(url, stream=True)
        except Exception :
            result = "Connectivity Error"
            result_links.remove(url)    #result_links    
            continue
        
        result1 = requests.get(url, stream=True, headers={})
        if result1.status_code == 200:
            with open(image_dest, 'wb') as f:
                result1.raw.decode_content = True
                shutil.copyfileobj(result1.raw, f)                
            #image2 = result1.raw.read()
            #open(image_dest,"wb").write(image2)   
            try:    
                parsed = urlparse(url)
                root, ext = splitext(parsed.path)
                if ext ==".jpg":                 
                    im = Image.open(image_dest) 
                    imag_w, imag_h  = im.size   
                    detection_length = image_analysis(image_dest,custom,imag_h)
                os.remove(image_dest)     
            except Exception:
                os.remove(image_dest)        
        else:
            result = "Image un-available to Download"
            #print(result)
            
"""def GenerateSpeech(text):
    global video_number
    ###########
    #Step 2 : 
    ###########
    #Here we have BackGround_Music.wav as the news back ground file which needs to be integrated to the speech file generated by gTTS
    #the output of these two is Final_Audio_videoNumber.wav. 
    
    speech_gtts = "speech_gtts"+"_"+str(video_number)+".wav"
    
    # Set the text input to be synthesized
    mytext=text.replace(",",' ,')
    mytext=mytext.replace(".",'''.<break time="300ms"/>''')
    mytext=mytext.replace("।",'''.<break time="300ms"/>''')
    mytext=re.sub(r'([\d])(\s*,\s*)([\d ])',r'\1,\3',mytext)
    mytext=re.sub(r"([^\d]+)(,)([^\d]+)",r'''\1,<break time="150ms"/>\3''', mytext) 
    ssml='''<speak><break time="1.5s"/>'''+mytext+" </speak>"
    input_text = texttospeech.types.SynthesisInput(ssml=ssml)
    
    #synthesis_input = texttospeech.types.SynthesisInput(text=text)
    
    voice = texttospeech.types.VoiceSelectionParams(
        name="hi-IN-Wavenet-A", 
        language_code="hi-IN"
        )
    
    audio_config = texttospeech.types.AudioConfig(speaking_rate=0.95,
        audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        #pitch=1
        )
    
    response = client.synthesize_speech(input_text, voice, audio_config)
    
    with open(speech_gtts, 'wb') as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "speech_gtts"')    
    
    sound = AudioSegment.from_file(speech_gtts)
    sound_BackGround = AudioSegment.from_file('BackGround_Music.wav')
    halfway_point = len(sound) + 150
    first_half = sound_BackGround[:halfway_point]
    Trimmed_background = "Trimmed_background"+"_"+str(video_number)+".wav"
    first_half.export(Trimmed_background, format="wav")
    
    audio1 = AudioSegment.from_file(Trimmed_background) 
    audio2 = AudioSegment.from_file(speech_gtts) 
    
    mixed = audio1.overlay(audio2) 
    Final_Audio = "Final_Audio"+"_"+str(video_number)+".wav"
    mixed.export(Final_Audio, format='wav')
    return halfway_point, Trimmed_background, speech_gtts, Final_Audio"""

def ProcessImages():
    #############
    #Step 3
    #############
    #Here for the images we downloaded in the step1 we are applying gradient effect
    print('check0')
    list_of_elements = os.listdir('.')
    list_of_elements = natsort.natsorted(list_of_elements)
    list_of_elements_new =[]
    gradient_magnitude=2.25
    test=(8,8,10)
    print('check1')
    for item in list_of_elements:
        if item.endswith('.jpg') and item!='1.jpg' and item!='custom2.jpg':
            img_original = image.load_img(item,target_size=(730,1180,3)) 
            try:
                if brisque.score(img_original) < 55:
                    print(brisque.score(img_original))
                    list_of_elements_new.append([item,brisque.score(img_original)])   
            except Exception:
                print("Image not included")
    print('check2')              
    list_of_elements_new=sorted(list_of_elements_new, key = lambda x: x[1])
    
    if len(list_of_elements_new) >= 5:  
        list_of_elements_new=list_of_elements_new[:5]
    
    list_of_elements_new = [item[0] for item in list_of_elements_new]
    
    for images in list_of_elements_new:
        im = Image.open(images)   
        width, height = im.size
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        width, height = im.size
        gradient = Image.new('L', (1, height), color=0xFF)
        for x in range(height):
            gradient.putpixel((0, x), int(255 * (1 - gradient_magnitude * float(x)/height)))     
        alpha = gradient.resize(im.size)
        alpha = alpha.rotate(180)
        black_im = Image.new('RGBA', (width, height), color=test)
        black_im.putalpha(alpha)
        gradient_im = Image.alpha_composite(im, black_im)
        gradient_im=gradient_im.convert("RGB")    #Wrote newly as not working with RGBA
        gradient_im.save(images)
    return list_of_elements, list_of_elements_new
        
def VideoGenerate(halfway_point, list_of_elements_new):
    ###########
    #Step 4 : 
    ###########
    #From the images generated above we need to create a mp4 file for video generation
    
    global video_number
    basedir = '.'
    #dir = '.'
    command='''ffmpeg '''
    image_length=0
    output_video = "output_video"+"_"+str(video_number)+".mp4"
    
    if video_number==0:
        list_of_elements_new = ['1.jpg', *list_of_elements_new]
    else:
        list_of_elements_new = [*list_of_elements_new]
    
    #list_of_elements_new=natsort.natsorted(list_of_elements_new)
    
    for item in list_of_elements_new:#list_of_elements:
        if item.endswith('.jpg'):
            image_length+=1
            command+="-i "+item+" "        
    
    k=0
    print('Video number & image length ', video_number, image_length)
    if video_number==0:
        k=1.5 #This 1.5second is the amount of the time we need to display the Way2News logo
        x=(((math.ceil(halfway_point/1000))-k)/(image_length-1)) #x=(math.ceil(halfway_point/1000))/image_length #Here we are calculating the number of seconds each image needs to be displayed
    else:
        x=(((math.ceil(halfway_point/1000)))/(image_length))
        
    command+='''-filter_complex "color=c=black:r=60:size=1280x2272:d={0}[black];'''.format(math.ceil(halfway_point/1000)) #change to audio length
    command+='''[0:v]format=pix_fmts=yuva420p,crop=w=2*floor(iw/2):h=2*floor(ih/2),scale=-6:6*ih,zoompan=z='if(eq(on,1),1,zoom+0.000417)':x='0':y='ih-ih/zoom':d=30*1:s=1280x2272,fade=t=in:st=0:d=1:alpha=0,fade=t=out:st=3:d=1:alpha=1,setpts=PTS-STARTPTS[v0];'''
    for a in range(1,image_length):
        if a==1:
            command+='''[{0}:v]format=pix_fmts=yuva420p,crop=w=2*floor(iw/2):h=2*floor(ih/2),scale=-6:6*ih,zoompan=z='if(eq(on,1),1,zoom+0.000417)':x='0':y='0':d=30*{2}:s=1280x2272,fade=t=in:st=0:d=1:alpha=1,fade=t=out:st={1}:d=1:alpha=1,setpts=PTS-STARTPTS+{0}*1.5/TB[v{0}];'''.format(a,(1.5+x),floor(x))#(2*a*x-k-1)(1.5+x)
        else:    
            command+='''[{0}:v]format=pix_fmts=yuva420p,crop=w=2*floor(iw/2):h=2*floor(ih/2),scale=-6:6*ih,zoompan=z='if(eq(on,1),1,zoom+0.000417)':x='0':y='0':d=30*{2}:s=1280x2272,fade=t=in:st=0:d=1:alpha=1,fade=t=out:st={1}:d=1:alpha=1,setpts=PTS-STARTPTS+{1}/TB[v{0}];'''.format(a,1.5+(a-1)*x,floor(x))
        
    command+='''[black][v0]overlay[ov0];'''
    
    #try :
    #if image_length > 3:
    for i in range(image_length-2):
        command+='''[ov{0}][v{1}]overlay[ov{1}];'''.format(i,i+1)
    print('check', image_length)
    print('check ', i)
    command+='''[ov{0}][v{1}]overlay=format=yuv420" -c:v libx264 '''.format(i+1,i+2)
    command+=output_video
    os.system(command)
    return output_video
# =============================================================================
#     except:   
#         os.remove(Trimmed_background)
#         os.remove(Final_Audio)
#         os.remove(speech_gtts)
#         
#         for item in list_of_elements:
#             if item.endswith('.jpg') and item!='1.jpg':
#                 os.remove(item)        
#         return "No relevant images found"
# =============================================================================

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

def Video_Processing(result_links,title,text):
    global detection_length
    global video_number
    title_lable = title
    
    if len(result_links) == 0:
        return "NO_IMAGE_LINKS"
    # 1 -> -----------------------------
    DownloadImages(result_links)
    # 2 -> -----------------------------
    halfway_point, Trimmed_background, speech_gtts, Final_Audio = GenerateSpeech(text)
    # 3 -> -----------------------------
    print('check-1')
    list_of_elements, list_of_elements_new = ProcessImages()
    # 4 -> -----------------------------
    output_video = VideoGenerate(halfway_point, list_of_elements_new)
       
    ###########
    #Step 5 : 
    ###########
    #Add the title to the video that is created earlier
    
        
    
    title_words=title.split(" ")
    converted_words=[]
    for each_word in title_words:
        converted_word=convert_errors(each_word)
        converted_words.append(converted_word)
    
    str1 = " " 
    title=str1.join(converted_words)
    
    lines = textwrap.wrap(title, width=25)
    text_split=' '#'\v '
    for line in lines:
        text_split+=line+'\v'+'\ '
    title = text_split      
    title = title.replace(':','-')
    
    video_Final = "Output"+"_"+str(video_number)+".mp4"
    command ='''ffmpeg -i '''+output_video+''' -vf drawtext='''+'''"fontfile=Rajdhani-Bold.ttf: \\text=\''''+title+'''\': fontcolor=white: fontsize=75: box=0:enable='between(t,1.7,'''+str(math.ceil(halfway_point/1000))+''')':  boxcolor=black@0.30: \\boxborderw=202: x=(w-text_w)/4.0: y=(h-text_h)/1.05" '''+'''-codec:a copy '''+video_Final
    os.system(command)
    
    ###########
    #Step 6 : 
    ###########
    #Once the above step is done we need to create mp4 file of the Final_Audio(AudioFile) and video_name(VideoFile) 
    video_name = "output"+"_" +"Final"+"_"+ str(video_number)+".mp4"
    command_new ='''ffmpeg '''+"-i"+" "+ video_Final +" "+"-i"+" "+Final_Audio+" -y "+"-shortest"+" "+ video_name 
    os.system(command_new)
    
    ###########
    #Step 7 : 
    ###########
    #Compress the final video file that was generated in the above step
    video_News = "Output"+"_" +"News"+"_"+ str(video_number)+".mp4"    
    command_news ='''ffmpeg '''+"-i"+" "+video_name+" "+"-vcodec libx264 -crf 30"+" "+video_News
    os.system(command_news)
    print('File ', video_News, 'ceated')
    video_number = int(video_number) + 1 
#    title_lable=title_lable[:90] +".mp4"
#    os.rename(video_News,title_lable)
    
    ###########
    #Step 8 : 
    ###########
    #Remove all the intermediate files that are not useful and move the Final file to the folder VIDEO
    os.remove(Trimmed_background)
    os.remove(Final_Audio)
    os.remove(video_Final)
    os.remove(output_video)
    os.remove(video_name)
    os.remove(speech_gtts)

    for item in list_of_elements:
        if item.endswith('.jpg') and item!='1.jpg':
            os.remove(item)
        
    
# =============================================================================
#     rpath = "VIDEO"
#     if not os.path.exists(rpath):
#         os.mkdir(rpath)
#     try:
#         shutil.move(title_lable,rpath)    
#     except Exception :
#         return "same file already exists"
# =============================================================================
    
    return video_News#title_lable
