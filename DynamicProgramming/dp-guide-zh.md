# Dynamic Programming 刷题指南（中文）

本指南围绕动态规划（DP）常见题型，帮助你从通用概念、典型模板到目录内 Notebook 快速定位解法。先掌握整体思维模型，再结合每题 Notebook 的详解复盘代码与测试。

## 基本概念速览
- **核心机制**：将复杂问题分解为重叠子问题，通过存储子问题的解避免重复计算，自底向上或自顶向下求解全局最优。
- **常见维度**：状态定义（一维/二维/多维）、状态转移方程、初始化、遍历顺序、空间优化。
- **高频陷阱**：状态定义不清、转移方程错误、初始化遗漏、遍历顺序颠倒、边界条件处理不当。
- **DP vs 贪心**：DP 保证全局最优但时间复杂度高；贪心局部最优可能不是全局最优但效率高。

### Python 实战要点
- 使用列表或字典存储 DP 状态，`dp = [0] * n` 或 `dp = {}` 或 `dp = [[0] * m for _ in range(n)]`。
- 记忆化搜索用 `@lru_cache(None)` 或手动字典缓存。
- 滚动数组优化空间：`dp[i]` 只依赖 `dp[i-1]` 时可用两个变量替代数组。
- 状态压缩用位运算：`1 << n` 表示 2^n 种状态。
- 逆向思维：有时"最多"等价于"总数减去最少"。

## 模式与模板

### 1. 线性 DP - 单序列
**识别信号**：一维数组，每个位置的状态只依赖前面的若干位置，如爬楼梯、打家劫舍、最长递增子序列。
**套路解析**：定义 `dp[i]` 表示以位置 i 结尾或前 i 个元素的最优解，通过前面的状态转移到当前状态。

**伪代码模板**:
```python
# 基础线性 DP
dp = [0] * (n + 1)
dp[0] = base_case

for i in range(1, n + 1):
    for j in range(i):  # 或只看前几个
        dp[i] = max(dp[i], dp[j] + transition(j, i))
return dp[n]
```

**适用题目**：
- `LC 70` Climbing Stairs
- `LC 198` House Robber
- `LC 213` House Robber II (环形)
- `LC 300` Longest Increasing Subsequence
- `LC 53` Maximum Subarray
- `LC 152` Maximum Product Subarray
- `LC 91` Decode Ways
- `LC 139` Word Break
- `LC 377` Combination Sum IV

**要点提醒**：
- 爬楼梯是斐波那契数列，可空间优化到 O(1)。
- 打家劫舍维护"选"与"不选"两种状态。
- LIS 可用贪心+二分优化到 O(n log n)。

### 2. 二维 DP - 双序列 / 矩阵路径
**识别信号**：二维网格、两个字符串匹配、矩阵路径问题，状态依赖上方、左方或左上方。
**套路解析**：定义 `dp[i][j]` 表示到达位置 (i, j) 或匹配前 i 和前 j 个字符的最优解。

**伪代码模板**:
```python
# 矩阵路径 DP
dp = [[0] * m for _ in range(n)]
# 初始化第一行和第一列
for i in range(n):
    dp[i][0] = initial_value
for j in range(m):
    dp[0][j] = initial_value

for i in range(1, n):
    for j in range(1, m):
        dp[i][j] = max(
            dp[i-1][j] + cost_down,
            dp[i][j-1] + cost_right
        )
return dp[n-1][m-1]
```

**适用题目**：
- `LC 62` Unique Paths
- `LC 63` Unique Paths II
- `LC 64` Minimum Path Sum
- `LC 72` Edit Distance
- `LC 97` Interleaving String
- `LC 115` Distinct Subsequences
- `LC 1143` Longest Common Subsequence
- `LC 516` Longest Palindromic Subsequence
- `LC 718` Maximum Length of Repeated Subarray

**要点提醒**：
- 编辑距离是经典双序列 DP，转移考虑插入/删除/替换。
- 可滚动数组优化空间到 O(min(m, n))。
- LCS 是双序列 DP 的基础模板。

### 3. 背包问题
**识别信号**：给定物品和容量限制，求最大价值或方案数，关键词"容量""重量""体积""恰好""至少""至多"。
**套路解析**：
- **0/1背包**：每个物品只能选一次，`dp[i][j]` 表示前 i 个物品容量 j 的最大价值。
- **完全背包**：每个物品可选无限次，内层循环正序遍历。
- **多重背包**：每个物品有数量限制，二进制优化转化为 0/1 背包。

