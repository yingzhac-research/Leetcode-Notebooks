# BFS 刷题指南（中文）

本指南梳理广度优先搜索（Breadth-First Search）的高频套路。识别题型 → 查阅对应模板 → 结合 Notebook 深化实现与测试。

## 基本概念速览
- **核心机制**：按层扩展节点，层数天然对应“最短步数”“最少轮数”。
- **常用工具**：`collections.deque`；入队即标记 `visited`，避免同层重复访问。
- **常见变体**：单源/多源、双向、0-1 BFS、拓扑入度法、额外状态、二分判可行等。
- **易错点**：邻居生成遗漏越界/障碍判断；未判重导致 TLE；层计数与返回条件混乱。

## 套路与模板

### 1. 树的层序遍历（Tree BFS）
- **识别信号**：二叉/多叉树按层输出、统计每层信息或寻找最浅/最深层节点。
- **模板要点**：
  - 队列初始只放根节点，层序循环使用 `for _ in range(len(queue))` 控制当前层。
  - 每弹出节点后立即把左右子节点入队；本层遍历完成后再写入结果/统计指标。
  - 若需要自底向上或锯齿形输出，可在层结束时反转或记录方向标志。
- **模板**：
```python
from collections import deque

def level_order(root):
    if not root:
        return []
    q = deque([root])
    levels = []
    while q:
        size = len(q)
        level = []
        for _ in range(size):
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        levels.append(level)
    return levels
```
- **代表 Notebook / 题目**：LC 102、LC 103、LC 515

### 2. 网格 / 矩阵 BFS（连通性 + 最短路）
- **识别信号**：棋盘、迷宫、岛屿；四/八方向扩展；判断连通块数量或最短路径。
- **模板要点**：
  - 使用方向数组枚举四/八邻；越界、障碍需提前过滤。
  - 根据题意选择在“入队时”或“弹出时”处理答案；最短路可在入队时记录距离。
  - 多起点可直接将所有起点压入初始队列并标记。
- **模板**：
```python
from collections import deque
DIRS4 = [(1,0), (-1,0), (0,1), (0,-1)]

def grid_bfs(starts, passable):
    q = deque(starts)
    seen = set(starts)
    steps = 0
    while q:
        for _ in range(len(q)):
            r, c = q.popleft()
            # 根据题意处理当前单元 (r,c)
            for dr, dc in DIRS4:
                nr, nc = r + dr, c + dc
                if passable(nr, nc) and (nr, nc) not in seen:
                    seen.add((nr, nc))
                    q.append((nr, nc))
        steps += 1
```
- **代表 Notebook / 题目**：LC 1091、LC 490、LC 1293

### 3. 多源 / 反向 BFS
- **识别信号**：题意描述从多个源点同步扩散，或“距离最近的目标/边界”。
- **模板要点**：
  - 将所有源点同时入队并把距离初始化为 0。
  - 逐层扩散即为“时间/距离”；反向思考时先从终点或边界入手。
  - 适合生成“距离场”，供后续二分或 DP 使用。
- **模板**：
```python
from collections import deque

def multi_source_bfs(sources, neighbors):
    q = deque(sources)
    dist = {s: 0 for s in sources}
    while q:
        node = q.popleft()
        for nxt in neighbors(node):
            if nxt not in dist:
                dist[nxt] = dist[node] + 1
                q.append(nxt)
    return dist
```
- **代表 Notebook / 题目**：LC 542、LC 994、LC 1765

### 4. 一般图的无权最短路 / 可达性
- **识别信号**：无权图需要最少步数或是否可达；可在隐式图（如数轴、棋盘映射）上使用。
- **模板要点**：
  - 邻接表构建图；如果是隐式图，`neighbors(node)` 函数负责生成邻居。
  - 访问判重必须在入队前完成，避免重复遍历。
  - 若仅判断可达，可在遇到目标立即返回；若求距离可在层循环外累加。
- **模板**：
```python
from collections import deque

def bfs_graph(n, edges, source, target):
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    q = deque([source])
    visited = {source}
    while q:
        node = q.popleft()
        if node == target:
            return True
        for nxt in graph[node]:
            if nxt not in visited:
                visited.add(nxt)
                q.append(nxt)
    return False
```
- **代表 Notebook / 题目**：LC 1971、LC 279

### 5. 双向 BFS（Bidirectional Search）
- **识别信号**：有明确起点和目标，状态图大且均匀；从两端扩展更快。
- **模板要点**：
  - 维护前向集合 `front` 和后向集合 `back`，每轮扩展节点数更少的一侧。
  - 扩展时生成的邻居若落在另一集合中，则已找到最短路径。
  - 注意在扩展后更新集合，避免重复扩展。
