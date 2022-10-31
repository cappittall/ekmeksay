
import gi
import os
import sys


gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
models= ['/usr/share/edgetpudemo/besas-lite-model50-effdet01.tflite', 
        '/usr/share/edgetpudemo/besas-lite-model50-effdet01-max25.tflite']

MODEL = models[0]
LABELS = '/usr/share/edgetpudemo/besas-labels.txt'

paths= ['/usr/lib/python3/dist-packages',
    '/home/cappittall/Documents/mendel'
        ]
home_paths = ['/home/mendel', '/home/cappittall/Documents/mendel']

x = 1 # 0-Coral device 1-home
path = paths[x]  # Evde 
home_path = home_paths[x]
if os.path.isfile('{}/sets.txt'.format(home_path)):
    vals = open('{}/sets.txt'.format(home_path), 'r').readline().split(',')
    vals[0] = float(vals[0])
    vals[4] = float(vals[4])
    vals[5] = bool(vals[5])
else:
    vals = [0.40, 'Francala', '/dev/video1:YUY2:1280x720:10/1','Otracker', 0.7,  True, 'down', 'Fırınno_01' ]

video_formats = [i[:-1] for i in open('{}/videoformats.txt'.format(home_path), 'r') .readlines()]
fno = vals[7][-2:]
ekmekler = [i[:-1] for i in open('{}/ekmekler{}.txt'.format(home_path, fno), 'r') .readlines()]

firinlar = [i[:-1] for i in open('{}/firinlar.txt'.format(home_path), 'r') .readlines()]

def on_ekmek_degisti(ekmek):
    global vals
    vals[1] = ekmek.get_active_text()
    save_defaults(vals)

def on_firinno_degisti(firinno, e_combo):
    vals[7] = firinno.get_active_text()
    save_defaults(vals)

    fno = vals[7][-2:]
    ekmekler = [i[:-1] for i in open('{}/ekmekler{}.txt'.format(home_path, fno), 'r') .readlines()]
    append_text(e_combo, ekmekler, vals[1])

def on_video_degisti(video):
    vals[2] = video.get_active_text()
    save_defaults(vals)

def start_stop(ssb, versions):
    vindex = versions.index(vals[3])
    
    axis = '--axis' if vals[5] else ''

    link0 = '/usr/bin/python3 {path}/edgetpuvisionVa/detect.py \
            --model {model} --label {labels}\
            --source {videosrc} --ekmek "{ekmek}" --threshold {threshold}\
            --roi {roi} {axis} --direction {direction} --firinno {firinno}'\
            .format(path=path, model=MODEL, labels=LABELS, videosrc=vals[2], ekmek=vals[1], threshold=vals[0], roi=vals[4], \
            axis = axis, direction=vals[6] , firinno=vals[7])

    link1 = '/usr/bin/python3 {path}/edgetpuvisionVb/detect.py \
            --model {model} --label {labels}\
            --source {videosrc} --ekmek "{ekmek}" --threshold {threshold}\
            --roi {roi} {axis} --direction {direction} --firinno {firinno}'\
            .format(path=path, model=MODEL, labels=LABELS, videosrc=vals[2], ekmek=vals[1], threshold=vals[0], roi=vals[4], \
            axis = axis, direction=vals[6], firinno=vals[7] )
   
   
    link2 = '/usr/bin/python3 {path}/examples-camera/detect.py \
            --model {model} --label {labels}\
            --source {videosrc} --ekmek "{ekmek}" --threshold {threshold}\
            --roi {roi} {axis} --direction {direction} --firinno {firinno}'\
            .format(path=path, model=MODEL, labels=LABELS, videosrc=vals[2], ekmek=vals[1], threshold=vals[0], roi=vals[4], \
            axis = axis, direction=vals[6], firinno=vals[7] )
            
    link3 = '/usr/bin/python3 {path}/edgetpuvisionVc/detect.py \
            --model {model} --label {labels}\
            --source {videosrc} --ekmek "{ekmek}" --threshold {threshold}\
            --roi {roi} {axis} --direction {direction} --firinno {firinno}'\
            .format(path=path, model=MODEL, labels=LABELS, videosrc=vals[2], ekmek=vals[1], threshold=vals[0], roi=vals[4], \
            axis = axis, direction=vals[6], firinno=vals[7] )
    
    link = [link0, link1, link2, link3][vindex]
    print(link)
    os.system(link)
    print('Back...')

def on_scale_chage(self, value):
    vals[0]= value 
    save_defaults(vals)

def on_scale_chage1(self, value):
    vals[4]= value 
    save_defaults(vals)

def close_computer(self):
    # Show our message dialog
    d = Gtk.MessageDialog(modal=True, buttons=Gtk.ButtonsType.OK_CANCEL)
    d.props.text = 'Bilgisayar kapatılacak...Eminmisiniz ?'
    response = d.run()
    d.destroy()
    # We only reset computer when the user presses the OK button
    if response == Gtk.ResponseType.OK:
        os.system('sudo shutdown now')

