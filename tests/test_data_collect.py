"""
Liste des tests relatifs au module datacollect.
"""

import sys
sys.path.insert(1, './src/')

import numpy
import pandas as pd
import data_collect
import pytest


def test_get_page_title():
   assert data_collect.get_page_title(
      "https://stackoverflow.com/questions/26812470/how-to-get-page-title-in-requests") == "python - How to get page title in requests - Stack Overflow"


def test_collect_comments():
    data = data_collect.collect_comments("/r/nottheonion/comments/jv0nu0/charles_koch_looks_back_on_his_political_legacy/")
    assert isinstance(data, list)
    if len(data) > 0:
        comment = data[0]
        assert isinstance(comment["text"], str)
        assert isinstance(comment["ups"], int)
        assert isinstance(comment["downs"], int)
        assert isinstance(comment["comments"], list)


def test_collect_posts():
    data = data_collect.collect_posts("https://www.reddit.com/r/nottheonion/")
    assert isinstance(data, pd.DataFrame)
    if len(data) > 0:
        assert isinstance(data["title"][0], str)
        assert isinstance(data["ups"][0], numpy.int64)
        assert isinstance(data["downs"][0], numpy.int64)
