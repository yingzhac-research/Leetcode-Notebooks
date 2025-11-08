# Stack 刷题指南（中文）

本指南聚焦面试中高频的栈（Stack）题型，梳理基础概念、常见套路与经典题目。建议先搭建对栈的整体认知，再配合对应 Notebook 深入理解细节、形成可复用的模板。

## 基本概念速览
- **核心能力**：栈遵循 LIFO（后进先出），适合处理“最近一次未完成任务”或“嵌套结构展开”问题。
- **常见操作**：`push` 入栈、`pop` 出栈、`peek` 取顶元素。部分题目要求扩展接口（如获取最小值、支持可重复遍历等）。
- **典型应用**：括号匹配、表达式求值、递归改写为迭代、时间区间模拟、单调栈求最值等。
- **失误集中地**：
  - 忘记在遍历结束后清理或结算剩余栈元素（如单调栈处理 sentinel）。
  - 对多栈/辅助栈的状态维护不足（如最小值栈与主栈不同步）。
  - 在表达式解析中忽略空格、符号优先级或负号边界。

### Python 实战要点
- 使用列表 `list` 作为栈，`append`/`pop` 均摊 O(1)。
- `collections.deque` 适合双端队列需求；若只做栈操作，`list` 更直接。
- 遇到需要同时维护值与索引的场景，可在栈中存储二元组 `(value, index)`。
- 针对单调栈，常在遍历末尾追加虚拟元素（补位 sentinel）触发清算逻辑。

## 栈套路与模板

### 1. 括号匹配与结构有效性
**识别信号**：题目涉及括号、标签配对验证，或需要计算合法嵌套结构的长度、得分、最少补全次数。
**套路解析**：使用栈记录尚未匹配的左括号或索引，遇到右括号时检查栈顶能否配对；若需要统计长度或得分，可在栈中存储索引或中间结果。

**伪代码模板**：
```python
stack = []
for char in sequence:
    if is_open(char):
        stack.append(char)
    elif stack and matches(stack[-1], char):
        stack.pop()
    else:
        handle_invalid_state()
post_process(stack)
```

**经典题目**：
- `LC 20 Valid Parentheses`
- `LC 32 Longest Valid Parentheses`
- `LC 856 Score of Parentheses`
- `LC 921 Minimum Add to Make Parentheses Valid`

**要点提醒**：
- 对于“最长/分数”类题目，栈里存索引或阶段得分以便回溯。
- 合法性校验题若允许“删除/补齐”，需额外记录待处理数量。

### 2. 嵌套字符串解码与路径简化
**识别信号**：题目包含嵌套括号编码、文件路径简化、递归展开字符串、相邻字符消除等场景。
**套路解析**：栈保存"进入嵌套前的状态"，遇到开括号/新层级时压栈，遇到闭括号/完成信号时出栈并合并结果；路径简化时用栈维护有效目录层级。

**伪代码模板**：
```python
stack = []
current = init_state()
for token in tokens:
    if triggers_new_context(token):
        stack.append(current)
        current = reset_state(token)
    elif is_closing(token):
        current = merge_with_parent(stack.pop(), current, token)
    else:
        current = update_state(current, token)
return finalize(current)
```

**经典题目**：
- `LC 71 Simplify Path`
- `LC 394 Decode String`
- `LC 1047 Remove All Adjacent Duplicates in String`

**要点提醒**：
- 适时压栈保存“之前的部分+当前倍数/层级”，出栈时统一合并。
- 在路径化简中注意忽略空目录、`.`，遇到 `..` 时兜底判断栈非空。

### 3. 表达式解析与求值
**识别信号**：题目要求计算表达式结果，涉及四则运算、运算符优先级、括号嵌套或后缀表达式。
**套路解析**：后缀表达式直接用栈存操作数，遇运算符出栈计算；中缀表达式需双栈分别存操作数和运算符，按优先级控制出栈顺序；遇括号时运算符栈先压入左括号作为屏障。

**伪代码模板（中缀）**：
```python
operands, operators = [], []
for token in expression:
    if token.isdigit():
        operands.append(token_value(token))
    elif token in '+-*/':
        while operators and priority(operators[-1]) >= priority(token):
            apply_operator(operands, operators.pop())
        operators.append(token)
    elif token == '(':
        operators.append(token)
    else:  # token == ')'
        while operators[-1] != '(':
            apply_operator(operands, operators.pop())
        operators.pop()
while operators:
    apply_operator(operands, operators.pop())
return operands[-1]
```

