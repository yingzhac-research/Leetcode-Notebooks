# LinkedList (链表) 刷题指南（中文）

本指南围绕链表（Linked List）常见题型，帮助你从通用概念、典型模板到目录内 Notebook 快速定位解法。先掌握整体思维模型，再结合每题 Notebook 的详解复盘代码与测试。

## 基本概念速览
- **核心机制**：线性数据结构，通过指针连接节点，支持高效的插入和删除操作（O(1)），但访问需要遍历（O(n)）。
- **节点结构**：每个节点包含数据域（val）和指针域（next），双向链表还有前驱指针（prev）。
- **常见维度**：单链表、双向链表、循环链表；虚拟头节点（dummy head）简化边界处理；快慢指针、递归与迭代两种实现风格。
- **高频陷阱**：空指针访问（NullPointerException）、边界情况处理（空链表、单节点）、指针断链导致内存泄漏、环形链表导致死循环、反转时指针顺序错误。

### Python 实战要点
- 链表节点定义：`class ListNode: def __init__(self, val=0, next=None): self.val = val; self.next = next`
- **虚拟头节点**（dummy head）是处理边界的利器：`dummy = ListNode(0); dummy.next = head`，最后返回 `dummy.next`。
- **快慢指针**：`slow = fast = head`，快指针每次走两步 `fast = fast.next.next`，慢指针走一步 `slow = slow.next`。
- **反转链表**：三指针法 `prev, curr, next`，或递归法（栈空间O(n)）。
- **遍历终止条件**：`while curr` 遍历所有节点，`while curr.next` 遍历到倒数第二个节点。
- **指针操作顺序**：先保存 `next = curr.next`，再修改 `curr.next = prev`，最后移动 `prev = curr; curr = next`。

## 模式与模板

### 1. 反转链表（单个/部分/K组）
**识别信号**：题目要求反转整个链表、反转部分区间、或每K个节点为一组反转。

**套路解析**：使用三指针（prev, curr, next）迭代反转，或递归反转。部分反转需要记录反转区间的前后节点，K组反转需要检查剩余节点数。

**伪代码模板**:
```python
# 迭代反转整个链表
def reverse_list(head):
    prev, curr = None, head
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    return prev

# 递归反转
def reverse_list_recursive(head):
    if not head or not head.next:
        return head
    new_head = reverse_list_recursive(head.next)
    head.next.next = head
    head.next = None
    return new_head

# 反转区间 [left, right]
def reverse_between(head, left, right):
    dummy = ListNode(0, head)
    prev = dummy
    for _ in range(left - 1):
        prev = prev.next

    # 反转 [left, right] 区间
    curr = prev.next
    for _ in range(right - left):
        next_node = curr.next
        curr.next = next_node.next
        next_node.next = prev.next
        prev.next = next_node

    return dummy.next
```
适用题目：`LC 206`, `LC 92`, `LC 25`, `LC 24`

- 反转是链表最基础的操作，务必掌握迭代和递归两种方法。
- K组反转（LC 25）是Hard难度，需要先统计长度判断是否够K个。

### 2. 快慢指针（环检测/中点/倒数第N个）
**识别信号**：题目涉及链表的中间节点、环检测、倒数第N个节点等需要"测量"链表的问题。

**套路解析**：快指针每次走两步，慢指针走一步。用于找中点（快指针到尾时慢指针在中点）、检测环（快慢指针相遇则有环）、找倒数第N个（快指针先走N步）。

**伪代码模板**:
```python
# 找中点（偶数个节点时返回第二个中点）
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow

# 环检测
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False

# 找环入口（Floyd判圈算法）
def detect_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            # 相遇后，一个指针回到head，同步前进
            slow = head
            while slow != fast:
                slow = slow.next
                fast = fast.next
            return slow
    return None

# 删除倒数第N个节点
def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)
    fast = slow = dummy
    # 快指针先走n+1步
    for _ in range(n + 1):
        fast = fast.next
    # 同步前进
    while fast:
        slow = slow.next
        fast = fast.next
    # 删除slow.next
    slow.next = slow.next.next
    return dummy.next
```
适用题目：`LC 141`, `LC 142`, `LC 876`, `LC 19`, `LC 234`

- 快慢指针是链表的核心技巧，相遇定理需要理解数学证明。
- 找倒数第N个节点时，快指针先走N+1步（为了让slow停在待删除节点的前一个）。

### 3. 合并链表（两个/K个有序链表）
**识别信号**：题目要求合并两个或多个有序链表，保持有序性。

**套路解析**：双指针比较节点值，选择较小的接到结果链表。K个链表可以使用最小堆（优先队列）或分治法（两两合并）。

