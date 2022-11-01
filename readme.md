# Yapılacaklar

1. /etc/systemd/system/bes.service 
    10,11. satıları aşağıdaki gibi değiştir: 
    10 WorkingDirectory=/home/mendel/ekmeksay
    11 ExecStart=/usr/bin/python3 /home/mendel/ekmeksay/main.py

2. main.py, detect.py, gstreamer.py dosyalarını mail ile gönder ve github a kopyala.

3. main.py içeriğini değiştir. 

4. cddd, cdddx ve baslat dosyalarını düzelt

5. yenile.sh diye dosya oluştur.



# Object Counting  

## !!! This project under development !!! Those notes here are for my own usage purpose

This app designed to count object where sliding from one point to another horizontal or vertical. For this use `--axis` option in order to vertical counting.

## How to use

- Get list of device spesification:  
    gst-device-monitor-1.0 >> device.txt

- Extract devices and clear Run
    python3 genvidfmts.py

this is new ops

Reference link for

- image/jpef:

$ gst-launch-1.0 glvideomixer name=m background=black sink_0::xpos=0 sink_0::ypos=0 sink_0::zorder=1 ! glimagesink v4l2src device=/dev/video2 ! image/jpeg, framerate=30/1,width=1920,height=1080 ! jpegdec ! glupload ! glcolorconvert ! m.sink_0

- video/raw-x:

$ gst-launch-1.0 glvideomixer name=m background=black sink_0::xpos=0 sink_0::ypos=0 sink_0::zorder=1 ! glimagesink v4l2src device=/dev/video2 ! video/x-raw,framerate=10/1,width=1280,height=720 !  glupload ! glcolorconvert ! m.sink_0

streamer.py line 296

Update from git:

git branch -r   ## Get all branchs etc.
git merge or git pull
