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

def rabin_karp(text: str, pattern: str, d: int = 256, q: int = 101_377) -> int:
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    if m > n:
        return -1
    h = pow(d, m-1, q)
    p = 0
    t = 0
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q
    for s in range(n - m + 1):
        if p == t:
            if text[s:s+m] == pattern:
                return s
        if s < n - m:
            t = (d * (t - ord(text[s]) * h) + ord(text[s + m])) % q
            if t < 0:
                t += q
    return -1

ALGORITHMS = {
    "Boyer–Moore (Horspool)": boyer_moore,
    "Knuth–Morris–Pratt": kmp,
    "Rabin–Karp": rabin_karp,
}

def choose_existing_substring(s: str, length: int = 32) -> str:
    start = max(0, len(s) // 3)
    m = re.search(r"\S", s[start:])
    if m:
        start += m.start()
    cand = s[start:start+length]
    cand = " ".join(cand.split())
    if len(cand) < 8:
        cand = " ".join(s[:length].split())
    return cand

def benchmark(text: str, pattern: str, fn, number: int = 800) -> float:
    fn(text, pattern)
    t = timeit.timeit(lambda: fn(text, pattern), number=number)
    return t / number

def main():
    p1 = Path("/mnt/data/стаття 1.txt")
    p2 = Path("/mnt/data/стаття 2.txt")
    text1 = p1.read_text(encoding="utf-8", errors="ignore")
    text2 = p2.read_text(encoding="utf-8", errors="ignore")

    existing1 = choose_existing_substring(text1, 40)
    existing2 = choose_existing_substring(text2, 40)
    fake1 = "___UNLIKELY_SUBSTRING___1___"
    fake2 = "___UNLIKELY_SUBSTRING___2___"

    rows = []
    def run_suite(text_label: str, text: str, exists_pat: str, fake_pat: str, repeats: int = 2):
        for algo_name, fn in ALGORITHMS.items():
            times = [benchmark(text, exists_pat, fn) for _ in range(repeats)]
            rows.append({
                "text": text_label, "pattern_type": "existing",
                "pattern_sample": exists_pat[:50] + ("…" if len(exists_pat) > 50 else ""),
                "algorithm": algo_name, "avg_seconds": sum(times)/len(times),
            })
            times = [benchmark(text, fake_pat, fn) for _ in range(repeats)]
            rows.append({
                "text": text_label, "pattern_type": "fake",
                "pattern_sample": fake_pat,
                "algorithm": algo_name, "avg_seconds": sum(times)/len(times),
            })

    run_suite("стаття 1", text1, existing1, fake1, repeats=2)
    run_suite("стаття 2", text2, existing2, fake2, repeats=2)

    df = pd.DataFrame(rows).sort_values(["text","pattern_type","avg_seconds"]).reset_index(drop=True)
    out_csv = Path("/mnt/data/results_substring_benchmark.csv")
    df.to_csv(out_csv, index=False)

    print("Existing patterns used:")
    print(f"  стаття 1: {existing1!r}")
    print(f"  стаття 2: {existing2!r}")
    print("\nResults (fastest first per case):")
    print(df.to_string(index=False))
    print(f"\nSaved CSV -> {out_csv}")

if __name__ == "__main__":
    main()
