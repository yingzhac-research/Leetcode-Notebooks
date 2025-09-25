# Two Pointers 刷题指南（中文）

本指南围绕双指针常见题型，帮助你从通用概念、典型模板到目录内现有题目快速定位解法。先掌握整体思维模型，再结合 Notebook 细节巩固代码实现。

## 基本概念速览
- **核心机制**：用两个（或更多）索引在同一结构上协同移动，以 O(n) 复杂度扫描全部有效状态。
- **常见维度**：指针方向（双端对撞、同向滑动、快慢指针）、是否允许排序、窗口是否需要维护附加信息。
- **选题信号**：题目要求“找有序对/区间/子串”，且可通过逐步收缩或扩张窗口避免回溯时，优先考虑双指针。
- **高频陷阱**：排序后忘记处理重复元素、窗口缩小时未同步维护计数、快慢指针在空链表或短数组上越界。

## Python 实战要点
- 提前绑定局部变量（如 `nums = sorted(nums)`）减少重复属性访问。
- 对滑动窗口，配合 `collections.Counter` 或 `defaultdict(int)` 管理频次；退出窗口时记得减到 0 再删除键。
- 快慢指针要先检查空节点，再让快指针先走一步，避免 `None.next` 抛错。

## 常见套路速查
| 模式 | 场景关键词 | 对应模板 | 当前 Notebook |
| --- | --- | --- | --- |
| 对撞指针 + 去重 | 排序数组/K-Sum/面积问题 | 模板 1 | `LC_15_3sum.ipynb` |
| 滑动窗口 | 最长/最短子串、包含条件 | 模板 2 | 待补充 |
| 快慢指针 | 环检测、中点查找 | 模板 3 | 待补充 |
| 分区重排 | 三色旗、原地分段 | 模板 4 | 待补充 |
| 双数组/双区间合并 | 归并、求交集 | 模板 5 | 待补充 |

## 通用模板代码
### 模板 1：排序 + 对撞指针（K-Sum 基础）
- **适用**：数组可排序，目标是找满足约束的二元/三元/四元组。
- **要点**：排序后固定外层元素，左右指针内层搜索；每次移动时跳过重复值。
```python
def three_sum(nums, target=0):
    nums.sort()
    n = len(nums)
    res = []
    for i in range(n):
        if i and nums[i] == nums[i - 1]:
            continue
        left, right = i + 1, n - 1
        while left < right:
            s = nums[i] + nums[left] + nums[right]
            if s == target:
                res.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
                while left < right and nums[right] == nums[right + 1]:
                    right -= 1
            elif s < target:
                left += 1
            else:
                right -= 1
    return res
```
- **目录映射**：`TwoPointers/LC_15_3sum.ipynb` 覆盖此模板，Notebook 中可补充 Two Sum 子过程的抽象。

### 模板 2：滑动窗口维护不变量
- **适用**：子数组/子串需满足某个约束（长度、元素频次、和、Distinct 数量等）。
- **要点**：右指针扩张窗口，左指针在违反约束时收缩；每次循环维护辅助计数结构。
```python
from collections import Counter

def longest_substring_k_distinct(s, k):
    counter = Counter()
    left = 0
    best = 0
    for right, ch in enumerate(s):
        counter[ch] += 1
        while len(counter) > k:
            counter[s[left]] -= 1
            if counter[s[left]] == 0:
                del counter[s[left]]
            left += 1
        best = max(best, right - left + 1)
    return best
```
- **目录映射**：当前目录尚无对应 Notebook，可在新增 `LC_340_longest-substring-with-at-most-k-distinct-characters.ipynb` 时引用。

### 模板 3：快慢指针（Floyd Cycle / 中点查找）
- **适用**：链表环检测、找到链表中点、判断是否有循环数组。
- **要点**：快指针一次两步，慢指针一次一步；若相遇则存在环；找环起点需重置一个指针到头部。
```python
class Node:
    def __init__(self, val, nxt=None):
        self.val = val
        self.next = nxt


def detect_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            entry = head
            while entry is not slow:
                entry = entry.next
                slow = slow.next
            return entry
    return None
```
- **目录映射**：待补充链表类题目如 `LC 142` 后，可将详细推导写入 Notebook。

### 模板 4：双指针分区重排
- **适用**：需要原地将数组按条件分段（如荷兰国旗、奇偶分离）。
- **要点**：维护左右边界指针，根据当前值交换并移动相关指针。
```python
def dutch_flag(nums):
    low, mid, high = 0, 0, len(nums) - 1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
    return nums
```
- **目录映射**：适用于未来的 `LC 75 Dutch National Flag`、`LC 905 Sort Array By Parity` 等题。

### 模板 5：双数组/区间归并
- **适用**：合并两个有序结构、求交集、找最短覆盖区间。
- **要点**：分别维护两个索引，根据比较结果推进；可在结果集中追加或更新当前答案。
```python
def interval_intersection(a, b):
    res = []
    i = j = 0
    while i < len(a) and j < len(b):
        lo = max(a[i][0], b[j][0])
        hi = min(a[i][1], b[j][1])
        if lo <= hi:
            res.append([lo, hi])
        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1
    return res
```
- **目录映射**：适用于未来可添加的 `LC 986 Interval List Intersections`、`LC 88 Merge Sorted Array` 等。

## 现有题目对照表
| Notebook | 套路 | 关键要点 | 待补充内容 |
| --- | --- | --- | --- |
| `TwoPointers/LC_15_3sum.ipynb` | 模板 1：排序 + 对撞指针 | 固定一层后双指针收缩；排序后跳过重复 | 可补充对 K-Sum 泛化的递归模板、剪枝策略及随机测试脚本 |

## 复习与拓展建议
- 先手写模板 1-5，确保理解指针移动条件和边界检查顺序。
- 新增 Notebook 时同步在本指南中登记所用模板，便于按模式复盘。
- 对滑动窗口类题目，建议在 Notebook 中明确记录窗口维持的统计量及其更新逻辑。
- 遇到数组题无法 O(n) 解时，优先尝试是否可通过排序 + 双指针或滑动窗口转化以降低复杂度。
