o
    dαax
  �                   @   s�   d Z ddlZddlZe�dd� ddlmZ ddlZddlZddl	m
Z ddlZdZdd� Zd	d
� Zdd� Zdd� Zdd� Zdd� ZdS )zCommon utilities.�    N�Gstz1.0)r   zlibedgetpu.so.1c                 C   s6   | � d�^} }tj| t�t|rd|d ini �gd�S )N�@�devicer   )Z
model_pathZexperimental_delegates)�split�tfliteZInterpreterZload_delegate�EDGETPU_SHARED_LIB)Z
model_filer   � r   �./common.py�make_interpreter   s   ���r
   c                 C   s"   | � � d d \}}}}|||fS )z6Returns input size as (width, height, channels) tuple.r   �shape)�get_input_details)�interpreter�_Zheight�widthZchannelsr   r   r	   �input_image_size$   s   
r   c                 C   s    | � � d d }| �|�� d S )zLReturns input tensor view as numpy array of shape (height, width, channels).r   �index)r   �tensor)r   Ztensor_indexr   r   r	   �input_tensor)   s   r   c                 C   sf   |� tjj�\}}|r1t�tj|jtjd�| �	� d d �}|t
| �dd�dd�f< |�|� dS dS )zCopies data to input tensor.)Zdtyper   r   N)�mapr   ZMapFlagsZREAD�npZreshapeZ
frombuffer�dataZuint8r   r   Zunmap)r   �buf�resultZmapinfoZ	np_bufferr   r   r	   �	set_input.   s   ��r   c                 C   sV   | � � | }t�| �|d �� �}d|vr|S |d \}}|dkr%|| S |||  S )z6Returns dequantized output tensor if quantized before.r   Zquantizationr   )Zget_output_detailsr   Zsqueezer   )r   �iZoutput_detailsZoutput_dataZscaleZ
zero_pointr   r   r	   �output_tensor7   s   r   c                 c   sL   � t j| d�}t�� }dV  	 t�� }|�|| � |}t|�t|� V  q)N)�maxleng        )�collections�deque�time�	monotonic�append�len�sum)Zwindow_sizeZwindow�prevZcurrr   r   r	   �avg_fps_counterB   s   ��r%   )�__doc__r   ZgiZrequire_versionZgi.repositoryr   Znumpyr   ZsvgwriteZtflite_runtime.interpreterr   r   r   r   r
   r   r   r   r   r%   r   r   r   r	   �<module>   s    		