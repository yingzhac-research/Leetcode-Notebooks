# Binary Search 刷题指南（中文）

本指南聚焦常用的二分查找与“答案二分”题型，梳理常见模板、适用场景与代表题目。通过分类总结和 Notebook 练习，可以快速形成一套可迁移的解题框架。

## 基本概念速览
- **核心能力**：在有序结构或单调判定函数上，通过收缩搜索区间在 O(log n) 时间内定位答案。
- **关键前提**：搜索空间呈现单调性（数组有序、答案满足单调布尔函数、可通过 mid 划分问题等）。
- **常见失误**：
  - 边界更新不当导致死循环 (`left = mid` / `right = mid`)，应使用 `left = mid + 1` 或 `right = mid - 1`。
  - 未区分「寻找存在值」与「寻找插入位置」的循环条件和返回值。
  - 在答案二分时，未正确设置可行条件，或者 `mid` 计算溢出。

### Python 实战要点
- 优先使用 `left + (right - left) // 2` 计算中点避免溢出。
- 在寻找左/右边界时，自定义 `lower_bound`/`upper_bound` 模板更稳定。
- `bisect` 模块可辅助处理有序数组插入、查找，但手写模板更能通过面试。
- 答案二分时先确定搜索区间上下界，再实现 `check(mid)` 判定函数。

## 二分模式与代表题型

### 1. 标准二分查找（存在性判断）
**适用情形**：在有序数组中判断目标是否出现，或返回其索引。
**套路解读**：维护 `[left, right]` 区间，中点与目标比较后收缩端点，直到找到或区间为空。

