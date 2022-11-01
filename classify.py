o
    dαa  �                	   @   s�   d Z ddlZddlZddlZddlZddlmZ ddlmZ ddl	m
Z
 ddl	mZ ddlmZ ee
�d	e
jd
d
dd�i��Zdd� Zdd� Zdd� Zdd� Zdd� Zdd� Zdd� Zdd� Zedkrhe�  dS dS )a  A demo which runs object classification on camera frames.

export TEST_DATA=/usr/lib/python3/dist-packages/edgetpu/test_data

python3 -m edgetpuvision.classify   --model ${TEST_DATA}/mobilenet_v2_1.0_224_inat_bird_quant.tflite   --labels ${TEST_DATA}/inat_bird_labels.txt
�    N)�classify)�edgetpu�   )�svg)�utils)�run_appz.backZblackz0.5em)�fillZstrokeZstroke_widthc                 C   s   dt d| d  � S )Nz%semg333333�?r   )�str)�length� r   �./classify.py�size_em(   s   r   c              
   C   s�  |j \}}}}d| }	t�� }
|
t7 }
tj||d|j  |	ddd�}||
7 }|d || d }}|d |	 || d }}dd� |D �}t|�D ]-\}}||d	 |	  }|tjd
d
tt|��dd||f dd�7 }|tj	|d||dd�7 }qH| r�|tjd
d
tt| ��dd||f dd�7 }|tj	| ||dd�7 }d|d d| |f g}tt
|��D ],\}}||d	 |	  }|tjd
d
tt|��dd||f dd�7 }|tj	|||dd�7 }q�t|�S )Ng���Q��?z%s %s %s %sZ	monospacei�  )�width�heightZviewBox�	font_sizeZfont_familyZfont_weight�   c                 S   s   g | ]}d | �qS )z	%s (%.2f)r   )�.0Zpairr   r   r   �
<listcomp>;   s    zoverlay.<locals>.<listcomp>g333333�?r   Z1emztranslate(%s, %s) scale(-1,-1)Zback)�x�yr   r   Z	transformZ_class�endZwhite)Ztext_anchorr   r   r   ztranslate(%s, %s) scale(1,-1))r   r   r   z6Inference time: %.2f ms (%.2f fps) inf rate:(%.2f fps)i�  g      �?)�windowr   ZDefs�
CSS_STYLESZSvg�	enumerateZRectr   �lenZText�reversedr	   )�title�results�inference_time�inference_rate�layoutZx0Zy0r   r   r   Zdefs�docZox1Zox2Zoy1Zoy2�lines�i�liner   r   r   r   �overlay+   sB   �
����r%   c                 C   sT   t �dd� �}| D ]}|D ]\}}||  |7  < qq	t|�� dd� dd�d |� S )Nc                   S   s   dS )Ng        r   r   r   r   r   �<lambda>Y   s    ztop_results.<locals>.<lambda>c                 S   s   | d S )Nr   r   )Zkvr   r   r   r&   ]   s    T)�key�reverse)�collections�defaultdict�sorted�items)r   �top_kZtotal_scoresr   �label�scorer   r   r   �top_resultsX   s   �r0   c                 c   s0   � t j| d�}|�g V � 	 |�t||�V � q)N)�maxlen)r)   �deque�appendr0   )�sizer-   r   r   r   r   �accumulator_   s   ��r5   c                 C   s6   t d|  � t |� |D ]\}}t d||f � qd S )Nz
Inference (rate=%.2f fps):z  %s, score=%.2f)�print)r   r   r.   r/   r   r   r   �print_resultse   s
   �r7   c                 #   s0  � t | j| jd�}|�d � t�d�}t�| j�\}}t�|�s"J �t	�
|�}t|�}t�| j�� d}t�|�V  d }	 |V \}}	}
t|�}|r�t�� }t�||� t�� | }tj|| j| jd�}� fdd�|D �}|�|�}| jrxt||� || }t|||||	�}nd }|
dkr�| }n|
dkr�t|�}q<)	N)r4   r-   �   T)r-   Zscore_thresholdc                    s   g | ]
\}}� | |f�qS r   r   )r   Zclass_idr/   ��labelsr   r   r   �   s    zrender_gen.<locals>.<listcomp>�o�n)r5   r   r-   �sendr   Zavg_fps_counterZmake_interpretersZmodelZsame_input_image_sizes�	itertools�cycle�nextZload_labelsr:   Zinput_image_size�time�	monotonicr   Zrun_inferencer   Zget_classesZ	thresholdr6   r7   r%   )�argsZaccZfps_counterZinterpretersZtitlesZinterpreterZdraw_overlay�outputZtensorr    Zcommandr   �startr   Zclassesr   r   r   r9   r   �
render_genk   sD   �



�

�rF   c                 C   sl   | j dddd� | j dddd� | j dtdd	d
� | j dtddd
� | j dtddd
� | j ddddd� d S )Nz--modelTz.tflite model path)�required�helpz--labelszlabel file pathz--window�
   z0number of frames to accumulate inference results)�type�defaultrH   z--top_k�   z/number of classes with highest score to displayz--thresholdg�������?zclass score thresholdz--printF�
store_truezPrint inference results)rK   �actionrH   )�add_argument�int�float)�parserr   r   r   �add_render_gen_args�   s$   ��
�
�
�

�rS   c                   C   s   t tt� d S )N)r   rS   rF   r   r   r   r   �main�   s   rT   �__main__)�__doc__�argparser)   r>   rA   Zpycoral.adaptersr   Zpycoral.utilsr   � r   r   Zappsr   r	   ZCssStyleZStyler   r   r%   r0   r5   r7   rF   rS   rT   �__name__r   r   r   r   �<module>   s2   �-+
