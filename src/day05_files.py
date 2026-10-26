r"""day05 语法练习（2026-10-26）

主题：文件读写 / 异常处理 / 列表生成式

运行方式：
    cd D:\code\python-roadmap
    python src\day05_files.py

做完后提交：
    git add . && git commit -m "day05: 文件/异常/推导式" && git push

提示：每个函数把 pass 换成你自己的代码，别删 docstring（docstring 写的就是验收标准）。
"""

import csv
from pathlib import Path
from day03_dict import word_count, top_n
# 这样写，不管从哪个目录运行，路径都指向仓库根目录下的 data/
DATA = Path(__file__).resolve().parent.parent / "data"


def read_file(path):
    """读一个文本文件，返回 (行数, 字符数)。

    例：文件内容是 "a b\nc\n" -> 返回 (2, 6)
        （2 行，字符数 6 = "a b\nc\n" 的长度，换行符也算）

    提示：
      - 用 with open(path, "r", encoding="utf-8") as f: 打开，with 会自动关文件
      - f.read() 一次读成一个大字符串；f.readlines() 读成列表，每个元素一行且**带 \\n**
      - 行数用 len(...)，字符数用 len(...)，两个 len 的对象不一样
    """
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return len(text.splitlines()),len(text)


def word_freq_from_file(path, n):
    """读文件，统计词频，返回出现次数最多的前 n 个 [(单词, 次数), ...]。

    例：word_freq_from_file(DATA / "q.txt", 2) -> [('the', 4), ('fox', 2)]

    提示：
      - 先读文本，再复用昨天的函数：from day03_dict import word_count, top_n
        （因为 day05_files.py 和 day03_dict.py 在同一个 src 目录下，可以直接 import）
      - 两个函数都写好了，你要写的只有「读文件」这一步
      - 按空格切词就能用，不用管标点
    """
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    counts = word_count(text)
    return top_n(counts,n)


def safe_read(path):
    """读文件，但文件不存在时**不许崩**。

    文件存在 -> 返回文件内容（str）
    文件不存在 -> 打印一句提示，返回 None

    例：safe_read(DATA / "不存在.txt") -> 打印提示，返回 None，程序继续跑

    提示：
      - try: ... except FileNotFoundError: ...
      - 想验证「except 真的被执行了」，就在 except 里 print 一行
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"文件不存在：{path}")
        return None


def csv_roundtrip(path, rows):
    """把 rows 写进 csv 文件，再读回来，返回「读回的内容是否和 rows 完全一致」（bool）。

    例：csv_roundtrip(DATA / "out.csv", [["a", "1"], ["b", "2"]]) -> True

    提示：
      - 写：with open(path, "w", encoding="utf-8", newline="") as f: csv.writer(f).writerows(rows)
      - 读：csv.reader(f) 读回来是**字符串**的二维列表，rows 里的 "1" 也得是字符串才能相等
      - 写文件时 newline="" 是 csv 模块的官方要求，不然 Windows 上会多出空行
      - 注意：rows 是 list[list[str]]，不是 list[dict]
    """
    with open(path, "w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(rows)
    with open(path, "r", encoding="utf-8", newline="") as f:  
        back = list(csv.reader(f))
    return back == rows


def clean_words(text):
    """（可选，10 分钟）用**列表生成式**把 text 变成干净的小写单词列表。

    例：clean_words("The FOX, the dog!") -> ['the', 'fox', 'the', 'dog']

    提示：
      - 一行写完：return [ ... for w in text.split() ... ]
      - 去标点可以用 w.strip(",.!?;:")，转小写用 w.lower()
      - 这就是廖雪峰「列表生成式」那一节的主场：带 if 的写法 [x for x in xs if 条件]
    """
    pass


if __name__ == "__main__":
    # 下面这段是自测，只有 python src\day05_files.py 直接运行才会执行。
    # 自己补 assert：正常路径 + 异常路径都要测。
    lines, chars = read_file(DATA / "sample.txt")
    assert lines == 6, f"行数错了：拿到 {lines}"
    assert chars == 304, f"字符数错了：拿到 {chars}"
    assert word_freq_from_file(DATA / "sample.txt", n=2) == [('the', 5), ('a', 4)]
    assert word_freq_from_file(DATA/ "sample.txt",n=5) == [('the', 5), ('a', 4), ('you', 3), ('quick', 2), ('fox', 2)]
    assert safe_read(DATA / "sample.txt").startswith("the quick")
    assert safe_read(DATA / "不存在.txt") is None     # 这行能跑完，就说明 except 生效了
    # 如果 except 没生效，上面这行会直接抛异常，程序在此结束，"全部通过"不会打印
    assert csv_roundtrip(DATA / "out.csv", [["a", "1"], ["b", "2"]]) is True
    assert csv_roundtrip(DATA / "out.csv", [["x,y", "3"]]) is True     # 带逗号，测转义
    # 反面教材：下面这行是故意写错的，用来验证函数真返回 bool 而不是返回列表。
    # 验证完必须注释掉，否则脚本每次都停在这里。跑法：取消注释 → 看它报错 → 再注释回去。
    # assert csv_roundtrip(DATA / "out.csv", [["a", "1"]]) == [["a", "1"]]
    print("全部通过")
