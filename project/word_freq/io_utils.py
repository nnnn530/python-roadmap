"""文件读写：这个文件只负责「搬数据」。

关键点：读文件失败时**故意不处理**，让 FileNotFoundError 往上冒，
交给 main.py 去变成一句人话。这样同一个函数，
今天给命令行用、明天给网页接口用，都能各自决定怎么报错。
"""

import json


def read_text(path):
    """读文件全部内容，返回一个字符串。

    文件不存在会抛 FileNotFoundError —— 这是故意的，别在这里 try/except。
    with 会在读完后自动关文件，不用手动 f.close()。
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_json(path, data):
    """把 data 写成 JSON 文件。

    ensure_ascii=False：中文原样写出来，而不是变成 \\u4f60 那种乱码样。
    indent=2：缩进 2 格，人看得懂。
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")   # 文件末尾补个换行，git 不会提示 "No newline at end of file"


if __name__ == "__main__":
    from pathlib import Path

    DATA = Path(__file__).resolve().parent.parent.parent / "data"
    text = read_text(DATA / "sample.txt")
    assert text.startswith("the quick brown fox")
    assert len(text) == 304

    # 测「文件不存在会抛异常」：用 try 抓住它，抓不到就说明函数写错了
    try:
        read_text(DATA / "这个文件不存在.txt")
    except FileNotFoundError:
        pass
    else:
        raise AssertionError("读不存在的文件居然没抛 FileNotFoundError")

    write_json(DATA / "_tmp_test.json", {"a": 1, "中文": "正常"})
    assert json.loads(read_text(DATA / "_tmp_test.json")) == {"a": 1, "中文": "正常"}
    (DATA / "_tmp_test.json").unlink()      # 测完删掉，别留垃圾

    print("io_utils.py 全部通过")
