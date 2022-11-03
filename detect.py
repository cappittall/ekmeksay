# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import colorsys
import itertools
import time
from collections import deque
from csv import writer

import numpy as np
from numpy.lib.twodim_base import _trilu_dispatcher
from periphery import GPIO
from pycoral.adapters import detect
from pycoral.utils import edgetpu

#from . 
import svg
from apps import run_app
#from . 
from utils import utils

#from tracker import ObjectTracker

from utils.sort import Sort
import os
import threading
from datetime import datetime 
import locale
locale.setlocale(locale.LC_ALL, '')


CSS_STYLES = str(svg.CssStyle({'.back': svg.Style(fill='black',stroke='black', stroke_width='0.5em'),\
    '.big': svg.Style(font_size='3em'),\
        '.big2': svg.Style(font_size='2em'),\
            '.small': svg.Style(font_size='0.25em'),\
              '.large': svg.Style(font_size='1.5em'),\
                '.bbox': svg.Style(fill_opacity=0.0, stroke_width='0.2em')}))

counter = [0,0,0,0,0,0,0,0]
counted_ids = [0 for i in range(100)]
filenames = '/home/mendel/files/files.csv'

ekmekler = []
cesits={}
#deque([i[:-1] for i in open('ekmekler%s.txt'%fno, 'r') .readlines()])
ndx=0
#son calisilan dosya
with open(filenames, 'r') as f:
    #son dosya adi ve remove  \n
    counter[5]= f.readlines()[-1][:-1] 
    print(counter[5])

#Son toplami dosyadan al
with open (counter[5], 'r') as g:
    print('acilan dosya adi', counter[5])
    #10/06/2022 11:02
    
    for line in g.readlines():
        linelist= line.split(',')
        ckey = linelist[1]
        if ckey not in cesits: cesits[ckey]=0
        cesits[ckey] += int(linelist[3])
    counter[4] = int(linelist[-1])
    print('counter <<<4>>>', counter[4])

def size_em(length):
    return '%sem' % str(0.6 * (length + 1))

def color(i, total):
    return tuple(int(255.0 * c) for c in colorsys.hsv_to_rgb(i / total, 1.0, 1.0))

def make_palette(keys):
    return {key : svg.rgb(color(i, len(keys))) for i, key in enumerate(keys)}

def make_get_color(color, labels):
    if color:
        return lambda obj_id: color

    if labels:
        palette = make_palette(labels.keys())
        return lambda obj_id: palette[obj_id]

    return lambda obj_id: 'white'

def sendemails():
    os.system('. mail')

def writetocsv():
    if counter[3] > 0:  ## At least should be 1 bread in 1 min
        counter[0] = time.strftime("%d/%m/%Y %H:%M")

        with open(counter[5], 'a') as ff:
            #'/home/mendel/besas_' + counter[0][:10].replace('/', '') + '.csv', 'a') as ff:
            wr = writer(ff)
            wr.writerow(counter[:5])
        counter[3]=0
        
