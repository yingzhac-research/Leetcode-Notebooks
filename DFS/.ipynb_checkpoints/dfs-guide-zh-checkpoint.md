# DFS 刷题指南（中文）

本指南围绕深度优先搜索（Depth-First Search）核心思路，总结常见题型、模板与实战注意事项。编写新 Notebook 时，请先快速浏览本指南，明确题目所属的 DFS 套路，再回到 Notebook 中展开分析、代码与测试。

## 基本概念速览
- **核心机制**：沿一条分支搜索直到底部，再回溯换分支；适合枚举所有路径、组合、区域或状态空间。
- **搜索形态**：递归/显式栈、树/图/网格/状态压缩、全量枚举与剪枝加速等；根据结构选择合适的数据表示。
- **时间复杂度**：通常与搜索空间大小成正比，通过剪枝、记忆化、状态压缩可有效降低无效分支。
- **常见失误**：遗漏 visited 标记导致死循环、回溯阶段未撤销状态、递归深度过深未做栈限制、全局变量未重置。

### Python 实战要点
- 默认递归深度约 1000，如需深层递归可 `sys.setrecursionlimit`，或改用显式栈实现。
- 记得在回溯场景中撤销选择（pop/标记复位），并确保 `visited` 使用不可变键（如 tuple）或直接索引数组。
- 对网格 DFS 可预定义方向数组 `dirs = [(1,0), (-1,0), (0,1), (0,-1)]`，提高可读性并减少重复代码。
- 组合枚举常配合排序、跳过重复元素；状态压缩需要位运算熟悉 `mask`、`setbit`、`clearbit` 操作。

## 模式与模板

### 1. 树/图 DFS（递归框架）
**套路解析**：遍历树或图节点，对每个节点先处理当前状态，再递归访问子节点。利用 `visited` 集避免重复访问，典型于树遍历、连通分量计数、拓扑前驱等。
**伪代码模板**:
```python
def dfs(node, parent=None):
    if node in visited:
        return
    visited.add(node)
    process(node)
    for nei in graph[node]:
        if nei == parent:
            continue
        dfs(nei, node)
```
适用场景：树遍历、图连通性检查、桥/割点、拓扑检测。


### 2. 回溯搜索（决策树枚举）
**套路解析**：在每一层做一个决策，递归枚举所有可能的选择组合；进入下一层前记录当前状态，递归返回时撤销决策。用于排列组合、子集、数独等需要遍历整棵解空间树的题目。
**伪代码模板**:
```python
def backtrack(path, choices):
    if meet_goal(path):
        ans.append(path.copy())
        return
    for choice in choices:
        if invalid(choice):
            continue
        apply(choice)
        backtrack(path + [choice], updated_choices)
        undo(choice)
```
适用场景：排列、组合、子集、N 皇后、有效括号生成等。


### 3. 网格 DFS / Flood Fill
**套路解析**：在二维网格上从起点扩散，访问相邻单元并标记已访问，常用来统计岛屿、边界填充、形状识别。需注意边界与障碍条件，避免重复访问。
**伪代码模板**:
```python
def dfs(r, c):
    if not in_grid(r, c) or grid[r][c] != target:
        return
    grid[r][c] = mark
    for dr, dc in dirs:
        dfs(r + dr, c + dc)
```
适用场景：LC 200 岛屿数量、LC 695 岛屿最大面积、连通区域标号等。


### 4. 组合计数与剪枝
**套路解析**：配合排序和约束条件，在搜索过程中提前终止不可能满足目标的分支。核心在于根据题目条件设计剪枝策略，如剩余和不足、数量超限、字典序控制。
**伪代码模板**:
```python
def dfs(idx, current_sum):
    if current_sum > target:
        return
    if idx == len(nums):
        update_answer()
        return
    # 选择当前元素
    choose(idx)
    dfs(idx + 1, current_sum + nums[idx])
    undo(idx)
    # 不选择或跳过重复
    if skip_condition:
        return
    dfs(next_idx, current_sum)
```
适用场景：组合总和、子集和、K 数字之和等。


### 5. 记忆化搜索（DFS + DP）
**套路解析**：对重复子问题维护缓存，将 DFS 与动态规划结合，避免重复计算。常见于「游戏/博弈」「从状态到终点的最优值」等题目。
**伪代码模板**:
```python
from functools import lru_cache

@lru_cache(None)
def dfs(state):
    if base_case(state):
        return value
    best = default
    for nxt in next_states(state):
        best = combine(best, dfs(nxt))
    return best
```
适用场景：带约束的路径计数、Stone Game、记忆化括号匹配、单词拆分等。


### 6. 位压缩状态 DFS
**套路解析**：用整数位表示元素是否使用，将原本复杂的状态空间映射到位掩码，通过移位与与/或运算快速遍历可行状态。
**伪代码模板**:
```python
def dfs(mask, cost):
    if mask == (1 << n) - 1:
        update_answer(cost)
        return
    for nxt in range(n):
        if mask & (1 << nxt):
            continue
        dfs(mask | (1 << nxt), cost + transition(mask, nxt))
```
适用场景：旅行商近似、排列路径、最小团队覆盖、机器人收集奖励等。


### 7. 迭代 DFS / 显式栈
**套路解析**：当递归深度可能超限或需要细粒度控制访问顺序时，用栈手动模拟 DFS。可以灵活插入前序/后序处理逻辑。
**伪代码模板**:
```python
stack = [(start, False)]  # (node, visited_children)
while stack:
    node, seen = stack.pop()
    if not seen:
        process_pre(node)
        stack.append((node, True))
        for nei in reversed(graph[node]):
            if should_visit(nei):
                stack.append((nei, False))
    else:
        process_post(node)
```
适用场景：大树/图遍历、需要前后序双阶段处理、避免递归限制的题目。

## 现有题目对照表
当前目录尚未创建 Notebook。添加新题目时，请按下表格式补全：

| Notebook | 套路 | 关键要点 | 待补充内容 |
| --- | --- | --- | --- |
| （待补充） | （对应模板） | （核心思路） | （复习或扩展 TODO） |

## 复习与拓展建议
- **先识别结构**：判断题目属于树、图、网格或组合枚举，再选择对应模板，提高建模速度。
- **写下不变量**：在回溯、剪枝、记忆化题目中，先明确每层递归维护的状态信息与约束，避免遗漏撤销或重复计算。
- **调试策略**：优先在小规模数据上打印路径或状态，确认递归顺序与回溯逻辑正确，再推广至大输入。
- **与 BFS 对比**：遇到搜索题时先思考 BFS vs DFS 的优势，必要时考虑双向搜索或启发式（A*）等组合策略。
- **持续补全目录**：每新增 DFS 题目 Notebook，请同步在对照表登记套路、核心要点与后续跟进提醒，保持指南与实际笔记一致。
