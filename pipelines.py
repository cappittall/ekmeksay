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
'''v4l2src device=/dev/video1 ! video/x-raw,format=YUY2,width=1280,height=720,framerate=10/1 ! glupload ! tee name=t
t. ! queue ! glsvgoverlaysink name=glsink
t. ! queue max-size-buffers=1 leaky=downstream ! glfilterbin filter=glbox ! video/x-raw,format=RGB,width=384,height=384 ! appsink name=appsin
k emit-signals=True max-buffers=1 drop=True sync=False'''
from gst import *


def decoded_file_src(filename):
    return [
        Source('file', location=filename),
        Filter('decodebin'),
    ]

def v4l2_src(fmt):    
    return [
        Source('v4l2', device=fmt.device),
        Caps('video/x-raw', format=fmt.pixel, width=fmt.size.width, height=fmt.size.height,
             framerate='%d/%d' % fmt.framerate),
    ]

def display_sink():
    return Sink('glsvgoverlay', name='glsink'),

def h264_sink():
    return Sink('app', name='h264sink', emit_signals=True, max_buffers=1, drop=False, sync=False)

def inference_pipeline(layout, stillimage=False):
    size = max_inner_size(layout.render_size, layout.inference_size)
    return [
        Filter('glfilterbin', filter='glbox'),
        Caps('video/x-raw', format='RGB', width=layout.inference_size.width, height=layout.inference_size.height),
        Sink('app', name='appsink', emit_signals=True, max_buffers=1, drop=True, sync=False),
    ]

# Display
def image_display_pipeline(filename, layout):
    return (
        [decoded_file_src(filename),
         Filter('imagefreeze'),
         Caps('video/x-raw', framerate='30/1'),
         Filter('glupload'),
         Tee(name='t')],
        [Pad('t'),
         Queue(),
         display_sink()],
        [Pad('t'),
         Queue(max_size_buffers=1, leaky='downstream'),
         inference_pipeline(layout)],
    )


def video_display_pipeline(filename, layout):
    return (
        [decoded_file_src(filename),
         Filter('glupload'),
         Tee(name='t')],
        [Pad('t'),
         Queue(),
         display_sink()],
        [Pad('t'),
         Queue(max_size_buffers=1, leaky='downstream'),
         inference_pipeline(layout)],
    )
## Ahanda burada çalattaşıyor - geldiği yer gstreamer.py line=265 
def camera_display_pipeline(fmt, layout):
    return (
        [v4l2_src(fmt),
         Filter('glupload'),
         Tee(name='t')],
        [Pad('t'),
         Queue(),
         display_sink()],
        [Pad(name='t'),
         Queue(max_size_buffers=1, leaky='downstream'),
         inference_pipeline(layout)],
    )

# Headless
def image_headless_pipeline(filename, layout):
    return (
      [decoded_file_src(filename),
       Filter('imagefreeze'),
       Filter('glupload'),
       inference_pipeline(layout)],
    )

def video_headless_pipeline(filename, layout):
    return (
        [decoded_file_src(filename),
         Filter('glupload'),
         inference_pipeline(layout)],
    )

def camera_headless_pipeline(fmt, layout):
    return (
        [v4l2_src(fmt),
         Filter('glupload'),
         inference_pipeline(layout)],
    )

# Streaming
def video_streaming_pipeline(filename, layout):
    return (
        [Source('file', location=filename),
         Filter('qtdemux'),
         Tee(name='t')],
        [Pad('t'),
         Queue(max_size_buffers=1),
         Filter('h264parse'),
         Caps('video/x-h264', stream_format='byte-stream', alignment='nal'),
         h264_sink()],
        [Pad('t'),
         Queue(max_size_buffers=1),
         Filter('decodebin'),
         inference_pipeline(layout)],
    )

def camera_streaming_pipeline(fmt, profile, bitrate, layout):
    return (
        [v4l2_src(fmt), Tee(name='t')],
        [Pad('t'),
         Queue(max_size_buffers=1, leaky='downstream'),
         Filter('videoconvert'),
         Filter('x264enc',
                 speed_preset='ultrafast',
                 tune='zerolatency',
                 threads=4,
                 key_int_max=5,
                 bitrate=int(bitrate / 1000),  # kbit per second.
                 aud=False),
          Caps('video/x-h264', profile=profile),
          Filter('h264parse'),
          Caps('video/x-h264', stream_format='byte-stream', alignment='nal'),
          h264_sink()],
        [Pad('t'),
         Queue(),
         inference_pipeline(layout)],
    )

