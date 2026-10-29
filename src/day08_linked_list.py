r"""day08 单链表（2026-10-29）

今天第一半：Node + LinkedList 的 append / to_list / __len__
（prepend / delete / reverse 等你这三个跑绿，我再补进这个文件）

链表长这样 —— 每个格子只认识下一个格子，谁都不认识「自己排第几」：

    self.head
        ↓
    [ 1 | · ]→[ 2 | · ]→[ 3 | None ]
      value next

运行：
    cd D:\code\python-roadmap
    python src\day08_linked_list.py
"""


class Node:
    """链表的一个格子：装一个值，外加「下一个格子在哪」。"""

    def __init__(self, value):
        self.value = value
        self.next = None        # None = 后面没有了，链表到此结束


class LinkedList:
    """只存一个 head；其余节点全靠 head 一路 next 摸过去。"""

    def __init__(self):
        self.head = None        # 第一个节点；空链表时是 None
        self.size = 0           # 自己数着，让 len() 是 O(1)，不用每次现数

    # ---------- 下面三个方法你来写 ----------

    def append(self, value):
        """尾插：把 value 装成新节点，接到链表最后面。

        ll = LinkedList(); ll.append(1); ll.append(2)  →  1 → 2

        四步（照着写，顺序别乱）：
          1) 造：new = Node(value)
          2) 空链表：self.head is None 时，让 head 指向 new（这条分支不写，节点就丢了）
          3) 非空：从头往后走，停在 next 是 None 的那个节点上，把它的 next 指到 new
             （注意：走的是 while，判断条件用 next is not None，别用 node is not None）
          4) self.size += 1
        """
        # TODO: 写这四步
        new = Node(value)
        if self.head is None:
            self.head = new
        else:
            node = self.head
            while node.next is not None:   # 只要后面还有，就往前挪
                node = node.next           # 便签挪到下一个节点
            node.next = new            # 停在最后一个节点上了，挂上去
        self.size += 1          

    def to_list(self):
        """把链表摊平成普通 list：[1, 2, 3]。空链表返回 []。"""
        # TODO: 造一个空 list，从 head 开始一路 next 收集 value，最后 return
        out = []
        node = self.head
        while node is not None:
            out.append(node.value)
            node = node.next
        return out
    def __len__(self):
        """定义了它，len(ll) 就能用。直接返回 self.size。"""
        # TODO: 一行
        return self.size

    # ---------- 第二半：你来写 ----------

    def prepend(self, value):
        """头插：新节点插到最前面，成为新的 head。

        ll.prepend(0)  →  0 → 1 → 2

        就两行，但**顺序不能反**：
            先让新节点的 next 指向原来的 head，再把 head 改成新节点。
        反了就完蛋：先把 head 改了，旧链表就从手里丢了，再也找不回来。
        self.size += 1 别忘了。
        """
        # TODO: 两行 + size
        new = Node(value)
        new.next = self.head
        self.head = new
        self.size += 1
        

    def delete(self, value):
        """删掉**第一个**值等于 value 的节点。删掉了返回 True，没找到返回 False。

        ll = 1 → 2 → 3
        ll.delete(2)  →  True，链表变成 1 → 3
        ll.delete(9)  →  False，链表不动

        难点：删中间节点需要拿到**它的前一个**（prev），才能 prev.next = cur.next 跳过它。
              但 head 没有前一个 → 单独判（if self.head.value == value: self.head = self.head.next）
              空链表先返回 False（不然 self.head.value 直接 AttributeError）
        """
        # TODO: 四段——空链表 / 删头 / 遍历找（记住 prev）/ 没找到
        if self.head == None:
            return False
        if self.head.value == value:
            self.head = self.head = self.head.next
            self.size -= 1
            return True
        pre = self.head
        cur = self.head.next
        while cur is not None:
            if cur.value == value:
                pre.next = cur.next
                self.size -= 1
                return True
            pre = pre.next
            cur = cur.next
        return False

    def reverse(self):
        """原地反转，不许新建链表，也不许新建节点，只改 next 指向。

        1 → 2 → 3 变成 3 → 2 → 1

        三张便签，循环里四句话（顺序别乱）：
            nxt = cur.next      # 先记住后面那个（不然等下 cur.next 一改就跟丢了）
            cur.next = prev     # 把当前节点的箭头掉头
            prev = cur          # prev 往前挪
            cur = nxt           # cur 往前挪
        循环结束时 prev 就是新的 head。
        """
        # TODO
        prev = None              # 已反转段：一开始是空的
        cur = self.head          # 未反转段：从头开始
        while cur is not None:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        self.head = prev

