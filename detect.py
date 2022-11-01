o
    -ac�9  �                   @   s�  d dl Z d dlZd dlZd dlZd dlmZ d dlmZ d dlZ	d dl
mZ d dlmZ d dlmZ d dlmZ d dlZd dlmZ d d	lmZ d d
lmZ d dlZd dlZd dlmZ d dlZe�ejd� ee�ej dddd�ej dd�ej dd�ej dd�ej ddd�ej ddd�d���Z!g d�a"dd� e#d�D �Z$dZ%g a&i Z'd a(e)e%d ��Z*e*�+� d! dd!� t"d"< e,t"d" � W d  � n1 s�w   Y  e)t"d" d ��BZ-e,d#t"d" � e-�+� D ]Z.e.�/d$�Z0e0d% Z1e1e'vr�d e'e1< e'e1  e2e0d& �7  < q�e2e0d! �t"d'< e,d(t"d' � W d  � n	1 �sw   Y  d)d*� Z3d+d,� Z4d-d.� Z5d/d0� Z6d1d2� Z7d3d4� Z8d5d6� Z9d7d8� Z:d9d:� Z;d;d<� Z<d=d>� Z=e>d?k�rUe=�  dS dS )@�    N)�deque)�writer)�_trilu_dispatcher)�GPIO)�detect)�edgetpu)�run_app)�utils)�Sort)�datetime� Zblackz0.5em)�fillZstroke�stroke_widthZ3em)�	font_size�2emz0.25emi�  z1.5em)�font_weightr   �        z0.2em)Zfill_opacityr   )z.backz.bigz.big2Zsmall�largez.bbox)r   r   r   r   r   r   r   r   c                 C   s   g | ]}d �qS )r   � ��.0�ir   r   �./detect.py�
<listcomp>4   s    r   �d   z/home/mendel/files/files.csv�r������   zacilan dosya adi�,�   �   �   zcounter <<<4>>>c                 C   s   dt d| d  � S )Nz%semg333333�?r   )�str)�lengthr   r   r   �size_emN   s   r$   c                 C   s    t dd� t�| | dd�D ��S )Nc                 s   s   � | ]	}t d | �V  qdS )g     �o@N)�int)r   �cr   r   r   �	<genexpr>R   s   � zcolor.<locals>.<genexpr>�      �?)�tuple�colorsysZ
hsv_to_rgb)r   �totalr   r   r   �colorQ   s    r,   c                    s   � fdd�t � �D �S )Nc              	      s&   i | ]\}}|t �t|t� ����qS r   )�svgZrgbr,   �len)r   r   �key��keysr   r   �
<dictcomp>U   s   & z make_palette.<locals>.<dictcomp>)�	enumerater0   r   r0   r   �make_paletteT   s   r4   c                    s4   � r� fdd�S |rt |�� ���fdd�S dd� S )Nc                    s   � S �Nr   �Zobj_id)r,   r   r   �<lambda>Y   �    z make_get_color.<locals>.<lambda>c                    s   � |  S r5   r   r6   )�paletter   r   r7   ]   s    c                 S   s   dS )N�whiter   r6   r   r   r   r7   _   r8   )r4   r1   )r,   �labelsr   )r,   r9   r   �make_get_colorW   s   r<   c                   C   s   t �d� d S )Nz. mail)�os�systemr   r   r   r   �
sendemailsa   �   r?   c                  C   sr   t d dkr7t�d�t d< tt d d��} t| �}|�t d d� � W d   � n1 s,w   Y  dt d< d S d S )Nr    r   �%d/%m/%Y %H:%Mr   �a)�counter�time�strftime�openr   �writerow)�ff�wrr   r   r   �
writetocsvd   s   ��rJ   c
           -   
   C   s
  | j \}
}}}d| }t�� td krdtd< |||  }|
||  }t�� }|t7 }tj||d| j  |ddd�}||7 }|D �]I}|d �� |d �� |d	 �� |d
 �� |d �� |d �� |d �� f\}}}}}}}| j\}}d| d| }}|| j	d  || j	d  }} || ||  || | || |  f\}!}"}#}$|dkr�dnd}%|"t
|$� |kr�|"t
|$� |d k r�|tvr�|dkr�td  d7  < td
  d7  < td tvr�dttd < ttd   d7  < t�|� t�d� nJtd t�� d k �r>|dk�r>t�d� tt td< td tv�rdttd < t�|� t�d� tjtdd���  t�� td< tjtdd���  |tj|!|"|#|$d|% dd�7 }tj|!|"d dd�}&|&tjtt
