o
    dαa�  �                   @   s�   d dl mZ dd� Zdd� ZG dd� d�ZG dd	� d	�ZG d
d� de�ZG dd� de�ZG dd� de�ZG dd� de�Z	G dd� de�Z
G dd� de�ZG dd� de�ZG dd� de�ZG dd� de�ZG dd� de�ZG dd� de�ZG d d!� d!e�Zd"S )#�    )�Sequencec                 C   s&   | � d�r| dd � n| } | �dd�S )N�_�   �-)�
startswith�replace)�k� r	   �./svg.py�_clean   s   r   c                 C   s   d|  S )Nzrgb(%s, %s, %s)r	   )Zcolorr	   r	   r
   �rgb   s   r   c                   @   s   e Zd Zdd� Zdd� ZdS )�Stylec                 K   s
   || _ d S �N)�_attrs��self�attrsr	   r	   r
   �__init__   s   
zStyle.__init__c                 C   s   d� dd� | j�� D ��S )N�;c                 s   �$   � | ]\}}d t |�|f V  qdS )z%s:%sN�r   ��.0r   �vr	   r	   r
   �	<genexpr>   �   �" z Style.__str__.<locals>.<genexpr>)�joinr   �items�r   r	   r	   r
   �__str__   s   zStyle.__str__N)�__name__�
__module__�__qualname__r   r   r	   r	   r	   r
   r      s    r   c                   @   s0   e Zd ZdZdZdd� Zedd� �Zdd� ZdS )	�TagNr	   c                 K   s0   || _ | jD ]}||vrtd|| jf ��qd S )Nz%Missing attribute "%s" from tag <%s/>)r   �REQUIRED_ATTRS�
ValueError�NAME)r   r   �attrr	   r	   r
   r   #   s   
��zTag.__init__c                 C   s   d S r   r	   r   r	   r	   r
   �value*   s   z	Tag.valuec                 C   sV   d� dd� | j�� D ��}|rd| }| j}|d u r!d| j|f S d| j||| jf S )N� c                 s   r   )z%s="%s"Nr   r   r	   r	   r
   r   /   r   zTag.__str__.<locals>.<genexpr>z<%s%s/>z<%s%s>%s</%s>)r   r   r   r(   r&   )r   Zsattrsr(   r	   r	   r
   r   .   s   zTag.__str__)	r    r!   r"   r&   r$   r   �propertyr(   r   r	   r	   r	   r
   r#      s    
r#   c                       s8   e Zd Z� fdd�Zdd� Zdd� Zedd� �Z�  ZS )	�TagContainerc                    s   t � jdi |�� g | _d S �Nr	   )�superr   �	_childrenr   ��	__class__r	   r
   r   8   �   
zTagContainer.__init__c                 C   s4   z	| j �|� W | S  ty   | j �|� Y | S w r   )r.   �extend�	TypeError�append)r   Zone_or_morer	   r	   r
   �add<   s   ��zTagContainer.addc                 C   s   | � |� | S r   )r5   )r   �childr	   r	   r
   �__iadd__D   s   
zTagContainer.__iadd__c                 C   s   d� dd� | jD ��S )N� c                 s   s   � | ]}t |�V  qd S r   )�str)r   r6   r	   r	   r
   r   J   s   � z%TagContainer.value.<locals>.<genexpr>)r   r.   r   r	   r	   r
   r(   H   s   zTagContainer.value)	r    r!   r"   r   r5   r7   r*   r(   �__classcell__r	   r	   r/   r
   r+   7   s    r+   c                       s    e Zd ZdZ� fdd�Z�  ZS )�SvgZsvgc                    s   t � jdi ddi|��� d S )NZxmlnszhttp://www.w3.org/2000/svgr	   )r-   r   r   r/   r	   r
   r   O   s   zSvg.__init__)r    r!   r"   r&   r   r:   r	   r	   r/   r
   r;   L   s    r;   c                   @   �   e Zd ZdZdS )�Group�gN�r    r!   r"   r&   r	   r	   r	   r
   r=   R   �    r=   c                   @   �   e Zd ZdZdZdS )�Line�line)Zx1Zy1Zx2Zy2N�r    r!   r"   r&   r$   r	   r	   r	   r
   rB   U   �    rB   c                   @   rA   )�RectZrect)�x�y�widthZheightNrD   r	   r	   r	   r
   rF   Y   rE   rF   c                   @   rA   )�CircleZcircle)�cx�cy�rNrD   r	   r	   r	   r
   rJ   ]   rE   rJ   c                   @   rA   )�EllipseZellipse)rK   rL   �rxZryNrD   r	   r	   r	   r
   rN   a   rE   rN   c                       s2   e Zd ZdZd� fdd�	Ze� fdd��Z�  ZS )�Text�textNc                    �   t � jdi |�� || _d S r,   �r-   r   �_text�r   rQ   r   r/   r	   r
   r   h   r1   zText.__init__c                    s   | j r| j S t� jS r   )rT   r-   r(   r   r/   r	   r
   r(   l   s   z
Text.valuer   �r    r!   r"   r&   r   r*   r(   r:   r	   r	   r/   r
   rP   e   s
    rP   c                       �,   e Zd ZdZ� fdd�Zedd� �Z�  ZS )�TSpanZtspanc                    rR   r,   rS   rU   r/   r	   r
   r   u   r1   zTSpan.__init__c                 C   s   | j S r   )rT   r   r	   r	   r
   r(   y   s   zTSpan.valuerV   r	   r	   r/   r
   rX   r   �
    rX   c                   @   rA   )�Path�path)�dNrD   r	   r	   r	   r
   rZ   }   rE   rZ   c                   @   r<   )�DefsZdefsNr?   r	   r	   r	   r
   r]   �   r@   r]   c                       rW   )�CssStyleZstylec                    s    t � jdi ddi�� || _d S )NZ_typeztext/cssr	   )r-   r   �_styles)r   Zstylesr/   r	   r
   r   �   s   
zCssStyle.__init__c                 C   s   dd� dd� | j�� D �� S )Nz<![CDATA[%s]]>�
c                 s   s    � | ]\}}d ||f V  qdS )z%s {%s}Nr	   r   r	   r	   r
   r   �   s   � z!CssStyle.value.<locals>.<genexpr>)r   r_   r   r   r	   r	   r
   r(   �   s   zCssStyle.valuerV   r	   r	   r/   r
   r^   �   rY   r^   N)�collectionsr   r   r   r   r#   r+   r;   r=   rB   rF   rJ   rN   rP   rX   rZ   r]   r^   r	   r	   r	   r
   �<module>   s"   