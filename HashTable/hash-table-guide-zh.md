# Hash Table 刷题指南（中文）

本指南聚焦面试中常见的哈希表题型，帮助你从概念、套路、模板到题目实例建立完整的复习路径。先掌握整体思维模型，再结合 Notebook 细节巩固代码实现。

## 基本概念速览
- **核心能力**：O(1) 平均时间内完成查找、插入、更新；当需要“记录已出现信息再快速查询”时优先考虑哈希表。
- **键的选择**：可以是原始值、前缀状态、组合签名或自定义对象，只要可哈希且稳定。
- **碰撞处理**：Python `dict` 使用开放寻址 + 动态扩容；保持键简单、容量不过大即可维持常数性能。
- **常见失误**：忘记初始化特殊状态（如前缀和 0）、键选择不唯一导致覆盖、回溯场景下未撤销状态。

### Python 实战要点
- `dict`/`set` 是默认工具；需要默认值时使用 `collections.defaultdict` 或 `Counter`。
- 元组、`frozenset`、bitmask 都是合法键；修改后记得重新赋值，避免就地改动可变对象。
- 频繁查询/更新时尽量局部变量绑定（`seen = dict()`）以降低属性查找开销。

## 模式与模板

### 1. 互补 / 前缀状态键
**套路解析**：当遍历序列时，利用哈希实时记录已出现的值或状态（如前缀和、同余类、访问历史），通过查表判定当前元素是否与目标互补或满足区间条件，常用于和差匹配、循环检测等情形。
**伪代码模板**:
```python
table = {initial_state: count}
for element in sequence:
    update running_state
    answer += table.get(target_adjusted_state, 0)
    table[running_state] = table.get(running_state, 0) + 1
```
适用题目：`LC 1`, `LC 202`, `LC 437`, `LC 523`, `LC 525`, `LC 560`, `LC 930`, `LC 957`, `LC 974`, `LC 1248`


- 核心：遍历时实时写入互补信息或前缀状态，后续元素只需 O(1) 查表即可确定答案。
- 牢记初始化 `freq[0] = 1` 处理从头开始的区间；回溯（如树上 DFS）时记得撤销计数。

### 2. 滑动窗口 + 哈希计数
**套路解析**：维护左右指针形成的窗口，借助哈希表跟踪窗口内元素频次或属性；当窗口违反约束时收缩，保持不变量，从而得到满足条件的最优子段。
**伪代码模板**:
```python
counter = {}
left = 0
for right, value in enumerate(sequence):
    counter[value] = counter.get(value, 0) + 1
    while window_violates_constraint(counter):
        counter[sequence[left]] -= 1
        if counter[sequence[left]] == 0:
            del counter[sequence[left]]
        left += 1
    update_answer(left, right, counter)
```
适用题目：`LC 3`, `LC 30`, `LC 76`, `LC 1248`, `LC 159`, `LC 1695`, `LC 340`, `LC 424`, `LC 438`, `LC 567`, `LC 904`, `LC 992`


- 工具思路：扩张右指针满足需求，超标时收缩左指针；统计窗口属性时用 Counter 追踪频次。
- 变量窗口常配合 `at_most(k) - at_most(k-1)` 计算“恰好 k” 的区间数。

### 3. 双向映射 / 一一映射校验
**套路解析**：同时维护两个方向的映射，逐步验证输入元素能否保持双射关系，防止出现多对一或一对多的冲突，常用于字符映射、模式匹配等。
**伪代码模板**:
```python
map_ab = {}
map_ba = {}
for a, b in zipped_sequences:
    if map_ab.get(a, b) != b or map_ba.get(b, a) != a:
        return False
    map_ab[a] = b
    map_ba[b] = a
return True
```
适用题目：`LC 205`, `LC 290`


- 关键：同步维护两个方向的映射，任一侧冲突立刻返回 False。
- 处理拆分后的字符串时，长度不符可提前剪枝。

