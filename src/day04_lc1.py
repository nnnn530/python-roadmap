r"""LC 1. 两数之和 —— 哈希表 O(n) 版（2026-10-25）

题目：给整数数组 nums 和整数 target，返回和为 target 的两个数的下标。
      保证恰好一个答案，同一个元素不能重复使用。

暴力版（2026-10-24）：双层循环 O(n²)，1719ms，击败 13.86%。
今天目标：一遍遍历 + dict，O(n)。

运行方式：
    cd D:\code\python-roadmap
    python src\day04_lc1.py

提交地址：
    https://leetcode.cn/problems/two-sum/

提示（写完再对照，别照抄）：
    1. 顺序必须是「先查后存」—— 存之前 dict 里只有前面的人，不可能查到自己
    2. key = 数字，value = 下标
"""


def two_sum(nums, target):
    """返回和为 target 的两个不同下标，无解返回 []。

    例：two_sum([2, 7, 11, 15], 9) -> [0, 1]
    """
    d = {}
    for i in range(len(nums)):
        if target - nums[i] in d:
            return [d[target - nums[i]],i]
        d[nums[i]] = i
    return []
            


if __name__ == "__main__":
    # 1. 题目样例
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]

    # 2. TODO: 补两条 —— 一条考「同一个元素不能重复用」，一条考「答案在数组末尾」
    #    参考数据：[3, 3] 目标 6 ／ [3, 2, 4] 目标 6
    assert two_sum([3, 2, 4], 6) == [1, 2]
    assert two_sum([3, 3], 6) == [0, 1]

    print("全部通过")
