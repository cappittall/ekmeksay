o
    ac�2  �                   @   s6  d dl Z d dlZd dlZd dlZd dlZd dlZd dlZd dlZd dlZd dl	Z	d dl
Z
d dlZd dlZd dlZd dlZe�dd� e�dd� e�dd� e�dd� e�d	d� e�d
d� e�dd� e�dd� d dlmZmZmZmZmZmZmZ e��  e�g � e�g � d dlmZ d dlmZ d dlT dZdZ dZ!dZ"G dd� dej#�Z$ej%dd� �Z&ej%dd� �Z'ej%dd� �Z(ej%dEdd��Z)dFd d!�Z*e �+d"d#�Z,d$d%� Z-d&d'� Z.d(d)� Z/d*d+� Z0ej%d,d-� �Z1d.d/� Z2d0d1� Z3d2d3� Z4d4d5� Z5d6d7� Z6d8d9� Z7d:d;� Z8d<d=� Z9d>d?� Z:d@dA� Z;dGdCdD�Z<dS )H�    N�Gtkz3.0�GLibz2.0�GObject�Gstz1.0�GstBase�GstGL�
GstPbutils�GstVideo)r   r   r   r   r   r	   r   )r   )�Image)�*�s�p�qZCoralc                   @   s    e Zd ZdZdZdZdd� ZdS )�Display�
fullscreen�windowZnonec                 C   s   | j S �N)�value)�self� r   �./gstreamer.py�__str__>   s   zDisplay.__str__N)�__name__�
__module__�__qualname__�
FULLSCREENZWINDOW�NONEr   r   r   r   r   r   9   s
    r   c              
   c   s6   � t �| d� zd V  W t �| d� d S t �| d� w )NFT)�os�set_blocking)�fdr   r   r   �nonblockingA   s
   �r    c                 c   sp   � t �| �}t �| �}|d t jt jB  @ |d< t �| t j|� zd V  W t �| t j|� d S t �| t j|� w )N�   )�termiosZ	tcgetattrZICANONZECHOZ	tcsetattrZTCSANOWZ	TCSAFLUSH)r   �old�newr   r   r   �term_raw_modeI   s   �

&r%   c               	   #   s�   � t �� � � fdd�} � fdd�}tj�� rYtj�� }t�|tj| � t	|��( t
|�� |V  W d   � n1 s:w   Y  W d   � d S W d   � d S 1 sRw   Y  d S dd� V  d S )Nc                    s   t j�� D ]}� �|� qdS )NT)�sys�stdin�read�put)r   �flagsZch��commandsr   r   �on_keypressX   s   zCommands.<locals>.on_keypressc                      s"   z� � � W S  tjy   Y d S w r   )�
get_nowait�queueZEmptyr   r+   r   r   r.   ]   s
   
�zCommands.<locals>.get_nowaitc                   S   s   d S r   r   r   r   r   r   �<lambda>i   s    zCommands.<locals>.<lambda>)r/   �Queuer&   r'   �isatty�filenor   Zio_add_watchZIO_INr%   r    )r-   r.   r   r   r+   r   �CommandsT   s   �

P�r4   c              	   #   sb   � t �|�� � �fdd�}tj|d�}|��  z� V  W � �d � |��  d S � �d � |��  w )Nc                     s(   	 � � � } | d u rd S �| �  � ��  qr   )�getZ	task_done)�args�r,   �processr   r   �runo   s   �zWorker.<locals>.run)�target)r/   r1   �	threadingZThread�startr)   �join)r8   �maxsizer9   �threadr   r7   r   �Workerk   s   �


�
r@   �pngc           	      C   s�   dt t�� d � }t�d|| d�}d}d|||f }|�|� td| � |rPd||f }t|d	��}|�|� W d   � n1 sCw   Y  td
| � d S d S )Nz%010di�  ZRGB�rawz/home/mendel/imagesz%s/img-%s.%szFrame saved as "%s"z%s/img-%s.svg�wzOverlay saved as "%s")	�int�time�	monotonicr
   Z	frombytesZsave�print�open�write)	Zrgb�size�overlay�ext�tagZimgZyol�name�fr   r   r   �
save_frame   s   
��rP   �Layout�rJ   r   �inference_size�render_sizec                 C   s4   t | � } t |� }t| |�}t||�}t||| |d�S )NrR   )�SizeZmin_outer_sizeZcenter_insiderQ   )rS   rT   rJ   r   r   r   r   �make_layout�   s   