**伪代码模板**:
```python
# 0/1 背包（空间优化版）
dp = [0] * (capacity + 1)
for i in range(n):
    for j in range(capacity, weight[i] - 1, -1):  # 逆序
        dp[j] = max(dp[j], dp[j - weight[i]] + value[i])

# 完全背包
dp = [0] * (capacity + 1)
for i in range(n):
    for j in range(weight[i], capacity + 1):  # 正序
        dp[j] = max(dp[j], dp[j - weight[i]] + value[i])

# 恰好装满的方案数
dp = [0] * (capacity + 1)
dp[0] = 1  # 初始化：容量0有1种方案
for num in nums:
    for j in range(capacity, num - 1, -1):
        dp[j] += dp[j - num]
```

**适用题目**：
- `LC 416` Partition Equal Subset Sum (0/1背包)
- `LC 494` Target Sum (0/1背包变形)
- `LC 474` Ones and Zeroes (二维0/1背包)
- `LC 322` Coin Change (完全背包)
- `LC 518` Coin Change II (完全背包方案数)
- `LC 377` Combination Sum IV (完全背包排列数)
- `LC 279` Perfect Squares (完全背包)
- `LC 1049` Last Stone Weight II (0/1背包)

**要点提醒**：
- 0/1背包逆序遍历，完全背包正序遍历。
- 求方案数时初始化 `dp[0] = 1`。
- 组合数和排列数的遍历顺序不同。

### 4. 区间 DP
**识别信号**：在一个区间上操作，问题规模逐渐缩小，如回文串、戳气球、矩阵链乘法。
**套路解析**：`dp[i][j]` 表示区间 [i, j] 的最优解，通过枚举分割点 k 将区间分为两部分。

**伪代码模板**:
```python
# 区间 DP
dp = [[0] * n for _ in range(n)]

# 初始化长度为1的区间
for i in range(n):
    dp[i][i] = base_case

# 按区间长度遍历
for length in range(2, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1
        for k in range(i, j):
            dp[i][j] = max(
                dp[i][j],
                dp[i][k] + dp[k+1][j] + cost(i, k, j)
            )
return dp[0][n-1]
```

**适用题目**：
- `LC 5` Longest Palindromic Substring
- `LC 516` Longest Palindromic Subsequence
- `LC 647` Palindromic Substrings
- `LC 312` Burst Balloons
- `LC 1039` Minimum Score Triangulation of Polygon
- `LC 1547` Minimum Cost to Cut a Stick
- `LC 375` Guess Number Higher or Lower II

**要点提醒**：
- 遍历顺序：按长度从小到大，或从右下到左上。
- 戳气球等题需要技巧性转化（虚拟边界）。
- 回文问题可用中心扩展或Manacher算法优化。

### 5. 状态机 DP
**识别信号**：问题有多个状态，状态之间有转移关系，如股票买卖、状态切换。
**套路解析**：定义多个状态数组，每个状态转移到其他允许的状态。

**伪代码模板**:
```python
# 股票问题状态机（最多k次交易）
# buy[i][j]: 第i天完成j次交易持有股票
# sell[i][j]: 第i天完成j次交易不持有股票

buy = [[-inf] * (k + 1) for _ in range(n)]
sell = [[0] * (k + 1) for _ in range(n)]

buy[0][0] = -prices[0]
for i in range(1, n):
    for j in range(k + 1):
        if j > 0:
            buy[i][j] = max(buy[i-1][j], sell[i-1][j-1] - prices[i])
        sell[i][j] = max(sell[i-1][j], buy[i-1][j] + prices[i])

# 空间优化版
hold = -prices[0]
free = 0
for i in range(1, n):
    new_hold = max(hold, free - prices[i])
    new_free = max(free, hold + prices[i])
    hold, free = new_hold, new_free
```

**适用题目**：
- `LC 121` Best Time to Buy and Sell Stock
- `LC 122` Best Time to Buy and Sell Stock II
- `LC 123` Best Time to Buy and Sell Stock III
- `LC 188` Best Time to Buy and Sell Stock IV
- `LC 309` Best Time to Buy and Sell Stock with Cooldown
- `LC 714` Best Time to Buy and Sell Stock with Transaction Fee
- `LC 1911` Maximum Alternating Subsequence Sum

