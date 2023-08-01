# -*- coding: utf-8 -*-
# 
# Copyright (c) 2023~2999 - Cologler <skyoflw@gmail.com>
# ----------
# 
# ----------

from padzero import _detect_patterns, _patterns_use_template

def test_detect_patterns():
    assert _detect_patterns(['1', '2', '3']) == [
        [{'text': ''}, {'text': '1', 'number': 1}, {'text': ''}],
        [{'text': ''}, {'text': '2', 'number': 2}, {'text': ''}],
        [{'text': ''}, {'text': '3', 'number': 3}, {'text': ''}]
    ]

    assert _detect_patterns(['vol.1', 'vol.2', 'vol.3']) == [
        [{'text': 'vol.'}, {'text': '1', 'number': 1}, {'text': ''}],
        [{'text': 'vol.'}, {'text': '2', 'number': 2}, {'text': ''}],
        [{'text': 'vol.'}, {'text': '3', 'number': 3}, {'text': ''}]
    ]

    assert _detect_patterns(['k8s vol.1', 'k8s vol.2', 'k8s vol.3']) == [
        [{'text': 'k8s vol.'}, {'text': '1', 'number': 1}, {'text': ''}],
        [{'text': 'k8s vol.'}, {'text': '2', 'number': 2}, {'text': ''}],
        [{'text': 'k8s vol.'}, {'text': '3', 'number': 3}, {'text': ''}]
    ]

def test_patterns_use_template():
    assert _patterns_use_template([
        [{'text': 'k8s vol.'}, {'text': '1', 'number': 1}, {'text': ''}],
        [{'text': 'k8s vol.'}, {'text': '2', 'number': 2}, {'text': ''}],
        [{'text': 'k8s vol.'}, {'text': '3', 'number': 3}, {'text': ''}]
    ], 'a*b') == [
        [{'text': 'a'}, {'text': '1', 'number': 1}, {'text': 'b'}],
        [{'text': 'a'}, {'text': '2', 'number': 2}, {'text': 'b'}],
        [{'text': 'a'}, {'text': '3', 'number': 3}, {'text': 'b'}]
    ]