**经典题目**：
- `LC 150 Evaluate Reverse Polish Notation`
- `LC 224 Basic Calculator`
- `LC 227 Basic Calculator II`

**要点提醒**：
- 处理一元负号时，可在遇到 `-` 前判断是否在首位或紧随 `(`。
- 后缀表达式直接用栈存操作数，遇到运算符就弹出两个数计算。

### 4. 单调栈：下一个更大/更小元素
**识别信号**：题目要求找"下一个更大/更小的元素"、"前面有多少个连续小于等于当前值"、或在序列中寻找第一个满足大小关系的位置。
**套路解析**：维护单调递减（找更大）或单调递增（找更小）的栈，存储索引；遍历时若当前元素破坏单调性，则弹出栈顶并记录答案，最后将当前元素索引入栈。

**伪代码模板**：
```python
stack = []  # 维护单调性（通常存索引）
for idx, value in enumerate(sequence):
    while stack and value_compare(value, sequence[stack[-1]]):
        prev_idx = stack.pop()
        answer[prev_idx] = idx
    stack.append(idx)
handle_remaining(stack)
```

**经典题目**：
- `LC 496 Next Greater Element I`
- `LC 503 Next Greater Element II`
- `LC 739 Daily Temperatures`
- `LC 901 Online Stock Span`

**要点提醒**：
- 循环数组常用“遍历两倍长度”技巧；对 stock span 需要在栈中存频次或累计跨度。
- 处理严格/非严格比较条件时注意栈内元素的出栈时机。

### 5. 单调栈：区间面积与贪心删减
**识别信号**：题目涉及直方图面积、雨水容量、矩阵最大矩形，或需要贪心删除 K 个数字保持字典序最小。
**套路解析**：单调栈维护递增序列，栈中元素作为"可能的左边界"；遇到更小值时触发结算（计算以栈顶为高度的矩形面积或水量）；删数字题则维护递增栈保证字典序，遇到更小数字时弹出栈顶直到满足删除数量。

**伪代码模板（直方图）**：
```python
stack = []
for i, h in enumerate(heights + [0]):  # 末尾补 0 触发结算
    while stack and heights[stack[-1]] > h:
        height = heights[stack.pop()]
        left = stack[-1] if stack else -1
        width = i - left - 1
        best = max(best, height * width)
    stack.append(i)
```

**经典题目**：
- `LC 42 Trapping Rain Water`
- `LC 84 Largest Rectangle in Histogram`
- `LC 85 Maximal Rectangle`
- `LC 402 Remove K Digits`

**要点提醒**：
- 雨水题需要根据左/右界高度决定装水量，可用双指针或单调栈方案。
- `Remove K Digits` 利用单调递增栈维护当前最优字典序，遍历结束后若仍需删除则从尾部裁剪。

### 6. 栈模拟系统过程与事件驱动
**识别信号**：题目模拟函数调用日志、时间统计、行星碰撞、撤销/重做机制等动态事件处理。
**套路解析**：栈保存当前活跃的上下文或实体，遇到"开始"事件入栈，遇到"结束"事件出栈并结算时间或状态；碰撞类问题需比较栈顶与新元素的方向/质量，决定是否抵消或覆盖。

**伪代码模板**：
```python
stack = []
for event in events:
    if starts_new_scope(event):
        stack.append(event_state(event))
    else:
        state = stack.pop()
        update_answer(state, event)
        if stack:
            adjust_parent(stack[-1], state)
```

**经典题目**：
- `LC 636 Exclusive Time of Functions`
- `LC 735 Asteroid Collision`

**要点提醒**：
- 处理函数日志时需要跟踪上一个时间戳或当前执行时间段。
- 碰撞问题要仔细讨论质量相等、方向相同等边界条件。

### 7. 栈增强数据结构
**识别信号**：题目要求在 O(1) 时间内获取栈的最小值、最大值，或需要按特定顺序迭代访问栈元素（如 BST 中序遍历）。
**套路解析**：Min/Max Stack 通过辅助栈或在每个元素中附加当前极值信息实现 O(1) 查询；BST 迭代器使用栈模拟中序遍历的递归过程，懒加载左链以节省空间。

**经典题目**：
- `LC 155 Min Stack`
- `LC 173 Binary Search Tree Iterator`