**伪代码模板**:
```python
# 合并两个有序链表
def merge_two_lists(l1, l2):
    dummy = ListNode(0)
    curr = dummy
    while l1 and l2:
        if l1.val < l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next
    curr.next = l1 if l1 else l2
    return dummy.next

# 合并K个有序链表（最小堆）
import heapq
def merge_k_lists(lists):
    heap = []
    # 初始化堆（注意Python3需要自定义比较）
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))

    dummy = ListNode(0)
    curr = dummy
    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))

    return dummy.next

# 合并K个链表（分治法）
def merge_k_lists_divide_conquer(lists):
    if not lists:
        return None
    if len(lists) == 1:
        return lists[0]

    mid = len(lists) // 2
    left = merge_k_lists_divide_conquer(lists[:mid])
    right = merge_k_lists_divide_conquer(lists[mid:])
    return merge_two_lists(left, right)
```
适用题目：`LC 21`, `LC 23`, `LC 88`, `LC 1634`

- 合并两个链表是基础，K个链表是Hard难度。
- 堆方法时间 O(N log K)，空间 O(K)；分治法时间 O(N log K)，空间 O(log K)（递归栈）。

### 4. 删除节点（特定值/重复/倒数第N个）
**识别信号**：题目要求删除链表中满足某种条件的节点（特定值、重复元素、倒数第N个等）。

**套路解析**：使用虚拟头节点简化边界处理，遍历时判断 `curr.next` 是否需要删除，若删除则 `curr.next = curr.next.next`，否则 `curr = curr.next`。

**伪代码模板**:
```python
# 删除特定值的所有节点
def remove_elements(head, val):
    dummy = ListNode(0, head)
    curr = dummy
    while curr.next:
        if curr.next.val == val:
            curr.next = curr.next.next
        else:
            curr = curr.next
    return dummy.next

# 删除有序链表的重复元素（保留一个）
def delete_duplicates(head):
    curr = head
    while curr and curr.next:
        if curr.val == curr.next.val:
            curr.next = curr.next.next
        else:
            curr = curr.next
    return head

# 删除有序链表的重复元素（完全删除）
def delete_duplicates_all(head):
    dummy = ListNode(0, head)
    prev = dummy
    while prev.next and prev.next.next:
        if prev.next.val == prev.next.next.val:
            val = prev.next.val
            while prev.next and prev.next.val == val:
                prev.next = prev.next.next
        else:
            prev = prev.next
    return dummy.next

# 删除倒数第N个节点（见快慢指针模板）
```
适用题目：`LC 203`, `LC 83`, `LC 82`, `LC 19`, `LC 237`

- 虚拟头节点可以统一处理头节点删除的边界情况。
- 删除重复元素时，"保留一个"和"完全删除"逻辑不同，注意区分。

### 5. 重排链表（奇偶重排/回文检测/重新排列）
**识别信号**：题目要求重新排列链表节点顺序，如奇偶分离、回文检测、特殊顺序重排（L0→Ln→L1→Ln-1...）。

**套路解析**：通常需要组合多种技巧：快慢指针找中点、反转链表、合并链表。回文检测通过快慢指针找中点后反转后半部分比较。

**伪代码模板**:
```python
# 回文链表检测
def is_palindrome(head):
    if not head or not head.next:
        return True

    # 快慢指针找中点
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # 反转后半部分
    prev, curr = None, slow
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node

    # 比较前后两半
    left, right = head, prev
    while right:  # 右半部分可能短一个节点
        if left.val != right.val:
            return False
        left = left.next
        right = right.next
    return True

# 奇偶重排
def odd_even_list(head):
    if not head or not head.next:
        return head

    odd = head
    even = head.next
    even_head = even

    while even and even.next:
        odd.next = even.next
        odd = odd.next
        even.next = odd.next
        even = even.next

    odd.next = even_head
    return head

# 重新排列链表（L0→Ln→L1→Ln-1...）
def reorder_list(head):
    if not head or not head.next:
        return

    # 1. 找中点
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # 2. 反转后半部分
    prev, curr = None, slow.next
    slow.next = None  # 断开前后两半
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node

    # 3. 合并前后两半
    first, second = head, prev
    while second:
        first_next = first.next
        second_next = second.next
        first.next = second
        second.next = first_next
        first = first_next
        second = second_next
```
适用题目：`LC 234`, `LC 328`, `LC 143`, `LC 86`

- 重排链表通常需要3步：找中点、反转后半部分、合并。
- 回文检测可以用栈（O(n)空间）或反转后半部分（O(1)空间）。

### 6. 复杂操作（复制随机指针/排序/相交/加法）
**识别信号**：题目涉及特殊的链表结构（如带随机指针）、排序、相交检测、链表表示数字相加等复杂场景。

