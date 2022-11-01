o
    ���b:  �                   @   s8   d Z ddlZddlZG dd� de�ZG dd� de�ZdS )a�  
This module provides the support for Tracker Object. 
This creates object for the specific tracker based on the name of the tracker provided 
in the command line of the demo.

To add more trackers here, simply replicate the SortTracker() code and replace it with 
the new tracker as required.

Developer simply needs to instantiate the object of ObjectTracker(trackerObjectName) with a valid 
trackerObjectName.

�    Nc                   @   �   e Zd Zdd� ZdS )�ObjectTrackerc                 C   s&   |dkr
t � | _d S td� d | _d S )N�sortzInvalid Tracker Name)�SortTrackerZtrackerObject�print)�selfZtrackerObjectName� r   �./tracker.py�__init__    s   
zObjectTracker.__init__N��__name__�
__module__�__qualname__r
   r   r   r   r	   r      �    r   c                   @   r   )r   c                 C   s@   t j�tj�tj�t�dd�� ddlm} |dddd�| _	d S )	Nz../third_partyzsort-masterr   )�Sort�   �   g333333�?)Zmax_ageZmin_hitsZiou_threshold)
�sys�path�append�os�join�dirname�__file__r   r   Zmot_tracker)r   r   r   r   r	   r
   )   s   ��zSortTracker.__init__Nr   r   r   r   r	   r   (   r   r   )�__doc__r   r   �objectr   r   r   r   r   r	   �<module>   s
   	