if __name__ == "__main__":
    # 1) 空链表：不崩，且长度是 0
    ll = LinkedList()
    assert ll.to_list() == [], f"空链表 to_list 应该是 []，拿到 {ll.to_list()}"
    assert len(ll) == 0, f"空链表长度应该是 0，拿到 {len(ll)}"

    # 2) 单节点
    ll.append(1)
    assert ll.to_list() == [1], f"单节点错了：{ll.to_list()}"
    assert len(ll) == 1, f"单节点长度错了：{len(ll)}"

    # 3) 多节点，且顺序必须是插入顺序（尾插）
    ll.append(2)
    ll.append(3)
    assert ll.to_list() == [1, 2, 3], f"多节点错了：{ll.to_list()}"
    assert len(ll) == 3, f"多节点长度错了：{len(ll)}"

    # 4) 直接查链表结构：head 是 1，最后一个节点的 next 必须是 None
    assert ll.head.value == 1, f"head 应该是 1，拿到 {ll.head.value}"
    node = ll.head
    while node.next is not None:
        node = node.next
    assert node.value == 3, f"最后一个节点应该是 3，拿到 {node.value}"

    # 5) 新链表互不干扰（别把节点存成类属性，那就成全局共享了）
    other = LinkedList()
    other.append(9)
    assert other.to_list() == [9] and ll.to_list() == [1, 2, 3], "两条链表串味了"

    # 6) 头插
    l2 = LinkedList()
    l2.prepend(2)
    assert l2.to_list() == [2] and len(l2) == 1, f"空链表头插错了：{l2.to_list()}"
    l2.prepend(1)
    l2.prepend(0)
    assert l2.to_list() == [0, 1, 2], f"头插顺序错了（应该是倒着插）：{l2.to_list()}"
    assert len(l2) == 3, f"头插后长度错了：{len(l2)}"

    # 7) 删除头节点
    assert l2.delete(0) is True, "删头节点应该返回 True"
    assert l2.to_list() == [1, 2], f"删头节点后错了：{l2.to_list()}"
    assert len(l2) == 2, f"删头节点后长度错了：{len(l2)}"

    # 8) 删除中间节点 / 尾节点
    l3 = LinkedList()
    for v in (1, 2, 3):
        l3.append(v)
    assert l3.delete(2) is True, "删中间节点应该返回 True"
    assert l3.to_list() == [1, 3], f"删中间节点后错了：{l3.to_list()}"
    assert l3.delete(3) is True, "删尾节点应该返回 True"
    assert l3.to_list() == [1], f"删尾节点后错了：{l3.to_list()}"
    assert l3.head.next is None, "删到只剩一个节点时 head.next 必须是 None"
    assert len(l3) == 1, f"删尾节点后长度错了：{len(l3)}"

    # 9) 删除不存在的值 / 空链表删除
    assert l3.delete(99) is False, "删不存在的值应该返回 False"
    assert l3.to_list() == [1] and len(l3) == 1, "删不存在的值不该改变链表"
    empty = LinkedList()
    assert empty.delete(1) is False, "空链表删除应该返回 False"
    assert empty.to_list() == [] and len(empty) == 0

    # 10) reverse：空 / 单 / 多
    r0 = LinkedList()
    r0.reverse()
    assert r0.to_list() == [] and len(r0) == 0, "空链表 reverse 不该崩"

    r1 = LinkedList()
    r1.append(1)
    r1.reverse()
    assert r1.to_list() == [1] and len(r1) == 1, "单节点 reverse 错了"

    r4 = LinkedList()
    for v in (1, 2, 3, 4):
        r4.append(v)
    r4.reverse()
    assert r4.to_list() == [4, 3, 2, 1], f"reverse 错了：{r4.to_list()}"
    assert r4.head.value == 4, f"reverse 后 head 应该是 4，拿到 {r4.head.value}"
    assert len(r4) == 4, f"reverse 后长度应该不变：{len(r4)}"
    assert r4.to_list()[0] == 4 and r4.to_list()[-1] == 1

    # 11) reverse 两次 = 变回原样（这条最能抓「改丢节点」的 bug）
    r5 = LinkedList()
    for v in (7, 8, 9):
        r5.append(v)
    r5.reverse()
    r5.reverse()
    assert r5.to_list() == [7, 8, 9], f"reverse 两次应该复原，拿到 {r5.to_list()}"

    print(f"ll.to_list() = {ll.to_list()}，len = {len(ll)}")
    print("全部通过（11 组断言）")
