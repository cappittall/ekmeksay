import os
import sys
from datetime import datetime


""" 
filenames='/home/mendel/files/files.csv'
counter = [0,0,0,0,0,0,0]

#son calisilan dosya
with open(filenames, 'r') as f:
    #son dosya adi ve remove  \n
    counter[5]= f.readlines()[-1][:-1] 
    print(counter[5])
iii=0
#Son toplami dosyadan .ek
with open (counter[5], 'r') as g:
    #10/06/2022 11:02
    try:
        gg=g.readlines()[-1].split(',')
        print(iii+1, gg)
        dd=gg[0]
        print(iii+2, gg)
        ddday=int(dd[0:2])
        print(iii+3, gg)
        ddmonth= int(dd[3:5])
        print(iii+4, gg)
        ddyear= int(dd[6:10])
        print(iii+5, gg)
        ddhour= int(dd[-5:-3])
        print(iii+6, gg)
        ddmin= int(dd[-2:]) 
        print(iii+7, gg)
        lastt= datetime(ddyear, ddmonth, ddday, ddhour, ddmin, 0 )
        if datetime.now() < lastt:
            datestrng='sudo hwclock --set --date="{}-{}-{} {}:{}:{}" --localtime'.format(ddyear, ddmonth, ddday, ddhour, ddmin, 0)
            print('Simdi, son satirdaki tarihten eski..;',datestrng)
            os.system(datestrng)
            
        counter[4] = int(gg[-1])
        print('counter.4 ',counter[4])
    except:
        print('hata oldu...') """



#  0---> efdet1, 1---> efdet0
models = ['besas-lite-model_edgetpu.tflite', #0
        'besas-lite-model-efdet0-edgetpu.tflite',#1
        'besas-efdet0-edgetpu01.tflite',#2
        'besas-efdet0-edgetpu02.tflite',#3
        'besas-l50-edgetpu00.tflite',#4
        'besas-l50-edgetpu01.tflite',#5
        'besas-l100-edgetpu00.tflite',#6
        'besas-l100-edgetpu01.tflite',#7
        'besas-new-model50-effdet00-max25-edgetpu.tflite',#8
        'besas-new-model50-efdet02-edgetpu.tflite',#9
        'efficientdet2-lite-ekmek-edgetpu.tflite', #10
        'all4one300_edgetpu.tflite', #11
        'besas-new-model50-effdet01-max25-edgetpu.tflite',#12
        'besas-new-model50-effdet01-edgetpu-ver2.tflite',#13
        'mobilenet_ssd_v1_coco_quant_postprocess_edgetpu.tflite',#14
        'vertex2.tflite', #15
        'modelv5_edgetpu.tflite' #16
        ]
paty= '/home/mendel/ekmeksay/models/'
version = str(max([int(i) for i in os.listdir(paty) if i.isdigit()]))
MODEL = paty+ 'modelv' + version + '_edgetpu.tflite'
#MODEL = '/usr/share/edgetpudemo/' + models[11] # 10 numara istedigim sonucu vermedi
LABELS = '/usr/share/edgetpudemo/besas-labels.txt'

print(MODEL) 

path = '/home/mendel/'
if os.path.isfile('/home/mendel/sets.txt'):
    vals = open('/home/mendel/sets.txt', 'r').readline().split(',')
    vals[0] = float(vals[0])
    vals[4] = float(vals[4])
    vals[5] = bool(vals[5])
else:
    vals = [0.40, 'Francala', '/dev/video1:image/jpeg:1920x1080:30/1','EdgeTpuVisionVa', 0.6,  True, 'down', 'Fırınno_02' ]

video_formats = [i[:-1] for i in open('videoformats.txt', 'r') .readlines()]
fno = vals[7][-2:]
ekmekler = [i[:-1] for i in open('ekmekler%s.txt'%fno, 'r') .readlines()]

firinlar = [i[:-1] for i in open('firinlar.txt', 'r') .readlines()]


while True:

    
    link0 = '/usr/bin/python3 /usr/lib/python3/dist-packages/otracker/detect.py \
    --threshold {} --ekmek "{}" --videosrc {} --firinno {}'.format(vals[0], vals[1], vals[2], vals[7] )

    axis = '--axis' if vals[5] else ''

    link1 = '/usr/bin/python3 /home/mendel/ekmeksay/detect.py \
            --model {model} --label {labels}\
            --source {videosrc} --ekmek "{ekmek}" --threshold {threshold}\
            --roi {roi} {axis} --direction {direction} --firinno {firinno}'\
            .format(model=MODEL, labels=LABELS, videosrc=vals[2], ekmek=vals[1], threshold=vals[0], roi=vals[4], \
            axis = axis, direction=vals[6] , firinno=vals[7])

    link2 = '/usr/bin/python3 /usr/lib/python3/dist-packages/edgetpuvisionVb/detect.py \
            --model {model} --label {labels}\
            --source {videosrc} --ekmek "{ekmek}" --threshold {threshold}\
            --roi {roi} {axis} --direction {direction} --firinno {firinno}'\
            .format(model=MODEL, labels=LABELS, videosrc=vals[2], ekmek=vals[1], threshold=vals[0], roi=vals[4], \
            axis = axis, direction=vals[6], firinno=vals[7] )
   
   
    link3 = '/usr/bin/python3 /usr/lib/python3/dist-packages/examples-camera/detect.py \
            --model {model} --label {labels}\
            --source {videosrc} --ekmek "{ekmek}" --threshold {threshold}\
            --roi {roi} {axis} --direction {direction} --firinno {firinno}'\
            .format(model=MODEL, labels=LABELS, videosrc=vals[2], ekmek=vals[1], threshold=vals[0], roi=vals[4], \
            axis = axis, direction=vals[6], firinno=vals[7] )
            
    link4 = '/usr/bin/python3 /usr/lib/python3/dist-packages/edgetpuvisionVc/detect.py \
            --model {model} --label {labels}\
            --source {videosrc} --ekmek "{ekmek}" --threshold {threshold}\
            --roi {roi} {axis} --direction {direction} --firinno {firinno}'\
            .format(model=MODEL, labels=LABELS, videosrc=vals[2], ekmek=vals[1], threshold=vals[0], roi=vals[4], \
            axis = axis, direction=vals[6], firinno=vals[7] )
    
    link = [link0, link1, link2, link3, link4][1]

    os.system(link)
    print('Back...')