# def overlay(title, objs, get_color, labels, inference_time, inference_rate, layout):
def overlay(layout, objs, trdata, axis, roi, inference_time, inference_rate, trend, sifirla, modelim ):
    x0, y0, width, height = layout.window
    font_size = 0.02 * height
    if time.time()>counter[6]: counter[6]=0

    ## Roi line drawing
    roi_y = y0 + height*roi
    roi_x = x0 + width*roi

    defs = svg.Defs()
    defs += CSS_STYLES
    doc = svg.Svg(width=width, height=height,
                  viewBox='%s %s %s %s' % layout.window,
                  font_size=font_size, font_family='monospace', font_weight=500)
    doc += defs

    #if (np.array(trdata)).size: #  and counter[6] ==0:
    for td in trdata:
        #print(trdata)
        x0_, y0_, x1_, y1_, trackID, score, labelid = td[0].item(), td[1].item(), td[2].item(), td[3].item(), td[4].item(), td[5].item(), td[6].item()

        inference_width, inference_height = layout.inference_size
        scale_x, scale_y = 1.0 / inference_width, 1.0 / inference_height
        sx, sy =  scale_x*layout.size[0], scale_y*layout.size[1]
        x, y, w, h = x0_*sx, y0_*sy, (x1_-x0_)*sx, (y1_-y0_)*sy

        colorm = 'green' if labelid == 0.0 else 'yellow'

        if y+int(h/2)  > roi_y and y+int(h/2) < roi_y * 1.015 and trackID not in counted_ids and labelid == 0.0 :
            counter[4] += 1
            counter[3] += 1
            if counter[1] not in cesits: cesits[counter[1]] = 0
            cesits[counter[1]] += 1 
            counted_ids.append(trackID)
            counted_ids.pop(0)

        elif counter[7] < time.time() - (60*2)  and labelid == 1.0:
            ekmekler.rotate(-1)
            counter[1]= ekmekler[ndx]
            if counter[1] not in cesits: cesits[counter[1]] = 0
            counted_ids.append(trackID)
            counted_ids.pop(0)
            threading.Thread(target=writetocsv, args=()).start()
            counter[7] = time.time()
            threading.Thread(target=sendemails, args=()).start()


        doc += svg.Rect(x=x, y=y, width=w, height=h, style='stroke:%s' % colorm, _class='bbox')

        t = svg.Text(x=x, y=y+5, fill='white')
        t += svg.TSpan(str(int(trackID)), dy='1em')
        doc += t
        t = svg.Text(x=x, y=y+h-20, fill='white')
        t += svg.TSpan(str(int(score*100))+'%', dy='1em')
        doc += t

    #Draw 2 line horizantol or vertical due to axis.
    if axis:
        doc += svg.Line(x1=0, y1=roi_y, x2=width, y2=roi_y, style="stroke:rgb(255,0,0);stroke-width:2")
        #doc += svg.Line(x1=0, y1=roi_y*1.1, x2=width, y2=roi_y*1.1, style="stroke:rgb(255,0,0);stroke-width:2")
    else:
        doc += svg.Line(x1=roi_x, y1=0, x2=roi_x, y2=width, style="stroke:rgb(255,0,0);stroke-width:2")
        #doc += svg.Line(x1=roi_x*1.1, y1=0, x2=roi_x*1.1, y2=width, style="stroke:rgb(255,0,0);stroke-width:2")

    if int(time.strftime("%M")) % 5  ==0  and counter[0] != time.strftime("%d/%m/%Y %H:%M"):
        threading.Thread(target=writetocsv, args=()).start()
        # writetocsv(counter)

    ox = x0 + 20
    oy1, oy2 = y0 + 20 + font_size, y0 + height -20
    # Title 
    title = 'Toplam {turu} {value:,} {val:}'.format(turu=counter[1], value= cesits[counter[1]], val=' Sifirliyor!..' if sifirla else '')
    doc += svg.Rect(x=0, y=0, width=size_em(len(title)+30), height='2em',
                        transform='translate(%s, %s) scale(1,-1)' % (ox, oy1), _class='big2')
    doc += svg.Text(title, x=ox, y=oy1, fill='white', _class='big2' )
    for keycesit in cesits:
        oy1 += 30
        doc += svg.Text(keycesit, x=width*0.55, y= oy1, fill='yellow', _class='large')
        doc += svg.Text(': {val:,}'.format(val=cesits[keycesit]), x=0.8*width, y=oy1, fill='yellow', _class='large')



    '''
    doc += svg.Rect(x=0, y=0, width=size_em(len(counter[1])), height='4em',
                        transform='translate(%s, %s) scale(1,-1)' % (ox+100, oy1+200), _class='back')
    '''        
                    
    doc += svg.Text(counter[1], x=ox+150, y=oy1+200, fill='red', _class='big')
    # Info
    line = 'Satirda bulunan:%d,  Inf. time %.2f ms (%.2f fps)(Track time: %.2f) %s model: %s' % (len(trdata), inference_time * 1000, 1.0 / inference_time, trend * 1000, counter[5].split('/')[-1], modelim  )
    y = oy2 #- 1.7 * font_size
    doc += svg.Rect(x=0, y=0, width=size_em(len(line)), height='1em',
                       transform='translate(%s, %s) scale(1,-1)' % (ox, y), _class='back')
    doc += svg.Text(line, x=ox, y=y, fill='white')

    return str(doc)

def print_results(inference_rate, objs):
    print('\nInference (rate=%.2f fps):' % inference_rate)
    for i, obj in enumerate(objs):
        print('    %d: %s, area=%.2f' % (i, obj, obj.bbox.area))

