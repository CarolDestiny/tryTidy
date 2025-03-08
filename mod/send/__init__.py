# -*- coding:utf-8 -*-
# flake8: noqa
from ._initialize import initialize
from ._msg import msg
from ._image import image
from ._voice import voice
from ._music import music
from ._imageUrl import imageUrl

__all__ = ['msg', 'image', 'voice', 'music', 'imageUrl']

__version__ = '0.1.0'
__author__ = 'Carol Destiny'
__doc___ = ''

initialize()