### 4. 结构签名 / 归类分组
**套路解析**：把原始元素转换为稳定可比的签名（排序结果、频次向量、相邻差值、结构化键等），然后用哈希按签名聚类，实现判重、分组或统计。
**伪代码模板**:
```python
groups = {}
for item in collection:
    signature = build_signature(item)
    groups.setdefault(signature, []).append(item)
return groups
```
适用题目：`LC 30`, `LC 36`, `LC 49`, `LC 187`, `LC 2352`, `LC 249`, `LC 609`


- 思路：将原始数据映射为稳定的签名（排序、频次、差值、矩阵行/列元组等），再用哈希把同类项聚合。
- Sudoku 等约束题可将坐标/值组合成键，一次遍历检查唯一性。

### 5. 值 → 位置 / 统计信息
**套路解析**：哈希记录值与其位置、索引列表或统计信息，配合遍历快速定位元素、稳定写入结果或累计频次，常见于去重、距离限制和采样等。
**伪代码模板**:
```python
info = {}
for index, value in enumerate(sequence):
    update_info(info, index, value)
    if meets_condition(info, index, value):
        update_answer(info, index, value)
```
适用题目：`LC 26`, `LC 27`, `LC 219`, `LC 380`, `LC 398`, `LC 599`, `LC 760`, `LC 1331`


- 关键词：哈希记录“原位信息”以便快速恢复或抽样；必要时配合数组实现 O(1) 删除/随机。

### 6. 频次驱动 / 桶排序
**套路解析**：先统计元素频次，再按频次驱动后续操作（分桶、排序、唯一性校验），适合 Top-K、高频输出或频率判重等任务。
**伪代码模板**:
```python
frequency = count_elements(items)
buckets = group_by_frequency(frequency)
for freq in iterate_from_high_to_low(buckets):
    process_bucket(freq, buckets[freq])
```
适用题目：`LC 1207`, `LC 1338`, `LC 347`, `LC 383`, `LC 451`


- 步骤：先统计频次，再按频次分桶或排序，适合 Top-K、按次数排序、唯一性校验等任务。

### 7. 哈希 + 图或拓展结构
**套路解析**：将哈希作为索引层，与链表、邻接表或堆等结构组合，维护复杂关系或缓存状态，例如 LRU、图相似度或随机化结构。
**伪代码模板**:
```python
structure = initialize_structure()
for relation in relations:
    update_hash_based_index(structure, relation)
    maintain_auxiliary_invariants(structure)
```
适用题目：`LC 734`, `LC 146`


- 在无向图相似度、LRU Cache 等题中，哈希常作为“索引层”，与双向链表/邻接表等结构配合使用。

