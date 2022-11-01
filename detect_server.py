o
    dαa�  �                   @   s>   d Z ddlmZ ddlmZmZ dd� Zedkre�  dS dS )a�  A demo which runs object detection and streams video to the browser.

export TEST_DATA=/usr/lib/python3/dist-packages/edgetpu/test_data

Run face detection model:
python3 -m edgetpuvision.detect_server   --model ${TEST_DATA}/mobilenet_ssd_v2_face_quant_postprocess_edgetpu.tflite

Run coco model:
python3 -m edgetpuvision.detect_server   --model ${TEST_DATA}/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite   --labels ${TEST_DATA}/coco_labels.txt
�   )�
run_server)�add_render_gen_args�
render_genc                   C   s   t tt� d S )N)r   r   r   � r   r   �./detect_server.py�main    s   r   �__main__N)�__doc__Zappsr   Zdetectr   r   r   �__name__r   r   r   r   �<module>   s   
