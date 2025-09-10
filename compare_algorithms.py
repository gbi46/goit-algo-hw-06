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