**要点提醒**：
- Min Stack 可通过双栈或在单栈中存储 `(value, current_min)` 避免额外空间。
- BST 迭代器需要懒加载：先沿左链压栈，访问节点后再处理右子树。

## 现有题目对照表
| Notebook | 套路 | 关键要点 | 待补充内容 |
| --- | --- | --- | --- |
| `Stack/LC_20_valid-parentheses.ipynb` | 括号匹配栈 | 一次扫描用栈匹配括号，空栈即合法 | 补充流式输入校验示例 |
| `Stack/LC_32_longest-valid-parentheses.ipynb` | 栈索引界限 | 栈存索引测距，sentinel 处理左界 | 增加与 DP 写法的复杂度对比 |
| `Stack/LC_71_simplify-path.ipynb` | 栈规范化路径 | 栈记录目录层级，忽略 `.`/`..` | 可补充 Windows 路径变体讨论 |
| `Stack/LC_150_evaluate-reverse-polish-notation.ipynb` | 栈求值 | 栈保存操作数，遇运算符即弹出计算 | 增加溢出及除零防护策略 |
| `Stack/LC_394_decode-string.ipynb` | 栈解码字符串 | 栈存前缀与重复次数，遇 `]` 回退 | 可附上大倍数下的性能数据 |
| `Stack/LC_496_next-greater-element-i.ipynb` | 单调栈找下一个更大值 | 维护递减栈映射首个更大数 | 扩展到含重复值的处理 |
| `Stack/LC_42_trapping-rain-water.ipynb` | 单调栈面积 | 栈存柱子索引计算被围高度 | 对比双指针做法的优劣 |
| `Stack/LC_901_online-stock-span.ipynb` | 栈模拟系统过程 | 栈累计跨度，保证摊还 O(1) | 添加批量调用的性能测试 |
| `Stack/LC_155_min-stack.ipynb` | 栈增强数据结构 | 元组存当前最小值，O(1) 查询 | 讨论双栈 vs. 单栈方案差异 |
| `Stack/LC_173_binary-search-tree-iterator.ipynb` | 栈惰性遍历 | 延迟压栈左链，迭代输出 BST 有序值 | 可补充反向迭代器实现 |

## 学习建议与配套 Notebook
- **模板练习**：优先熟悉上述 7 类模板，先以伪代码保证过程正确，再动手实现。
- **逐题演练**：本目录下的 Notebook 覆盖了每种套路的典型题目：
  - 括号类：`Stack/LC_20_valid-parentheses.ipynb`, `Stack/LC_32_longest-valid-parentheses.ipynb`, `Stack/LC_856_score-of-parentheses.ipynb`, `Stack/LC_921_minimum-add-to-make-parentheses-valid.ipynb`
  - 嵌套/字符串栈：`Stack/LC_71_simplify-path.ipynb`, `Stack/LC_394_decode-string.ipynb`, `Stack/LC_1047_remove-all-adjacent-duplicates-in-string.ipynb`
  - 表达式解析：`Stack/LC_150_evaluate-reverse-polish-notation.ipynb`, `Stack/LC_224_basic-calculator.ipynb`, `Stack/LC_227_basic-calculator-ii.ipynb`
  - 单调栈（下一更大）：`Stack/LC_496_next-greater-element-i.ipynb`, `Stack/LC_503_next-greater-element-ii.ipynb`, `Stack/LC_739_daily-temperatures.ipynb`, `Stack/LC_901_online-stock-span.ipynb`
  - 单调栈（面积/删数）：`Stack/LC_42_trapping-rain-water.ipynb`, `Stack/LC_84_largest-rectangle-in-histogram.ipynb`, `Stack/LC_85_maximal-rectangle.ipynb`, `Stack/LC_402_remove-k-digits.ipynb`
  - 系统模拟：`Stack/LC_636_exclusive-time-of-functions.ipynb`, `Stack/LC_735_asteroid-collision.ipynb`
  - 增强数据结构：`Stack/LC_155_min-stack.ipynb`, `Stack/LC_173_binary-search-tree-iterator.ipynb`
- **交叉复盘**：在 Notebook 中对照 `Complexity Trade-off Table` 与 `Follow-up Variants`，理解同一套路在不同题目中的微调方式。
- **持续扩充**：若遇到新的栈题型（例如“队列模拟栈”“状态机+回撤”），更新本指南并补充 Notebook，保持仓库体系一致。

