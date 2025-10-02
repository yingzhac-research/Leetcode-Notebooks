# Tree 刷题指南（中文）

本指南聚焦二叉树常见题型, 覆盖遍历,深度衡量,平衡性,BST 操作,结构比较与序列化等面试高频考点.通过模块化 Notebook 练习, 可以快速构建树结构题目的模板库与调试方法.

## 基本概念速览
- **核心能力**: 在递归结构上建立分治思维, 同时掌握栈,队列等辅助数据结构的配合方式.
- **常见前提**: 二叉树结点可为空, 需要谨慎处理 `None` 或空指针情况; BST 则具备有序性约束.
- **高频误区**:
  - 忽略返回值含义, 递归时只处理一侧导致答案丢失.
  - 遍历模板未做好初始化或终止条件, 产生死循环或重复访问.
  - 层序遍历中忘记锁定当前层大小, 导致不同层级混合.

### Python 实战要点
- 定义 `TreeNode` 时建议保持默认参数为 `None`, 方便构造测试树.
- 递归需要关注最大深度, 在链式树上可选择显式栈或尾递归规避栈溢出.
- BFS 使用 `collections.deque` 提升出队效率, 同时避免列表 `pop(0)` 的 O(n) 成本.
- Node 值可能重复, 处理 LCA 或子树比较时应基于节点引用而非仅比较数值.

## 树形题型与代表模板

### 1. 基础遍历模板
**适用情形**: 中序,先序,后序遍历获取节点顺序; BFS 层序输出.
**套路解读**: 递归与显式栈互为镜像, 队列负责层级控制.中序遍历可用于 BST 有序输出, 层序遍历可求每层统计.

**模板精要**:
```python
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
```

**代表 Notebook**:
- `Tree/LC_94_binary-tree-inorder-traversal.ipynb`
- `Tree/LC_102_binary-tree-level-order-traversal.ipynb`

### 2. 深度与高度度量
**适用情形**: 计算最大深度,最小深度或路径长度, 评估树的层级结构.
**套路解读**: 后序遍历返回高度值; 层序遍历可通过层数计数求深度.

**代表 Notebook**:
- `Tree/LC_104_maximum-depth-of-binary-tree.ipynb`
- `Tree/LC_543_diameter-of-binary-tree.ipynb`

### 3. 结构平衡与镜像操作
**适用情形**: 判断树是否平衡,生成镜像版本等.
**套路解读**: 自底向上合并高度与平衡状态; 镜像直接交换左右子树.

**代表 Notebook**:
- `Tree/LC_110_balanced-binary-tree.ipynb`
- `Tree/LC_226_invert-binary-tree.ipynb`

### 4. BST 专题
**适用情形**: 查询第 k 小,验证有序性,迭代器等.
**套路解读**: 中序遍历提供自然有序序列; 维护子树大小可实现 O(h) 级查询.

**代表 Notebook**:
- `Tree/LC_230_kth-smallest-element-in-a-bst.ipynb`

### 5. 最近公共祖先与结构比较
**适用情形**: 定位共享祖先,判断子树.
**套路解读**: 后序遍历收集左右子树信息; 子树比较需保证结构与数值一致.

**代表 Notebook**:
- `Tree/LC_236_lowest-common-ancestor-of-a-binary-tree.ipynb`
- `Tree/LC_572_subtree-of-another-tree.ipynb`

### 6. 树的序列化与恢复
**适用情形**: 将树结构持久化或跨进程传输.
**套路解读**: 层序遍历输出节点值, 使用占位符表示空指针; 反序列化按序重建指针关系.

**代表 Notebook**:
- `Tree/LC_297_serialize-and-deserialize-binary-tree.ipynb`

## 现有题目对照表
| Notebook | 套路 | 关键要点 | 待补充内容 |
| --- | --- | --- | --- |
| `Tree/LC_94_binary-tree-inorder-traversal.ipynb` | 迭代中序 | 显式栈模拟递归 | 可追加 Morris 遍历比较 |
| `Tree/LC_102_binary-tree-level-order-traversal.ipynb` | BFS 层序 | 队列锁定层级 | 补充层级统计与锯齿遍历链接 |
| `Tree/LC_104_maximum-depth-of-binary-tree.ipynb` | 深度递归 | 后序获取高度 | 展示迭代 BFS 求深度对照 |
| `Tree/LC_110_balanced-binary-tree.ipynb` | 自底向上平衡判定 | -1 哨兵提前终止 | 讨论尾递归或显式栈实现 |
| `Tree/LC_226_invert-binary-tree.ipynb` | 镜像操作 | 递归交换左右子树 | 增补迭代 BFS 写法示例 |
| `Tree/LC_230_kth-smallest-element-in-a-bst.ipynb` | BST 中序 + 计数 | 只遍历前 k 个节点 | 拓展子树大小维护的多次查询方案 |
| `Tree/LC_236_lowest-common-ancestor-of-a-binary-tree.ipynb` | 后序 LCA | 左右子树返回值合并 | 提示父指针或二进制提升写法 |
| `Tree/LC_297_serialize-and-deserialize-binary-tree.ipynb` | 层序序列化 | 占位符裁剪压缩 | 记录先序版本的优缺点 |
| `Tree/LC_543_diameter-of-binary-tree.ipynb` | 高度 + 直径 | nonlocal 累计最长路径 | 扩展记录路径节点列表 |
| `Tree/LC_572_subtree-of-another-tree.ipynb` | 递归匹配 | 同时比较值与结构 | 探讨哈希序列化降复杂度 |

## 学习建议
- **模板建库**: 将中序,层序,后序,LCA 等模板整理成独立函数, 在新题中快速复用.
- **调试技巧**: 使用层序 `serialize` 辅助打印树形, 便于验证递归逻辑是否正确.
- **复杂度分析**: 对每道题总结时间与空间复杂度, 特别是 BST 与 LCA 类题目中的 `O(h)` 与 `O(n)` 差异.
- **进阶拓展**: 尝试将本指南中的模板迁移到多叉树或带权树, 探索并查集,线段树等更复杂结构的联系.
