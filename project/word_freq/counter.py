"""词频统计：这个文件只负责「算」，不打印、不读写文件、不退出程序。

为什么这么分？因为它要能被别的东西直接拿去用：
  - 明天写 pytest 测试它
  - 后天写个网页接口，用户点一下就调它
如果它里面 print 了，测试输出会被污染，网页接口也会返回一堆乱码。
"""


def count_words(text):
    """把一段文本变成 {单词: 出现次数}。

    例：count_words("a b a c a") -> {'a': 3, 'b': 1, 'c': 1}
    例：count_words("")          -> {}          # 空文本不会报错，直接空字典
    """
    counts = {}
    # split() 括号里不给东西 = 按所有空白字符切开（空格、换行、Tab 都算）
    for word in text.split():
        # 字典里没有这个词就当 0 次，然后再 +1
        counts[word] = counts.get(word, 0) + 1
    return counts


def top_n(counts, n):
    """按次数从多到少取前 n 个，返回 [('the', 5), ('a', 4), ...]。

    例：top_n({'a': 3, 'b': 1, 'c': 2}, 2) -> [('a', 3), ('c', 2)]
    例：top_n({'a': 1}, 5)                 -> [('a', 1)]     # n 比词多，全给就行
    """
    if n <= 0:
        # 坑：不拦的话 counts 切片会变成 ordered[:-1]（倒着数），
        # 结果就是「少几个词」而不报错 —— 这就是 Py 的负索引静默行为。
        return []

    pairs = counts.items()
    # 按每个 (单词, 次数) 里的第 2 个元素（也就是次数）从大到小排
    ordered = sorted(pairs, key=lambda pair: pair[1], reverse=True)
    return ordered[:n]


if __name__ == "__main__":
    # 只有直接运行这个文件时才跑自测；被 main.py import 时不会跑。
    assert count_words("a b a c a") == {"a": 3, "b": 1, "c": 1}
    assert count_words("") == {}
    assert count_words("a\nb\ta") == {"a": 2, "b": 1}      # 换行、Tab 也要能切开
    assert top_n({"a": 3, "b": 1, "c": 2}, 2) == [("a", 3), ("c", 2)]
    assert top_n({"a": 1}, 5) == [("a", 1)]
    assert top_n({"a": 1}, 0) == []
    print("counter.py 全部通过")
