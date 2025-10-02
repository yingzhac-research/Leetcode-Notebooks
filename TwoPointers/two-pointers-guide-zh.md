# Two Pointers 刷题指南（中文）

本指南围绕双指针常见题型，帮助你从通用概念、典型模板到目录内 Notebook 快速定位解法。先掌握整体思维模型，再结合每题 Notebook 的详解复盘代码与测试。

## 基本概念速览
- **核心机制**：在同一结构上使用两个（或更多）索引协同移动，以 O(n) 代价扫描全部有效状态。
- **常见维度**：指针方向（双端对撞、同向滑动、快慢指针）、是否允许排序、窗口是否维护附加信息。
- **高频陷阱**：排序后忘记去重、窗口缩小时未同步维护计数、快慢指针在空链表或短数组上越界。

### Python 实战要点
- 对数组类题目可先 `nums = sorted(nums)` 保证一次排序后指针遍历即可。
- 滑动窗口配合 `collections.Counter`/`defaultdict(int)` 管理频次，退出窗口时减到 0 并删除键。
- 快慢指针前先排除空结构，并让快指针抢先一步，避免 `None.next` 抛错。

## 模式与模板

### 1. 双端对撞指针
**套路解析**：从区间两端向内推进，通过比较左右边界决定哪一侧移动，逐步缩小搜索空间，常用于和差约束或最优值计算。
**伪代码模板**:
```python
left = start
right = end
while left < right:
    update_answer_with(left, right)
    move_pointer_based_on_strategy()
```
适用题目：`LC 11`, `LC 15`, `LC 42`, `LC 167`


- 右移短板或调整两端之和控制搜索空间；排序后配合去重保证输出唯一。

### 2. 滑动窗口（变量窗口约束）
**套路解析**：维护动态窗口并利用哈希跟踪窗口属性，超出约束时收缩窗口，保持不变量得到最优或可行解。
**伪代码模板**:
```python
# 求最大/最长：窗口非法时收缩
left = 0
for right, value in enumerate(sequence):
    include(value)
    while violates_constraint():
        exclude(sequence[left])
        left += 1
    update_answer(left, right)
```
```python
# 求最小/最短：窗口满足目标时收缩
left = 0
for right, value in enumerate(sequence):
    include(value)
    while satisfies_goal():
        update_answer(left, right)
        exclude(sequence[left])
        left += 1
```
适用题目：
- 最长/最大窗口：`LC 424`, `LC 904`, `LC 1004`, `LC 1208`
- 最短/最小窗口：`LC 76`, `LC 209`


- 明确维护的目标：最长场景在违约时收缩窗口；最短场景在满足目标时立刻尝试压缩。

### 3. 定长窗口 / 频次匹配
**套路解析**：固定窗口长度，将窗口特征与目标比较，滑动时同步更新新入/移出元素的贡献，常用于排列或频次匹配。
**伪代码模板**:
```python
window_size = len(pattern)
setup_window(window_size)
if window_matches(): record()
for right in range(window_size, len(sequence)):
    add(sequence[right])
    remove(sequence[right - window_size])
    if window_matches(): record()
```
适用题目：`LC 438`, `LC 567`


- 固定窗口只需在滑动时同步更新新入/旧出字符的频次与匹配计数。

### 4. 快慢指针与稳定压缩
**套路解析**：使用两个速率不同或角色不同的指针实现原地修改，如去重、删除或检测循环。
**伪代码模板**:
```python
write = 0
for read in range(len(sequence)):
    if keep(sequence[read]):
        sequence[write] = sequence[read]
        write += 1
return write
```
适用题目：`LC 26`, `LC 27`, `LC 80`, `LC 283`


- 快指针扫描、慢指针写入干净区间是处理“原地删除/保留”题目的通用套路。

### 5. 分区重排 / 荷兰国旗
**套路解析**：维护多段区间的不变量，通过交换和移动指针完成原地分区。
**伪代码模板**:
```python
low = 0
mid = 0
high = len(nums) - 1
while mid <= high:
    if nums[mid] in lower_group:
        swap(low, mid); low += 1; mid += 1
    elif nums[mid] in middle_group:
        mid += 1
    else:
        swap(mid, high); high -= 1
```
适用题目：`LC 75`


- 维护三个区间不变量：`[0..low-1]=0`, `[low..mid-1]=1`, `[high+1..] = 2`。

### 6. 字符串首尾操作
**套路解析**：左右指针在字符串两端移动，跳过或处理特定字符，实现回文判断、部分翻转等。
**伪代码模板**:
```python
left = 0
right = len(chars) - 1
while left < right:
    advance_to_relevant(left)
    advance_to_relevant(right)
    process(chars[left], chars[right])
    left += 1
    right -= 1
```
适用题目：`LC 125`, `LC 344`, `LC 345`


- 双端移动时先过滤非目标字符，再执行交换或比较。

### 7. 双数组 / 区间归并
**套路解析**：并行遍历两个有序结构，根据边界关系推进指针实现合并、交集或同步扫描。
**伪代码模板**:
```python
i = j = 0
while i < len(A) and j < len(B):
    compare(A[i], B[j])
    record_intersection_if_any()
    advance_pointer_with_smaller_endpoint()
```
适用题目：`LC 88`, `LC 986`