**套路解析**：
- **复制随机指针**：使用哈希表映射原节点到新节点，或原地复制（交叉插入新节点）。
- **链表排序**：归并排序（O(n log n)时间，O(log n)空间），快排（不推荐，链表不适合）。
- **相交检测**：双指针，A走完走B，B走完走A，相遇点即交点（若不相交则都走到None）。
- **链表加法**：模拟手工加法，注意进位和链表长度不一致。

**伪代码模板**:
```python
# 复制带随机指针的链表（哈希表法）
def copy_random_list(head):
    if not head:
        return None

    # 第一遍：复制节点并建立映射
    old_to_new = {}
    curr = head
    while curr:
        old_to_new[curr] = Node(curr.val)
        curr = curr.next

    # 第二遍：连接next和random
    curr = head
    while curr:
        if curr.next:
            old_to_new[curr].next = old_to_new[curr.next]
        if curr.random:
            old_to_new[curr].random = old_to_new[curr.random]
        curr = curr.next

    return old_to_new[head]

# 链表排序（归并排序）
def sort_list(head):
    if not head or not head.next:
        return head

    # 快慢指针找中点
    slow, fast, prev = head, head, None
    while fast and fast.next:
        prev = slow
        slow = slow.next
        fast = fast.next.next
    prev.next = None  # 断开前后两半

    # 递归排序
    left = sort_list(head)
    right = sort_list(slow)

    # 合并
    return merge_two_lists(left, right)

# 相交链表检测
def get_intersection_node(headA, headB):
    if not headA or not headB:
        return None

    a, b = headA, headB
    while a != b:
        a = a.next if a else headB
        b = b.next if b else headA
    return a

# 两数相加（链表表示）
def add_two_numbers(l1, l2):
    dummy = ListNode(0)
    curr = dummy
    carry = 0

    while l1 or l2 or carry:
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0
        total = val1 + val2 + carry

        carry = total // 10
        curr.next = ListNode(total % 10)
        curr = curr.next

        if l1:
            l1 = l1.next
        if l2:
            l2 = l2.next

    return dummy.next
```
适用题目：`LC 138`, `LC 148`, `LC 160`, `LC 2`, `LC 445`

- 复制随机指针的哈希表法空间O(n)，原地交叉法空间O(1)但更复杂。
- 链表排序首选归并排序，时间O(n log n)，空间O(log n)（递归栈）。
- 相交链表的双指针技巧非常巧妙，通过"走完自己走对方"消除长度差。

## 复杂度对比

| 操作 | 数组 | 链表 | 备注 |
| --- | --- | --- | --- |
| 访问第i个元素 | O(1) | O(n) | 链表需要遍历 |
| 头部插入 | O(n) | O(1) | 数组需要移动元素 |
| 尾部插入 | O(1)* | O(n) | 链表需要遍历到尾部 |
| 中间插入 | O(n) | O(1)* | *已知位置时，链表O(1) |
| 删除 | O(n) | O(1)* | 同上 |
| 查找 | O(n) | O(n) | 无序情况下 |
| 空间占用 | 连续 | 分散+指针 | 链表额外存储指针 |

## 识别链表问题的关键特征

1. **指针操作**：题目描述涉及"下一个"、"前驱"、"后继"等指针关系。
2. **顺序访问**：只能从头到尾遍历，不支持随机访问。
3. **动态插入删除**：需要频繁插入或删除元素，且不关心随机访问。
4. **空间限制**：要求O(1)额外空间，无法使用数组辅助。
5. **环形结构**：题目提到"环"、"循环"、"相遇"等关键词。
6. **特殊节点结构**：如带随机指针、双向链表、多级链表。

## 常见陷阱与调试技巧

1. **空指针异常**：访问 `curr.next` 前必须检查 `curr is not None`。
2. **边界情况**：空链表（head=None）、单节点链表（head.next=None）务必测试。
3. **虚拟头节点**：头节点可能被删除或修改时，使用 `dummy = ListNode(0, head)` 简化逻辑。
4. **指针断链**：修改指针前，先保存下一个节点 `next = curr.next`，避免链表断裂。
5. **反转顺序**：反转链表时，三指针的更新顺序是：保存next → 修改curr.next → 移动prev/curr。
6. **快慢指针边界**：`while fast and fast.next` 防止 `fast.next.next` 空指针访问。
7. **环形链表死循环**：修改链表前检查是否有环，或使用快慢指针检测。
8. **递归栈溢出**：链表过长时递归可能栈溢出，考虑迭代实现。
9. **返回值**：注意题目要求返回链表头还是修改后的节点，或直接修改（in-place）。

## 链表 vs 递归

很多链表问题既可以用迭代也可以用递归实现：

### 迭代 vs 递归对比

| 方面 | 迭代 | 递归 |
| --- | --- | --- |
| 空间复杂度 | O(1) | O(n)（调用栈） |
| 代码简洁性 | 较复杂 | 简洁优雅 |
| 理解难度 | 需要管理指针 | 需要理解递归思维 |
| 性能 | 更快，无函数调用开销 | 慢，有栈开销 |
| 适用场景 | 长链表、生产环境 | 短链表、面试展示思维 |

