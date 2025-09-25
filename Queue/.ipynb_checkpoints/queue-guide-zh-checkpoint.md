# Queue 刷题指南（中文）

本指南聚焦面试场景中离不开队列与双端队列（deque）的题型，帮助你从概念、套路到代表题目建立系统复习路径。围绕不同应用模式梳理常见模板，再结合目录下的 Notebook 深挖细节、形成可迁移的解题框架。

## 基本概念速览
- **核心能力**：先进先出（FIFO）数据访问，或双端队列支持两端插入/弹出；广泛用于层序遍历、BFS 最短路、滑动窗口优化与流式统计。
- **常见变体**：循环队列、优先队列（最小/最大堆）、单调队列（维护窗口最大/最小值）、双端队列（允许双端操作）。
- **失误集中地**：
  - BFS 时未正确标记访问状态或重复入队导致爆栈。
  - 单调队列维护条件写反，导致窗口内值未按顺序。
  - 处理字符串/矩阵时忘记边界或初始多源入队处理。

### Python 实战要点
- `collections.deque` 是默认队列/双端队列实现；`append`, `appendleft`, `popleft` 均摊 O(1)。
- `queue.Queue` 线程安全但较慢；单线程题目不建议使用。
- 单调队列通常只存索引，便于根据窗口长度过期元素。
- 多源 BFS 先把所有起点入队并标记距离 0，循环时用层序更新。

## 队列模式与代表题型

### 1. 层序遍历与树的 BFS
**套路解读**：用队列按层顺序处理节点，常搭配每层计数或记录层序方向。

**模板精要**：
```python
from collections import deque
queue = deque([root])
while queue:
    level_size = len(queue)
    level_vals = []
    for _ in range(level_size):
        node = queue.popleft()
        level_vals.append(node.val)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    process(level_vals)
```

**经典题目**：
- `Queue/LC_102_binary-tree-level-order-traversal.ipynb`
- `Queue/LC_103_binary-tree-zigzag-level-order-traversal.ipynb`
- `Queue/LC_199_binary-tree-right-side-view.ipynb`

### 2. Flood Fill 与连通块 BFS
**套路解读**：通过队列扩散访问格子、标记已访问区域，适合求连通块数量或最短扩散时间。

**经典题目**：
- `Queue/LC_200_number-of-islands.ipynb`
- `Queue/LC_994_rotting-oranges.ipynb`

### 3. 多源 BFS 与距离变换
**套路解读**：一次性把多个起点入队，按层次扩散记录距离或最短步数。

**经典题目**：
- `Queue/LC_542_01-matrix.ipynb`
- `Queue/LC_1091_shortest-path-in-binary-matrix.ipynb`

### 4. 图搜索与状态空间最短路
**套路解读**：在图或状态空间中寻找最短步数，往往结合 visited 去重并按层扩展。

**经典题目**：
- `Queue/LC_433_minimum-genetic-mutation.ipynb`
- `Queue/LC_752_open-the-lock.ipynb`
- `Queue/LC_785_is-graph-bipartite.ipynb`

### 5. 拓扑排序（Kahn 算法）
**套路解读**：计算入度、将入度为 0 的节点入队，不断弹出构建拓扑序或检测环。

**经典题目**：
- `Queue/LC_207_course-schedule.ipynb`
- `Queue/LC_210_course-schedule-ii.ipynb`

### 6. 单调队列：滑动窗口统计
**套路解读**：维护窗口内的单调队列以获取最大/最小值或满足区间限制。

**经典题目**：
- `Queue/LC_239_sliding-window-maximum.ipynb`
- `Queue/LC_862_shortest-subarray-with-sum-at-least-k.ipynb`
- `Queue/LC_1438_longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit.ipynb`

### 7. 单调队列：动态规划加速
**套路解读**：在 DP 转移中，通过双端队列维护候选最大/最小值，实现 O(n) 优化。

**经典题目**：
- `Queue/LC_1696_jump-game-vi.ipynb`
- `Queue/LC_1425_constrained-subsequence-sum.ipynb`

### 8. 队列 & 双端队列设计题
**套路解读**：围绕队列语义构建自定义数据结构，关注 API 定义、边界处理与 O(1) 保证。

**经典题目**：
- `Queue/LC_225_implement-stack-using-queues.ipynb`
- `Queue/LC_232_implement-queue-using-stacks.ipynb`
- `Queue/LC_622_design-circular-queue.ipynb`
- `Queue/LC_641_design-circular-deque.ipynb`
- `Queue/LC_933_number-of-recent-calls.ipynb`

## 复习建议
- **先掌握模板**：优先熟悉 BFS、单调队列与 Kahn 算法的伪代码；对比不同题目如何设置入队条件与 visited 判定。
- **结合 Notebook 深挖**：每份 Notebook 按模板提供题目背景、解法讨论、复杂度分析与验证用例；运行验证单元巩固细节。
- **分类回顾**：将遇到的新题按上述套路归档，确保“触类旁通”——一旦确定是 BFS/单调队列题，就能迅速套用方程与边界处理。
- **持续扩充**：若后续遇到新的队列应用（例如双端队列模拟回文、优先队列 Dijkstra），请更新本指南并同步新增 Notebook，保持仓库体系完整。

