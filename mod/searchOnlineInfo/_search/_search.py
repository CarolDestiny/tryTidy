# -*- coding:utf-8 -*-
import requests
from .._bing._bing import bing


def auto(query):
    """
    Searches the web for the specified query and returns the results.
    """
    response = requests.get(
        'https://api.openinterpreter.com/v0/browser/search',
        params={"query": query},
    )
    if response.status_code == 200 and response.json()["result"]:
        return response.json()["result"]
    else:
        querys = query.split(" ")
        result = bing(querys)
        if result:
            return result
        else:
            result = bing(query)
            if result:
                return result
            else:
                return "未搜索到合适结果"
