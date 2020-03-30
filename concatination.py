import os
import natsort


command=''
dir = '.'
list_of_elements = os.listdir(dir)
list_of_elements = natsort.natsorted(list_of_elements)


names = []
for item in list_of_elements:
   if item.endswith('.mp4'):  
       command=''
       command+='ffmpeg' +" -i "+item+" "+"-c copy -bsf:v h264_mp4toannexb -f mpegts"+" "+item.replace('.mp4','.ts')    
       names.append(item.replace('.mp4','.ts'))
       print("command is",command)
       os.system(command)

#Construction of the second part ffmpeg -i "concat:intermediate1.ts|intermediate2.ts|intermediate3.ts" -c copy -bsf:a aac_adtstoasc output.mp4

last_element=names[len(names)-1]
command1='''ffmpeg -i "concat:'''

for item in names:
   if last_element==item:
       command1+=item+'"'
   else:
       command1+=item+"|"

command1+=''' -c copy -bsf:a aac_adtstoasc '''

Video_Final=0
video_output="Final_Concatenated_Video"+str(Video_Final)+".mp4"
command1+=video_output

#Combine both the commands
command_final=command+command1
os.system(command1)




