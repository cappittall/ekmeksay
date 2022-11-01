o
    dαa�!  �                   @   s�   d Z ddlT dd� Zdd� Zdd� Zd	d
� Zd%dd�Zdd� Zdd� Zdd� Z	dd� Z
dd� Zdd� Zdd� Zdd� Zdd� Z	 	!	d&d"d#�Zd$S )'a`  v4l2src device=/dev/video1 ! video/x-raw,format=YUY2,width=1280,height=720,framerate=10/1 ! glupload ! tee name=t
t. ! queue ! glsvgoverlaysink name=glsink
t. ! queue max-size-buffers=1 leaky=downstream ! glfilterbin filter=glbox ! video/x-raw,format=RGB,width=384,height=384 ! appsink name=appsin
k emit-signals=True max-buffers=1 drop=True sync=False�    )�*c                 C   s   t d| d�td�gS )N�file��location�	decodebin)�Source�Filter)�filename� r
   �./pipelines.py�decoded_file_src   s   
�r   c                 C   s0   t d| jd�td| j| jj| jjd| j d�gS )NZv4l2)�device�video/x-rawz%d/%d)�format�width�height�	framerate)r   r   �CapsZpixel�sizer   r   r   )�fmtr
   r
   r   �v4l2_src   s
   ��r   c                   C   s   t ddd�fS )NZglsvgoverlayZglsink��name��Sinkr
   r
   r
   r   �display_sink"   s   r   c                   C   s   t ddddddd�S )N�appZh264sinkT�   F�r   Zemit_signalsZmax_buffersZdrop�syncr   r
   r
   r
   r   �	h264_sink%   s   r    Fc              
   C   sD   t | j| j�}tddd�tdd| jj| jjd�tddd	d
d	dd�gS )NZglfilterbinZglbox)�filterr   ZRGB)r   r   r   r   ZappsinkTr   Fr   )Zmax_inner_sizeZrender_sizeZinference_sizer   r   r   r   r   )�layoutZ
stillimager   r
   r
   r   �inference_pipeline(   s
   
�r#   c                 C   sR   t | �td�tddd�td�tdd�gtd�t� t� gtd�tdd	d
�t|�gfS )N�imagefreezer   z30/1)r   �glupload�tr   r   �
downstream��max_size_buffersZleaky)r   r   r   �Tee�Pad�Queuer   r#   �r	   r"   r
   r
   r   �image_display_pipeline1   s   
��
��r.   c                 C   sB   t | �td�tdd�gtd�t� t� gtd�tddd�t|�gfS �Nr%   r&   r   r   r'   r(   )r   r   r*   r+   r,   r   r#   r-   r
   r
   r   �video_display_pipelineA   s   ��
��r0   c                 C   sD   t | �td�tdd�gtd�t� t� gtdd�tddd�t|�gfS r/   )r   r   r*   r+   r,   r   r#   �r   r"   r
   r
   r   �camera_display_pipelineN   s   ��
��r2   c                 C   s   t | �td�td�t|�gfS )Nr$   r%   �r   r   r#   r-   r
   r
   r   �image_headless_pipeline\   s   ��r4   c                 C   �   t | �td�t|�gfS �Nr%   r3   r-   r
   r
   r   �video_headless_pipelined   �
   ��r7   c                 C   r5   r6   )r   r   r#   r1   r
   r
   r   �camera_headless_pipelinek   r8   r9   c              	   C   s`   t d| d�td�tdd�gtd�tdd�td�td	d
dd�t� gtd�tdd�td�t|�gfS )Nr   r   �qtdemuxr&   r   r   )r)   �	h264parse�video/x-h264�byte-stream�nal�Zstream_formatZ	alignmentr   )r   r   r*   r+   r,   r   r    r#   r-   r
   r
   r   �video_streaming_pipelines   s    
����r@   c                 C   sz   t | �tdd�gtd�tddd�td�tddd	d
dt|d �dd�td|d�td�tdddd�t� gtd�t� t|�gfS )Nr&   r   r   r'   r(   ZvideoconvertZx264encZ	ultrafastZzerolatency�   �   i�  F)Zspeed_presetZtuneZthreadsZkey_int_max�bitrateZaudr<   )�profiler;   r=   r>   r?   )	r   r*   r+   r,   r   �intr   r    r#   )r   rD   rC   r"   r
   r
   r   �camera_streaming_pipeline�   s,   

�
���rF   c                  C   s@   zt d��� �� } d| v rW dS d| v rW dS W d S    Y d S )Nz#/sys/firmware/devicetree/base/modelZmx8mq�mt8167)�open�read�lower)Zmodelr
   r
   r   �get_dev_board_model�   s   ��rK   �/dev/video1�rawc                    s�  |dkrd}n	|dkrd}nd}|� d�rd| }n#|� d�r$d	| }n|� d
�r.d| }n|�d�r5dnd}d||f }t� }|rnt|d | d  |d | d  �� t� fdd�| D ��� dj� d � d d�}	|d7 }nH|r�d|v r�|d7 }dj| d | d d�}	n2|d7 }d }	n+t|d | d  |d | d  �� t� fdd�| D ��� dj� d � d d�}	|d7 }d}
d}d }|j| d | d d�}|j|d |d d�}|j||||
|	d!�}td"|� |S )#NZh264z9video/x-h264,width={width},height={height},framerate=30/1z
image/jpegz7image/jpeg,width={width},height={height},framerate=30/1z8video/x-raw,width={width},height={height},framerate=30/1z
/dev/videozv4l2src device=%s ! {src_caps}�httpzsouphttpsrc location=%s�rtspzrtspsrc location=%sZaviZavidemuxr:   z�filesrc location=%s ! %s name=demux  demux.video_0
                    ! queue ! decodebin  ! videorate
                    ! videoconvert n-threads=4 ! videoscale n-threads=4
                    ! {src_caps} ! {leaky_q} r   r   c                 3   �   � | ]	}t |�  �V  qd S �N�rE   ��.0�x�Zscaler
   r   �	<genexpr>�   �   � z"get_my_pipeline.<locals>.<genexpr>z)video/x-raw,width={width},height={height})r   r   z� ! decodebin ! queue ! videoconvert ! videoscale
        ! {scale_caps} ! videobox name=box autocrop=true ! {sink_caps} ! {sink_element}
        rG   a�   ! decodebin ! queue ! v4l2convert ! {scale_caps} !
              glupload ! glcolorconvert ! video/x-raw(memory:GLMemory),format=RGBA !
              tee name=t
                t. ! queue ! glfilterbin filter=glbox name=glbox ! queue ! {sink_caps} ! {sink_element}
                t. ! queue ! glsvgoverlay name=gloverlay sync=false ! glimagesink fullscreen=true
                     qos=false sync=false
            z,video/x-raw,format=BGRA,width={w},height={h})�w�hz� ! decodebin ! glupload ! tee name=t
                t. ! queue ! glfilterbin filter=glbox name=glbox ! {sink_caps} ! {sink_element}
                t. ! queue ! glsvgoverlaysink name=glsink sync=false
            c                 3   rP   rQ   rR   rS   rV   r
   r   rW   �   rX   a+   ! tee name=t
            t. ! {leaky_q} ! videoconvert ! videoscale ! {scale_caps} ! videobox name=box autocrop=true
               ! {sink_caps} ! {sink_element}
            t. ! {leaky_q} ! videoconvert
               ! rsvgoverlay name=overlay ! videoconvert ! ximagesink sync=false
            z>appsink name=appsink emit-signals=true max-buffers=1 drop=truez4video/x-raw,format=RGB,width={width},height={height}z)queue max-size-buffers=1 leaky=downstream)Zleaky_q�src_caps�	sink_capsZsink_element�
scale_capszGstreamer pipeline:
)�
startswith�endswithrK   �min�tupler   �print)Zsrc_sizeZappsink_sizeZvideosrcZvideofmtZheadlessZSRC_CAPSZPIPELINEZdemuxZcoralr]   ZSINK_ELEMENTZ	SINK_CAPSZLEAKY_Qr[   r\   Zpipeliner
   rV   r   �get_my_pipeline�   sT   





�"
"�
rc   N)F)rL   rM   F)�__doc__Zgstr   r   r   r    r#   r.   r0   r2   r4   r7   r9   r@   rF   rK   rc   r
   r
   r
   r   �<module>   s(   
	