def get_dev_board_model():
  try:
    model = open('/sys/firmware/devicetree/base/model').read().lower()
    if 'mx8mq' in model:
        return 'mx8mq'
    if 'mt8167' in model:
        return 'mt8167'
  except: pass
  return None

def get_my_pipeline(src_size,
                 appsink_size,
                 videosrc='/dev/video1',
                 videofmt='raw',
                 headless=False):
    if videofmt == 'h264':
        SRC_CAPS = 'video/x-h264,width={width},height={height},framerate=30/1'
    elif videofmt == 'image/jpeg':
        SRC_CAPS = 'image/jpeg,width={width},height={height},framerate=30/1'
    else:
        SRC_CAPS = 'video/x-raw,width={width},height={height},framerate=30/1'
    if videosrc.startswith('/dev/video'):
        PIPELINE = 'v4l2src device=%s ! {src_caps}'%videosrc
    elif videosrc.startswith('http'):
        PIPELINE = 'souphttpsrc location=%s'%videosrc
    elif videosrc.startswith('rtsp'):
        PIPELINE = 'rtspsrc location=%s'%videosrc
    else:
        demux =  'avidemux' if videosrc.endswith('avi') else 'qtdemux'
        PIPELINE = """filesrc location=%s ! %s name=demux  demux.video_0
                    ! queue ! decodebin  ! videorate
                    ! videoconvert n-threads=4 ! videoscale n-threads=4
                    ! {src_caps} ! {leaky_q} """ % (videosrc, demux)

    coral = get_dev_board_model()
    if headless:
        scale = min(appsink_size[0] / src_size[0], appsink_size[1] / src_size[1])
        scale = tuple(int(x * scale) for x in src_size)
        scale_caps = 'video/x-raw,width={width},height={height}'.format(width=scale[0], height=scale[1])
        PIPELINE += """ ! decodebin ! queue ! videoconvert ! videoscale
        ! {scale_caps} ! videobox name=box autocrop=true ! {sink_caps} ! {sink_element}
        """
    elif coral:
        if 'mt8167' in coral:
            PIPELINE += """ ! decodebin ! queue ! v4l2convert ! {scale_caps} !
              glupload ! glcolorconvert ! video/x-raw(memory:GLMemory),format=RGBA !
              tee name=t
                t. ! queue ! glfilterbin filter=glbox name=glbox ! queue ! {sink_caps} ! {sink_element}
                t. ! queue ! glsvgoverlay name=gloverlay sync=false ! glimagesink fullscreen=true
                     qos=false sync=false
            """
            scale_caps = 'video/x-raw,format=BGRA,width={w},height={h}'.format(w=src_size[0], h=src_size[1])
        else:
            PIPELINE += """ ! decodebin ! glupload ! tee name=t
                t. ! queue ! glfilterbin filter=glbox name=glbox ! {sink_caps} ! {sink_element}
                t. ! queue ! glsvgoverlaysink name=glsink sync=false
            """
            scale_caps = None
    else:
        scale = min(appsink_size[0] / src_size[0], appsink_size[1] / src_size[1])
        scale = tuple(int(x * scale) for x in src_size)
        scale_caps = 'video/x-raw,width={width},height={height}'.format(width=scale[0], height=scale[1])
        PIPELINE += """ ! tee name=t
            t. ! {leaky_q} ! videoconvert ! videoscale ! {scale_caps} ! videobox name=box autocrop=true
               ! {sink_caps} ! {sink_element}
            t. ! {leaky_q} ! videoconvert
               ! rsvgoverlay name=overlay ! videoconvert ! ximagesink sync=false
            """

    SINK_ELEMENT = 'appsink name=appsink emit-signals=true max-buffers=1 drop=true'
    SINK_CAPS = 'video/x-raw,format=RGB,width={width},height={height}'
    LEAKY_Q = 'queue max-size-buffers=1 leaky=downstream'

    src_caps = SRC_CAPS.format(width=src_size[0], height=src_size[1])
    sink_caps = SINK_CAPS.format(width=appsink_size[0], height=appsink_size[1])
    pipeline = PIPELINE.format(leaky_q=LEAKY_Q,
        src_caps=src_caps, sink_caps=sink_caps,
        sink_element=SINK_ELEMENT, scale_caps=scale_caps)

    print('Gstreamer pipeline:\n', pipeline)
    return pipeline
