# Tree 刷题指南（中文）

本指南聚焦二叉树与二叉搜索树（BST）常见题型，覆盖遍历、深度衡量、平衡性验证、BST 操作、结构比较与序列化等面试高频考点。通过模块化 Notebook 练习，快速构建树结构题目的模板库与调试方法。

## 基本概念速览
- **核心能力**：在递归结构上建立分治思维，同时掌握栈、队列等辅助数据结构的配合方式。
- **常见前提**：二叉树节点可为空，需要谨慎处理 `None` 或空指针情况；BST 具备左子树 < 根 < 右子树的有序性约束。
- **高频误区**：
  - 忽略返回值含义，递归时只处理一侧导致答案丢失。
  - 遍历模板未做好初始化或终止条件，产生死循环或重复访问。
  - 层序遍历中忘记锁定当前层大小，导致不同层级混合。
  - BST 题目中混淆"中序遍历有序"与"每次比较大小"的适用场景。

### Python 实战要点
- 定义 `TreeNode` 时建议保持默认参数为 `None`，方便构造测试树。
- 递归需要关注最大深度，在链式树上可选择显式栈或尾递归规避栈溢出。
- BFS 使用 `collections.deque` 提升出队效率，避免列表 `pop(0)` 的 O(n) 成本。
- 节点值可能重复，处理 LCA 或子树比较时应基于节点引用而非仅比较数值。
- 使用 `nonlocal` 或类成员变量在递归中维护全局答案（如最大路径和、直径）。

## 树形题型与模板

### 1. 基础遍历：前序 / 中序 / 后序 / 层序
**识别信号**：题目要求按特定顺序输出节点值、验证遍历序列、构造二叉树或统计每层信息。
**套路解析**：
- **前序**：根 → 左 → 右，适合自顶向下传递信息（如路径、深度）。
- **中序**：左 → 根 → 右，BST 中序遍历得到有序序列。
- **后序**：左 → 右 → 根，适合自底向上合并子树信息（如高度、子树和）。
- **层序**：使用队列按层遍历，适合求层级统计、最短路径。

**伪代码模板**：
```python
# 中序遍历（迭代）
def inorder(root):
    stack, current, result = [], root, []
    while current or stack:
        while current:
            stack.append(current)
            current = current.left
        node = stack.pop()
        result.append(node.val)
        current = node.right
    return result

# 层序遍历
from collections import deque
def level_order(root):
    if not root:
        return []
    queue = deque([root])
    levels = []
    while queue:
        level_size = len(queue)
        level = []
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        levels.append(level)
    return levels
```

**适用题目**：
- `LC 94` Binary Tree Inorder Traversal
- `LC 102` Binary Tree Level Order Traversal
- `LC 103` Binary Tree Zigzag Level Order Traversal
- `LC 144` Binary Tree Preorder Traversal
- `LC 145` Binary Tree Postorder Traversal

### 2. 深度与高度度量
**识别信号**：题目要求计算树的最大/最小深度、路径长度、节点到根的距离或树的直径。
**套路解析**：
- **最大深度**：后序递归，`max(左子树深度, 右子树深度) + 1`。
- **最小深度**：需考虑叶子节点定义（左右子树都为空），BFS 更优。
- **直径**：在求高度的同时维护全局最大值 `左高度 + 右高度`。
- **路径和**：前序遍历传递累积和，叶子节点判断是否等于目标。

**伪代码模板**：
```python
# 最大深度
def max_depth(root):
    if not root:
        return 0
    return max(max_depth(root.left), max_depth(root.right)) + 1

# 直径（需要 nonlocal 维护答案）
def diameter(root):
    ans = 0
    def height(node):
        nonlocal ans
        if not node:
            return 0
        left = height(node.left)
        right = height(node.right)
        ans = max(ans, left + right)
        return max(left, right) + 1
    height(root)
    return ans

# 路径和
def has_path_sum(root, target):
    if not root:
        return False
    if not root.left and not root.right:
        return root.val == target
    target -= root.val
    return has_path_sum(root.left, target) or has_path_sum(root.right, target)
```

**适用题目**：
- `LC 104` Maximum Depth of Binary Tree
- `LC 111` Minimum Depth of Binary Tree
- `LC 112` Path Sum
- `LC 113` Path Sum II
- `LC 543` Diameter of Binary Tree
- `LC 124` Binary Tree Maximum Path Sum

### 3. 结构验证：平衡性 / 对称性 / 完全性
**识别信号**：题目要求判断树是否平衡、对称、完全二叉树或相同结构。
**套路解析**：
- **平衡树**：自底向上返回高度，若左右子树高度差 > 1 则返回 -1 标记失败。
- **对称树**：递归比较左子树的左与右子树的右、左子树的右与右子树的左。
- **相同树**：同时递归两棵树，比较当前节点值与左右子树结构。
- **完全二叉树**：层序遍历，遇到第一个空节点后不应再有非空节点。

