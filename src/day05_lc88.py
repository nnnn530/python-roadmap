r"""LC 88. 合并两个有序数组（2026-10-26）

题目：nums1 长度是 m + n，前 m 个是有效数据，后 n 个 0 是空位；
      nums2 长度是 n。把 nums2 合并进 nums1，结果非递减。
      **原地修改 nums1，函数返回 None。**

注意三个前提（昨天 26 题就是漏了数据前提）：
    1. 两个数组都已经非递减有序 —— 不是乱序合并
    2. 必须原地改 nums1，不能 return 一个新数组
    3. nums1 后面那 n 个 0 是占位符，不是真实数据，排序时不能带进去

运行方式：
    cd D:\code\python-roadmap
    python src\day05_lc88.py

提交地址：
    https://leetcode.cn/problems/merge-sorted-array/

两版，按顺序写：
    v1 暴力：有效部分 + nums2 拼起来 → 排序 → 塞回 nums1[:]     （5 分钟，先 AC）
    v2 双指针从后往前：p1 = m-1，p2 = n-1，p = m+n-1，谁大填谁    （正解，O(m+n)）

提示（写完再对照，别照抄）：
    - nums1[:] = ...   改的是「同一个列表的内容」，外部能看到
    - nums1 = ...      只是让名字指向新列表，外部看不到，等于没改
"""


def merge_v1(nums1, m, nums2, n):
    """v1：能过就行，不管效率。原地改 nums1，返回 None。

    例：nums1 = [1,2,3,0,0,0], m=3, nums2=[2,5,6], n=3
        -> nums1 变成 [1,2,2,3,5,6]
    """
    for i in range(m,m+n):
        nums1[i] = nums2[i-m]
    nums1[:] = sorted(nums1)
    return None


def merge_v2(nums1, m, nums2, n):
    """v2：双指针从后往前，原地改 nums1，返回 None。

    想一想再动手：为什么从后往前填，就不会覆盖掉还没用到的元素？
    （从前往后填会发生什么？拿 [4,5,6,0,0,0] + [1,2,3] 在纸上走一遍）
    """
    p = m+n-1
    while n > 0:                      # 燃料是 nums2，它空了就收工
        if m > 0 and nums1[m-1] > nums2[n-1]:
            nums1[p] = nums1[m-1]
            m -= 1
        else:
            nums1[p] = nums2[n-1]
            n -= 1
        p -= 1
       
    




if __name__ == "__main__":
    a = [1, 2, 3, 0, 0, 0]
    merge_v1(a, 3, [2, 5, 6], 3)
    assert a == [1, 2, 2, 3, 5, 6], f"v1 错了：{a}"

    b = [1, 2, 3, 0, 0, 0]
    merge_v2(b, 3, [2, 5, 6], 3)
    assert b == [1, 2, 2, 3, 5, 6], f"v2 错了：{b}"

    # TODO: 补两条边界，自己想数据（写完两版再补）
    #   1. n = 0：nums2 为空，nums1 不该变
    #   2. m = 0：nums1 全是占位，结果应该就是 nums2

    print("全部通过")
