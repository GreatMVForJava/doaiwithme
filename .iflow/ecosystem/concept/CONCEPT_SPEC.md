# CONCEPT_SPEC.md - 概念目录规范

> **命名**: 全大写+下划线，作为当前目录层级的规范
> **定位**: 概念的定义层，方法论和规范的边界层

---

## 核心要点（必须记住）

- **概念分层**：L0 核心要点 → L1 概念详情 → L2 规范引用
- **触发映射**：具体场景 → 概念文件（不是模糊的"概念对齐"）
- **边界清晰**：概念定义在 concept/，方法论在 experience/，规范在 rule/ 或 skills/

---

## 目录结构

```
concept/
├── CONCEPT_SPEC.md              # L0 目录规范
├── GLOBAL_CONCEPTS.md           # L0 核心要点索引
├── ai-collaboration/            # L1 目录：AI协作概念
│   ├── reuse.md                 # 复用
│   ├── deposition.md            # 沉淀
│   ├── hallucination.md         # 幻觉
│   ├── 500-404.md               # 500=404（含规范选择策略）
│   ├── content-classification.md # 协作内容分类
│   ├── legibility.md            # Application Legibility（可读性）
│   └── ai-to-ai-collaboration.md # AI-AI协作协议
├── execution-mode/              # L1 目录：执行模式概念
│   ├── workflow-vs-dialog.md    # 工作流模式 vs 对话模式
│   ├── node-context.md          # 节点上下文依赖
│   ├── sdd-workflow.md          # SDD流程（需求→设计→开发）
│   └── harness-engineering.md   # Harness Engineering（AI协作架构）
├── token-economics/             # L1 目录：Token经济学概念
│   ├── three-layer-model.md     # 三层信息模型
│   ├── teach-vs-api.md          # 教知识 > 注册 API
│   ├── effect-equivalence.md    # 效果等价
│   └── knowledge-base.md        # 知识基座（踩坑/经验/团队知识）
└── three-palaces-six-courts/    # L1 目录：三宫六院协作架构
    └── three-palaces-six-courts.md  # 三宫六院完整定义（合并文件）
```

---

## 文件命名规范

### L0 文件（目录级）

| 文件 | 命名规则 | 说明 |
|------|---------|------|
| `CONCEPT_SPEC.md` | 全大写+下划线 | 目录规范文件 |
| `GLOBAL_CONCEPTS.md` | 全大写+下划线 | 核心要点索引 |

### L1 目录

| 规则 | 说明 | 示例 |
|------|------|------|
| 命名格式 | 小写+短横杠，语义化 | `ai-collaboration/`、`token-economics/` |
| 语义要求 | 表达概念类别，不是层级标记 | ✅ `ai-collaboration/` ❌ `l1-concepts/` |

### L1 文件

| 规则 | 说明 | 示例 |
|------|------|------|
| 命名格式 | 小写+短横杠，概念名 | `three-layer-model.md`、`hallucination.md` |
| 语义要求 | 概念的英文翻译，便于检索 | ✅ `hallucination.md` ❌ `huanjue.md` |
| 特殊情况 | 数字概念可用数字开头 | `500-404.md`（500=404 概念） |

---

## 触发条件映射（核心）

> **设计原则**：从模糊的"概念对齐"改为具体的触发场景

### AI 协作场景触发

| 具体场景 | 触发概念 | 文件路径 |
|---------|---------|---------|
| AI 输出一句话带过（如"已完成"） | 幻觉 | `@.iflow/ecosystem/concept/ai-collaboration/hallucination.md` |
| AI 遇到无法解决的问题 / 需要选择适用规范 | 500=404 | `@.iflow/ecosystem/concept/ai-collaboration/500-404.md` |
| AI 完成任务后需要记录 | 沉淀 | `@.iflow/ecosystem/concept/ai-collaboration/deposition.md` |
| AI 需要查找历史经验 | 复用 | `@.iflow/ecosystem/concept/ai-collaboration/reuse.md` |
| AI 判断文件属于谁使用 | 协作内容分类 | `@.iflow/ecosystem/concept/ai-collaboration/content-classification.md` |
| AI 编写或审查代码时 | Application Legibility | `@.iflow/ecosystem/concept/ai-collaboration/legibility.md` |
| AI 需要与其他AI实例协作 | AI-AI协作 | `@.iflow/ecosystem/concept/ai-collaboration/ai-to-ai-collaboration.md` |
| AI 交接任务给其他AI | AI-AI协作 | `@.iflow/ecosystem/concept/ai-collaboration/ai-to-ai-collaboration.md` |

### 执行模式场景触发

| 具体场景 | 触发概念 | 文件路径 |
|---------|---------|---------|
| AI 判断是固定流程还是交互对话 | 工作流 vs 对话模式 | `@.iflow/ecosystem/concept/execution-mode/workflow-vs-dialog.md` |
| AI 从零开始理解项目 | 冷启动 | `@.iflow/ecosystem/experience/cold-start.md` |
| AI 设计节点数据传递 | 节点上下文依赖 | `@.iflow/ecosystem/concept/execution-mode/node-context.md` |
| AI 需要拆解需求为任务 | SDD流程 | `@.iflow/ecosystem/concept/execution-mode/sdd-workflow.md` |
| AI 需要建立AI与人的"契约" | SDD流程 | `@.iflow/ecosystem/concept/execution-mode/sdd-workflow.md` |
| AI 设计 Agent 系统架构 | Harness Engineering | `@.iflow/ecosystem/concept/execution-mode/harness-engineering.md` |
| AI 优化 AI 编程效率 | Harness Engineering | `@.iflow/ecosystem/concept/execution-mode/harness-engineering.md` |
| AI 构建 AI 协作环境 | Harness Engineering | `@.iflow/ecosystem/concept/execution-mode/harness-engineering.md` |

