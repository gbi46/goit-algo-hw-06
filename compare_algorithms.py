from pathlib import Path
from statistics import mean

import pandas as pd
import re, timeit

def boyer_moore(text: str, pattern: str) -> int:
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    if m > n:
        return -1
    skip = {c: m for c in set(text)}
    for i in range(m - 1):
        skip[pattern[i]] = m - 1 - i
    i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i
        i += skip.get(text[i + m - 1], m)
    return -1

def kmp(text: str, pattern: str) -> int:
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    lps = [0] * m
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    i = j = 0
    while i < n:
        if pattern[j] == text[i]:
            i += 1; j += 1
            if j == m:
                return i - j
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1
