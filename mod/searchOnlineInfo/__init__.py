# -*- coding:utf-8 -*-
# flake8: noqa
# 提供多种网络方法搜索信息
from ._initialize import initialize
from ._search._search import auto
from ._bing._bing import bing

__all__ = ['auto', 'bing']

__version__ = '0.1.0'
__author__ = 'Carol Destiny'
__doc__ = '提供多种网络方法搜索信息'

initialize()