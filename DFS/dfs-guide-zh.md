# DFS 刷题指南（中文）

本指南按照深度优先搜索（Depth-First Search）的常见套路整理。识别题型 → 对照相应模板 → 查看代表 Notebook 深化理解与练习。

## 基本概念速览
- **核心思想**：沿分支深入到底再回溯；适用于枚举方案、树/图聚合、状态递归与记忆化。
- **实现形式**：递归（常配合回溯或记忆化）、显式栈、网格就地染色、图邻接表遍历。
- **递归深度**：Python 默认栈深约 1000，必要时 `sys.setrecursionlimit` 或改显式栈。

## 套路与模板

### 1. 树的基础 DFS（遍历 / 验证 / 路径）
- **识别信号**：二叉/多叉树需要前序/中序/后序遍历、验证性质、统计路径或祖先关系。
- **模板要点**：
  - 递归进入节点时可做前序处理，左右子树递归后做后序聚合；中序在左右递归之间。
  - 树结构天然无环，可通过参数 `parent` 控制回溯（在图状树题中）。
  - 根据题意决定返回值：如 LCA 返回节点指针，路径和返回 True/False 或累积值。
- **模板**：
```python
import sys
sys.setrecursionlimit(10**6)

def dfs_tree(node):
    if not node:
        return
    # 前序处理 node
    dfs_tree(node.left)
    # 中序位置
    dfs_tree(node.right)
    # 后序位置
```
- **代表 Notebook / 题目**：LC 94、LC 144、LC 145、LC 236

### 2. 网格 / 矩阵 DFS（连通分量 / 搜索）
- **识别信号**：棋盘、岛屿、迷宫；四/八方向深搜；连通块计数、填色或搜索路径。
- **模板要点**：
  - 方向数组统一维护 4/8 邻；递归时先判断越界和目标值。
  - 可以就地修改（如将 1 改 0）替代 visited；若需保留原网格，可改用布尔 visited。
  - 搜索型（如单词搜索）需要回溯撤销占位符或 visited 标记。
- **模板**：
```python
DIRS4 = [(1,0), (-1,0), (0,1), (0,-1)]

def grid_dfs(x, y):
    if not (0 <= x < m and 0 <= y < n) or grid[x][y] != 1:
        return
    grid[x][y] = 0  # 就地标记防重复
    for dx, dy in DIRS4:
        grid_dfs(x + dx, y + dy)
```
- **代表 Notebook / 题目**：LC 200、LC 695、LC 733、LC 1020

### 3. 图的 DFS（连通性 / 克隆 / 环检测）
- **识别信号**：一般图可达、克隆、检测有向环、DFS 版拓扑排序。
- **模板要点**：
  - 使用邻接表遍历；无向图在递归时跳过父节点。
  - 有向环检测采用 3 色法：白（未访问）、灰（递归栈中）、黑（已完成）。
  - Tarjan 类算法在此基础上维护时间戳与 low 值。
- **模板**：
```python
def dfs_graph(u, parent=-1):
    seen.add(u)
    for v in graph[u]:
        if v == parent:
            continue
        if v not in seen:
            dfs_graph(v, u)
```
有向图判环：
```python
WHITE, GRAY, BLACK = 0, 1, 2
color = [WHITE] * n

def has_cycle(u):
    color[u] = GRAY
    for v in graph[u]:
        if color[v] == GRAY:
            return True
        if color[v] == WHITE and has_cycle(v):
            return True
    color[u] = BLACK
    return False
```
- **代表 Notebook / 题目**：LC 547、LC 133、LC 207、LC 1192

### 4. 回溯（组合 / 子集 / 排列 / 棋盘）
- **识别信号**：需要枚举所有方案或构造一组满足条件的结果；存在“做选择→递归→撤销”的过程。
- **模板要点**：
  - 组合/子集问题通常对输入排序，利用 `i > start and nums[i] == nums[i-1]` 同层去重。
  - 排列去重采用 `used` 数组 + “相同数字只有前一个已使用时才能选”。
  - 剪枝：如目标和剩余值不足、桶容量超限时提前 return。
- **模板**：
```python
def backtrack(start, path):
    res.append(path.copy())
    for i in range(start, len(nums)):
        if i > start and nums[i] == nums[i-1]:
            continue
        path.append(nums[i])
        backtrack(i + 1, path)
        path.pop()
```
排列去重：
```python
def permute_unique(nums):
    nums.sort()
    used = [False] * len(nums)
    path, res = [], []
    def dfs():
        if len(path) == len(nums):
            res.append(path.copy()); return
        for i in range(len(nums)):
            if used[i]:
                continue
            if i > 0 and nums[i] == nums[i-1] and not used[i-1]:
                continue
            used[i] = True
            path.append(nums[i])
            dfs()
            path.pop()
            used[i] = False
    dfs()
    return res
```
- **代表 Notebook / 题目**：LC 39、LC 40、LC 46、LC 47、LC 77、LC 90、LC 216

