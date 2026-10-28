r"""day07 LeetCode 344. 反转字符串（2026-10-28）

题目（大白话）：给你一个字符清单，比如 ["h","e","l","l","o"]，
把它的顺序整个倒过来，变成 ["o","l","l","e","h"]。

规矩：必须「原地」改 —— 不许造一个新列表再 return。
    s = s[::-1]        ❌ 造了个新列表，原来那个 s 一动没动
    s[:] = s[::-1]     ✅ 往原来那个列表里塞，这才叫原地

运行：
    cd D:\code\python-roadmap
    python src\day07_lc344.py
"""


def reverse_string(s):
    """原地反转，返回 None（调用方自己看 s 变成什么样了）。

    s: list[str]
    """
    l = 0                 # 左手，最左边
    r = len(s) - 1        # 右手，最右边
    while l < r:
        # TODO: 这里写一行，把 s[l] 和 s[r] 对调
        s[l], s[r] = s[r], s[l]
        # 下面两行是「两只手往中间挪」，已经写好了，别删
        l += 1
        r -= 1


def reverse_string_slice(s):
    """同样原地反转，但用切片一行写完（进阶题）。

    提示：s[:] = s[::-1]
    """
    # TODO: 这里写一行
    s[:] = s[::-1]


if __name__ == "__main__":
    # 1) 题面样例
    a = ["h", "e", "l", "l", "o"]
    reverse_string(a)
    assert a == ["o", "l", "l", "e", "h"], f"样例错了：{a}"

    # 2) 自己造的边界：空 / 单个 / 两个 / 偶数个
    b = []
    reverse_string(b)
    assert b == [], f"空列表错了：{b}"

    c = ["a"]
    reverse_string(c)
    assert c == ["a"], f"单字符错了：{c}"

    d = ["a", "b"]
    reverse_string(d)
    assert d == ["b", "a"], f"两个字符错了：{d}"

    e = list("abcd")
    reverse_string(e)
    assert e == list("dcba"), f"偶数个错了：{e}"

    # 3) 切片版
    f = list("algorithm")
    reverse_string_slice(f)
    assert f == list("mhtirogla"), f"切片版错了：{f}"

    # 4) 随机压测：两个版本都必须和标准答案 src[::-1] 完全一致
    import random

    for _ in range(2000):
        n = random.randint(0, 8)
        src = [random.choice("abc") for _ in range(n)]
        expect = src[::-1]

        x = src[:]                    # 拷贝一份再传，别让两次调用互相污染
        reverse_string(x)
        assert x == expect, f"双指针错了：输入 {src}，期望 {expect}，拿到 {x}"

        y = src[:]
        reverse_string_slice(y)
        assert y == expect, f"切片版错了：输入 {src}，期望 {expect}，拿到 {y}"

    print("全部通过（5 组手写断言 + 2000 组随机压测）")