**要点提醒**：
- 明确状态定义：持有/不持有、第几次交易、是否冷却。
- 画状态转移图帮助理解。
- 可用滚动变量优化空间。

### 6. 状态压缩 DP
**识别信号**：集合元素选择、排列组合、N 皇后、旅行商问题，状态数为 2^n。
**套路解析**：用整数的二进制位表示状态，位运算操作状态转移。

**伪代码模板**:
```python
# 状态压缩 DP
n = len(nums)
dp = [0] * (1 << n)
dp[0] = base_case

for mask in range(1 << n):
    for i in range(n):
        if mask & (1 << i):  # 第i位为1
            prev_mask = mask ^ (1 << i)  # 去掉第i位
            dp[mask] = max(dp[mask], dp[prev_mask] + value(i))

# 枚举子集
mask = full_mask
while mask:
    # 处理 mask
    mask = (mask - 1) & full_mask
```

**适用题目**：
- `LC 526` Beautiful Arrangement
- `LC 698` Partition to K Equal Sum Subsets
- `LC 847` Shortest Path Visiting All Nodes
- `LC 943` Find the Shortest Superstring
- `LC 1125` Smallest Sufficient Team
- `LC 1434` Number of Ways to Wear Different Hats to Each Other

**要点提醒**：
- 位运算技巧：`mask & (1 << i)` 检查第 i 位，`mask | (1 << i)` 设置第 i 位。
- 时间复杂度通常 O(2^n * n) 或 O(2^n * n^2)。
- 适用于 n ≤ 20 的小规模问题。

### 7. 树形 DP
**识别信号**：在树结构上求解，如树的直径、树上最大独立集、子树统计。
**套路解析**：后序遍历，从叶子向根传递信息，根据子树状态计算当前节点状态。

**伪代码模板**:
```python
# 树形 DP
def dfs(node):
    if not node:
        return base_case

    left = dfs(node.left)
    right = dfs(node.right)

    # 选择当前节点
    select = node.val + left.not_select + right.not_select
    # 不选择当前节点
    not_select = max(left.select, left.not_select) + \
                 max(right.select, right.not_select)

    return State(select, not_select)

# 返回单边最大贡献
def max_path_sum(node):
    nonlocal answer
    if not node:
        return 0
    left = max(0, max_path_sum(node.left))
    right = max(0, max_path_sum(node.right))
    answer = max(answer, left + node.val + right)
    return node.val + max(left, right)
```

**适用题目**：
- `LC 337` House Robber III
- `LC 124` Binary Tree Maximum Path Sum
- `LC 543` Diameter of Binary Tree
- `LC 968` Binary Tree Cameras
- `LC 979` Distribute Coins in Binary Tree
- `LC 1245` Tree Diameter

**要点提醒**：
- 区分"向上返回"和"全局答案"。
- 返回值通常是单边最优，全局答案在递归中更新。
- 可能需要返回多个状态（选/不选）。

### 8. 数位 DP
**识别信号**：统计一定范围内满足某种条件的数的个数，如不含某数字、数字和等。
**套路解析**：按位构造数字，记忆化搜索每一位的选择。

**伪代码模板**:
```python
from functools import lru_cache

@lru_cache(None)
def dfs(pos, tight, state):
    """
    pos: 当前处理到第几位
    tight: 是否受上界限制
    state: 自定义状态（如数字和、是否出现某数字）
    """
    if pos == -1:
        return check(state)

    limit = int(num[pos]) if tight else 9
    result = 0

    for digit in range(0, limit + 1):
        new_tight = tight and (digit == limit)
        new_state = update_state(state, digit)
        result += dfs(pos - 1, new_tight, new_state)

    return result
```

**适用题目**：
- `LC 233` Number of Digit One
- `LC 357` Count Numbers with Unique Digits
- `LC 600` Non-negative Integers without Consecutive Ones
- `LC 902` Numbers At Most N Given Digit Set
- `LC 1012` Numbers With Repeated Digits

**要点提醒**：
- 记忆化搜索比迭代更直观。
- 注意前导零的处理。
- tight 标记控制当前位的上界。

### 9. 记忆化搜索 / 自顶向下 DP
**识别信号**：递归解法存在大量重复计算，适合用缓存优化。
**套路解析**：递归 + 哈希表/装饰器缓存中间结果。

