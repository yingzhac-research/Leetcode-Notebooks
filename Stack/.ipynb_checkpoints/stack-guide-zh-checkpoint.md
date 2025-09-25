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
**适用场景**：括号/标签是否成对出现、合法子串长度、最少修改次数等。

**通用模板**：
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
**适用场景**：处理嵌套结构、反复合并字符串、模拟文件路径指令。

**通用模板**：
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
**适用场景**：中缀/后缀表达式求值、处理运算符优先级、支持括号嵌套。

**通用模板（中缀）**：
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
**适用场景**：寻找下一次满足条件的位置或值，常见于温度、股票、循环数组等。

**通用模板**：
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
**适用场景**：直方图最大矩形、矩阵最大全 1 子矩形、保持字典序最小的数。

**通用模板**（直方图）：
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
**适用场景**：函数调用栈时间统计、相互碰撞、手工实现撤销机制等。

**通用模板**：
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
**适用场景**：在常规栈操作基础上增加“获取最小值”“受控遍历”等。

**经典题目**：
- `LC 155 Min Stack`
- `LC 173 Binary Search Tree Iterator`

**要点提醒**：
- Min Stack 可通过双栈或在单栈中存储 `(value, current_min)` 避免额外空间。
- BST 迭代器需要懒加载：先沿左链压栈，访问节点后再处理右子树。

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

