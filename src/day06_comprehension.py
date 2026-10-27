r"""day06 练习（2026-10-27）

主题：列表生成式 / 字典推导式 / 切片 / 迭代

运行方式：
    cd D:\code\python-roadmap
    python src\day06_comprehension.py

要求：每个函数都用推导式写（不许用 for + append），并且每个函数至少 1 条
assert，其中必须有一条喂空列表 / 空串 / 单元素。
写完自问：「如果我把实现写错，哪条 assert 会拦住我？」
"""


def squares(n):
    """返回 1..n 里所有**偶数**的平方，列表生成式一行写完。

    例：squares(6) -> [4, 16, 36]
        squares(0) -> []
        squares(1) -> []

    提示：range(1, n + 1) 才取得到 n；偶数用 i % 2 == 0。
    这是「for 后面带 if」的过滤写法。
    """
    return [i * i for i in range(1, n + 1) if i % 2 == 0]


def flatten_comp(nested):
    """用两层列表生成式把二维列表压平。

    例：flatten_comp([[1, 2], [3], []]) -> [1, 2, 3]
        flatten_comp([]) -> []
        flatten_comp([[], []]) -> []

    提示：两层 for 的顺序和嵌套循环一致，外层写前面：
        [x for row in nested for x in row]
    写完对比 day03 的 flatten（for + extend 版）：哪个更快读懂？哪个更短？
    """
    return [x for row in nested for x in row]


def to_lower(words):
    """把字符串列表全部转成小写。

    例：to_lower(["A", "bC", ""]) -> ["a", "bc", ""]
        to_lower([]) -> []

    注意：这题**不是**过滤题 —— 空串 lower() 之后还是空串，要原样留着。
    如果你顺手写了 if，那说明你把「过滤」和「改写」搞混了。
    """
    return [c.lower() for c in words ]


def dict_comp(nums):
    """字典推导式：{偶数: 它的平方}，只保留偶数。

    例：dict_comp([1, 2, 3, 4]) -> {2: 4, 4: 16}
        dict_comp([]) -> {}
        dict_comp([1, 3]) -> {}

    提示：{键表达式: 值表达式 for x in nums if 条件}
    """
    return {k: k**2 for k in nums if k % 2 == 0}


def top_words(text, n):
    """词频 Top n，返回 [(词, 次数), ...]，按次数从高到低。

    例：top_words("a b a c a", 2) -> [('a', 3), ('b', 1)]
        top_words("", 3) -> []
        top_words("a", 5) -> [('a', 1)]     # n 超过词数不报错

    提示：
      - 复用现成的：from day03_dict import word_count
      - 先用推导式把 items 变成 [(词, 次数)]：[(w, c) for w, c in counts.items()]
      - 再 sorted(..., key=..., reverse=True)[:n]
    写完对比 day03 的 top_n：两版差在哪？要改成「按次数升序」各要动几个字？
    """
    from day03_dict import word_count
    counts = word_count(text)
    return sorted(counts.items(), key=lambda p: p[1], reverse=True)[:n]




if __name__ == "__main__":
    # 下面自己写 assert，跑 python src\day06_comprehension.py 直接执行到这里。
    # 建议顺序：先写正常样例 → 跑 → 再补空输入 → 再跑。
    # 一条断言都没写就别打印"全部通过"。
    assert squares(6) == [4, 16, 36]
    assert squares(0) == []     # range(1, 1) 空
    assert squares(1) == []     # 1 是奇数，被 if 过滤掉
    assert flatten_comp([[1, 2], [3], []]) == [1, 2, 3]
    assert flatten_comp([]) == []
    assert flatten_comp([[], []]) == []
    assert to_lower(["A", "bC", ""]) == ["a", "bc", ""]
    assert to_lower([]) == []

    assert dict_comp([1, 2, 3, 4]) == {2: 4, 4: 16}
    assert dict_comp([]) == {}
    assert dict_comp([1, 3]) == {}

    assert top_words("a a a b b c", 2) == [('a', 3), ('b', 2)]
    assert top_words("", 3) == []
    assert top_words("a", 5) == [('a', 1)]
    print("全部通过")
