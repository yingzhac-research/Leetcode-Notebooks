# Union-Find (并查集) 刷题指南（中文）

本指南围绕并查集（Disjoint Set Union, DSU）常见题型，帮助你从通用概念、典型模板到目录内 Notebook 快速定位解法。先掌握整体思维模型，再结合每题 Notebook 的详解复盘代码与测试。

## 基本概念速览
- **核心机制**：维护一组不相交的集合，支持快速合并（Union）和查询（Find）操作，通常用于解决连通性、等价关系、分组问题。
- **核心优化**：路径压缩（Path Compression）+ 按秩合并（Union by Rank/Size），使单次操作均摊时间复杂度接近 O(α(n))，α 为阿克曼函数的反函数，实际可视为常数。
- **常见维度**：连通分量计数、等价类合并、动态连通性判断、最小生成树、带权关系、反向操作（删除→倒序添加）。
- **高频陷阱**：忘记路径压缩导致退化、合并时未使用根节点、边界情况下的孤立节点处理、带权并查集的权值更新错误。

### Python 实战要点
- 并查集通常用数组 `parent[]` 和 `rank[]` 实现，父节点初始化为自己 `parent[i] = i`。
- `find(x)` 递归查找根节点并压缩路径：`parent[x] = find(parent[x])`。
- `union(x, y)` 合并时，先找到两个根节点，按秩合并避免树过深。
- 统计连通分量数：初始化 `count = n`，每次成功合并 `count -= 1`。
- 带权并查集：在 `parent[]` 基础上维护 `weight[]` 数组，合并时更新相对权值。

## 模式与模板

### 1. 基础连通性判断
**识别信号**：题目要求判断两个节点是否连通，或统计连通分量个数，通常涉及"朋友圈"、"省份"、"岛屿"等场景。

**套路解析**：使用标准并查集模板，初始化每个节点为独立集合，根据边或关系进行合并，最后统计连通分量数或查询两点是否在同一集合。

**伪代码模板**:
```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [1] * n
        self.count = n  # 连通分量数

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # 路径压缩
        return self.parent[x]

    def union(self, x, y):
        root_x, root_y = self.find(x), self.find(y)
        if root_x == root_y:
            return False
        # 按秩合并
        if self.rank[root_x] < self.rank[root_y]:
            root_x, root_y = root_y, root_x
        self.parent[root_y] = root_x
        self.rank[root_x] += self.rank[root_y]
        self.count -= 1
        return True

    def is_connected(self, x, y):
        return self.find(x) == self.find(y)
```
适用题目：`LC 547`, `LC 684`, `LC 990`, `LC 1971`

- 路径压缩是关键优化，将查找路径上的所有节点直接指向根节点。
- 按秩合并保证树的高度尽可能小，避免退化成链表。

### 2. 冗余连接检测
**识别信号**：题目给定一系列边，要求找出导致环的"多余边"，或判断图中是否存在环。

**套路解析**：遍历所有边，对每条边的两个节点尝试合并，如果发现两个节点已经连通（在同一集合），则当前边是冗余边。

**伪代码模板**:
```python
def find_redundant_connection(edges):
    uf = UnionFind(len(edges) + 1)
    for u, v in edges:
        if uf.is_connected(u, v):
            return [u, v]  # 冗余边
        uf.union(u, v)
    return []
```
适用题目：`LC 684`, `LC 685`, `LC 1559`

- 无向图中，第一条连接已连通节点的边即为答案。
- 有向图需要考虑入度和环检测的特殊情况。

### 3. 等价类合并 / 账户合并
**识别信号**：题目涉及等价关系（传递性），需要将具有等价关系的元素归为一组，如账户合并、字符串等价等。

**套路解析**：将等价关系视为"连接边"，通过并查集合并所有等价元素，最后遍历每个集合输出结果。

**伪代码模板**:
```python
def merge_accounts(accounts):
    email_to_id = {}
    uf = UnionFind(len(accounts))

    for i, account in enumerate(accounts):
        for email in account[1:]:
            if email in email_to_id:
                uf.union(i, email_to_id[email])
            else:
                email_to_id[email] = i

    # 按根节点分组
    groups = defaultdict(list)
    for email, user_id in email_to_id.items():
        root = uf.find(user_id)
        groups[root].append(email)

    return [[accounts[root][0]] + sorted(emails)
            for root, emails in groups.items()]
```
适用题目：`LC 721`, `LC 737`, `LC 839`, `LC 1061`, `LC 1202`

- 哈希表建立元素到集合ID的映射关系。
- 最后按根节点分组，输出每个等价类。

### 4. 最小生成树（Kruskal 算法）
**识别信号**：题目要求连接所有节点的最小代价，或构建最小生成树。

**套路解析**：将所有边按权值排序，从小到大遍历，使用并查集判断边的两端是否已连通，未连通则加入生成树。