def render_gen(args):
    global counter, ekmekler, ndx, cesits

    fps_counter  = utils.avg_fps_counter(30)

    interpreters, titles = utils.make_interpreters(args.model)
    assert utils.same_input_image_sizes(interpreters)
    interpreters = itertools.cycle(interpreters)
    interpreter = next(interpreters)

    
    #racker = objectOfTracker.trackerObject.mot_tracker
    tracker = Sort(max_age=30, min_hits=0, iou_threshold=.30)

    
    led = GPIO("/dev/gpiochip2", 13, "out")  # pin 37
    btn_start_stop = GPIO("/dev/gpiochip4", 13, "in")  # pin 36
    btn_reset = GPIO("/dev/gpiochip4", 12, "in")  # pin 22
    btn_up = GPIO("/dev/gpiochip0", 7, "in") # pin 29
    #btn_down  = GPIO("/dev/gpiochip0", 8, "in") # pin 31 (29-31 yan yana) 
    

    fno = args.firinno[-2:]
    ekmekler= deque([i[:-1] for i in open('/home/mendel/ekmekler%s.txt'%fno, 'r') .readlines()])
    ndx = ekmekler.index(args.ekmek)
    counter[1] = ekmekler[ndx]
    counter[2] = args.firinno
    ##


    labels = utils.load_labels(args.labels) if args.labels else None
    filtered_labels = set(l.strip() for l in args.filter.split(',')) if args.filter else None
    get_color = make_get_color(args.color, labels)

    draw_overlay = True
    
    width, height = utils.input_image_size(interpreter)
    yield width, height

    output = None

    sifirla = False
    ccc=-10
    startt=trstart=trend=0
    mailgitti= False
    fpscc=10

    while True:

        ccc += 1
        tensor, layout, command = (yield output)

        inference_rate = next(fps_counter)
        if draw_overlay:
            if ccc==fpscc or ccc<0:
                inference_time = (time.monotonic()-startt)/fpscc
                startt=time.monotonic()
                edgetpu.run_inference(interpreter, tensor)
                #Object detections max 50 results
                objs = detect.get_objects(interpreter, args.threshold)[:args.top_k]
                #Filter the object at counting area.
                ccc=0
                
                x0, y0 = layout.inference_size
                roi_y = y0 * args.roi 
                # roi_x = x0 * args.roi 
                
                objs =[obj for obj in objs if obj.bbox.ymax >= roi_y*0.90 and 
                                              obj.bbox.ymin <= roi_y*1.0]


                #objsss= len([obj for obj in objs if obj.bbox.ymax > roi_y * 0.95]) 
                
                
                #Filtering the big or small sized detections.
                objs = [obj for obj in objs \
                    if args.min_area <= obj.bbox.scale(1.0 / width, 1.0 / height).area <= args.max_area]

                detections = np.array([[obj.bbox.xmin, obj.bbox.ymin, obj.bbox.xmax, obj.bbox.ymax, obj.score, obj.id] for obj in objs ]) if len(objs)>0 else np.empty((0,7))
            else:
                detections = np.empty((0,7))
            
            #Adding to the tracking object
            # detections = [[obj.bbox.xmin, obj.bbox.ymin, obj.bbox.xmax, obj.bbox.ymax, obj.score] for obj in objs]
            '''
            detections = []

            for n in range(0, len(objs)):
                element = [] 
                element.append(objs[n].bbox.xmin)
                element.append(objs[n].bbox.ymin)
                element.append(objs[n].bbox.xmax)
                element.append(objs[n].bbox.ymax)
                element.append(objs[n].score)  
                detections.append(element) 
            '''

            trdata = tracker.update(detections)
            trstart = time.monotonic()
            #draw the boxes with tracking data(trdata)
            output = overlay(layout, objs, trdata, args.axis, args.roi, inference_time, inference_rate, trend, sifirla, args.model.split('/')[-1])
            trend = time.monotonic()-trstart
        else:
            output = None

        if sifirla:
        #if int(time.strftime("%M")) % 1  ==0  and counter[0] != time.strftime("%d/%m/%Y %H:%M"):
            if not mailgitti:
                threading.Thread(target=writetocsv, args=()).start()
                threading.Thread(target=sendemails, args=()).start()
                mailgitti=True
                datenow = time.strftime('%d%m_%H%M')
                counter[5] = '/home/mendel/files/b%s_%04d.csv' % (datenow, int(counter[5].split('.csv')[0][-4:])+1)

                print(counter[5])
                with open(filenames, 'a') as ff:
                    wr = writer(ff)
                    wr.writerow([counter[5]])

            cesits={}
            counter[4] = 0
        else: mailgitti = False
       

        draw_overlay = not btn_start_stop.read() 
        sifirla = btn_reset.read()

        led.write(btn_start_stop.read())
        if not draw_overlay: ccc=0

        # Buton Ekmekler previous
        if btn_up.read():
            ekmekler.rotate(1)
            counter[1] = ekmekler[ndx]
            if counter[1] not in cesits: cesits[counter[1]]=0            
    
    ## Close the lights ##
    led.write(False)
    led.close()
    btn_start_stop.close()
    btn_reset.close()
    btn_up.close()
    btn_down.close()
    
def add_render_gen_args(parser):
    parser.add_argument('--model',
                        help='.tflite model path', required=True)
    parser.add_argument('--labels',
                        help='labels file path')
    parser.add_argument('--top_k', type=int, default=50,
                        help='Max number of objects to detect')
    parser.add_argument('--threshold', type=float, default=0.5,
                        help='Detection threshold')
    parser.add_argument('--min_area', type=float, default=0.00005, #0.0015,
                        help='Min bounding box area')
    parser.add_argument('--max_area', type=float, default=0.005,
                        help='Max bounding box area')
    parser.add_argument('--filter', default=None,
                        help='Comma-separated list of allowed labels')
    parser.add_argument('--color', default=None,
                        help='Bounding box display color'),
    parser.add_argument('--print', default=False, action='store_true',
                        help='Print inference results')
    parser.add_argument('--tracker', help='Name of the Object Tracker To be used.',
                        default='sort',
                        choices=[None, 'sort'])
    parser.add_argument('--roi', type=float,
                        default=0.9, help='ROI Position (0-1)')

    parser.add_argument('--axis', default=False, action="store_true", 
                        help='Axis for cumulative counting (default= x axis)')

    parser.add_argument('--ekmek', default='Francalı', help='Sayilacak ekmek türü')

    parser.add_argument('--firinno', default='Fırın_no-01', help='Takip edilen fırın numarası')

    parser.add_argument('--direction', default='down', help='Hangi yöne sayılacak')
    
def main():
    run_app(add_render_gen_args, render_gen)

if __name__ == '__main__':
    main()
