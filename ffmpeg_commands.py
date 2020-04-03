
#write text on video
ffmpeg -i into_mobile_size.mp4 -filter:v drawtext="fontfile=/home/home/Downloads/Video_Generation_Complete/Rajdhani-Bold.ttf:text='कॉपर कैन्यन, सिएरा माद्रे, मेक्सिको।':fontcolor=red@1.0:fontsize=30:y=h/2:x=0"-y outputxx.mp4

ffmpeg -i /home/home/Downloads/Video_Generation_Complete/into_mobile_size.mp4 -vf drawtext=fontfile=/home/home/Downloads/Video_Generation_Complete/Rajdhani-Bold.ttf:text=test -qscale 0 outputx.mp4

ffmpeg -i /home/home/Downloads/Video_Generation_Complete/into_mobile_size.mp4 -filter:v drawtext="fontfile=//home//home//ownloads//Video_Generation_Complete//Mangal.ttf:text='कॉपर कैन्यन, सिएरा माद्रे, मेक्सिको।':fontcolor=red@1.0:fontsize=30:y=h/2:x=0"-y outputxx.mp4

command ='''ffmpeg -i '''+output_video+''' -vf drawtext='''+'''"fontfile=Rajdhani-Bold.ttf: \\text=\''''+title+'''\': fontcolor=white: fontsize=75: box=0:enable='between(t,1.7,'''+str(math.ceil(halfway_point/1000))+''')':  boxcolor=black@0.30: \\boxborderw=202: x=(w-text_w)/4.0: y=(h-text_h)/1.05" '''+'''-codec:a copy '''+video_Final




###logo adding

ffmpeg -y -i Output_News_2.mp4 -i logo.png \-filter_complex "overlay=x=main_w*0.01:y=main_h*0.01" output_with_logo_3.mp4

# =============================================================================
# 
# ffmpeg -i way2news_logo.png -vf scale=320:240 output_320x240.png
# 
# ffmpeg -i into_mobile_size.mp4 -i anim_text0.mp4 -filter_complex "overlay=0:366" combined.mp4
# 
# 
# =============================================================================
#overlay two videos
ffmpeg \
    -i anim_text0.mp4 -i into_mobile_size.mp4 \
    -filter_complex " \
        [0:v]setpts=PTS-STARTPTS, scale=460x720[top]; \
        [1:v]setpts=PTS-STARTPTS, scale=446x792, \
             format=yuva420p,colorchannelmixer=aa=0.9[bottom]; \
        [top][bottom]overlay=shortest=1" out121.mp4
        
        
##########################################################################
#add image to video starting 
ffmpeg -i output_with_logo1.mp4 -i 1.jpg \
-filter_complex "[0:v][1:v] overlay=100:100:enable='between(t,0,3)'" \
-pix_fmt yuv420p -c:a copy \
output111.mp4
    
