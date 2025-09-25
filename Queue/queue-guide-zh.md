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
**适用情形**：需要按层收集树节点信息、构建层序输出或在树上执行分层统计时。
**套路解读**：用队列顺序处理每一层节点，常搭配层大小计数或层序记录，确保同层节点一起被消费。

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
**适用情形**：网格或矩阵上需要统计连通块、扩散标记或模拟区域填充时。
**套路解读**：从任意陆地/目标格出发，用队列向四邻或八邻扩散，逐一标记同一连通块，避免重复访问。

**模板精要**：
```python
from collections import deque

def flood_fill(grid, start):
    rows, cols = len(grid), len(grid[0])
    queue = deque([start])
    grid[start[0]][start[1]] = MARKED
    while queue:
        x, y = queue.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == TARGET:
                grid[nx][ny] = MARKED
                queue.append((nx, ny))
```

**经典题目**：
- `Queue/LC_200_number-of-islands.ipynb`
- `Queue/LC_994_rotting-oranges.ipynb`


### 3. 多源 BFS 与距离变换
**适用情形**：需要同时从多个源点出发，计算到最近源点的距离或最短传播时间时。
**套路解读**：把所有源点统一压入队列作为第 0 层，逐层松弛邻居距离，实现整体传播的最短路更新。

**模板精要**：
```python
from collections import deque

queue = deque()
dist = [[float('inf')] * cols for _ in range(rows)]
for r, c in sources:
    dist[r][c] = 0
    queue.append((r, c))
while queue:
    x, y = queue.popleft()
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols and dist[nx][ny] > dist[x][y] + 1:
            dist[nx][ny] = dist[x][y] + 1
            queue.append((nx, ny))
```

**经典题目**：
- `Queue/LC_542_01-matrix.ipynb`
- `Queue/LC_1091_shortest-path-in-binary-matrix.ipynb`


### 4. 图搜索与状态空间最短路
**适用情形**：在状态空间或图上寻找最少步数达到目标配置、验证可达性或发现最短操作序列时。
**套路解读**：使用 BFS 在无权图/状态空间中扩展邻居，配合 visited 集合去重，首个到达目标的路径即最短。

**模板精要**：
```python
from collections import deque

def bfs_shortest(start):
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        state, dist = queue.popleft()
        if is_goal(state):
            return dist
        for nxt in expand(state):
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, dist + 1))
    return -1
```

**经典题目**：
- `Queue/LC_433_minimum-genetic-mutation.ipynb`
- `Queue/LC_752_open-the-lock.ipynb`
- `Queue/LC_785_is-graph-bipartite.ipynb`


### 5. 拓扑排序（Kahn 算法）
**适用情形**：处理有向无环图依赖、课程安排或构建执行顺序并检测是否有环时。
**套路解读**：先统计各节点入度，队列维护入度为 0 的节点，逐步出队并削减邻居入度，构造拓扑序列。

**模板精要**：
```python
from collections import deque, defaultdict

def topo_order(n, edges):
    graph = defaultdict(list)
    indegree = [0] * n
    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1
    queue = deque([i for i in range(n) if indegree[i] == 0])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in graph[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return order
```

**经典题目**：
- `Queue/LC_207_course-schedule.ipynb`
- `Queue/LC_210_course-schedule-ii.ipynb`


### 6. 单调队列：滑动窗口统计
**适用情形**：在固定长度窗口内维护最大值/最小值或检查窗口是否满足约束时。
**套路解读**：使用双端队列记录可能成为答案的索引，保持单调性并及时剔除过期元素，实现 O(n) 窗口更新。

**模板精要**：
```python
from collections import deque

def window_max(nums, k):
    dq = deque()
    result = []
    for i, val in enumerate(nums):
        while dq and dq[0] <= i - k:
            dq.popleft()
        while dq and nums[dq[-1]] <= val:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result
```

**经典题目**：
- `Queue/LC_239_sliding-window-maximum.ipynb`
- `Queue/LC_862_shortest-subarray-with-sum-at-least-k.ipynb`
- `Queue/LC_1438_longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit.ipynb`


