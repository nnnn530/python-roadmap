r"""LC 88 压力测试（2026-10-26）

用法（在 D:\code\python-roadmap 下）：
    python tools\check_lc88.py

它会用「固定反例 + 300 组随机数据」跑你 src\day05_lc88.py 里的 merge_v1 / merge_v2，
和标准答案（Python 内置 sorted）对比。对了就说 OK，错了会打印【输入 → 你得到的 → 应该得到的】。
"""

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from day05_lc88 import merge_v1, merge_v2  # noqa: E402

FIXED = [
    ([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3),   # 题面样例
    ([4, 5, 6, 0, 0, 0], 3, [1, 2, 3], 3),   # nums2 全比 nums1 小
    ([5, 6, 7, 0, 0, 0], 3, [1, 2, 3], 3),   # 同上，换个数
    ([1], 1, [], 0),                          # n = 0
    ([0], 0, [1], 1),                         # m = 0
    ([0, 0, 0], 0, [1, 2, 3], 3),             # m = 0 且 n > 1
    ([2, 0], 1, [1], 1),                      # 最小规模
    ([1, 2, 3, 0, 0], 3, [4, 5], 2),          # nums2 全比 nums1 大
]


def run_one(fn, nums1, m, nums2, n):
    got = list(nums1)
    try:
        fn(got, m, list(nums2), n)
    except Exception as e:  # 边界没处理好通常会在这里炸出来
        return f"异常 {type(e).__name__}: {e}"
    return got


def check(fn, label, cases):
    bad = 0
    for nums1, m, nums2, n in cases:
        expect = sorted(nums1[:m] + nums2[:n])
        got = run_one(fn, nums1, m, nums2, n)
        if got != expect:
            bad += 1
            if bad <= 4:
                print(f"  [X] nums1={nums1} m={m} nums2={nums2} n={n}")
                print(f"      你的结果: {got}")
                print(f"      正确答案: {expect}")
    total = len(cases)
    if bad == 0:
        print(f"  [OK] {label}：{total} 组全过")
    else:
        print(f"  [X] {label}：{total} 组里错了 {bad} 组")
    return bad


def random_cases(count, seed=0):
    rnd = random.Random(seed)
    out = []
    for _ in range(count):
        m = rnd.randint(0, 4)
        n = rnd.randint(0, 4)
        base = sorted(rnd.randint(-5, 5) for _ in range(m))
        add = sorted(rnd.randint(-5, 5) for _ in range(n))
        out.append((base + [0] * n, m, add, n))
    return out


def main():
    cases = FIXED + random_cases(300)
    print(f"固定反例 {len(FIXED)} 组 + 随机 300 组\n")
    total_bad = 0
    for fn, label in ((merge_v1, "merge_v1"), (merge_v2, "merge_v2")):
        total_bad += check(fn, label, cases)
    print()
    if total_bad == 0:
        print("两个版本都全过 —— 可以上 LeetCode 提交了。")
        return 0
    print("别只盯着题面那一组样例。先自己 debug，卡住再来找我。")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
