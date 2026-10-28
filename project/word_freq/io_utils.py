r"""文件读写：只负责「搬数据」。

日志规范：这里只 getLogger，不配置（不 basicConfig、不加 Handler）。
因为它是「库」—— 不知道使用者要把日志打到屏幕还是写文件，那是入口的事。
"""

import json
import logging

log = logging.getLogger(__name__)


def read_text(path):
    """读文件全部内容，返回一个字符串。

    文件不存在会抛 FileNotFoundError —— 这是故意的，别在这里 try/except。
    谁调用谁负责解释这个错（命令行怎么说、网页怎么返回，各不一样）。
    """
    log.debug("准备读取：%s", path)
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    log.debug("读到 %d 个字符", len(text))
    return text


def write_json(path, data):
    """把 data 写成 JSON 文件。

    ensure_ascii=False：中文原样写出来，而不是变成 \u4f60。
    indent=2：缩进 2 格，人看得懂。
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")   # 末尾补换行，git 不会提示 "No newline at end of file"
    log.info("已写入 JSON：%s", path)


if __name__ == "__main__":
    import logging
    from pathlib import Path

    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s %(name)s: %(message)s")

    DATA = Path(__file__).resolve().parent.parent.parent / "data"
    text = read_text(DATA / "sample.txt")
    assert text.startswith("the quick brown fox")
    assert len(text) == 304

    try:
        read_text(DATA / "这个文件不存在.txt")
    except FileNotFoundError:
        pass
    else:
        raise AssertionError("读不存在的文件居然没抛 FileNotFoundError")

    write_json(DATA / "_tmp_test.json", {"a": 1, "中文": "正常"})
    assert json.loads(read_text(DATA / "_tmp_test.json")) == {"a": 1, "中文": "正常"}
    (DATA / "_tmp_test.json").unlink()

    print("io_utils.py 全部通过")