�rV   c                 C   s    | � d�}t|�d�|�d��S )Nr   �width�height)Zget_structurerU   Z	get_value)ZcapsZ	structurer   r   r   �	caps_size�   s   

�rY   c                 C   sD   t �| ��� �� }t�� }|�|�}|�� }t|�dksJ �|d S )N�   r   )	�pathlib�Path�absolute�as_urir   Z
DiscovererZdiscover_uriZget_video_streams�len)�filenameZuriZ
discoverer�infoZstreamsr   r   r   �get_video_info�   s   
rb   c                 C   sD   | � d�}|s	| }tj�tjj�}|�|�r |�� \}}}}|S d S )N�glsink)�get_by_namer   ZQueryZnew_seeking�Format�TIME�queryZparse_seeking)�pipeline�elementrg   �_�seekabler   r   r   �get_seek_element�   s   

rl   c                 c   sD   � | � d�}|�� }|�tjj�\}}|r||jfV  |�|� d S )Nzpull-sample)�emitZ
get_buffer�mapr   ZMapFlagsZREAD�dataZunmap)�sink�sample�buf�resultZmapinfor   r   r   �pull_sample�   s   �
rt   c                    s   � fdd�}|S )Nc                    sL   t | ��\}}� |t|�� �� W d   � tjjS 1 sw   Y  tjjS r   )rt   rY   Zget_capsr   �
FlowReturn�OK)rp   rh   rq   ro   �r8   r   r   �callback�   s   
��z%new_sample_callback.<locals>.callbackr   )r8   rx   r   rw   r   �new_sample_callback�   s   ry   c                 C   s�   |j tjjkr.t|�}|r(|r(tjjtjjB }|�tj	j
|d�s&t��  d S d S t��  d S |j tjjkrG|�� \}}tj�d||f � d S |j tjjkrd|�� \}}tj�d||f � t��  d S d S )Nr   zWarning: %s: %s
zError: %s: %s
)�typer   �MessageTypeZEOSrl   Z	SeekFlagsZFLUSHZKEY_UNITZseek_simplere   rf   r   �	main_quitZWARNINGZparse_warningr&   �stderrrI   ZERRORZparse_error)�bus�messagerh   �loopZseek_elementr*   �err�debugr   r   r   �on_bus_message�   s    ��r�   c                 C   s   |� d�}|r|��  d S d S )NrK   )rd   Zset_eos)rp   rh   rK   r   r   r   �on_sink_eos�   s   
�r�   c                 C   s�   t | ��o\}}d }d}	|� }
|
tkrd}	n&|
tkr0tdt��  � td|j � td|j � n|
tkr9t	�
�  n|
}|tj|tjd�|d�}|�d�}|rT|�d	|� |	ri|�||j|f� W d   � tjjS W d   � tjjS 1 svw   Y  tjjS )
NFTzTimestamp: %.2fzRender size: %d x %dzInference size: %d x %d)Zdtype)�commandrc   �svg)rt   �COMMAND_SAVE_FRAME�COMMAND_PRINT_INFOrG   rE   rF   rT   rS   �COMMAND_QUITr   r|   �npZ
frombufferZuint8rd   Zset_propertyr)   r   ru   rv   )rp   rh   �render_overlay�layout�images�get_commandrq   ro   Zcustom_commandrP   r�   r�   rc   r   r   r   �on_new_sample�   s8   
�

��
��r�   c                   s,   � � d �}t� � t|� fdd�|||d�S )Nc                    s   � � | ||f�S r   )�send)Ztensorr�   r�   ��render_overlay_genr   r   r0   �   s   zrun_gen.<locals>.<lambda>)�sourcer�   �display)r�   �nextr9   )r�   r�   r�   r�   rS   r   r�   r   �run_gen�   s   

�r�   c                C   s0   t || |�}|r|\}}t|||||� dS dS )NTF)�get_pipeline�run_pipeline)rS   r�   r�   r�   r�   rs   r�   rh   r   r   r   r9   �   s   r9   c                 C   s�   t | �}|rt||j�}|t|j||j|jdd�fS tj�| �}tj�	|�rCt
|�}t|�� |�� �}t||�}|t|�� |||�fS d S )NF)Zsrc_sizeZappsink_sizeZvideosrcZvideofmtZheadless)Zparse_formatrV   rJ   Zget_my_pipelineZdeviceZpixelr   �path�
expanduser�isfilerb   rU   Z	get_widthZ
get_height�file_pipline�is_image)r�   rS   r�   �fmtr�   r`   ra   rT   r   r   r   r�     s   

�
r�   c                 C   s   |t ju r
t| |�S t| |�S r   )r   r   Zcamera_headless_pipelineZcamera_display_pipeline)r�   r�   r�   r   r   r   �camera_pipeline  s   


r�   c                 C   sD   |t ju r| rt||�S t||�S |t ju }| rt||�S t||�S r   )r   r   Zimage_headless_pipelineZvideo_headless_pipeliner   Zimage_display_pipelineZvideo_display_pipeline)r�   r`   r�   r�   r   r   r   r   r�     s   