**伪代码模板**：
```python
# 平衡树
def is_balanced(root):
    def height(node):
        if not node:
            return 0
        left = height(node.left)
        right = height(node.right)
        if left == -1 or right == -1 or abs(left - right) > 1:
            return -1
        return max(left, right) + 1
    return height(root) != -1

# 对称树
def is_symmetric(root):
    def mirror(left, right):
        if not left and not right:
            return True
        if not left or not right:
            return False
        return (left.val == right.val and
                mirror(left.left, right.right) and
                mirror(left.right, right.left))
    return mirror(root, root) if root else True

# 相同树
def is_same_tree(p, q):
    if not p and not q:
        return True
    if not p or not q or p.val != q.val:
        return False
    return is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)
```

**适用题目**：
- `LC 100` Same Tree
- `LC 101` Symmetric Tree
- `LC 110` Balanced Binary Tree
- `LC 958` Check Completeness of a Binary Tree

### 4. 树的变换：翻转 / 镜像 / 展平
**识别信号**：题目要求翻转树、生成镜像、将树展平为链表或修改树结构。
**套路解析**：
- **翻转**：递归交换每个节点的左右子树。
- **展平为链表**：前序遍历记录节点顺序，再依次连接右指针；或用后序遍历原地修改。
- **修改结构**：通常需要在递归过程中保存父节点或前驱节点信息。

**伪代码模板**：
```python
# 翻转二叉树
def invert_tree(root):
    if not root:
        return None
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root

# 展平为链表（前序）
def flatten(root):
    def dfs(node):
        if not node:
            return None
        left_tail = dfs(node.left)
        right_tail = dfs(node.right)
        if left_tail:
            left_tail.right = node.right
            node.right = node.left
            node.left = None
        return right_tail or left_tail or node
    dfs(root)
```

**适用题目**：
- `LC 114` Flatten Binary Tree to Linked List
- `LC 226` Invert Binary Tree

### 5. BST 专题：查找 / 插入 / 删除 / 验证
**识别信号**：题目明确为 BST，要求利用有序性进行查找、验证、查询第 K 小、范围和等操作。
**套路解析**：
- **验证 BST**：中序遍历结果应严格递增；或递归传递上下界。
- **查找/插入**：利用大小关系只遍历一侧子树。
- **删除**：找到目标后处理三种情况（叶子、单子树、双子树）。
- **第 K 小**：中序遍历计数到 K 即返回。
- **范围和**：剪枝访问，只在 [L, R] 范围内累加。

**伪代码模板**：
```python
# 验证 BST（递归带上下界）
def is_valid_bst(root, min_val=float('-inf'), max_val=float('inf')):
    if not root:
        return True
    if not (min_val < root.val < max_val):
        return False
    return (is_valid_bst(root.left, min_val, root.val) and
            is_valid_bst(root.right, root.val, max_val))

# 第 K 小元素
def kth_smallest(root, k):
    stack = []
    current = root
    while True:
        while current:
            stack.append(current)
            current = current.left
        current = stack.pop()
        k -= 1
        if k == 0:
            return current.val
        current = current.right

# BST 插入
def insert_into_bst(root, val):
    if not root:
        return TreeNode(val)
    if val < root.val:
        root.left = insert_into_bst(root.left, val)
    else:
        root.right = insert_into_bst(root.right, val)
    return root
```

**适用题目**：
- `LC 98` Validate Binary Search Tree
- `LC 230` Kth Smallest Element in a BST
- `LC 450` Delete Node in a BST
- `LC 700` Search in a Binary Search Tree
- `LC 701` Insert into a Binary Search Tree
- `LC 938` Range Sum of BST

### 6. 最近公共祖先（LCA）
**识别信号**：题目要求找两个节点的最近公共祖先，可能是普通二叉树或 BST。
**套路解析**：
- **普通二叉树**：后序遍历，若左右子树各包含一个目标则当前节点为 LCA。
- **BST**：利用有序性，若 p、q 分别在当前节点两侧则为 LCA，否则向同一侧递归。

**伪代码模板**：
```python
# 普通二叉树 LCA
def lowest_common_ancestor(root, p, q):
    if not root or root == p or root == q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root
    return left or right

# BST LCA
def lca_bst(root, p, q):
    if p.val < root.val > q.val:
        return lca_bst(root.left, p, q)
    if p.val > root.val < q.val:
        return lca_bst(root.right, p, q)
    return root
```