- 从末尾写入或比较两个区间终点，可避免覆盖未处理元素并保持线性复杂度。

## 现有题目对照表
| Notebook | 套路 | 关键要点 | 待补充内容 |
| --- | --- | --- | --- |
| `TwoPointers/LC_11_container-with-most-water.ipynb` | 双端指针收缩 | 移动短板寻找更高界面 | 补充面积与指针移动示意图 |
| `TwoPointers/LC_15_3sum.ipynb` | 排序+对撞（模板 1） | 固定一层后双指针去重 | 补充递归 k-sum 模板 |
| `TwoPointers/LC_26_remove-duplicates-from-sorted-array.ipynb` | 快慢指针稳定压缩 | 新值写入前缀保持顺序 | 比较 while 与 for 写法 |
| `TwoPointers/LC_27_remove-element.ipynb` | 快慢指针覆盖 | 非目标值写回前段 | 追加交换到尾部的替代实现 |
| `TwoPointers/LC_42_trapping-rain-water.ipynb` | 双端指针 + 边界高 | left/right max 决定移动 | 列出前缀数组与栈解法链接 |
| `TwoPointers/LC_75_sort-colors.ipynb` | 荷兰国旗分区（模板 4） | low/mid/high 三指针维持不变量 | 画出三段区间含义示意 |
| `TwoPointers/LC_76_minimum-window-substring.ipynb` | 滑动窗口需求匹配（模板 2） | formed/required 控制窗口收缩 | 记录无解返回空串原因 |
| `TwoPointers/LC_80_remove-duplicates-from-sorted-array-ii.ipynb` | 快慢指针+次数限制 | write-2 对比当前值限制≤2 | 推导通用 keep<=k 扩展 |
| `TwoPointers/LC_88_merge-sorted-array.ipynb` | 逆向双指针合并（模板 5） | 从尾部填充避免覆盖 | 补充 nums2 先耗尽分支说明 |
| `TwoPointers/LC_125_valid-palindrome.ipynb` | 双向指针过滤 | 跳过非字母数字再比较 | 说明 Unicode isalnum 差异 |
| `TwoPointers/LC_167_two-sum-ii-input-array-is-sorted.ipynb` | 排序双指针求和 | 和小于目标左移否则右移 | 强调 1-based 输出处理 |
| `TwoPointers/LC_209_minimum-size-subarray-sum.ipynb` | 正数窗口收缩 | sum>=target 时更新最短 | 加上 prefix+二分方法对比 |
| `TwoPointers/LC_283_move-zeroes.ipynb` | 稳定压缩+填充零 | 先复制非零再补零 | 覆盖全零/全非零测试 |
| `TwoPointers/LC_344_reverse-string.ipynb` | 首尾交换 | 左右指针逐步互换 | 对比切片反转的空间消耗 |
| `TwoPointers/LC_345_reverse-vowels-of-a-string.ipynb` | 条件交换 | 双指针只在元音处交换 | 支持自定义元音集合 |
| `TwoPointers/LC_424_longest-repeating-character-replacement.ipynb` | 窗口+maxFreq | 窗口长-最高频≤k | 说明为何 maxFreq 可不递减 |
| `TwoPointers/LC_438_find-all-anagrams-in-a-string.ipynb` | 定长窗口频次差 | 滑动维护计数差为 0 | 提供返回子串示例 |
| `TwoPointers/LC_567_permutation-in-string.ipynb` | 定长窗口匹配 | matches 统计满足字符数 | 强调计数降为 0 的处理 |
| `TwoPointers/LC_904_fruit-into-baskets.ipynb` | 窗口 distinct≤2 | 维护两种水果并更新最大长度 | 与 LC159 做模板互联 |
| `TwoPointers/LC_838_push-dominoes.ipynb` | 双端对撞指针 | 相反力量双向扩散计算稳定状态 | 考虑 O(1) 空间双指针写法 |
| `TwoPointers/LC_986_interval-list-intersections.ipynb` | 双数组指针（模板 5） | 比较区间端点输出交集 | 说明闭区间边界 |
| `TwoPointers/LC_1004_max-consecutive-ones-iii.ipynb` | 窗口零计数 | zeros>k 时收缩 | 可补充返回窗口边界 |
| `TwoPointers/LC_1208_get-equal-substrings-within-budget.ipynb` | 费用受限窗口 | 累计差值成本并控预算 | 展示 prefix+二分替代法 |

## 复习与拓展建议
- **熟记模板**：模板 1-7 亲手推导一次，明确左右指针、窗口变量的更新顺序。
- **对照表查漏**：新增或复盘题目时，先定位所属套路，再回到 Notebook 查看细节与测试。
- **强化窗口不变量**：滑动窗口题务必写明窗口维护的统计量、约束判断与收缩条件。
- **多场景迁移**：思考每个模板如何扩展到链表、矩阵或多指针场景，形成可复用的面试套路库。
