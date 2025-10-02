# BFS 刷题指南（中文）

本指南围绕广度优先搜索（Breadth-First Search）梳理常见题型、模板与 Notebook 映射。编写新笔记前先确定题目属于哪类 BFS 模式，再回到对应 Notebook 补齐分析、代码与测试。

## 基本概念速览
- **核心机制**：按层扩展节点，优先访问距离起点最近的状态；适用于最短步数、最短路径、按层统计等问题。
- **典型结构**：使用 `collections.deque` 实现队列；访问状态时立即标记 `visited`，避免重复扩展。
- **常见变体**：单源 BFS、双向 BFS、多源扩散、状态图 BFS、拓扑 BFS（入度法）等。
- **易错点**：忘记在入队时标记 visited，导致重复入队；层数统计混乱；状态压缩不当造成内存或时间炸裂。

### Python 实战要点
- 使用 `deque.popleft()` 获取 O(1) 出队性能。
- 对网格 BFS 预先定义方向数组，例如 `dirs = [(1,0), (-1,0), (0,1), (0,-1)]`。
- 层数（步数）统计常通过“记录当前层队列长度”或在队列中存 `(node, depth)`。
- 状态图 BFS 中，`visited` 可以是 `set`（字符串/元组）或数组（整数/坐标）。
- 对规模较大的无权图，可考虑双向 BFS；遇到 0/1 权重可以扩展为 0-1 BFS。

## 模式与模板

### 1. 网格单源最短路径 BFS
**套路解析**：从单一起点出发，逐层扩展到目标位置，常用于网格最短路径、障碍绕行等问题。状态主要由 `(row, col)` 或 `(row, col, extra)` 组成。
**伪代码模板**：
```python
queue = deque([(sr, sc, 0)])
visited[sr][sc] = True
while queue:
    r, c, dist = queue.popleft()
    if (r, c) == target:
        return dist
    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        if valid(nr, nc) and not visited[nr][nc]:
            visited[nr][nc] = True
            queue.append((nr, nc, dist + 1))
return -1
```
- 代表题目：
  - `BFS/LC_1091_shortest-path-in-binary-matrix.ipynb`
  - `BFS/LC_1293_shortest-path-in-a-grid-with-obstacles-elimination.ipynb`
  - `BFS/LC_490_the-maze.ipynb`

### 2. 多源扩散 BFS
**套路解析**：多个起点同时向外扩散，常用于最近距离场、感染传播。初始化时把所有起点一次性入队，BFS 层数即传播时间或距离。
**伪代码模板**：
```python
queue = deque(sources)
for r, c in sources:
    dist[r][c] = 0
while queue:
    r, c = queue.popleft()
    for nr, nc in neighbors(r, c):
        if dist[nr][nc] > dist[r][c] + 1:
            dist[nr][nc] = dist[r][c] + 1
            queue.append((nr, nc))
```
- 代表题目：
  - `BFS/LC_542_01-matrix.ipynb`
  - `BFS/LC_994_rotting-oranges.ipynb`
  - `BFS/LC_1765_map-of-highest-peak.ipynb`

### 3. 状态图 BFS（字符串/数组/整数）
**套路解析**：节点是抽象状态（密码、棋盘、数字），通过合法操作产生邻居。BFS 第一时间找到最短操作序列。
**伪代码模板**：
```python
queue = deque([(start, 0)])
visited = {start}
while queue:
    state, steps = queue.popleft()
    if state == target:
        return steps
    for nxt in generate_neighbors(state):
        if nxt not in visited and nxt not in blocked:
            visited.add(nxt)
            queue.append((nxt, steps + 1))
return -1
```
- 代表题目：
  - `BFS/LC_752_open-the-lock.ipynb`
  - `BFS/LC_279_perfect-squares.ipynb`
  - `BFS/LC_773_sliding-puzzle.ipynb`

### 4. 树按层遍历与层次统计
**套路解析**：对树结构进行层序访问，常用于输出层级列表、zigzag 顺序、每层最大值等。核心是记录当前层结点数量。
**伪代码模板**：
```python
queue = deque([root])
while queue:
    size = len(queue)
    level = []
    for _ in range(size):
        node = queue.popleft()
        level.append(node.val)
        enqueue children...
    process(level)
```
- 代表题目：
  - `BFS/LC_102_binary-tree-level-order-traversal.ipynb`
  - `BFS/LC_103_binary-tree-zigzag-level-order-traversal.ipynb`
  - `BFS/LC_515_find-largest-value-in-each-tree-row.ipynb`