r�   c                   C   s   t ��  d S r   )r   r|   r   r   r   r   �quit)  �   r�   Tc                 C   s�  t | � t�| �} | �� }|��  |�dt| |� |tjur�dd� }dd� }	t	�
t	jj�}
|
�t� |
�|jj|jj� |tju rE|
��  t	�� }|
�|� |��  | �d�}|�d||� |�|�}|�|� |�� }|�|� |�d|	|� |
�d	t	j� |
��  d
d� }|�||� t t!���}t"� ��}dt#j$t%t#j$||d�|||d�t&d�i|p�i �}|�'� D ]\}}| �|�}|r�|�'� D ]\}}|�||| � q�q�|r�t(�)t(j*t+j,t	j� | �-tj.j/� zzt	�0�  W n	 t1y�   Y nw W | �-tj.j2� n| �-tj.j2� w t(j3�4� �5d��r	 t(j3�4� �5d��sW d   � n1 �s!w   Y  W d   � d S W d   � d S 1 �s:w   Y  d S )Nr   c                 S   s   |� �  d S r   )Z
queue_draw)rp   �widgetr   r   r   �
on_gl_draw:  r�   z run_pipeline.<locals>.on_gl_drawc                 S   s$   | � � }|�|j|j|j|j� dS )NF)Zget_allocationZset_render_rectangle�x�yrW   rX   )r�   Zeventrc   Z
allocationr   r   r   �on_widget_configure>  s
   �z)run_pipeline.<locals>.on_widget_configurerc   Zdrawnzconfigure-eventzdelete-eventc                 S   sr   |j tjjkr5|�� \}}|tjkr5|�tj	�}|�
d�}|r5tj�tjd�}t�||�� � |j�|� tjjS )N�contextT)rz   r   r{   ZNEED_CONTEXTZparse_context_typer   ZGL_DISPLAY_CONTEXT_TYPEZget_by_interfacer	   ZVideoOverlayZget_propertyZContextr$   Zcontext_set_gl_displayZget_display�src�set_contextZBusSyncReplyZPASS)r~   r   rc   rj   Zcontext_typeZsinkelementZ
gl_contextZdisplay_contextr   r   r   �on_bus_message_sync`  s   

z)run_pipeline.<locals>.on_bus_message_syncZappsink)r�   )r�   r�   r�   r�   )z
new-sampleZeosF)6rG   r   Zparse_launchZget_busZadd_signal_watchZconnectr�   r   r   r   ZWindowZ
WindowTypeZTOPLEVELZ	set_title�WINDOW_TITLEZset_default_sizerT   rW   rX   r   r   ZDrawingArea�addZrealizerd   Zget_wayland_window_handleZset_window_handleZ#get_default_wayland_display_contextr�   r|   Zshow_allZset_sync_handlerr@   rP   r4   �	functools�partialr�   r�   �itemsr   Zunix_signal_addZPRIORITY_DEFAULT�signal�SIGINTZ	set_state�StateZPLAYING�main�KeyboardInterruptZNULLZMainContext�defaultZ	iteration)rh   r�   r�   r�   r�   Zhandle_sigintZsignalsr~   r�   r�   r   Zdrawing_arearc   Z	wl_handleZ
wl_displayr�   r�   r�   rN   Z	componentZsignal_nameZsignal_handlerr   r   r   r�   ,  sz   








����

��� ��T�r�   )r   )NrA   )TN)=�collections�
contextlib�enumZfcntlr�   r   r[   r/   r�   r&   r"   r;   rE   Znumpyr�   ZgiZrequire_versionZgi.repositoryr   r   r   r   r   r	   r   Zthreads_initZinitr   ZPILr
   Z	pipelinesr�   r�   r�   r�   �Enumr   �contextmanagerr    r%   r4   r@   rP   �
namedtuplerQ   rV   rY   rb   rl   rt   ry   r�   r�   r�   r�   r9   r�   r�   r�   r�   r�   r   r   r   r   �<module>   s|   $






	

	