### 7. 单调队列：动态规划加速
**适用情形**：DP 转移仅依赖最近 k 个状态的最大/最小值，希望把 O(nk) 降到 O(n) 时。
**套路解读**：把 DP 中的候选状态放入双端队列，维护单调性和窗口范围，以常数时间得到最佳转移。

**模板精要**：
```python
from collections import deque

def dp_with_deque(nums, k):
    dq = deque([0])
    dp = [0] * len(nums)
    dp[0] = nums[0]
    for i in range(1, len(nums)):
        while dq and dq[0] < i - k:
            dq.popleft()
        dp[i] = nums[i] + dp[dq[0]]
        while dq and dp[i] >= dp[dq[-1]]:
            dq.pop()
        dq.append(i)
    return dp[-1]
```

**经典题目**：
- `Queue/LC_1696_jump-game-vi.ipynb`
- `Queue/LC_1425_constrained-subsequence-sum.ipynb`


### 8. 队列 & 双端队列设计题
**适用情形**：题目要求自行实现队列/双端队列接口、控制容量或提供 O(1) 时间复杂度操作时。
**套路解读**：围绕队列语义构建自定义数据结构，常见做法包括环形数组、双栈倒腾、单队列旋转等。

**模板精要**：
```python
from collections import deque

class RecentCounter:
    def __init__(self):
        self.queue = deque()
    def ping(self, t: int) -> int:
        self.queue.append(t)
        threshold = t - WINDOW
        while self.queue and self.queue[0] < threshold:
            self.queue.popleft()
        return len(self.queue)
```

**经典题目**：
- `Queue/LC_225_implement-stack-using-queues.ipynb`
- `Queue/LC_232_implement-queue-using-stacks.ipynb`
- `Queue/LC_622_design-circular-queue.ipynb`
- `Queue/LC_641_design-circular-deque.ipynb`
- `Queue/LC_933_number-of-recent-calls.ipynb`

## 现有题目对照表
| Notebook | 套路 | 关键要点 | 待补充内容 |
| --- | --- | --- | --- |
| `Queue/LC_102_binary-tree-level-order-traversal.ipynb` | 树层序 BFS | 队列逐层出队并收集节点值 | 增补按层聚合统计示例 |
| `Queue/LC_200_number-of-islands.ipynb` | 网格 flood fill | 队列扩散标记连通块 | 加入 8 邻域/对角扩散对比 |
| `Queue/LC_542_01-matrix.ipynb` | 多源 BFS | 所有 0 作为源点统一松弛距离 | 比较动态规划两遍解法 |
| `Queue/LC_433_minimum-genetic-mutation.ipynb` | 状态空间 BFS | 逐位尝试突变并过滤银行 | 补充双向 BFS/启发式策略 |
| `Queue/LC_207_course-schedule.ipynb` | 拓扑排序 Kahn | 入度为 0 入队并削减依赖 | 追加返回环中课程的思路 |
| `Queue/LC_239_sliding-window-maximum.ipynb` | 单调队列窗口 | 维护递减队列快速取最大值 | 附多语言或多线程实现对比 |
| `Queue/LC_1696_jump-game-vi.ipynb` | 单调队列 DP | 窗口内选最大 dp 实现 O(n) | 说明记忆压缩或懒惰删除技巧 |
| `Queue/LC_622_design-circular-queue.ipynb` | 环形数组设计 | head/size 控制固定容量 | 探讨动态扩容与线程安全 |
| `Queue/LC_933_number-of-recent-calls.ipynb` | 队列滑动计数 | 剔除窗口外时间戳保持最新数量 | 通用化任意窗口长度参数 |

## 学习建议
- **按套路梳理**：对照上文 8 大模式，分别手写模板代码，确认入队、出队及 visited 更新顺序。
- **多题对比**：每种模式至少挑两题对照 Notebook，比较边界处理与复杂度分析。
- **多语言实践**：若目标岗位涉及多语言，尝试将核心模板迁移到 Java/C++/Go，熟悉标准库队列/Deque API。
- **性能验证**：给多源 BFS、单调队列题目补充随机测试或压力测试脚本，验证在极端输入下的表现。
- **知识回填**：遇到拓扑排序、状态空间搜索的高阶变体（例如带权或启发式搜索）时，把思考补充回指南和对应 Notebook。