def reset_computer(self):
    # Show our message dialog
    d = Gtk.MessageDialog(modal=True, buttons=Gtk.ButtonsType.OK_CANCEL)
    d.props.text = 'Bilgisayar kapatıp açılacak...Eminmisiniz ?'
    response = d.run()
    d.destroy()
    # We only reset computer when the user presses the OK button
    if response == Gtk.ResponseType.OK:
        os.system('sudo reboot now')

def on_version_changed(version):
    vals[3] = version.get_active_text()
    save_defaults(vals)

def save_defaults(vals): 
    # Write the current vals into a file in order to restore at re-run
    with open('{}/sets.txt'.format(home_path), 'w') as f:
        f.write(','.join([str(i) for i in vals]))
    return True

def on_switch_change(sw, status):
    vals[5] = status
    save_defaults(vals)

def append_text(s,arr, v):
    s.remove_all()
    for i in arr:
        s.append_text(i)

    try:
        s.set_active(arr.index(v))
    except:
        s.set_active(0)

win = Gtk.Window()
win.set_border_width(10)
win.set_default_size(1200, 500)

hb = Gtk.HeaderBar(title="Besas Ekmek Fabrikası")
hb.set_subtitle("Fırın çıkış ekmek sayım app")
hb.props.show_close_button = True
win.set_titlebar(hb)

sst_button = Gtk.Button.new_with_label(label="BAŞLAT")


close_button = Gtk.ToggleToolButton()
rst_button = Gtk.ToggleToolButton()
 
image = Gtk.Image()
image1 = Gtk.Image()
image.set_from_file('{}/kapat.png'.format(home_path))
image1.set_from_file('{}/reset.png'.format(home_path))
close_button.set_icon_widget(image)
rst_button.set_icon_widget(image1)

rst_button.connect('clicked', reset_computer)
close_button.connect('clicked', close_computer)

hb.pack_end(close_button)
hb.pack_end(rst_button)
# hb.pack_start(sst_button)

box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
win.add(box)

hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
hbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
box.add(hbox1)
box.add(hbox2)
box.add(hbox3)
box.add(hbox4)


label01 = Gtk.Label(label='Hassasiyet yüzdesi :')
hbox2.pack_start(label01, True, True, 0)
scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, min=0.0, max=1.0, step=0.05)
scale.set_digits(1)
scale.set_value_pos(Gtk.PositionType.LEFT)
scale.set_value(vals[0])
scale.connect('format-value', on_scale_chage)
hbox2.pack_start(scale, True, True, 0)


label03 = Gtk.Label(label='Sayım çizgisi (Ekran%):')
hbox2.pack_start(label03, True, True, 0)
scale1 = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL,min=0.0, max=1.0, step=0.05)
scale1.set_digits(1)
scale1.set_value_pos(Gtk.PositionType.LEFT)
scale1.set_value(vals[4])
scale1.connect('format-value', on_scale_chage1)
hbox2.pack_start(scale1, True, True, 0)

label04 = Gtk.Label(label="Sağ-Sol")
label05 = Gtk.Label(label="Aşağı-Yukarı")
switch = Gtk.Switch()
switch.connect('state-set', on_switch_change)
switch.set_active(vals[5])


hbox2.pack_start(label04, False, False,0)
hbox2.pack_start(switch, False, False, 0)
hbox2.pack_start(label05, False, False, 0)

### Version control combo menu
vers_combo = Gtk.ComboBoxText()
vers_combo.set_entry_text_column(0)
vers_combo.connect("changed", on_version_changed)
versions = ['EdgeTpuVisionVa', 'EdgeTpuVisionVb','Examples-camera', 'EdgeTpuVisionVc']
append_text(vers_combo, versions, vals[3])
        

hb.pack_end(vers_combo)

### Ekmek seçimi combo menü
label02 = Gtk.Label(label='Ekmek türü :')
ekmek_combo = Gtk.ComboBoxText()
ekmek_combo.set_entry_text_column(0)
ekmek_combo.connect("changed", on_ekmek_degisti)
append_text(ekmek_combo, ekmekler, vals[1])


### Fırın no seçimi combo menü
label06 = Gtk.Label(label='Fırın no :')
firinno_combo = Gtk.ComboBoxText()
firinno_combo.set_entry_text_column(0)
firinno_combo.connect("changed", on_firinno_degisti, ekmek_combo)
append_text(firinno_combo, firinlar, vals[7])



#video secimi combo menu
label03 = Gtk.Label(label='Video boyutu :')
video_combo = Gtk.ComboBoxText()
video_combo.set_entry_text_column(0)
video_combo.connect("changed", on_video_degisti)
append_text(video_combo, video_formats, vals[2])

### Push to the screen
hbox1.pack_start(label02, True, True, 0)
hbox1.pack_start(ekmek_combo, True, True, 0)
hbox1.pack_start(firinno_combo, True, True, 0)
hbox1.pack_start(label03, True, False, 0)
hbox1.pack_start(video_combo, True, False, 0)
hbox4.pack_end(sst_button, True, True, 10)

sst_button.connect("clicked", start_stop, versions)

# sst_button(True, versions)

win.connect('delete-event', Gtk.main_quit)
win.show_all()
Gtk.main()
