# Greedy 刷题指南（中文）

本指南围绕贪心算法常见题型，帮助你从通用概念、典型模板到目录内 Notebook 快速定位解法。先掌握整体思维模型，再结合每题 Notebook 的详解复盘代码与测试。

## 基本概念速览
- **核心机制**：在每一步选择当前状态下的局部最优解，期望通过局部最优的叠加达到全局最优，通常具有 O(n log n) 或 O(n) 时间复杂度。
- **常见维度**：排序策略（按结束时间、起始时间、收益等）、选择标准（最早、最大、最小）、证明方法（交换论证、反证法）。
- **高频陷阱**：贪心策略未经证明就使用、排序关键字选择错误、忽略边界情况导致漏解、混淆局部最优与全局最优的适用条件。

### Python 实战要点
- 贪心题通常需要先排序，使用 `sorted(items, key=lambda x: ...)` 灵活指定排序规则。
- 优先队列（堆）是贪心的好帮手，`import heapq` 配合 `heappush/heappop` 维护动态最值。
- 多关键字排序可用元组 `(primary, secondary)`，Python 会按字典序自动比较。
- 反向思考：有时"贪心删除最差"等价于"贪心保留最优"，选择更简洁的视角。

## 模式与模板

### 1. 区间调度 / 活动选择
**套路解析**：按结束时间排序，贪心选择最早结束的活动，保证后续空间最大化。适用于不重叠区间、会议室分配等问题。
**伪代码模板**:
```python
# 按结束时间排序
intervals.sort(key=lambda x: x[1])
count = 0
last_end = float('-inf')
for start, end in intervals:
    if start >= last_end:
        count += 1
        last_end = end
return count
```
适用题目：`LC 435`, `LC 452`, `LC 646`, `LC 253`

- 选择最早结束的活动是经典贪心策略，可用交换论证证明正确性。

### 2. 跳跃游戏 / 最远可达
**套路解析**：维护当前能到达的最远位置，贪心地在每个位置更新最远边界，判断是否能覆盖终点或统计最少跳跃次数。
**伪代码模板**:
```python
# 判断能否到达终点
max_reach = 0
for i in range(len(nums)):
    if i > max_reach:
        return False
    max_reach = max(max_reach, i + nums[i])
return max_reach >= len(nums) - 1
```
```python
# 最少跳跃次数
jumps = 0
current_end = 0
farthest = 0
for i in range(len(nums) - 1):
    farthest = max(farthest, i + nums[i])
    if i == current_end:
        jumps += 1
        current_end = farthest
return jumps
```
适用题目：`LC 55`, `LC 45`, `LC 1306`

- 跳跃游戏的核心是维护"当前跳跃能到达的最远边界"，到达边界时必须进行下一跳。

### 3. 数组分配 / 双指针贪心
**套路解析**：对两个数组排序后，用双指针贪心匹配，最小满足或最大化收益。常见于饼干分配、救生艇等场景。
**伪代码模板**:
```python
# 贪心分配：小的配小的
children.sort()
cookies.sort()
i = j = 0
count = 0
while i < len(children) and j < len(cookies):
    if cookies[j] >= children[i]:
        count += 1
        i += 1
    j += 1
return count
```
适用题目：`LC 455`, `LC 881`, `LC 826`

- 排序后用最小满足条件的资源匹配当前需求，避免浪费大资源在小需求上。

### 4. 字符串构造 / 字典序贪心
**套路解析**：通过贪心选择字符顺序构造字典序最小或最大的字符串，常用单调栈或计数策略。
**伪代码模板**:
```python
# 移除 k 个字符使字典序最小
stack = []
to_remove = k
for char in num:
    while stack and to_remove > 0 and stack[-1] > char:
        stack.pop()
        to_remove -= 1
    stack.append(char)
# 移除剩余 k 个
stack = stack[:len(stack) - to_remove]
return ''.join(stack).lstrip('0') or '0'
```
适用题目：`LC 402`, `LC 316`, `LC 321`, `LC 1663`

- 单调栈维护递增/递减序列，配合计数保证剩余字符满足约束。

### 5. 任务调度 / 优先队列
**套路解析**：用堆维护任务优先级，贪心选择当前收益最大或惩罚最小的任务执行，常配合时间轴或冷却时间。
**伪代码模板**:
```python
import heapq
# 按截止时间排序，用最大堆维护利润
tasks.sort(key=lambda x: x[1])  # 按截止时间
max_heap = []
for profit, deadline in tasks:
    heapq.heappush(max_heap, -profit)
    if len(max_heap) > deadline:
        heapq.heappop(max_heap)
return -sum(max_heap)
```
适用题目：`LC 621`, `LC 767`, `LC 1353`, `LC 1834`

- 堆可以动态维护最优选择，配合时间约束实现贪心调度。

### 6. 股票买卖 / 累积收益
**套路解析**：贪心累加所有上升区间的收益，或配合状态机处理交易次数限制。
**伪代码模板**:
```python
# 无限次交易：累加所有上涨
profit = 0
for i in range(1, len(prices)):
    if prices[i] > prices[i-1]:
        profit += prices[i] - prices[i-1]
return profit
```
适用题目：`LC 122`, `LC 121`, `LC 123`, `LC 714`

- 将连续上涨拆解为每日收益累加，等价于低买高卖的最优策略。

### 7. 最小代价 / 合并石子
**套路解析**：每次贪心选择代价最小的操作执行，用堆维护候选，直到满足目标。
**伪代码模板**:
```python
import heapq
# 合并石子：每次合并最小的两堆
heapq.heapify(stones)
total_cost = 0
while len(stones) > 1:
    first = heapq.heappop(stones)
    second = heapq.heappop(stones)
    cost = first + second
    total_cost += cost
    heapq.heappush(stones, cost)
return total_cost
```
适用题目：`LC 1167`, `LC 1046`, `LC reorganize-string`

