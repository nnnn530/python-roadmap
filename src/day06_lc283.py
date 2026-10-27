r"""LC 283. 移动零（2026-10-27）

题目：把数组里所有 0 移到末尾，非零元素的**相对顺序不变**。
      **原地修改 nums，函数返回 None。**

三个前提（先圈出来再写）：
    1. 原地改 —— 不能 return 一个新数组，LeetCode 判的是 nums 本身
    2. 非零元素相对顺序不能变 —— 所以不能简单 sorted
    3. 0 可能一个都没有，也可能全是 0

运行方式：
    cd D:\code\python-roadmap
    python src\day06_lc283.py

提交地址：
    https://leetcode.cn/problems/move-zeroes/

两版，按顺序写：
    v1 覆盖 + 补零：slow 指向下一个非零该放的位置，fast 扫全表，
                    扫完把 [slow, len) 补 0          （两趟，好懂，先 AC）
    v2 交换：       nums[slow], nums[fast] = nums[fast], nums[slow]
                    一趟搞定，每个非零元素最多移动一次  （进阶要求）

提示（写完再对照，别照抄）：
    - slow 只在「真的放进一个非零数」时才 +1，跳过 0 时不动
    - v1 里 slow 走到末尾后，剩下的位置必须手动清零 —— 忘了就是今天的
      「假通过」：样例可能刚好过，全 0 的用例立刻暴露
"""


def move_zeroes_v1(nums):
    """v1：覆盖 + 补零。原地改 nums，返回 None。

    例：nums = [0,1,0,3,12] -> nums 变成 [1,3,12,0,0]
    """
    slow = 0 ; fast = 0
    while fast < len(nums):
        if nums[fast] != 0:
            nums[slow] = nums[fast]
            slow += 1
        fast += 1
    for i in range(slow, len(nums)):
        nums[i] = 0
    return None
    


def move_zeroes_v2(nums):
    """v2：交换。原地改 nums，返回 None。每个非零元素最多移动一次。

    例：nums = [0,1,0,3,12] -> nums 变成 [1,3,12,0,0]
    """
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != 0:
            if slow != fast:
                nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1
    return None



if __name__ == "__main__":
    # 边界一个都别省：这题的 bug 基本都藏在「没有 0」和「全是 0」里。
    for fn in (move_zeroes_v1, move_zeroes_v2):
        name = fn.__name__

        nums = [0, 1, 0, 3, 12]
        assert fn(nums) is None, f"{name} 必须返回 None"
        assert nums == [1, 3, 12, 0, 0], f"{name} 题面样例: {nums}"

        nums = [0]
        fn(nums)
        assert nums == [0], f"{name} 单个 0: {nums}"

        nums = []
        fn(nums)
        assert nums == [], f"{name} 空数组: {nums}"

        nums = [0, 0, 0]
        fn(nums)
        assert nums == [0, 0, 0], f"{name} 全 0: {nums}"

        nums = [1, 2, 3]
        fn(nums)
        assert nums == [1, 2, 3], f"{name} 无 0: {nums}"

        nums = [0, 0, 1]
        fn(nums)
        assert nums == [1, 0, 0], f"{name} 0 在前面: {nums}"

        nums = [1, 0]
        fn(nums)
        assert nums == [1, 0], f"{name} 长度 2: {nums}"

    print("全部通过")