**伪代码模板**:
```python
from functools import lru_cache

@lru_cache(None)
def dp(state):
    if is_base_case(state):
        return base_value

    result = init_value
    for next_state in get_transitions(state):
        result = combine(result, dp(next_state))

    return result

# 或手动字典
memo = {}
def dp(state):
    if state in memo:
        return memo[state]
    if is_base_case(state):
        return base_value

    result = solve(state)
    memo[state] = result
    return result
```

**适用题目**：
- `LC 70` Climbing Stairs
- `LC 139` Word Break
- `LC 140` Word Break II
- `LC 329` Longest Increasing Path in a Matrix
- `LC 1478` Allocate Mailboxes

**要点提醒**：
- Python 的 `@lru_cache` 很方便，但参数必须可哈希。
- 适合状态空间不规则的问题。
- 可能比自底向上更直观，但有递归栈深度限制。

### 10. 概率 / 期望 DP
**识别信号**：求概率、期望值，通常涉及随机选择或游戏。
**套路解析**：定义 `dp[state]` 为某状态下的概率或期望，逆向或正向推导。

**伪代码模板**:
```python
# 期望 DP
dp = [0] * (n + 1)
dp[target] = 0  # 目标状态期望为0

for i in range(target - 1, -1, -1):
    dp[i] = 1 + sum(dp[i + j] * prob[j] for j in range(1, k + 1))
```

**适用题目**：
- `LC 808` Soup Servings
- `LC 837` New 21 Game
- `LC 1227` Airplane Seat Assignment Probability

**要点提醒**：
- 期望问题通常逆向 DP。
- 概率问题注意归一化。
- 可能需要高精度或近似处理。

## 现有题目对照表
| Notebook | 套路 | 难度 | 关键要点 |
| --- | --- | --- | --- |
| `DP/LC_70_climbing-stairs.ipynb` | 线性DP | Easy | 斐波那契，空间优化 |
| `DP/LC_198_house-robber.ipynb` | 线性DP | Medium | 选/不选两状态 |
| `DP/LC_213_house-robber-ii.ipynb` | 线性DP | Medium | 环形数组，拆分两次 |
| `DP/LC_53_maximum-subarray.ipynb` | 线性DP | Medium | Kadane算法 |
| `DP/LC_152_maximum-product-subarray.ipynb` | 线性DP | Medium | 维护最大最小值 |
| `DP/LC_300_longest-increasing-subsequence.ipynb` | 线性DP | Medium | O(n²) DP或O(n log n)贪心+二分 |
| `DP/LC_139_word-break.ipynb` | 线性DP | Medium | 完全背包变形 |
| `DP/LC_91_decode-ways.ipynb` | 线性DP | Medium | 双指针状态转移 |
| `DP/LC_62_unique-paths.ipynb` | 二维DP | Medium | 组合数或DP |
| `DP/LC_63_unique-paths-ii.ipynb` | 二维DP | Medium | 处理障碍物 |
| `DP/LC_64_minimum-path-sum.ipynb` | 二维DP | Medium | 最小路径和 |
| `DP/LC_72_edit-distance.ipynb` | 二维DP | Hard | 经典双序列DP |
| `DP/LC_1143_longest-common-subsequence.ipynb` | 二维DP | Medium | LCS模板 |
| `DP/LC_416_partition-equal-subset-sum.ipynb` | 0/1背包 | Medium | 转化为背包问题 |
| `DP/LC_494_target-sum.ipynb` | 0/1背包 | Medium | 01背包方案数 |
| `DP/LC_322_coin-change.ipynb` | 完全背包 | Medium | 最少硬币数 |
| `DP/LC_518_coin-change-ii.ipynb` | 完全背包 | Medium | 组合数 |
| `DP/LC_5_longest-palindromic-substring.ipynb` | 区间DP | Medium | 中心扩展或DP |
| `DP/LC_516_longest-palindromic-subsequence.ipynb` | 区间DP | Medium | 区间DP模板 |
| `DP/LC_312_burst-balloons.ipynb` | 区间DP | Hard | 逆向思维 |
| `DP/LC_121_best-time-to-buy-and-sell-stock.ipynb` | 状态机 | Easy | 单次交易 |
| `DP/LC_122_best-time-to-buy-and-sell-stock-ii.ipynb` | 状态机 | Medium | 无限次交易 |
| `DP/LC_123_best-time-to-buy-and-sell-stock-iii.ipynb` | 状态机 | Hard | 最多2次交易 |
| `DP/LC_188_best-time-to-buy-and-sell-stock-iv.ipynb` | 状态机 | Hard | 最多k次交易 |
| `DP/LC_309_best-time-to-buy-and-sell-stock-with-cooldown.ipynb` | 状态机 | Medium | 冷却期 |
| `DP/LC_337_house-robber-iii.ipynb` | 树形DP | Medium | 树上打家劫舍 |
| `DP/LC_124_binary-tree-maximum-path-sum.ipynb` | 树形DP | Hard | 树上最大路径和 |
| `DP/LC_329_longest-increasing-path-in-a-matrix.ipynb` | 记忆化搜索 | Hard | DFS+记忆化 |