**适用题目**：
- `LC 235` Lowest Common Ancestor of a Binary Search Tree
- `LC 236` Lowest Common Ancestor of a Binary Tree

### 7. 子树与结构比较
**识别信号**：题目要求判断一棵树是否是另一棵树的子树、比较两棵树的结构、或验证序列化相等性。
**套路解析**：
- **子树判断**：遍历主树每个节点，判断以该节点为根的子树是否与目标树相同。
- **结构比较**：递归同时遍历两棵树，比较节点值与左右子树结构。
- **序列化哈希**：将子树序列化为字符串，通过哈希快速比较（需处理空节点占位）。

**伪代码模板**：
```python
# 判断子树
def is_subtree(root, subRoot):
    if not root:
        return False
    if is_same_tree(root, subRoot):
        return True
    return is_subtree(root.left, subRoot) or is_subtree(root.right, subRoot)

def is_same_tree(p, q):
    if not p and not q:
        return True
    if not p or not q or p.val != q.val:
        return False
    return is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)
```

**适用题目**：
- `LC 100` Same Tree
- `LC 572` Subtree of Another Tree

### 8. 树的序列化与反序列化
**识别信号**：题目要求将树转换为字符串或数组形式存储，并能从序列化结果恢复原树。
**套路解析**：
- **层序序列化**：使用队列遍历，空节点用占位符（如 `null`）表示。
- **前序序列化**：递归输出 `根,左,右`，空节点用占位符。
- **反序列化**：按相同顺序解析字符串，重建节点和指针关系。

**伪代码模板**：
```python
from collections import deque

# 层序序列化
def serialize(root):
    if not root:
        return ""
    queue = deque([root])
    result = []
    while queue:
        node = queue.popleft()
        if node:
            result.append(str(node.val))
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append("null")
    return ",".join(result)

# 层序反序列化
def deserialize(data):
    if not data:
        return None
    values = data.split(",")
    root = TreeNode(int(values[0]))
    queue = deque([root])
    i = 1
    while queue:
        node = queue.popleft()
        if values[i] != "null":
            node.left = TreeNode(int(values[i]))
            queue.append(node.left)
        i += 1
        if values[i] != "null":
            node.right = TreeNode(int(values[i]))
            queue.append(node.right)
        i += 1
    return root
```

**适用题目**：
- `LC 297` Serialize and Deserialize Binary Tree
- `LC 449` Serialize and Deserialize BST

### 9. 树形 DP：路径和 / 打家劫舍 / 后序合并
**识别信号**：题目要求统计路径和、最大路径、树上选点最大收益等优化问题。
**套路解析**：
- **路径和**：递归维护从根到当前节点的路径信息，叶子节点判断。
- **最大路径和**：后序遍历返回单边最大贡献，全局维护"左+根+右"的最大值。
- **打家劫舍**：每个节点返回"选"和"不选"两种状态的最优解。

**伪代码模板**：
```python
# 最大路径和
def max_path_sum(root):
    max_sum = float('-inf')
    def dfs(node):
        nonlocal max_sum
        if not node:
            return 0
        left = max(0, dfs(node.left))
        right = max(0, dfs(node.right))
        max_sum = max(max_sum, left + node.val + right)
        return node.val + max(left, right)
    dfs(root)
    return max_sum

# 打家劫舍 III
def rob(root):
    def dfs(node):
        if not node:
            return (0, 0)  # (不选, 选)
        left = dfs(node.left)
        right = dfs(node.right)
        rob_current = node.val + left[0] + right[0]
        not_rob = max(left) + max(right)
        return (not_rob, rob_current)
    return max(dfs(root))
```

**适用题目**：
- `LC 112` Path Sum
- `LC 113` Path Sum II
- `LC 124` Binary Tree Maximum Path Sum
- `LC 337` House Robber III
- `LC 543` Diameter of Binary Tree