|��dd�7 }&||&7 }tj|!|"|$ d dd�}&|&tjtt
|d ��d  dd�7 }&||&7 }q?|�r�|tjd|||d!d"�7 }n|tj|d||d!d"�7 }t
t�d#��d dk�r�td t�d$�k�r�tjtdd���  |
d }'|d | || d }(})d%jtd |�r�d&nd'd(�}*|tjddtt|*�d) �d*d+|'|(f d,d-�7 }|tj|*|'|(dd,d.�7 }tD ])}+|(d)7 }(|tj|+|d/ |(dd0d.�7 }|tjd1jt|+ d2�d3| |(dd0d.�7 }�q		 |tjtd |'d4 |(d5 d6d7d.�7 }d8t|�|d9 d| |d9 td � d:�d |	f },|)}"|tjddtt|,��dd+|'|"f d;d-�7 }|tj|,|'|"dd�7 }t|�S )<Ng{�G�z�?�   r   z%s %s %s %sZ	monospacei�  )�width�heightZviewBoxr   Zfont_familyr   r   �   r    r!   r   r(   r   ZgreenZyellowg=
ףp=�?�   �x   r   r   ��target�argsz	stroke:%s�bbox)�x�yrL   rM   �style�_classr:   )rU   rV   r   Z1em)Zdy�   r   �%z"stroke:rgb(255,0,0);stroke-width:2)Zx1Zy1Zx2Zy2rW   z%MrA   zToplam uretim {value:,} {val:}z Sifirliyor!..r   )�value�val�   r   ztranslate(%s, %s) scale(1,-1)Zbig2)rU   rV   rL   rM   Z	transformrX   )rU   rV   r   rX   g�������?r   z	: {val:,})r\   g�������?�   ��   ZredZbigzPSatirda bulunan:%d,  Inf. time %.2f ms (%.2f fps)(Track time: %.2f) %s model: %si�  �/Zback)!ZwindowrD   rC   r-   ZDefs�
CSS_STYLESZSvg�item�inference_size�sizer%   �counted_ids�cesits�append�pop�ekmekler�rotate�ndx�	threading�ThreadrJ   �startr?   ZRectZTextZTSpanr"   ZLinerE   �formatr$   r.   �split)-�layout�objs�trdata�axis�roi�inference_time�inference_rate�trend�sifirlaZmodelim�x0�y0rL   rM   r   �roi_yZroi_xZdefs�docZtdZx0_Zy0_Zx1_Zy1_ZtrackID�scoreZlabelidZinference_widthZinference_heightZscale_xZscale_yZsxZsyrU   rV   �w�hZcolorm�tZoxZoy1Zoy2�titleZkeycesit�liner   r   r   �overlayo   s�   �
X
,4
 


"
,�,$2�r�   c                 C   s8   t d|  � t|�D ]\}}t d|||jjf � q
d S )Nz
Inference (rate=%.2f fps):z    %d: %s, area=%.2f)�printr3   rT   �area)rw   rr   r   �objr   r   r   �print_results�   s   �r�   c           %      #   s�  � t �d�}t �� j�\}}t �|�sJ �t�|�}t|�}tdddd�}t	ddd�}t	ddd	�}t	dd
d	�}t	ddd	�}	� j
dd � }
tdd� td|
 d��� D ��at�� j�att td< � j