## 现有题目对照表
| Notebook | 套路 | 关键要点 | 待补充内容 |
| --- | --- | --- | --- |
| `HashTable/LC_1_two-sum.ipynb` | 互补查找（模板 1） | 单次扫描查询 target-num；处理重复索引 | 可追加随机压力测试覆盖极端输入 |
| `HashTable/LC_3_longest-substring-without-repeating-characters.ipynb` | 滑动窗口 + 哈希计数 | 窗口维护 last seen；遇重复收缩左指针 | 补充 Python 与 JS 复杂度对比 |
| `HashTable/LC_30_substring-with-concatenation-of-all-words.ipynb` | 滑动窗口 + 频次表 | 多起点窗口计数单词出现次数 | 新增错位窗口的可视化示例 |
| `HashTable/LC_36_valid-sudoku.ipynb` | 键为 (row,col,box) 的状态表 | 一次遍历同步校验三类约束 | 加入非法数字（>9）异常讨论 |
| `HashTable/LC_49_group-anagrams.ipynb` | 签名分组（模板 4） | 26 频次向量映射同组 | 扩展示例至 Unicode 字符集 |
| `HashTable/LC_76_minimum-window-substring.ipynb` | 滑动窗口 + 需求计数 | need/window 频次差确定收缩时机 | 记录多个最优窗口并比较 |
| `HashTable/LC_1207_unique-number-of-occurrences.ipynb` | 频次判重（模板 5） | 统计后用集合检测重复次数 | 展示 setdefault / Counter 两种写法 |
| `HashTable/LC_1248_count-number-of-nice-subarrays.ipynb` | 前缀奇数计数 | 记录奇数下标组合数 | 补充朴素 O(n^2) 对比 |
| `HashTable/LC_128_longest-consecutive-sequence.ipynb` | 哈希集合边界延伸 | 只在序列起点向右扩张 | 添加随机打乱数组的性能实验 |
| `HashTable/LC_1331_rank-transform-of-an-array.ipynb` | 值→排名映射（模板 D） | 去重排序后构建 value->rank | 补充 streaming 情况讨论 |
| `HashTable/LC_1338_reduce-array-size-to-the-half.ipynb` | 频次降序贪心 | Counter + 排序直到删半数 | 加一版桶排序写法 |
| `HashTable/LC_146_lru-cache.ipynb` | 哈希 + 双向链表 | dict 映射节点，链表维护使用顺序 | 补充 Python OrderedDict 对比 |
| `HashTable/LC_159_longest-substring-with-at-most-two-distinct-characters.ipynb` | 滑动窗口限制 distinct | Counter 维护字符种类 ≤2 | 说明与 LC904 的类比 |
| `HashTable/LC_1695_maximum-erasure-value.ipynb` | 滑动窗口 + 集合 | 窗口保持元素唯一并滚动求和 | 加入大数值溢出讨论 |
| `HashTable/LC_187_repeated-dna-sequences.ipynb` | 签名分组（滚动编码） | 记录长度10 序列出现次数 | 实现 rolling hash 作为扩展 |
| `HashTable/LC_202_happy-number.ipynb` | 检测循环哈希/集合 | 平方和序列重复即非快乐数 | 补充 Floyd 快慢指针版本 |
| `HashTable/LC_205_isomorphic-strings.ipynb` | 双向映射（模板 3） | 同步维护 s->t 与 t->s | 考虑 Unicode 扩展测试 |
| `HashTable/LC_219_contains-duplicate-ii.ipynb` | 值→最近索引（模板 D） | 字典保存上次位置判距离 | 加入滑动窗口集合写法 |
| `HashTable/LC_2352_equal-row-and-column-pairs.ipynb` | 签名分组（模板 4） | 行列序列化为元组比对 | 补充空间复杂度压缩技巧 |
| `HashTable/LC_242_valid-anagram.ipynb` | 频次比较 | Counter 或数组比较字符次数 | 增加排序法的复杂度对照 |
| `HashTable/LC_26_remove-duplicates-from-sorted-array.ipynb` | 值→位置哈希 | seen 记录首次位置，写指针构造唯一前缀 | 追加 O(1) 双指针无哈希版本对照 |
| `HashTable/LC_27_remove-element.ipynb` | 值→频次统计 | stats 统计被删除次数并稳定写入 | 输出删除元素的统计摘要 |
| `HashTable/LC_249_group-shifted-strings.ipynb` | 差值签名分组 | 模 26 差值序列为键 | 举出含空字符串/单字符用例 |
| `HashTable/LC_290_word-pattern.ipynb` | 双射映射（模板 3） | pattern 与单词双向校验 | 补充 split 异常处理 |
| `HashTable/LC_340_longest-substring-with-at-most-k-distinct-characters.ipynb` | 滑动窗口 + 计数 | 收缩直至 distinct≤k | 加入多语言实现比较 |
| `HashTable/LC_347_top-k-frequent-elements.ipynb` | 桶排序频次（模板 5） | Counter + bucket 取前 K | 展示 heap 解法性能对比 |
| `HashTable/LC_380_insert-delete-getrandom-o1.ipynb` | 哈希 + 数组 | dict 记录索引，数组支持 O(1) 随机 | 补充随机种子控制说明 |
| `HashTable/LC_383_ransom-note.ipynb` | 频次检查 | 统计 magazine 字符供给 | 考虑大写混合输入 |
| `HashTable/LC_398_random-pick-index.ipynb` | 值→索引列表（模板 D） | dict 存索引数组随机返回 | 补充水库抽样实现 |
| `HashTable/LC_424_longest-repeating-character-replacement.ipynb` | 滑动窗口 + maxFreq | 窗口长-最高频≤k 即有效 | 说明为何 maxFreq 不必递减 |
| `HashTable/LC_437_path-sum-iii.ipynb` | 前缀和哈希（模板 2） | DFS 累积 prefix 并回溯减计数 | 加一版迭代栈写法 |
| `HashTable/LC_438_find-all-anagrams-in-a-string.ipynb` | 固定窗口频次 | 滑动窗口维护计数差为 0 | 新增直接返回子串版本 |
| `HashTable/LC_451_sort-characters-by-frequency.ipynb` | 桶排序频次 | 按频次降序拼接字符串 | 比较排序 vs 桶实现 |
| `HashTable/LC_523_continuous-subarray-sum.ipynb` | 前缀模记忆 | 记录前缀 mod k 的最早索引 | 补充负 k 的测试 |
| `HashTable/LC_525_contiguous-array.ipynb` | 平衡值前缀 | 0 视作 -1，重复平衡值得最长区间 | 强调初始化 balance=0:-1 |
| `HashTable/LC_560_subarray-sum-equals-k.ipynb` | 前缀和计数（模板 2） | freq[prefix-k] 累加答案 | 加入随机数组 fuzz 测试 |
| `HashTable/LC_567_permutation-in-string.ipynb` | 固定窗口频次 | 计数匹配即存在排列 | 说明 matches 计数更新逻辑 |
| `HashTable/LC_599_minimum-index-sum-of-two-lists.ipynb` | 值→索引和 | dict 存第一列表索引累加最小和 | 考虑索引和相同时排序输出 |
| `HashTable/LC_609_find-duplicate-file-in-system.ipynb` | 签名分组（模板 4） | 文件内容作键聚合路径 | 扩展到大文件 streaming 方案 |
| `HashTable/LC_734_sentence-similarity.ipynb` | 邻接表查关系 | word->set 构建无向图 | 提及传递闭包为何不需 |
| `HashTable/LC_760_find-anagram-mappings.ipynb` | 值→索引栈 | 多重值用栈/队列逐个映射 | 加入随机 perm 验证 |
| `HashTable/LC_904_fruit-into-baskets.ipynb` | 窗口 distinct≤2 | Counter 控制水果种类数 | 关联 TwoPointers 目录的窗口模板 |
| `HashTable/LC_930_binary-subarrays-with-sum.ipynb` | 前缀和计数 | 统计 prefix-目标 的次数 | 补充多组 0/1 边界案例 |
| `HashTable/LC_957_prison-cells-after-n-days.ipynb` | 状态循环检测 | bitmask/元组记录首次出现天数 | 附上循环长度推导说明 |
| `HashTable/LC_974_subarray-sums-divisible-by-k.ipynb` | 前缀模计数 | Hash 记录每个模值出现次数 | 强调 Python 取模与负数 |
| `HashTable/LC_992_subarrays-with-k-different-integers.ipynb` | 双窗口差法 | atMost(k)-atMost(k-1) 求恰好 K | 补充复杂度推导细节 |

## 复习与拓展建议
- **优先练模板**：先手写模板 1-7，确认键设计、初始化与回溯场景的处理顺序。
- **按模式复盘**：增删 Notebook 时同步更新对应套路，巩固“键是什么、值存什么”的核心认知。
- **结合 Notebook**：复习时对照 `HashTable/LC_xxx.ipynb` 的详解、测试用例与 follow-up，查漏补缺。
- **延伸思考**：哈希技巧常与滑动窗口、前缀和、图结构等组合使用，遇到需要“状态记忆 + 快速查找”时优先考虑是否能转化为哈希问题。
