o
    dαaj  �                   @   sb   d dl Z d dlZd dlZd dlZd dlT G dd� d�ZG dd� de�ZG dd� de�Zd	d
� ZdS )�    N)�*c                   @   s@   e Zd Zdd� Zedd� �Zdd� Zdd� Zd	d
� Zdd� Z	dS )�Camerac                 C   s$   t �||�| _|| _d | _d | _d S �N)�	gstreamerZmake_layout�_layout�_loop�_thread�render_overlay)�self�render_size�inference_size�loop� r   �./camera.py�__init__   s   
zCamera.__init__c                 C   s   | j jS r   )r   r   �r
   r   r   r   �
resolution    s   zCamera.resolutionc                 C   s   d S r   r   r   r   r   r   �request_key_frame$   �   zCamera.request_key_framec              	      sr   � fdd�}�fdd�}ddt �|�ii}	��|||||�}
tjt j|
�j�j|t jj	d|	fd��_
�j
��  d S )	Nc                    s   � � | � d S r   )�write)�data�_)�objr   r   �	on_buffer(   s   z)Camera.start_recording.<locals>.on_bufferc                    s   � j r
� � | ||� d S r   )r	   )ZtensorZlayoutZcommandr   r   r   r	   +   s   z.Camera.start_recording.<locals>.render_overlayZh264sinkz
new-sampleF)�target�args)r   Znew_sample_callback�make_pipeline�	threadingZThreadZrun_pipeliner   r   ZDisplayZNONEr   �start)r
   r   �format�profile�inline_headers�bitrate�intra_periodr   r	   ZsignalsZpipeliner   )r   r
   r   �start_recording'   s   �
��zCamera.start_recordingc                 C   s   t ��  | j��  d S r   )r   �quitr   �joinr   r   r   r   �stop_recording<   s   zCamera.stop_recordingc                 C   s   t �r   )�NotImplemented�r
   �fmtr    r!   r"   r#   r   r   r   r   @   r   zCamera.make_pipelineN)
�__name__�
__module__�__qualname__r   �propertyr   r   r$   r'   r   r   r   r   r   r      s    
r   c                       �$   e Zd Z� fdd�Zdd� Z�  ZS )�
FileCamerac                    s2   t �|�}t� j|�� |�� f||d� || _d S )N�r   )r   Zget_video_info�superr   Z	get_widthZ
get_height�	_filename)r
   �filenamer   r   �info��	__class__r   r   r   D   s
   
�
zFileCamera.__init__c                 C   s   t �| j| j�S r   )�	pipelinesZvideo_streaming_pipeliner3   r   r)   r   r   r   r   J   s   zFileCamera.make_pipeline�r+   r,   r-   r   r   �__classcell__r   r   r6   r   r0   C   s    r0   c                       r/   )�DeviceCamerac                    s   t � j|j|dd� || _d S )NFr1   )r2   r   �size�_fmt)r
   r*   r   r6   r   r   r   N   s   
zDeviceCamera.__init__c                 C   s   t �| j||| j�S r   )r8   Zcamera_streaming_pipeliner=   r   r)   r   r   r   r   R   s   zDeviceCamera.make_pipeliner9   r   r   r6   r   r;   M   s    r;   c                 C   s>   t | �}|rt||�S tj�| �}tj�|�rt|||�S d S r   )Zparse_formatr;   �os�path�
expanduser�isfiler0   )�sourcer   r   r*   r4   r   r   r   �make_cameraU   s   
rC   )	r>   r   r   r8   Zgstr   r0   r;   rC   r   r   r   r   �<module>   s   *