**伪代码模板**:
```python
def minimum_spanning_tree(n, edges):
    edges.sort(key=lambda x: x[2])  # 按权值排序
    uf = UnionFind(n)
    total_cost = 0
    edge_count = 0

    for u, v, weight in edges:
        if uf.union(u, v):
            total_cost += weight
            edge_count += 1
            if edge_count == n - 1:  # n个节点需要n-1条边
                break

    return total_cost if edge_count == n - 1 else -1
```
适用题目：`LC 1584`, `LC 1168`, `LC 1319`, `LC 1489`

- Kruskal 算法的核心是贪心 + 并查集。
- 边数达到 n-1 时，所有节点已连通。

### 5. 网格连通性
**识别信号**：二维网格中判断连通区域，统计岛屿数量，或处理网格的动态变化（如砖块掉落）。

**套路解析**：将二维坐标映射为一维 ID（`id = i * cols + j`），对相邻的陆地/有效格子进行合并，统计连通分量。

**伪代码模板**:
```python
def grid_connectivity(grid):
    m, n = len(grid), len(grid[0])
    uf = UnionFind(m * n)

    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                idx = i * n + j
                # 向右和向下合并
                for di, dj in [(0, 1), (1, 0)]:
                    ni, nj = i + di, j + dj
                    if ni < m and nj < n and grid[ni][nj] == 1:
                        uf.union(idx, ni * n + nj)

    # 统计连通分量
    return len({uf.find(i * n + j) for i in range(m) for j in range(n) if grid[i][j] == 1})
```
适用题目：`LC 200`, `LC 305`, `LC 803`, `LC 959`, `LC 1254`

- 网格问题通常需要将 2D 坐标转为 1D 索引。
- 可以添加虚拟节点（如边界）简化边界处理。

### 6. 带权并查集
**识别信号**：题目涉及节点间的相对关系（如距离、比例），需要维护节点间的权值关系。

**套路解析**：在标准并查集基础上增加 `weight[]` 数组，表示节点到父节点的权值，路径压缩和合并时需要同步更新权值。

**伪代码模板**:
```python
class WeightedUnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.weight = [0] * n  # weight[x] 表示 x 到 parent[x] 的权值

    def find(self, x):
        if self.parent[x] != x:
            root = self.find(self.parent[x])
            self.weight[x] += self.weight[self.parent[x]]  # 路径压缩时累加权值
            self.parent[x] = root
        return self.parent[x]

    def union(self, x, y, w):
        # x 到 y 的权值为 w
        root_x, root_y = self.find(x), self.find(y)
        if root_x == root_y:
            return
        self.parent[root_x] = root_y
        # weight[root_x] = weight[y] - weight[x] + w
        self.weight[root_x] = self.weight[y] - self.weight[x] + w

    def get_weight(self, x, y):
        if self.find(x) != self.find(y):
            return None  # 不在同一集合
        return self.weight[x] - self.weight[y]
```
适用题目：`LC 399`, `LC 765`, `LC 952`, `LC 1627`

- 带权并查集的权值更新是难点，需要仔细推导公式。
- 常用于处理除法等价、倍数关系等问题。

### 7. 动态连通性 / 反向操作
**识别信号**：题目涉及删除操作后判断连通性，或逆序处理操作序列。

**套路解析**：由于并查集不支持高效删除，可以反向思考：将删除操作倒序变为添加操作，从最终状态逆推到初始状态。

**伪代码模板**:
```python
def dynamic_connectivity(operations):
    # 倒序处理删除操作
    operations.reverse()
    uf = UnionFind(n)
    results = []

    for op in operations:
        if op.type == "add":
            uf.union(op.u, op.v)
        results.append(uf.count)  # 记录当前连通分量数

    return results[::-1]  # 再反转回正序
```
适用题目：`LC 803`, `LC 1970`, `LC 2092`

- 删除边的问题可以转化为倒序添加边。
- 反向思维是并查集处理删除操作的经典技巧。

### 8. 连通性优化 / 虚拟节点
**识别信号**：题目涉及多个节点与某个"中心"或"边界"的连通性，直接建边会导致大量冗余。

**套路解析**：引入虚拟节点代表"中心"或"边界"，将所有相关节点连接到虚拟节点，减少边数和合并次数。

**伪代码模板**:
```python
def virtual_node_optimization(grid):
    m, n = len(grid), len(grid[0])
    uf = UnionFind(m * n + 1)  # +1 为虚拟边界节点
    virtual = m * n

    for i in range(m):
        for j in range(n):
            if is_boundary(i, j):
                uf.union(i * n + j, virtual)  # 连接到虚拟节点
            # 其他合并逻辑...

    # 检查某点是否与边界连通
    return uf.is_connected(target, virtual)
```
适用题目：`LC 130`, `LC 417`, `LC 1254`

- 虚拟节点可以大幅简化多源连通性问题。
- 边界、多个起点等场景都适用此技巧。

## 复杂度对比

| 操作 | 无优化 | 路径压缩 | 按秩合并 | 两者结合 |
| --- | --- | --- | --- | --- |
| Find | O(n) | O(log n) | O(log n) | O(α(n)) ≈ O(1) |
| Union | O(n) | O(log n) | O(log n) | O(α(n)) ≈ O(1) |
| 空间 | O(n) | O(n) | O(n) | O(n) |