td< � jrnt �� j�nd }� jr�tdd� � j�d�D ��nd }t� j|�}d}t �|�\����fV  d }d}d}d } }}d}d}	 |d7 }|V \}}}t|�}|�rC||ks�|dk �rt�� | | }t�� }t�||� t� |� j!�d � j"� }d}|j#\}}|� j$ d ��fdd�|D �}� ��fdd�|D �}t%|�dk�rt&�'dd� |D ��nt&�(d�}nt&�(d�}	 |�)|�} t�� }t*||| � j+� j$||||� j�d �d! �
}t�� | }nd }|�r�|�s�t,j-t.d"d#��/�  t,j-t0d"d#��/�  d}t�1d$�}!d%|!t2td& �d'�d d(d � �d f td&< t3td& � tt4d)��}"t5|"�}#|#�6td& g� W d   � n	1 �s�w   Y  dtd*< i }$nd}|�7�  }|�7� }|�8|�7� � |�s�d}|	�7� �r�t�9d� tt td< td |$v�r�d|$td < q�)+Nr]   r   g333333�?)Zmax_ageZmin_hitsZiou_thresholdz/dev/gpiochip2�   �outz/dev/gpiochip4�in�   z/dev/gpiochip0rO   �����c                 S   s   g | ]}|d d� �qS )Nr   r   r   r   r   r   r   �   s    zrender_gen.<locals>.<listcomp>z/home/mendel/ekmekler%s.txtr   r   rN   c                 s   s   � | ]}|� � V  qd S r5   )�strip)r   �lr   r   r   r'   �   s   � zrender_gen.<locals>.<genexpr>r   TFi�����
   ��������?c                    s(   g | ]}|j j� kr|j j� kr|�qS r   )rT   �ymin�ymax�r   r�   )r|   r   r   r     s   ( c                    s@   g | ]}� j |j�d � d � �j  kr� jkrn n|�qS )r(   )Zmin_arearT   Zscaler�   Zmax_arear�   )rS   rM   rL   r   r   r     s
    ��c                 S   s0   g | ]}|j j|j j|j j|j j|j|jg�qS r   )rT   Zxminr�   Zxmaxr�   r~   �idr�   r   r   r   r   "  s   0 )r   rO   r`   r   r   rQ   z	%d%m_%H%Mz/home/mendel/files/b%s_%04d.csvr   z.csv�����rB   r!   )<r	   Zavg_fps_counterZmake_interpretersZmodelZsame_input_image_sizes�	itertools�cycle�nextr
   r   Zfirinnor   rF   �	readlinesri   �indexZekmekrk   rC   r;   Zload_labels�filter�setrp   r<   r,   Zinput_image_sizerD   �	monotonicr   Zrun_inferencer   Zget_objectsZ	thresholdZtop_krc   ru   r.   �npZarray�empty�updater�   rt   rl   rm   rJ   rn   r?   rE   r%   r�   �	filenamesr   rG   �read�writerj   �closeZbtn_down)%rS   Zfps_counterZinterpretersZtitlesZinterpreterZtrackerZledZbtn_start_stopZ	btn_resetZbtn_upZfnor;   Zfiltered_labelsZ	get_colorZdraw_overlay�outputry   ZcccZstarttZtrstartrx   Z	mailgittiZfpsccZtensorrq   Zcommandrw   rv   rr   rz   r{   Z
detectionsrs   ZdatenowrH   rI   rf   r   )rS   rM   r|   rL   r   �
render_gen�   s�   �

 
$

.

*
.�



�r�   c                 C   s  | j dddd� | j ddd� | j dtd	d
d� | j dtddd� | j dtddd� | j dtddd� | j dd dd� | j dd dd�f | j ddddd� | j dd d!d d!gd"� | j d#td$d%d� | j d&ddd'd� | j d(d)d*d� | j d+d,d-d� | j d.d/d0d� d S )1Nz--modelz.tflite model pathT)�help�requiredz--labelszlabels file path)r�   z--top_k�2   zMax number of objects to detect)�type�defaultr�   z--thresholdg�������?zDetection thresholdz
--min_areag-C��6
?zMin bounding box areaz
--max_areag{�G�zt?zMax bounding box areaz--filterz&Comma-separated list of allowed labels)r�   r�   z--colorzBounding box display colorz--printF�
store_truezPrint inference results)r�   �actionr�   z	--trackerz&Name of the Object Tracker To be used.�sort)r�   r�   �choicesz--roir�   zROI Position (0-1)z--axisz.Axis for cumulative counting (default= x axis)z--ekmeku	   Francalıu   Sayilacak ekmek türüz	--firinnou   Fırın_no-01u   Takip edilen fırın numarasız--directionZdownu   Hangi yöne sayılacak)�add_argumentr%   �float)�parserr   r   r   �add_render_gen_argse  sP   ��
�
�
�
���
���
�r�   c                   C   s   t tt� d S r5   )r   r�   r�   r   r   r   r   �main�  r@   r�   �__main__)?�argparser*   r�   rD   �collectionsr   Zcsvr   Znumpyr�   Znumpy.lib.twodim_baser   Z	peripheryr   Zpycoral.adaptersr   Zpycoral.utilsr   r-   Zappsr   r	   Z
utils.sortr
   r=   rl   r   �locale�	setlocale�LC_ALLr"   ZCssStyleZStylera   rC   �rangere   r�   ri   rf   rk   rF   �fr�   r�   �gr�   rp   ZlinelistZckeyr%   r$   r,   r4   r<   r?   rJ   r�   r�   r�   r�   r�   �__name__r   r   r   r   �<module>   s|   



��
�
a "