- **模板**：
```python
def bidirectional_bfs(start, target, neighbors):
    if start == target:
        return 0
    front, back = {start}, {target}
    level = 0
    while front and back:
        if len(front) > len(back):
            front, back = back, front
        next_front = set()
        for node in front:
            for nxt in neighbors(node):
                if nxt in back:
                    return level + 1
                if nxt not in next_front:
                    next_front.add(nxt)
        front = next_front
        level += 1
    return -1
```
- **代表 Notebook / 题目**：LC 127、LC 752

### 6. 状态空间 BFS（额外状态 / 位压缩 / 谜题）
- **识别信号**：节点除了位置还带“钥匙集合”“剩余资源”等附加信息。
- **模板要点**：
  - 将完整状态（位置 + 资源/掩码等）存入 visited，防止不同路径重复访问同状态。
  - 若状态空间大，可先排序或压缩状态（例如 bitmask）。
  - 在 expand 函数中生成合法邻居，注意剪枝和去重。
- **模板**：
```python
from collections import deque

def state_bfs(start_state, expand, is_goal):
    q = deque([start_state])
    seen = {start_state}
    steps = 0
    while q:
        for _ in range(len(q)):
            state = q.popleft()
            if is_goal(state):
                return steps
            for nxt in expand(state):
                if nxt not in seen:
                    seen.add(nxt)
                    q.append(nxt)
        steps += 1
    return -1
```
- **代表 Notebook / 题目**：LC 1293、LC 773

### 7. 0-1 BFS
- **识别信号**：边权只有 0 或 1（免费/收费）。
- **模板要点**：
  - 使用 deque 模拟优先队列：代价 0 的邻居入队首，代价 1 的邻居入队尾。
  - dist 数组可直接 `new_dist < dist[nxt]` 时更新，保持最短路径性质。
  - 若存在更大权重请改用 Dijkstra。
- **模板**：
```python
from collections import deque

def zero_one_bfs(start, neighbors):
    dist = {start: 0}
    dq = deque([start])
    while dq:
        node = dq.popleft()
        for nxt, cost in neighbors(node):  # cost ∈ {0, 1}
            new_dist = dist[node] + cost
            if new_dist < dist.get(nxt, float('inf')):
                dist[nxt] = new_dist
                if cost == 0:
                    dq.appendleft(nxt)
                else:
                    dq.append(nxt)
    return dist
```
- **代表 Notebook / 题目**：LC 1368

### 8. 拓扑排序 / Kahn BFS
- **识别信号**：有向图依赖、课程安排、逐层剥叶子；无环图的层序结构。
- **模板要点**：
  - 构建邻接表与入度数组；初始队列包含所有入度 0 节点。
  - 弹出节点后遍历邻居减一入度，为 0 时入队；可在层级上统计完成轮数。
  - 若最终处理节点数少于 n，则存在环。
- **模板**：
```python
from collections import deque, defaultdict

def topo_bfs(n, edges):
    graph = defaultdict(list)
    indeg = [0] * n
    for u, v in edges:
        graph[u].append(v)
        indeg[v] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    while q:
        node = q.popleft()
        order.append(node)
        for nxt in graph[node]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                q.append(nxt)
    return order if len(order) == n else []
```
- **代表 Notebook / 题目**：LC 207、LC 210、LC 802

### 9. 二分 / 判可行 + BFS
- **识别信号**：问题需要“最大化/最小化”某阈值；BFS 用于固定阈值后的可行性判断。
- **模板要点**：外层二分或枚举阈值，内层套 BFS 判是否可达；可先用多源 BFS 生成距离场辅助判断。
- **代表题目**：1970、2812、1631 等（待补 Notebook）

## 练习路线
1. 树层序：102 → 107 → 103 → 515 → 637 → 662
2. 网格连通性：200 → 733 → 1091 → 490 → 934
3. 多源/反向：542 → 994 → 1765 → 130（围住区域）
4. 一般图：1971 → 841 → 279 → 909 → 815
5. 双向：127 → 752 → 433
6. 状态 BFS：773 → 1293 → 1345 → 847 → 864
7. 0-1 BFS：1368 → 2290
8. 拓扑：207 → 210 → 310 → 802
9. 二分 + BFS：1970 → 2812 → 1631

## 小技巧 Checklist
- 入队即标记 `visited`，防止重复。
- 网格 BFS 可就地染色节省空间。
- 双向 BFS 需扩展较小集合，遇到对端立即返回。
- 0-1 BFS 仅适用 0/1 权重；其他权重用 Dijkstra。
- 多源扩散题把所有源点放入初始队列。
- 二分 + BFS 时，先预处理“距离场”可帮助剪枝。

## TODO / 扩展
- 补充 `LC_2812`、`LC_2290` 等 Notebook，覆盖二分判定与 0-1 BFS 场景。
- 收集 BFS + Trie/加权变种案例（如 `LC_505`、`LC_126`）。