**推荐策略**：
- 面试时，先说递归思路（展示思维清晰），再优化为迭代（展示工程能力）。
- 生产环境优先迭代，避免栈溢出风险。

## 刷题建议

### 阶段一：基础巩固（必刷）
1. **LC 206** - Reverse Linked List (Easy) - 反转链表基础
2. **LC 141** - Linked List Cycle (Easy) - 快慢指针入门
3. **LC 21** - Merge Two Sorted Lists (Easy) - 合并链表基础
4. **LC 83** - Remove Duplicates from Sorted List (Easy) - 删除节点基础
5. **LC 203** - Remove Linked List Elements (Easy) - 虚拟头节点

### 阶段二：核心技巧（重点）
6. **LC 19** - Remove Nth Node From End (Medium) - 快慢指针进阶
7. **LC 142** - Linked List Cycle II (Medium) - Floyd判圈算法
8. **LC 92** - Reverse Linked List II (Medium) - 部分反转
9. **LC 234** - Palindrome Linked List (Easy) - 综合技巧
10. **LC 143** - Reorder List (Medium) - 找中点+反转+合并
11. **LC 328** - Odd Even Linked List (Medium) - 重排链表
12. **LC 160** - Intersection of Two Linked Lists (Easy) - 双指针技巧

### 阶段三：高级应用（拓展）
13. **LC 82** - Remove Duplicates from Sorted List II (Medium) - 复杂删除
14. **LC 138** - Copy List with Random Pointer (Medium) - 哈希表应用
15. **LC 148** - Sort List (Medium) - 归并排序
16. **LC 23** - Merge k Sorted Lists (Hard) - 堆/分治
17. **LC 25** - Reverse Nodes in k-Group (Hard) - K组反转
18. **LC 2** - Add Two Numbers (Medium) - 链表模拟加法
19. **LC 445** - Add Two Numbers II (Medium) - 高位在前的加法
20. **LC 86** - Partition List (Medium) - 分割链表

### 阶段四：综合提升（选做）
21. **LC 147** - Insertion Sort List (Medium) - 插入排序
22. **LC 61** - Rotate List (Medium) - 旋转链表
23. **LC 24** - Swap Nodes in Pairs (Medium) - 两两交换
24. **LC 725** - Split Linked List in Parts (Medium) - 分割链表

## 本目录 Notebook 参考表

| 题号 | 题目 | 难度 | 核心模式 |
| --- | --- | --- | --- |
| LC 206 | Reverse Linked List | Easy | 反转链表基础 |
| LC 92 | Reverse Linked List II | Medium | 部分反转 |
| LC 25 | Reverse Nodes in k-Group | Hard | K组反转 |
| LC 24 | Swap Nodes in Pairs | Medium | 两两交换 |
| LC 141 | Linked List Cycle | Easy | 快慢指针 |
| LC 142 | Linked List Cycle II | Medium | Floyd判圈算法 |
| LC 876 | Middle of the Linked List | Easy | 快慢指针找中点 |
| LC 19 | Remove Nth Node From End | Medium | 快慢指针删除 |
| LC 21 | Merge Two Sorted Lists | Easy | 合并两个链表 |
| LC 23 | Merge k Sorted Lists | Hard | 堆/分治合并 |
| LC 203 | Remove Linked List Elements | Easy | 删除特定值 |
| LC 83 | Remove Duplicates from Sorted List | Easy | 删除重复保留一个 |
| LC 82 | Remove Duplicates from Sorted List II | Medium | 删除重复完全删除 |
| LC 234 | Palindrome Linked List | Easy | 回文检测 |
| LC 328 | Odd Even Linked List | Medium | 奇偶重排 |
| LC 143 | Reorder List | Medium | 重新排列 |
| LC 86 | Partition List | Medium | 分割链表 |
| LC 138 | Copy List with Random Pointer | Medium | 复制随机指针 |
| LC 148 | Sort List | Medium | 归并排序 |
| LC 160 | Intersection of Two Linked Lists | Easy | 相交检测 |
| LC 2 | Add Two Numbers | Medium | 链表加法 |
| LC 445 | Add Two Numbers II | Medium | 高位在前加法 |
| LC 61 | Rotate List | Medium | 旋转链表 |

---

**使用建议**：链表是面试最基础的数据结构，建议按照阶段顺序刷题，先掌握反转、快慢指针、合并等核心技巧，再挑战Hard题目。每个模式对应目录内的若干 Notebook，先看本 Guide 理解核心思路和模板，再打开对应 Notebook 查看完整代码、测试用例和详细复盘。祝刷题顺利！
