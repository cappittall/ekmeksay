o
    dαa�
  �                   @   sh   d dl Z d dlZd dlZd dlmZ d dlmZmZ d dlm	Z	 d dl
Z
ee
�� �Zdd� Zdd� ZdS )	�    N)�make_camera)�Display�run_gen)�StreamingServerc                    s�   t jt jd� tjtjd�}|jdddd� |jdtdd	d
� |jddddd� | |� |�� }||�� t	|j
t� �|j�}|d usDJ �t||j���� �fdd�}||_t��  W d   � d S 1 sdw   Y  d S )N)�level��formatter_class�--source�2/dev/videoN:FMT:WxH:N/D or .mp4 file or image filez/dev/video0:YUY2:640x480:30/1��help�defaultz	--bitratei@B zVideo streaming bitrate (bit/s))�typer   r   �--loopF�
store_true�Loop input video file�r   �actionr   c                    s,   � � | ||f�}��|r|� d S t� d S )N)�sendZsend_overlay�	EMPTY_SVG)ZtensorZlayoutZcommandZoverlay��genZserver� �	./apps.py�render_overlay0   s   z"run_server.<locals>.render_overlay)�loggingZbasicConfig�INFO�argparse�ArgumentParser�ArgumentDefaultsHelpFormatter�add_argument�int�
parse_argsr   �source�next�loopr   Zbitrater   �signal�pause)�add_render_gen_args�
render_gen�parser�args�camerar   r   r   r   �
run_server   s,   �
�
�
"�r-   c                 C   s�   t jt jd�}|jdddd� |jdddd	d
� |jdtttjdd� | |� |�� }t||�|j|j	|j
d�s@td|j� d S d S )Nr   r	   r
   z/dev/video0:YUY2:1280x720:30/1r   r   Fr   r   r   z--displaymodezDisplay mode)r   �choicesr   r   )r#   r%   ZdisplayzInvalid source argument:)r   r   r   r    r   Z
FULLSCREENr"   r   r#   r%   Zdisplaymode�print)r(   r)   r*   r+   r   r   r   �run_app8   s(   �
����r0   )r   r   r&   r,   r   Z	gstreamerr   r   Zstreaming.serverr   Zsvg�strZSvgr   r-   r0   r   r   r   r   �<module>   s   