### 5. DFS + 记忆化（自顶向下 DP / DAG 搜索）
- **识别信号**：重叠子问题，状态可哈希；天然有递归公式。
- **模板要点**：
  - 使用 `@lru_cache` 或手动字典缓存结果；保证状态只访问一次。
  - 状态定义越小越好（如 bitmask、索引+剩余值等）。
  - 若存在环需先处理（例如转换为 DAG 或使用三色法）避免无限递归。
- **模板**：
```python
from functools import lru_cache

@lru_cache(None)
def solve(state):
    if is_base(state):
        return base_value
    best = default
    for nxt in transitions(state):
        best = combine(best, solve(nxt))
    return best
```
- **代表 Notebook / 题目**：LC 329、LC 140、LC 241、LC 464

### 6. 树形 DP（后序合并 / 换根）
- **识别信号**：树上统计全局最优、路径、计数；向父节点返回“单边贡献”。
- **模板要点**：
  - 后序遍历子树信息，在当前节点合并并更新全局答案。
  - 向父节点返回值通常只有一侧（避免重复路径），例如最大路径和只返回单边贡献。
  - 换根 DP 需要二次 DFS：一次计算子树信息，二次换根传播。
- **模板**：
```python
def dfs_tree_dp(node):
    if not node:
        return base_info
    left = dfs_tree_dp(node.left)
    right = dfs_tree_dp(node.right)
    # 根据 left/right 计算当前节点答案与返回值
    return merged_info
```
- **代表 Notebook / 题目**：LC 124、LC 1723、LC 1986

### 7. Tarjan / 低链接（桥 / 割点 / SCC）
- **识别信号**：需要找关键边/点、强连通分量。
- **模板要点**：
  - DFS 过程中维护时间戳 `tin[u]` 和 `low[u]`（能回到的最小时间戳）。
  - 遍历未访问的邻居 v 后更新 `low[u] = min(low[u], low[v])`；若 `low[v] > tin[u]`，说明 (u,v) 是桥。
  - 遇到已访问且非父节点的邻居时，更新 `low[u] = min(low[u], tin[v])`。
- **模板**：
```python
time = 0
tin = [-1] * n
low = [0] * n
bridges = []

def dfs(u, parent=-1):
    global time
    tin[u] = low[u] = time
    time += 1
    for v in graph[u]:
        if v == parent:
            continue
        if tin[v] == -1:
            dfs(v, u)
            low[u] = min(low[u], low[v])
            if low[v] > tin[u]:
                bridges.append((u, v))
        else:
            low[u] = min(low[u], tin[v])
```
- **代表 Notebook / 题目**：LC 1192

### 8. 分治式 DFS（Divide & Conquer）
- **识别信号**：问题被划分为子区间/子表达式，递归求解后合并结果。
- **模板要点**：
  - 递归边界是单个元素或空区间；合并阶段将左右子结果组合。
  - 若子问题存在重叠，可配合记忆化缓存中间结果。
- **模板**：
```python
def divide_and_conquer(l, r):
    if l == r:
        return base_case(l)
    ans = []
    for mid in range(l, r):
        left = divide_and_conquer(l, mid)
        right = divide_and_conquer(mid + 1, r)
        ans.extend(combine(left, right))
    return ans
```
- **代表 Notebook / 题目**：LC 241

### 9. 搜索优化与工程化技巧
- **识别信号**：回溯状态空间大、需要剪枝/去重/显式栈优化；资源/时间约束紧。
- **技巧要点**：
  - 剪枝：排序后优先放大元素，结合上界估计提前返回（`LC_1723`）。
  - 位掩码剪枝：`LC_473`、`LC_1986` 使用 bitmask 快速判断冲突。
  - 显式栈模拟递归，避免栈溢出；三色法处理有向环。

## 练习路线
1. 树基础 DFS：94 → 144 → 145 → 236 → 124
2. 网格 DFS：200 → 695 → 733 → 1020 → 329
3. 图 DFS：547 → 133 → 207 → 1192
4. 回溯：77 → 90 → 46 → 47 → 39 → 40 → 216
5. 记忆化 DFS：329 → 140 → 241 → 464
6. 树形 DP / 高级剪枝：124 → 1723 → 1986
7. Tarjan：1192（继续练割点/强连通）
8. 分治：241 搭配 395、95 等

## 小技巧 Checklist
- 深递归前调高 `sys.setrecursionlimit` 或使用显式栈。
- 网格/图 DFS 在进入节点时标记；单词搜索类需要回溯撤销标记。
- 去重：组合/排列先排序；同层跳重 vs `used[i-1]`；字符串可用位掩码。
- 剪枝：排序 + 上界估计；优先处理“最难放”的元素；位运算快速判冲突。
- 记忆化：保证无环；DAG 上缓存子问题；对有环图需先拆解。
- Tarjan：注意父边判断、low 值更新顺序。
- 树形 DP：区分“向父返回”与“当前节点答案”，换根需两次遍历。

## TODO / 扩展
- 补充 `LC_79/212`（Trie + DFS）与 `LC_337/968`（更多树形 DP）。
- 增加 Euler Tour/树上前缀技巧示例。
- 收集更多分治/表达式类 DFS Notebook（如 395、95）。