**模板精要**：
```python
def binary_search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

**经典题目**：
- `BinarySearch/LC_704_binary-search.ipynb`
- `BinarySearch/LC_74_search-a-2d-matrix.ipynb`

### 2. lower_bound / upper_bound 边界查找
**适用情形**：需要定位目标的最左或最右出现位置，或找到插入点。
**套路解读**：通过不变量设计，将循环写成 `while left < right`，或在模板中维护答案变量。

**模板精要**：
```python
def lower_bound(nums, target):
    left, right = 0, len(nums)
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left  # 最左插入位置
```

**经典题目**：
- `BinarySearch/LC_34_find-first-and-last-position-of-element-in-sorted-array.ipynb`
- `BinarySearch/LC_35_search-insert-position.ipynb`
- `BinarySearch/LC_744_find-smallest-letter-greater-than-target.ipynb`

### 3. 旋转数组 & 山峰查找
**适用情形**：数组经过旋转/山峰变换但保持局部单调，需要定位峰值或特定目标。
**套路解读**：利用 mid 与端点比较判断落在哪个单调区间，或通过相邻元素判断峰值方向。

**模板精要**：
```python
def search_rotated(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        if nums[left] <= nums[mid]:  # 左侧有序
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:  # 右侧有序
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1
```

**经典题目**：
- `BinarySearch/LC_33_search-in-rotated-sorted-array.ipynb`
- `BinarySearch/LC_81_search-in-rotated-sorted-array-ii.ipynb`
- `BinarySearch/LC_153_find-minimum-in-rotated-sorted-array.ipynb`
- `BinarySearch/LC_162_find-peak-element.ipynb`
- `BinarySearch/LC_852_peak-index-in-a-mountain-array.ipynb`

### 4. 二分答案（整数域）
**适用情形**：答案本身处于一段区间，且存在“可行性”单调关系，如“最小满足条件的值”。
**套路解读**：在候选答案区间 `[lo, hi]` 上二分，`check(mid)` 返回是否可行，然后更新区间，最终得到最优答案。

**模板精要**：
```python
def binary_search_answer(lo, hi, check):
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if check(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**经典题目**：
- `BinarySearch/LC_875_koko-eating-bananas.ipynb`
- `BinarySearch/LC_1011_capacity-to-ship-packages-within-d-days.ipynb`
- `BinarySearch/LC_1482_minimum-number-of-days-to-make-m-bouquets.ipynb`
- `BinarySearch/LC_1552_magnetic-force-between-two-balls.ipynb`
- `BinarySearch/LC_1870_minimum-speed-to-arrive-on-time.ipynb`

### 5. 二分答案（浮点 / 精度控制）
**适用情形**：答案为实数，如浮点平方根、几何距离等，需要在误差范围内逼近。
**套路解读**：使用固定次数迭代或 while 循环结合精度阈值，更新 `mid`。Python 中需注意浮点误差。

**模板精要**：
```python
def sqrt_float(x, eps=1e-6):
    left, right = (0.0, max(1.0, x))
    while right - left > eps:
        mid = (left + right) / 2
        if mid * mid >= x:
            right = mid
        else:
            left = mid
    return right
```

**经典题目**：
- `BinarySearch/LC_69_sqrtx.ipynb`
- `BinarySearch/LC_644_maximum-average-subarray-ii.ipynb` *(若有需要可扩展)*

### 6. 值域二分 + 计数函数
**适用情形**：通过“统计 ≤ mid 的元素个数”验证某个数是否满足条件，常见于找第 k 小值。
**套路解读**：`check(mid)` 返回满足条件的数量，根据数量与目标比较收缩区间。

**模板精要**：
```python
def kth_value(lo, hi, count_leq, k):
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if count_leq(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**经典题目**：
- `BinarySearch/LC_287_find-the-duplicate-number.ipynb`
- `BinarySearch/LC_378_kth-smallest-element-in-a-sorted-matrix.ipynb`
- `BinarySearch/LC_668_kth-smallest-number-in-multiplication-table.ipynb`

### 7. 二分 + 贪心 / 可行性验证
**适用情形**：对于一个候选答案，使用贪心/模拟判断是否满足条件（如分配、装载、分割）。
**套路解读**：结合答案二分的模板，通过贪心 `check(mid)` 判断可行性。常用于“最小最大值”或“最大最小值”问题。

**模板精要**：
```python
def feasible(limit):
    groups = 1
    total = 0
    for num in nums:
        if total + num > limit:
            groups += 1
            total = 0
        total += num
    return groups <= m
```

**经典题目**：
- `BinarySearch/LC_410_split-array-largest-sum.ipynb`
- `BinarySearch/LC_658_find-k-closest-elements.ipynb`
- `BinarySearch/LC_1482_minimum-number-of-days-to-make-m-bouquets.ipynb`

### 8. 二分结合其他数据结构
**适用情形**：二分决定某个索引/值后，再借助其他数据结构查询（如前缀和、双指针）。
**套路解读**：先定位索引，再配合队列/栈/哈希等结构优化求解。

**经典题目**：
- `BinarySearch/LC_240_search-a-2d-matrix-ii.ipynb`
- `BinarySearch/LC_658_find-k-closest-elements.ipynb`

## 现有题目对照表
| Notebook | 套路 | 关键要点 | 待补充内容 |
| --- | --- | --- | --- |
| `BinarySearch/LC_704_binary-search.ipynb` | 标准二分 | 经典左右闭区间模板 | 可增加递归版本说明 |
| `BinarySearch/LC_35_search-insert-position.ipynb` | lower_bound | 找插入点返回 left | 加上 bisect 对比与性能数据 |
| `BinarySearch/LC_33_search-in-rotated-sorted-array.ipynb` | 旋转数组二分 | 判断哪边有序后再决定方向 | 补充重复值或多次旋转讨论 |
| `BinarySearch/LC_153_find-minimum-in-rotated-sorted-array.ipynb` | 旋转数组二分 | 通过 mid 与 right 比较确定区间 | 增加含重复元素版本对照 |
| `BinarySearch/LC_162_find-peak-element.ipynb` | 峰值查找 | 比较 mid 与 mid+1 决定上升方向 | 讨论多峰情况下返回任意峰值的依据 |
| `BinarySearch/LC_74_search-a-2d-matrix.ipynb` | 二分映射索引 | 将二维坐标压平 | 补充行内/列内二分方案比较 |
| `BinarySearch/LC_278_first-bad-version.ipynb` | 答案二分 | 找到第一个满足条件的版本 | 记录 API 调用次数分析 |
| `BinarySearch/LC_287_find-the-duplicate-number.ipynb` | 值域二分 | 统计 `<= mid` 个数判断重复 | 对比 Floyd 快慢指针方法 |
| `BinarySearch/LC_658_find-k-closest-elements.ipynb` | 二分+滑窗 | 先找左边界再扩散 | 添加双指针/堆方案对比 |
| `BinarySearch/LC_875_koko-eating-bananas.ipynb` | 答案二分+贪心 | `check(mid)` 模拟吃香蕉速度 | 给出速度上下界推导 |
| `BinarySearch/LC_1011_capacity-to-ship-packages-within-d-days.ipynb` | 答案二分+贪心 | 按容量模拟装船 | 补充二分边界的数学证明 |
| `BinarySearch/LC_410_split-array-largest-sum.ipynb` | 答案二分+贪心 | 通过 mid 判断需要的子数组数 | 加入 DP 对比及复杂度分析 |
| `BinarySearch/LC_1482_minimum-number-of-days-to-make-m-bouquets.ipynb` | 答案二分 | 判断在 mid 天能否制作 m 束 | 讨论边界条件（花不足） |
| `BinarySearch/LC_1552_magnetic-force-between-two-balls.ipynb` | 答案二分 | 检查最小距离可行性 | 提供排序+二分的完整复杂度分析 |
| `BinarySearch/LC_1870_minimum-speed-to-arrive-on-time.ipynb` | 答案二分 | 计算在速度 mid 下是否按时到达 | 考虑浮点误差与向上取整 |
| `BinarySearch/LC_744_find-smallest-letter-greater-than-target.ipynb` | upper_bound | 找第一个大于 target 的元素 | 扩展到循环数组的写法 |
| `BinarySearch/LC_2410_maximum-matching-of-players-with-trainers.ipynb` | 二分+贪心 | 排序后二分定位可用训练师 | 结合 lower_bound 与在线匹配思路 |

## 学习建议
- **模板背诵**：分别手写“存在性二分”“lower/upper_bound”“答案二分”三个常用模板，熟悉循环条件和返回值处理。
- **题型归类**：做题时先辨别属于哪一类模式，再把题目映射到模板，避免盲目修改代码。
- **构造 `check` 函数**：答案二分的难点在于正确构造单调判定函数，建议对每题列出 `mid` 意义、可行区间和边界推导。
- **边界调试**：准备多组极端测试（空数组、单元素、重复元素、最小/最大值）验证实现正确性。
- **多语言迁移**：在主语言之外，实现一遍 C++/Java 模板，习惯 `lower_bound`/`upper_bound` 内置函数与差异。