## 现有题目对照表
| Notebook | 套路 | 关键要点 | 待补充内容 |
| --- | --- | --- | --- |
| `Tree/LC_94_binary-tree-inorder-traversal.ipynb` | 迭代中序遍历 | 显式栈模拟递归，左链压栈 | 追加 Morris 遍历 O(1) 空间方案 |
| `Tree/LC_100_same-tree.ipynb` | 结构比较 | 递归同步遍历两树比较值与结构 | 补充迭代 BFS 双队列写法 |
| `Tree/LC_101_symmetric-tree.ipynb` | 对称性验证 | 镜像递归比较左右子树 | 加入迭代栈实现对比 |
| `Tree/LC_102_binary-tree-level-order-traversal.ipynb` | 层序遍历 | 队列锁定层级，逐层输出 | 补充自底向上、锯齿形遍历链接 |
| `Tree/LC_104_maximum-depth-of-binary-tree.ipynb` | 深度递归 | 后序获取左右子树高度 | 展示迭代 BFS 求深度方案 |
| `Tree/LC_110_balanced-binary-tree.ipynb` | 平衡判定 | 自底向上返回 -1 哨兵提前终止 | 讨论尾递归或显式栈实现 |
| `Tree/LC_111_minimum-depth-of-binary-tree.ipynb` | 最小深度 | BFS 首次遇叶子即返回 | 对比递归需处理单子树情况 |
| `Tree/LC_112_path-sum.ipynb` | 路径和 | 前序传递累积和，叶子判断 | 扩展到返回所有路径方案 |
| `Tree/LC_226_invert-binary-tree.ipynb` | 镜像操作 | 递归交换左右子树 | 增补迭代 BFS 写法示例 |
| `Tree/LC_230_kth-smallest-element-in-a-bst.ipynb` | BST 中序 + 计数 | 只遍历前 k 个节点即返回 | 拓展子树大小维护的多次查询方案 |
| `Tree/LC_235_lowest-common-ancestor-of-a-binary-search-tree.ipynb` | BST LCA | 利用有序性判断分支方向 | 补充迭代写法节省递归栈 |
| `Tree/LC_236_lowest-common-ancestor-of-a-binary-tree.ipynb` | 后序 LCA | 左右子树返回值合并找祖先 | 提示父指针或二进制提升写法 |
| `Tree/LC_297_serialize-and-deserialize-binary-tree.ipynb` | 层序序列化 | 占位符裁剪压缩，队列重建 | 记录前序版本的优缺点 |
| `Tree/LC_543_diameter-of-binary-tree.ipynb` | 高度 + 直径 | nonlocal 累计最长路径 | 扩展记录路径节点列表 |
| `Tree/LC_572_subtree-of-another-tree.ipynb` | 子树匹配 | 遍历主树每节点判断相同性 | 探讨哈希序列化降复杂度 |
| `Tree/LC_98_validate-binary-search-tree.ipynb` | BST 验证 | 递归传递上下界或中序递增 | 对比迭代中序与递归方案 |
| `Tree/LC_114_flatten-binary-tree-to-linked-list.ipynb` | 展平为链表 | 前序遍历原地修改右指针 | 后序遍历更优雅的写法 |
| `Tree/LC_124_binary-tree-maximum-path-sum.ipynb` | 树形 DP | 后序返回单边贡献，全局维护最大值 | 加入负值节点的剪枝讨论 |

## 复习与拓展建议
- **模板建库**：将中序、层序、后序、LCA、树形 DP 等模板整理成独立函数，在新题中快速复用。
- **调试技巧**：使用层序 `serialize` 辅助打印树形，便于验证递归逻辑是否正确；手绘小树模拟递归调用栈。
- **复杂度分析**：对每道题总结时间与空间复杂度，特别是 BST 与 LCA 类题目中的 O(h) 与 O(n) 差异。
- **递归 vs 迭代**：熟练掌握递归写法后，尝试用显式栈改写为迭代，应对面试中的 follow-up。
- **进阶拓展**：
  - Morris 遍历实现 O(1) 空间的中序遍历。
  - 线段树、树状数组等高级树形结构。
  - 多叉树、Trie、并查集等结构的联系。
  - 树上倍增、树链剖分等竞赛算法（MLE 面试较少涉及）。

## 练习路线
1. **基础遍历**：94 → 102 → 144 → 145 → 103
2. **深度与路径**：104 → 111 → 112 → 113 → 543 → 124
3. **结构验证**：100 → 101 → 110 → 958
4. **树的变换**：226 → 114
5. **BST 专题**：98 → 700 → 701 → 230 → 450 → 938
6. **LCA**：235 → 236
7. **子树与比较**：100 → 572
8. **序列化**：297 → 449
9. **树形 DP**：112 → 113 → 124 → 337 → 543

## 小技巧 Checklist
- 递归前先判空，避免 NoneType 错误。
- 后序遍历适合自底向上合并信息（高度、和、直径）。
- 前序遍历适合自顶向下传递信息（路径、深度、边界）。
- 中序遍历是 BST 的有序输出，适合验证、查找第 K 小。
- 层序遍历用队列，记得锁定层大小 `for _ in range(len(queue))`。
- 使用 `nonlocal` 或类成员变量维护全局答案，避免返回值传递复杂。
- BST 题目优先考虑利用有序性剪枝，避免遍历全树。
- LCA 题目注意返回节点引用而非值，处理空节点边界。
