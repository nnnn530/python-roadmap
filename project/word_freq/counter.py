"""词频统计：这个文件只负责「算」，不打印、不读写文件、不退出程序。

日志规范同上：只 getLogger，不配置。
注意 log.xxx 用的是 %s 占位而不是 f-string —— 因为日志被级别挡住时，
f-string 已经把字符串拼好了（白干），占位符则是真到要输出时才格式化。
"""

import logging

log = logging.getLogger(__name__)


def count_words(text):
    """把一段文本变成 {单词: 出现次数}。

    例：count_words("a b a c a") -> {'a': 3, 'b': 1, 'c': 1}
    例：count_words("")          -> {}
    """
    counts = {}
    for word in text.split():
        counts[word] = counts.get(word, 0) + 1
    log.debug("统计完成：%d 个不同的词", len(counts))
    return counts


def top_n(counts, n):
    """按次数从多到少取前 n 个，返回 [('the', 5), ('a', 4), ...]。

    例：top_n({'a': 3, 'b': 1, 'c': 2}, 2) -> [('a', 3), ('c', 2)]
    """
    if n <= 0:
        # 双重防御：入口已经用 positive_int 拦过 n<1，
        # 但这个函数是「库」，不能假设调用方守规矩（明天网页接口也会调它）。
        # 不拦的话 counts 切片会变成 ordered[:-1]（倒着数），少几个词还不报错。
        log.warning("top_n 收到非法的 n=%s，返回空列表", n)
        return []

    pairs = counts.items()
    ordered = sorted(pairs, key=lambda pair: pair[1], reverse=True)
    return ordered[:n]


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s %(name)s: %(message)s")

    assert count_words("a b a c a") == {"a": 3, "b": 1, "c": 1}
    assert count_words("") == {}
    assert count_words("a\nb\ta") == {"a": 2, "b": 1}
    assert top_n({"a": 3, "b": 1, "c": 2}, 2) == [("a", 3), ("c", 2)]
    assert top_n({"a": 1}, 5) == [("a", 1)]
    assert top_n({"a": 1}, 0) == []
    print("counter.py 全部通过")
