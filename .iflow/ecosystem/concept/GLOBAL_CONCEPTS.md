# 全局概念词典

> **定位**: L0 核心要点索引，启动时加载
> **详细规范**: @.iflow/ecosystem/concept/CONCEPT_SPEC.md
> **触发条件**: 详见 CONCEPT_SPEC.md 的触发条件映射（具体场景 → 概念文件）

---

## 如何使用

1. **AI 启动时**：加载本文件核心要点（L0）
2. **遇到具体场景时**：查阅 `@.iflow/ecosystem/concept/CONCEPT_SPEC.md` 的触发条件映射
3. **深入理解概念时**：加载对应的 L1 概念文件

---

## 核心要点（必须记住）

| 概念 | 一句话定义 | L1 路径 |
|------|-----------|---------|
| **复用** | AI 复用之前的编码经验和知识 | @.iflow/ecosystem/concept/ai-collaboration/reuse.md |
| **沉淀** | AI 将经验沉淀到相应目录 | @.iflow/ecosystem/concept/ai-collaboration/deposition.md |
| **幻觉** | AI 生成不存在的代码或 API | @.iflow/ecosystem/concept/ai-collaboration/hallucination.md |
| **500=404** | 允许只关注能解决的问题 | @.iflow/ecosystem/concept/ai-collaboration/500-404.md |
| **AI Rules 是圈不是线** | 不可能满足所有规范，按需选择 | @.iflow/ecosystem/concept/ai-collaboration/ai-rules-circle.md |
| **三层信息模型** | L0 概览 → L1 详情 → L2 规范 | @.iflow/ecosystem/concept/token-economics/three-layer-model.md |
| **教知识 > 注册 API** | LLM 最强的能力是理解自然语言指令 | @.iflow/ecosystem/concept/token-economics/teach-vs-api.md |
| **效果等价** | 形式不同但效果相同 | @.iflow/ecosystem/concept/token-economics/effect-equivalence.md |
| **冷启动** | AI 从零理解项目 | @.iflow/ecosystem/concept/execution-mode/cold-start.md |
| **执行力公式** | 执行力 = 文档质量 × 工具能力 | @.iflow/ecosystem/concept/skill-execution/execution-formula.md |

---

## 概念分类

| 类别 | L1 目录 | 核心概念 | 触发场景 |
|------|--------|---------|---------|
| **AI协作** | `ai-collaboration/` | 复用、沉淀、幻觉、500=404 | 协作过程中 |
| **执行模式** | `execution-mode/` | 工作流/对话模式、冷启动 | 设计流程时 |
| **Token经济学** | `token-economics/` | 三层模型、教知识、效果等价 | 设计Skill时 |
| **Skill执行** | `skill-execution/` | 五种模式、执行力公式 | 评估Skill时 |

---

## 概念关系图

```
复合工程（方法论体系）
├── AI协作概念
│   ├── 复用 → 沉淀 → 经验固化
│   ├── 幻觉 → 防止 → 质量保证
│   └── 500=404 + AI Rules → 灵活执行
├── Token经济学
│   ├── 三层信息模型 → 渐进加载
│   ├── 教知识 > 注册 API → Skill设计
│   └── 效果等价 → 降低负担
└── 执行模式
    ├── 冷启动 → 四层防御
    └── 执行力公式 → 质量评估
```

---

**版本**: v5.0
**设计**: L0 核心要点索引 + L1 概念详情文件 + L2 规范引用