## 识别并查集问题的关键特征

1. **连通性判断**：题目要求判断两个节点/元素是否在同一组/连通分量中。
2. **动态合并**：需要在遍历过程中动态合并集合，而不是一次性处理所有关系。
3. **等价关系传递**：如果 A~B 且 B~C，则 A~C，需要传递闭包。
4. **分组/聚类**：将元素按某种关系分为若干不相交的组。
5. **最小生成树**：Kruskal 算法的核心数据结构。
6. **避免环**：在构建图或树时，需要判断添加边是否会形成环。

## 经典变种与扩展

### 按秩合并 vs 按大小合并
- **按秩合并**：`rank[x]` 表示以 x 为根的树的高度，合并时矮树接到高树上。
- **按大小合并**：`size[x]` 表示以 x 为根的集合元素个数，合并时小集合接到大集合上。
- 两者效果相近，按大小合并更直观，且 `size` 信息本身常用于统计。

### 路径压缩的两种实现
```python
# 递归版本（推荐）
def find(self, x):
    if self.parent[x] != x:
        self.parent[x] = self.find(self.parent[x])
    return self.parent[x]

# 迭代版本
def find(self, x):
    root = x
    while self.parent[root] != root:
        root = self.parent[root]
    # 第二次遍历压缩路径
    while x != root:
        next_x = self.parent[x]
        self.parent[x] = root
        x = next_x
    return root
```

### 并查集 vs DFS/BFS
- **并查集优势**：支持动态合并，单次操作接近 O(1)，适合增量式构建连通性。
- **DFS/BFS 优势**：可以获取路径信息、遍历顺序，适合静态图的一次性遍历。
- **选择原则**：如果需要动态判断连通性或增量合并，选并查集；如果需要路径或遍历顺序，选 DFS/BFS。

## 常见陷阱与调试技巧

1. **忘记路径压缩**：导致 `find` 操作退化为 O(n)，在大数据下超时。
2. **合并时未找根**：直接 `union(x, y)` 而不是 `union(find(x), find(y))`，导致错误合并。
3. **初始化错误**：数组大小不足（忘记 +1）或索引从 1 开始时边界处理错误。
4. **带权并查集权值更新**：路径压缩时忘记累加权值，或合并时公式推导错误。
5. **孤立节点处理**：题目中可能存在孤立节点（无边），需要正确初始化连通分量数。
6. **二维网格索引**：二维坐标转一维时，行列搞反（应为 `i * cols + j`）。

## 刷题建议

1. **基础巩固**：先刷 LC 547, 684, 990 掌握标准模板。
2. **网格问题**：练习 LC 200, 305, 803 熟悉二维转一维技巧。
3. **最小生成树**：LC 1584, 1319 理解 Kruskal 算法。
4. **带权并查集**：LC 399, 952 掌握权值更新公式。
5. **综合应用**：LC 721, 839, 959 提升综合能力。
6. **反向操作**：LC 803, 1970 理解删除转添加的技巧。

## 本目录 Notebook 参考表

| 题号 | 题目 | 难度 | 核心模式 |
| --- | --- | --- | --- |
| LC 547 | Number of Provinces | Medium | 基础连通性 |
| LC 684 | Redundant Connection | Medium | 冗余连接检测 |
| LC 685 | Redundant Connection II | Hard | 有向图冗余边 |
| LC 721 | Accounts Merge | Medium | 等价类合并 |
| LC 737 | Sentence Similarity II | Medium | 等价关系传递 |
| LC 765 | Couples Holding Hands | Hard | 带权/复杂合并 |
| LC 803 | Bricks Falling When Hit | Hard | 反向操作 |
| LC 839 | Similar String Groups | Medium | 等价类合并 |
| LC 952 | Largest Component Size by Common Factor | Hard | 带权并查集 |
| LC 959 | Regions Cut By Slashes | Medium | 网格连通性 |
| LC 990 | Satisfiability of Equality Equations | Medium | 基础连通性 |
| LC 1061 | Lexicographically Smallest Equivalent String | Medium | 等价类合并 |
| LC 1202 | Smallest String With Swaps | Medium | 等价类合并 |
| LC 1319 | Number of Operations to Make Network Connected | Medium | 连通性 + 计数 |
| LC 1391 | Check if There is a Valid Path in a Grid | Hard | 网格连通性 |
| LC 1559 | Detect Cycles in 2D Grid | Medium | 网格环检测 |
| LC 1584 | Min Cost to Connect All Points | Medium | 最小生成树 |
| LC 1627 | Graph Connectivity With Threshold | Hard | 带权并查集 |
| LC 1971 | Find if Path Exists in Graph | Easy | 基础连通性 |
| LC 200 | Number of Islands | Medium | 网格连通性 |

---

**使用建议**：每个模式对应目录内的若干 Notebook，先看本 Guide 理解核心思路和模板，再打开对应 Notebook 查看完整代码、测试用例和详细复盘。祝刷题顺利！