## 复习与拓展建议
- **识别DP类型**：做题时先判断是哪种DP模式，套用对应模板。
- **状态定义要清晰**：写出状态表示什么，明确维度含义。
- **推导转移方程**：根据子问题关系写出递推式，画图辅助理解。
- **初始化要完整**：base case 必须正确，否则后续全错。
- **遍历顺序要对**：自底向上时注意依赖关系，避免使用未计算的状态。
- **空间优化技巧**：
  - 一维DP：滚动变量
  - 二维DP：滚动数组（只用两行）
  - 背包问题：逆序/正序遍历
- **调试方法**：打印DP数组，检查状态转移是否正确。
- **证明正确性**：
  - 最优子结构：最优解包含子问题的最优解
  - 无后效性：当前状态不影响之前的状态
- **对照表查漏**：复盘题目时，先识别DP模式，再查看 Notebook 实现细节。
- **MLE/AI 场景迁移**：DP 在序列标注、强化学习、最优化问题中广泛应用。

## DP 解题步骤
1. **定义状态**：`dp[i]` 或 `dp[i][j]` 表示什么？
2. **找状态转移方程**：当前状态如何从之前状态转移？
3. **初始化**：base case 是什么？
4. **确定遍历顺序**：从小到大还是从大到小？
5. **返回答案**：最终答案在哪个位置？
6. **优化空间**：能否用滚动数组或变量优化？

## 常见 DP 优化技巧
- **滚动数组**：二维DP降为一维
- **单调队列/栈**：优化转移时的min/max查找
- **前缀和/差分**：快速计算区间和
- **贪心+二分**：如LIS的 O(n log n) 解法
- **矩阵快速幂**：线性递推优化到 O(log n)
- **斜率优化**：某些DP的转移优化
- **四边形不等式**：区间DP的优化

## 练习路线
1. **线性DP基础**：70 → 198 → 53 → 300 → 139
2. **线性DP进阶**：213 → 152 → 91 → 377
3. **二维DP基础**：62 → 63 → 64 → 1143
4. **二维DP进阶**：72 → 97 → 115 → 718
5. **背包问题**：416 → 494 → 322 → 518 → 279
6. **区间DP**：5 → 516 → 647 → 312
7. **状态机DP**：121 → 122 → 123 → 188 → 309 → 714
8. **树形DP**：337 → 124 → 543 → 968
9. **状态压缩DP**：698 → 847 → 943
10. **记忆化搜索**：139 → 140 → 329

## DP vs 其他算法
| 算法 | 适用场景 | 时间复杂度 | 空间复杂度 |
| --- | --- | --- | --- |
| DP | 最优子结构+重叠子问题 | O(状态数×转移) | O(状态数) |
| 贪心 | 局部最优→全局最优 | O(n log n) | O(1) |
| 分治 | 无重叠子问题 | O(n log n) | O(log n) |
| 回溯 | 枚举所有方案 | O(2^n) 或 O(n!) | O(n) |

## 小技巧 Checklist
- 画递归树/状态转移图帮助理解。
- 先写暴力递归，再改记忆化，最后改迭代DP。
- 注意边界条件：空数组、单元素、全相同等。
- 背包问题：0/1逆序，完全正序。
- 打印DP数组调试，观察状态转移。
- 时间复杂度 = 状态数 × 每个状态的转移次数。
- 空间优化：画出依赖关系，确定只需保留哪些状态。
