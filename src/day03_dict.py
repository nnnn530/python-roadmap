r"""day03 语法练习（2026-10-24）

主题：dict / set / 条件判断 / 循环

运行方式：
    cd D:\code\python-roadmap
    python src\day03_dict.py

做完后提交：
    git add . && git commit -m "day03: 词频统计 + dict 练习" && git push

提示：每个函数把 pass 换成你自己的代码，别删 docstring。
"""


def word_count(text):
    """统计 text 里每个单词出现的次数，返回 {单词: 次数}。

    例：word_count("a b a c a") -> {'a': 3, 'b': 1, 'c': 1}

    核心：用 d.get(w, 0) + 1 累加。
    """
    counts = {}
    for w in text.split():
        counts[w] = counts.get(w, 0) + 1
    return counts


def top_n(counts, n):
    """按次数从高到低取前 n 个，返回 [(单词, 次数), ...]。

    例：top_n({"a": 3, "b": 1, "c": 2}, 2) -> [('a', 3), ('c', 2)]

    提示：sorted(counts.items(), key=?, reverse=?)
    """
    return sorted(counts.items(), key=lambda p: p[1], reverse=True)[:n]


def flatten(nested):
    """把二维列表压成一维，用 for 循环，别用库。

    例：flatten([[1, 2], [3, 4]]) -> [1, 2, 3, 4]
        flatten([[], [1]]) -> [1]
    """
    result = []
    for sub in nested:
        for x in sub:
            result.append(x)
    return result


def list_ops():
    """拿 [3, 1, 4, 1, 5] 练 append / insert / pop，每步 print 出来。

    这个函数不需要返回值，看着终端输出自己对。
    """
    a =  [3, 1, 4, 1, 5]
    print(a)
    a.append(9)
    print(a)
    a.insert(0,7)
    print(a)
    x = a.pop()
    print(x,a)
    y = a.pop(0)
    print(y,a)
    a.remove(1)
    print(a)
    print(len(a))

    
    


if __name__ == "__main__":
    # 下面这段是自测，只有在 python src\day03_dict.py 直接运行时才会执行
    print(word_count("a b a c a"))  # 期望：{'a': 3, 'b': 1, 'c': 1}
    assert flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]
    assert flatten([[], [1]]) == [1]

    assert top_n({"a": 3, "b": 1, "c": 2}, 2) == [("a", 3), ("c", 2)]

    list_ops()

    print("全部通过")