### Token 经济学场景触发

| 具体场景 | 触发概念 | 文件路径 |
|---------|---------|---------|
| AI 设计新的 Skill | 三层信息模型、教知识 vs API | `@.iflow/ecosystem/concept/token-economics/` |
| AI 优化 Token 消耗 | 三层信息模型 | `@.iflow/ecosystem/concept/token-economics/three-layer-model.md` |
| AI 判断是否需要沙箱隔离 | 效果等价 | `@.iflow/ecosystem/concept/token-economics/effect-equivalence.md` |
| AI 需要团队知识共享 | 知识基座 | `@.iflow/ecosystem/concept/token-economics/knowledge-base.md` |
| AI 设计经验沉淀机制 | 知识基座 | `@.iflow/ecosystem/concept/token-economics/knowledge-base.md` |
| AI 处理踩坑信号 | 知识基座 | `@.iflow/ecosystem/concept/token-economics/knowledge-base.md` |

### 三宫六院场景触发

| 具体场景 | 触发概念 | 文件路径 |
|---------|---------|---------|
| AI 需要规划复杂任务 | 乾清宫（规划）| `@.iflow/ecosystem/concept/three-palaces-six-courts/three-palaces-six-courts.md` |
| AI 需要审核方案质量 | 交泰宫（审核）| `@.iflow/ecosystem/concept/three-palaces-six-courts/three-palaces-six-courts.md` |
| AI 需要协调多任务执行 | 坤宁宫（调度）| `@.iflow/ecosystem/concept/three-palaces-six-courts/three-palaces-six-courts.md` |
| AI 需要理解模糊需求 | 承乾院（理解）| `@.iflow/ecosystem/concept/three-palaces-six-courts/three-palaces-six-courts.md` |
| AI 需要执行具体任务 | 延禧院（执行）| `@.iflow/ecosystem/concept/three-palaces-six-courts/three-palaces-six-courts.md` |
| AI 需要协调多方协作 | 永和院（协同）| `@.iflow/ecosystem/concept/three-palaces-six-courts/three-palaces-six-courts.md` |
| AI 需要汇报进展或反馈 | 景仁院（反馈）| `@.iflow/ecosystem/concept/three-palaces-six-courts/three-palaces-six-courts.md` |
| AI 需要审校执行结果 | 钟粹院（审校）| `@.iflow/ecosystem/concept/three-palaces-six-courts/three-palaces-six-courts.md` |
| AI 需要沉淀经验知识 | 景阳院（沉淀）| `@.iflow/ecosystem/concept/three-palaces-six-courts/three-palaces-six-courts.md` |
| AI 需要监控任务进度 | 钦天监（监控）| `@.iflow/ecosystem/concept/three-palaces-six-courts/three-palaces-six-courts.md` |

### Cache 场景触发（每次执行必须）

| 具体场景 | 触发操作 | 文件路径 |
|---------|---------|---------|
| AI 启动预检阶段 | 读取 Cache | `@.iflow/cache/task-progress.json` |
| AI 开始新任务 | 写入任务边界 | `@.iflow/cache/task-progress.json` |
| AI 有待确认任务 | 写入待办 | `@.iflow/cache/pending-tasks.json` |
| AI 完成子任务 | 更新进度 | `@.iflow/cache/task-progress.json` |
| AI 需要跳过任务 | 写入跳过记录 | `@.iflow/cache/skipped-tasks.json` |
| AI 自检阶段 | 读取完成条件 | `@.iflow/cache/task-progress.json` |
| AI 任务完成 | 清理 Cache | 删除/更新相关记录 |

---

## 边界划分（避免重复）

| 内容类型 | 存放位置 | 说明 |
|---------|---------|------|
| **概念定义** | `concept/` | "是什么"、"什么场景用" |
| **方法论** | `methodology/method-index.md` | "怎么用"、"步骤是什么" |
| **经验沉淀** | `experience/deposition-records.md` | "踩坑记录"、"历史经验" |
| **规范** | `rule/` 或 `skills/` | "具体规则"、"实现细节" |

### 示例：三层信息模型

| 层级 | 文件 | 内容 |
|------|------|------|
| **概念** | `concept/token-economics/three-layer-model.md` | 定义：分层主动获取，Token 效率最大化 |
| **方法论** | `methodology/method-index.md` | 方法：渐进式披露原则 |
| **规范** | `skills/SKILLS_SPEC.md` | 实现：加载层级、Token 预算 |

### 示例：幻觉

| 层级 | 文件 | 内容 |
|------|------|------|
| **概念** | `concept/ai-collaboration/hallucination.md` | 定义：四种幻觉类型 |
| **方法论** | `methodology/method-index.md` | 方法：防止幻觉的检查方法 |
| **规范** | `endPoint.md` | 执行：核心要点中强制要求具体证据 |

---

## 分层规则

| 层级 | 内容 | 加载时机 | Token 预算 |
|------|------|---------|-----------|
| **L0** | 核心要点表格 | 启动时加载 | ~200 |
| **L1** | 概念详情（定义+场景+示例） | 触发场景时加载 | ~300/概念 |
| **L2** | 方法论/规范引用 | 深入时加载 | 按需 |

---

**最后更新**：2026-05-15
**版本**：v2.1
**设计原则**：触发条件具体化、边界清晰化、避免重复