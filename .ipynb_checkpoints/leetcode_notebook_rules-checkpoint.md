# LeetCode Notebook Generation Rules

对每一道准备题目，Jupyter Notebook 必须严格遵循以下结构与内容规范。除非题目本身不具备对应信息，否则所有模块都要填写到位。

## 目录组织与文件命名
- 按照主要 Topic 建立目录（如 `UnionFind`, `SlidingWindow`, `BinaryTree` 等）。
- 若 Notebook 对应的 Topic 目录不存在，则先创建再放入 Notebook，支持多 Topic 时归入主 Topic。
- Topic 名称需使用约定俗成的英文关键词（如 `HashTable`），避免同义词造成目录碎片。
- File: `LC_<problem-number>_<kebab-case-title>.ipynb`
- Title markdown cell (第一格) 使用 `# <problem-number>. <Official Title>`

## Notebook 总体结构
1. **Metadata 摘要 (Markdown)**
   - 题目来源链接（若无法访问则注明）
   - 标签/考察点（例如: `Array`, `Sliding Window`）
   - 难度等级
   - 推荐优先级（高/中/低，用于复习计划）
2. **Problem Statement 原题描述 (Markdown)**
   - 原题完整英文描述。
   - 若官方描述不可用，注明数据来源并给出可靠的完整版本。
   - 若题目为 LeetCode Premium，必须补充官方的输入输出示例；非 Premium 题默认不额外列示示例，保持结构简洁。
3. **Progressive Hints (Markdown)**
   - 至少 3 条，由浅入深；每条前置 `Hint 1`, `Hint 2` 等。
4. **Solution Overview (Markdown)**
   - 直击核心思路的摘要。
   - 若有多种典型解法，列表概述优缺点及使用场景。
5. **Detailed Explanation (Markdown)**
   - 对主解法进行分步推导，可配流程图/示意伪代码（Markdown 描述）。
   - 涉及的数据结构或算法模板需简述原理。
6. **Complexity Trade-off Table (Markdown)**
   - 使用表格列出每种解法的时间、空间复杂度。
7. **Reference Implementation (Code)**
    - 默认使用 Python 3（除非题目明确要求其他语言）。
    - 代码需包含函数签名，并在关键步骤加入清晰注释，确保复习时能快速理解思路。
8. **Complexity Analysis (Markdown)**
    - 对主解法逐条说明时间复杂度、空间复杂度、瓶颈所在。
9. **Edge Cases & Pitfalls (Markdown)**
     - 列举潜在误区、特殊输入、精度/溢出风险等。
10. **Follow-up Variants (Markdown)**
     - 枚举两到三个可能的 follow-up 问题或在 MLE/AI 场景下的衍生需求。
11. **Takeaways (Markdown)**
     - 用于总结本题的复习要点和可迁移的技巧。
12. **Similar Problems (Markdown)**
     - 列出与本题思路接近或常搭配训练的题目，使用 Markdown 表格，列为 `Problem ID`, `Problem Title`, `Technique`。

## 额外要求
- Notebook 顶部增加 `Topic Alignment` 区块，说明该题与 MLE / AI Engineer 面试的关联（例如 pipeline 调度、特征处理、图算法等）。
- 若题目涉及概率、组合数学或数值稳定性，需单独添加小节说明相关数学背景。
- 所有 Markdown 中的列表、表格使用标准 ASCII，避免混用中文标点和英文标点导致渲染问题。
- Notebook 中的代码块需可独立运行，必要时在结尾添加 `reset` 或帮助读者清理环境的说明。
- 不再单独展示输入输出示例，保持整体结构精简；如需强调，可在解题思路或详解中口头描述。

## 使用方式
- 每次新增题目时，复制此模板作为骨架补全。
- 若未来需要扩展额外模块（例如 Benchmark、可视化），需在模板中统一更新后再应用。
