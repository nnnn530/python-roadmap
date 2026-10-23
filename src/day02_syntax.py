r"""day02 语法练习（2026-10-23）

运行方式：
    cd D:\code\python-roadmap
    python src\day02_syntax.py

做完后提交：
    git add . && git commit -m "day02: 切片 + 回文 + tuple 交换" && git push

提示：每个函数把 pass 换成你自己的代码，别删 docstring。
"""


def slice_demo(s):
    """返回 3 个值：前 3 个字符、后 3 个字符、反转后的字符串。"""
    s1 = s[0:3:1]
    s2 = s[len(s)-3:len(s):1]
    s3 = s[::-1]
    return s1,s2,s3

def is_palindrome(s):
    """判断 s 是否回文（正着念和倒着念一样），用切片 s[::-1]。"""
    if s == s[::-1]:
        return True
    else:
        return False


def tuple_swap(a, b):
    """用 tuple 一步交换 a 和 b，返回交换后的 (a, b)。"""
    return b,a


if __name__ == "__main__":
    # 下面这段是自测，只有在 python src\day02_syntax.py 直接运行时才会执行
    print(slice_demo("abcdefg"))  # 期望：('abc', 'efg', 'gfedcba')

    assert is_palindrome("abcba") is True
    assert is_palindrome("abca") is False

    assert tuple_swap(1, 2) == (2, 1)

    print("全部通过")