### 5. 拓扑 BFS（Kahn 算法与逆向拓扑）
**套路解析**：使用入度队列处理 DAG 中的入度为 0 节点，或在反向图上处理出度为 0 节点。常用于课程安排、依赖解析、安全节点判断。
**伪代码模板**：
```python
queue = deque(nodes with indegree == 0)
order = []
while queue:
    node = queue.popleft()
    order.append(node)
    for nei in graph[node]:
        indegree[nei] -= 1
        if indegree[nei] == 0:
            queue.append(nei)
```
或逆向：
```python
queue = deque(nodes with outdegree == 0)
while queue:
    node = queue.popleft()
    for prev in reverse[node]:
        outdegree[prev] -= 1
        if outdegree[prev] == 0:
            queue.append(prev)
```
- 代表题目：
  - `BFS/LC_207_course-schedule-bfs.ipynb`
  - `BFS/LC_210_course-schedule-ii.ipynb`
  - `BFS/LC_802_find-eventual-safe-states.ipynb`

## 现有题目对照表
| Notebook | 套路 | 关键要点 | 待补充内容 |
| --- | --- | --- | --- |
| `BFS/LC_1091_shortest-path-in-binary-matrix.ipynb` | 网格单源 BFS | 八方向最短路径 | 补充 A* 版本对比 |
| `BFS/LC_1293_shortest-path-in-a-grid-with-obstacles-elimination.ipynb` | 网格单源 BFS | 状态扩展添加剩余消除次数 | 讨论启发式剪枝策略 |
| `BFS/LC_490_the-maze.ipynb` | 网格单源 BFS | 滚动直到撞墙再停下 | 加入最短路径长度/路径复原 |
| `BFS/LC_542_01-matrix.ipynb` | 多源 BFS | 同步扩散求最近 0 距离 | 添加 DP 两遍解法对照 |
| `BFS/LC_994_rotting-oranges.ipynb` | 多源 BFS | 层数即分钟数 | 拓展对角传播/不同速度 |
| `BFS/LC_1765_map-of-highest-peak.ipynb` | 多源 BFS | 多水源构造高度场 | 探讨无水场景处理策略 |
| `BFS/LC_752_open-the-lock.ipynb` | 状态图 BFS | 生成 8 个相邻锁状态 | 实现双向 BFS 优化 |
| `BFS/LC_279_perfect-squares.ipynb` | 状态图 BFS | 层数等于最少平方数 | 对比 DP/四平方定理 |
| `BFS/LC_773_sliding-puzzle.ipynb` | 状态图 BFS | 6! 状态空间搜索 | 提供双向 BFS 或 A* 讨论 |
| `BFS/LC_102_binary-tree-level-order-traversal.ipynb` | 树层序 BFS | 基础层序模板 | 拓展输出自底向上顺序 |
| `BFS/LC_103_binary-tree-zigzag-level-order-traversal.ipynb` | 树层序 BFS | 方向翻转实现 Zigzag | 使用 deque 优化插入性能 |
| `BFS/LC_515_find-largest-value-in-each-tree-row.ipynb` | 树层序 BFS | 逐层维护最大值 | 统计最小值/平均值对比 |
| `BFS/LC_207_course-schedule-bfs.ipynb` | 拓扑 BFS | 入度为 0 队列检测环 | 记录拓扑序供调试 |
| `BFS/LC_210_course-schedule-ii.ipynb` | 拓扑 BFS | 输出任一拓扑序 | 讨论字典序最小序列 |
| `BFS/LC_802_find-eventual-safe-states.ipynb` | 逆向拓扑 BFS | 反向图减少出度 | 延伸到权重/概率模型 |

## 复习与拓展建议
- **识别模式**：题目涉及“最短步数”“最短路径”“按层统计”“依赖解析”时优先考虑 BFS，并判断是否需要单源、多源或拓扑。
- **理清状态**：明确节点表示、邻居生成和终止条件，确保状态空间有限且可判重。
- **优化技巧**：
  - 双向 BFS 可显著降低深度。
  - 入队即标记 visited，防止重复扩展。
  - 对于多源扩散，初始化队列包含所有源点。
- **拓扑场景**：掌握 Kahn 算法（入度法）和逆向拓扑（出度法），在依赖图中判断可行性、生成顺序或找安全节点。
- **持续同步**：新增 BFS 笔记时，记得更新本指南的模板列表和对照表，保持目录与内容一致。需要对同一问题编写不同范式（如 DFS 与 BFS）时，注意命名区别并在指南中标注。 