- 哈夫曼编码思想：每次合并代价最小的两项，最小化总代价。

### 8. 加油站 / 环形数组
**套路解析**：累积盈亏，贪心选择起点，若总盈余非负则必有解，起点选在盈亏转正处。
**伪代码模板**:
```python
total_tank = 0
current_tank = 0
start = 0
for i in range(len(gas)):
    diff = gas[i] - cost[i]
    total_tank += diff
    current_tank += diff
    if current_tank < 0:
        start = i + 1
        current_tank = 0
return start if total_tank >= 0 else -1
```
适用题目：`LC 134`

- 若总油量≥总消耗，必存在解；起点选在累积油量首次转正的位置。

## 现有题目对照表
| Notebook | 套路 | 关键要点 | 待补充内容 |
| --- | --- | --- | --- |
| `Greedy/LC_45_jump-game-ii.ipynb` | 跳跃游戏（模板 2） | 维护当前跳跃边界与最远可达 | 补充 BFS 类比说明 |
| `Greedy/LC_55_jump-game.ipynb` | 最远可达（模板 2） | 更新 max_reach 判断覆盖 | 对比回溯与 DP 方法 |
| `Greedy/LC_122_best-time-to-buy-and-sell-stock-ii.ipynb` | 累积收益（模板 6） | 累加所有上涨区间 | 画出股价折线图示意 |
| `Greedy/LC_134_gas-station.ipynb` | 环形数组（模板 8） | 总盈余非负则有解，起点选转正处 | 说明为何不需回头检查 |
| `Greedy/LC_253_meeting-rooms-ii.ipynb` | 区间调度 | 最小堆维护会议结束时间 | 差分数组替代法 |
| `Greedy/LC_316_remove-duplicate-letters.ipynb` | 字典序贪心（模板 4） | 单调栈+计数保证字典序 | 补充 visited 集合作用 |
| `Greedy/LC_402_remove-k-digits.ipynb` | 字典序最小（模板 4） | 单调栈移除递减峰 | 处理前导零与全删边界 |
| `Greedy/LC_435_non-overlapping-intervals.ipynb` | 区间调度（模板 1） | 按结束时间排序贪心选择 | 最少移除=总数-最多不重叠 |
| `Greedy/LC_452_minimum-number-of-arrows-to-burst-balloons.ipynb` | 区间调度 | 按结束排序，重叠则共用箭 | 强调边界重叠算重叠 |
| `Greedy/LC_455_assign-cookies.ipynb` | 双指针贪心（模板 3） | 小饼干配小胃口 | 倒序贪心替代法 |
| `Greedy/LC_621_task-scheduler.ipynb` | 任务调度（模板 5） | 最高频任务决定冷却周期 | 公式推导与模拟对比 |
| `Greedy/LC_646_maximum-length-of-pair-chain.ipynb` | 区间调度（模板 1） | 同活动选择，DP 对比 | 补充 DP 转移方程 |
| `Greedy/LC_714_best-time-to-buy-and-sell-stock-with-transaction-fee.ipynb` | 股票+手续费 | 扣除手续费累加收益 | 状态机图解 |
| `Greedy/LC_763_partition-labels.ipynb` | 区间合并 | 记录字符最远位置扩展窗口 | 对比差分数组法 |
| `Greedy/LC_767_reorganize-string.ipynb` | 任务调度（模板 5） | 最大堆交替放置字符 | 处理无解条件 |
| `Greedy/LC_826_most-profit-assigning-work.ipynb` | 双指针贪心 | 排序后贪心匹配能力与利润 | 补充桶排序优化 |
| `Greedy/LC_860_lemonade-change.ipynb` | 找零贪心 | 优先用大面额找零 | 列举找零决策树 |
| `Greedy/LC_881_boats-to-save-people.ipynb` | 双指针贪心（模板 3） | 最重与最轻配对 | 为何不需三人船 |
| `Greedy/LC_1005_maximize-sum-of-array-after-k-negations.ipynb` | 堆贪心 | 反转最小值 k 次 | 排序+翻转替代堆 |
| `Greedy/LC_1046_last-stone-weight.ipynb` | 堆（模板 7） | 最大堆模拟碰撞 | 不是最优化，纯模拟 |
| `Greedy/LC_1167_minimum-cost-to-connect-sticks.ipynb` | 哈夫曼（模板 7） | 最小堆合并代价最小化 | 证明贪心正确性 |
| `Greedy/LC_1353_maximum-number-of-events-that-can-be-attended.ipynb` | 优先队列+扫描线 | 按天贪心选最早结束事件 | 扫描线思想图解 |
| `Greedy/LC_1663_smallest-string-with-a-given-numeric-value.ipynb` | 字典序贪心 | 从后往前放最大字符 | 倒序构造原理 |

## 复习与拓展建议
- **证明贪心正确性**：通过交换论证或反证法，确保局部最优能导出全局最优，避免盲目使用。
- **排序是贪心基础**：多数贪心题需要先排序，明确排序关键字（时间、收益、长度等）是解题第一步。
- **优先队列配合贪心**：动态最值问题用堆维护候选集，`heapq` 模块是 Python 的标准工具。
- **对照表查漏**：新增或复盘题目时，先识别贪心模式，再回到 Notebook 查看实现细节与边界处理。
- **多角度思考**：有些题可以用 DP 也可以用贪心，比较两者的时间复杂度与代码复杂度，选择更优解。
- **MLE/AI 场景迁移**：贪心在任务调度、资源分配、特征选择等场景有广泛应用，理解模板可迁移到系统设计中。
