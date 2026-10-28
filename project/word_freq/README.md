# 词频统计器 v1

给一个 txt 文件，告诉里面出现最多的词。

## 用法

在仓库根目录 `D:\code\python-roadmap` 下执行：

```bash
# 看参数说明
python project\word_freq\main.py -h

# 统计 data\sample.txt，输出前 5 个词（默认前 10 个）
python project\word_freq\main.py --file data\sample.txt --top 5
```

输出：

```
the         5
a           4
you         3
quick       2
fox         2
```

```bash
# 把结果写成 JSON 文件，打印到屏幕换成一句"已写入"
python project\word_freq\main.py --file data\sample.txt --top 3 --output out.json
```

`out.json` 内容：

```json
{
  "file": "data\\sample.txt",
  "top": {
    "the": 5,
    "a": 4,
    "you": 3
  }
}
```

## 参数

| 参数 | 必填 | 默认 | 说明 |
|---|---|---|---|
| `--file` | 是 | — | 要统计的 txt 文件路径 |
| `--top` | 否 | `10` | 输出前 N 个词 |
| `--output` | 否 | 无（打印到屏幕） | 把结果写成 JSON 文件 |

## 文件分工

```
project/word_freq/
├── main.py      # 跟用户打交道：解析参数、打印、决定退出码
├── counter.py   # 只管算：count_words / top_n，不打印
├── io_utils.py  # 只管读写：read_text / write_json，不打印
└── README.md    # 就是你正在看的这个
```

`counter.py` 和 `io_utils.py` 里没有一句 `print`，也没有 `sys.exit`。
这样它们能被 pytest 直接测、能被别的程序直接调用。

## 出错时

| 情况 | 输出 | 退出码 |
|---|---|---|
| 文件不存在 | `错误：找不到文件 xxx.txt` | 1 |
| 传的是文件夹 | `错误：xxx 是个文件夹（或者我没有权限读），请给一个 txt 文件` | 1 |
| 不是 UTF-8 文本 | `错误：xxx 不是 UTF-8 编码的文本，读不了` | 1 |
| 没给 `--file` | argparse 自动报 `required: --file` | 2 |
| `--top` 不是数字 | argparse 自动报 `invalid int value` | 2 |

退出码 0 = 成功，非 0 = 失败，写脚本串流程时靠它判断。

## 自测

```bash
python project\word_freq\counter.py     # counter.py 全部通过
python project\word_freq\io_utils.py    # io_utils.py 全部通过
```

## 已知限制（v1 故意不做）

- 按空白切词，标点跟着单词走：`dog,` 和 `dog` 算两个词
- 区分大小写：`The` 和 `the` 算两个词
- 次数相同时，按首次出现的先后排（`sorted` 是稳定排序）
