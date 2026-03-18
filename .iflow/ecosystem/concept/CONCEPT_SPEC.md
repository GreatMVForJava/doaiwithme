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
│   ├── 500-404.md               # 500=404
│   ├── ai-rules-circle.md       # AI Rules 是圈不是线
│   └── content-classification.md # 协作内容分类
├── execution-mode/              # L1 目录：执行模式概念
│   ├── workflow-vs-dialog.md    # 工作流模式 vs 对话模式
│   ├── node-context.md          # 节点上下文依赖
│   └── cold-start.md            # 冷启动
├── token-economics/             # L1 目录：Token经济学概念
│   ├── three-layer-model.md     # 三层信息模型
│   ├── cqrs.md                  # CQRS 解耦
│   ├── hash-optimization.md     # 增量哈希优化
│   ├── teach-vs-api.md          # 教知识 > 注册 API
│   └── effect-equivalence.md    # 效果等价
└── skill-execution/             # L1 目录：Skill执行概念
    ├── five-modes.md            # 五种Skill模式
    └── execution-formula.md     # 执行力公式
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
| AI 遇到无法解决的问题 | 500=404 | `@.iflow/ecosystem/concept/ai-collaboration/500-404.md` |
| AI 需要选择适用规范 | AI Rules 是圈不是线 | `@.iflow/ecosystem/concept/ai-collaboration/ai-rules-circle.md` |
| AI 完成任务后需要记录 | 沉淀 | `@.iflow/ecosystem/concept/ai-collaboration/deposition.md` |
| AI 需要查找历史经验 | 复用 | `@.iflow/ecosystem/concept/ai-collaboration/reuse.md` |
| AI 判断文件属于谁使用 | 协作内容分类 | `@.iflow/ecosystem/concept/ai-collaboration/content-classification.md` |

### 执行模式场景触发

| 具体场景 | 触发概念 | 文件路径 |
|---------|---------|---------|
| AI 判断是固定流程还是交互对话 | 工作流 vs 对话模式 | `@.iflow/ecosystem/concept/execution-mode/workflow-vs-dialog.md` |
| AI 从零开始理解项目 | 冷启动 | `@.iflow/ecosystem/concept/execution-mode/cold-start.md` |
| AI 设计节点数据传递 | 节点上下文依赖 | `@.iflow/ecosystem/concept/execution-mode/node-context.md` |

### Token 经济学场景触发

| 具体场景 | 触发概念 | 文件路径 |
|---------|---------|---------|
| AI 设计新的 Skill | 三层信息模型、教知识 vs API | `@.iflow/ecosystem/concept/token-economics/` |
| AI 优化 Token 消耗 | 三层信息模型 | `@.iflow/ecosystem/concept/token-economics/three-layer-model.md` |
| AI 设计缓存机制 | CQRS 解耦 | `@.iflow/ecosystem/concept/token-economics/cqrs.md` |
| AI 判断是否需要沙箱隔离 | 效果等价 | `@.iflow/ecosystem/concept/token-economics/effect-equivalence.md` |

### Skill 执行场景触发

| 具体场景 | 触发概念 | 文件路径 |
|---------|---------|---------|
| AI 选择 Skill 执行方式 | 五种模式 | `@.iflow/ecosystem/concept/skill-execution/five-modes.md` |
| AI 评估 Skill 质量 | 执行力公式 | `@.iflow/ecosystem/concept/skill-execution/execution-formula.md` |

---

## 边界划分（避免重复）

| 内容类型 | 存放位置 | 说明 |
|---------|---------|------|
| **概念定义** | `concept/` | "是什么"、"什么场景用" |
| **方法论** | `experience/collaboration-method.md` | "怎么用"、"步骤是什么" |
| **规范** | `rule/` 或 `skills/` | "具体规则"、"实现细节" |

### 示例：三层信息模型

| 层级 | 文件 | 内容 |
|------|------|------|
| **概念** | `concept/token-economics/three-layer-model.md` | 定义：分层信息注入，Token 效率最大化 |
| **方法论** | `experience/collaboration-method.md` | 方法：渐进式披露原则（十四） |
| **规范** | `skills/SKILLS_SPEC.md` | 实现：加载层级、Token 预算 |

### 示例：幻觉

| 层级 | 文件 | 内容 |
|------|------|------|
| **概念** | `concept/ai-collaboration/hallucination.md` | 定义：四种幻觉类型 |
| **方法论** | `experience/collaboration-method.md` | 方法：防止幻觉的检查方法 |
| **规范** | `endPoint.md` | 执行：核心要点中强制要求具体证据 |

---

## 分层规则

| 层级 | 内容 | 加载时机 | Token 预算 |
|------|------|---------|-----------|
| **L0** | 核心要点表格 | 启动时加载 | ~200 |
| **L1** | 概念详情（定义+场景+示例） | 触发场景时加载 | ~300/概念 |
| **L2** | 方法论/规范引用 | 深入时加载 | 按需 |

---

## 概念文件模板

```markdown
# {概念名}

> **定位**: {一句话定位}
> **L2 引用**: @.iflow/ecosystem/{方法论或规范路径}

---

## 定义

{概念的定义}

## 使用场景

- 场景1：{描述}
- 场景2：{描述}

## 示例

{具体示例}

## L2 详细内容

- 方法论：@.iflow/ecosystem/experience/collaboration-method.md#章节
- 规范：@.iflow/ecosystem/{规范目录}/{规范文件}.md
```

---

**最后更新**：2026-03-17
**版本**：v2.0
**设计原则**：触发条件具体化、边界清晰化、避免重复