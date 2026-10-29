r"""day08 预热：class 到底怎么写（2026-10-29）

先不碰链表。这个文件只干一件事：让你看清 class 的语法骨架。
运行它，然后把最后那个 TODO 补掉，再改 append。

    cd D:\code\python-roadmap
    python src\day08_class_warmup.py

---------------------------------------------
一句话：class 是图纸，实例是照图纸造出来的实物。

    class Dog:            ← 图纸，写一次
        ...

    d = Dog("旺财")        ← 照图纸造一条狗，d 就是那个实物
    d.bark()              ← 让这条狗叫（不是让"图纸"叫）

self 就是"这条狗自己"。写方法时第一个参数永远是 self，
但你调用时不用传 —— d.bark() 里 Python 自动把 d 塞进 self。
"""


class Dog:
    def __init__(self, name):
        """__init__ = 造对象时自动跑一次，负责把属性装上去。

        Dog("旺财") 一执行：
          1) 先凭空造出一个空对象
          2) 把空对象当 self、把 "旺财" 当 name，跑这个方法
          3) 跑完把对象交给你（d）
        """
        self.name = name        # 往"自己身上"贴一张便签：name = "旺财"
        self.count = 0          # 每个新对象都从 0 开始

    def bark(self):
        """方法 = 长在对象身上的函数。第一个参数一定是 self。"""
        self.count += 1         # 改自己身上的 count；写 count += 1 就错了
        print(f"{self.name}: 汪！(第 {self.count} 次)")

    def __len__(self):
        """双下划线包着的是"给 Python 看的暗号"。
        定义了它，len(d) 才有人接。"""
        return self.count


class NumberBox:
    """和链表同构的小例子：一个 head（第一个数）+ 一个 size。

    链表的 append 和这里 add 的骨架一模一样：
        NumberBox.head  ↔  LinkedList.head
        self.size += 1  ↔  self.size += 1
    只是链表要把新节点"挂到最后一个节点后面"，这里只是塞进 list。
    """

    def __init__(self):
        self.head = None        # 空的时候就是 None —— 和链表一样
        self.size = 0

    def add(self, value):
        if self.head is None:   # 空盒子：第一个就是头
            self.head = value
        else:
            pass                # 非空：链表在这里要"走到尾巴再挂"
        self.size += 1

    def __len__(self):
        return self.size

    def reset(self):
        # TODO: 把这个盒子清空 —— 两行，一行把 head 变回 None，一行把 size 变回 0
        #       写完下面断言才会过
        raise NotImplementedError("reset 还没写")


if __name__ == "__main__":
    d = Dog("旺财")
    d.bark()                    # 旺财: 汪！(第 1 次)
    d.bark()                    # 旺财: 汪！(第 2 次)
    assert len(d) == 2, f"len(d) 应该是 2，拿到 {len(d)}"

    d2 = Dog("小黑")             # 第二条狗是独立的对象，count 互不影响
    assert len(d2) == 0, f"新狗的 count 应该是 0，拿到 {len(d2)}"
    assert d.name == "旺财" and d2.name == "小黑"

    box = NumberBox()
    assert box.head is None and len(box) == 0
    box.add(7)
    assert box.head == 7 and len(box) == 1

    box.reset()
    assert box.head is None, f"reset 后 head 应该是 None，拿到 {box.head}"
    assert len(box) == 0, f"reset 后长度应该是 0，拿到 {len(box)}"

    print(f"len(d) = {len(d)}，d.name = {d.name}")
    print("预热全部通过")
