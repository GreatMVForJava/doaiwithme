# 全局概念词典

> **定位**: L0 核心要点索引，启动时主动读取
> **详细规范**: @.iflow/ecosystem/concept/CONCEPT_SPEC.md
> **触发条件**: 详见 CONCEPT_SPEC.md 的触发条件映射（具体场景 → 概念文件）

---

## 如何使用

1. **AI 启动时**：主动读取本文件核心要点（L0）
2. **遇到具体场景时**：查阅 `@.iflow/ecosystem/concept/CONCEPT_SPEC.md` 的触发条件映射
3. **深入理解概念时**：主动读取对应的 L1 概念文件

---

## 核心要点（必须记住）

| 概念 | 一句话定义 | L1 路径 |
|------|-----------|---------|
| **复用** | AI 复用之前的编码经验和知识 | @.iflow/ecosystem/concept/ai-collaboration/reuse.md |
| **沉淀** | AI 将经验沉淀到相应目录 | @.iflow/ecosystem/concept/ai-collaboration/deposition.md |
| **幻觉** | AI 生成不存在的代码或 API | @.iflow/ecosystem/concept/ai-collaboration/hallucination.md |
| **500=404** | 允许只关注能解决的问题 | @.iflow/ecosystem/concept/ai-collaboration/500-404.md |
| **Application Legibility** | 代码不仅要对人可读，更要对 Agent 可读 | @.iflow/ecosystem/concept/ai-collaboration/legibility.md |
| **三层信息模型** | L0 概览 → L1 详情 → L2 规范 | @.iflow/ecosystem/concept/token-economics/three-layer-model.md |
| **教知识 > 注册 API** | LLM 最强的能力是理解自然语言指令 | @.iflow/ecosystem/concept/token-economics/teach-vs-api.md |
| **效果等价** | 形式不同但效果相同 | @.iflow/ecosystem/concept/token-economics/effect-equivalence.md |
| **冷启动** | AI 从零理解项目 | @.iflow/ecosystem/experience/cold-start.md |
| **SDD流程** | 用 Spec 文档作为 AI 与人"契约"的开发方法论 | @.iflow/ecosystem/concept/execution-mode/sdd-workflow.md |
| **Harness Engineering** | AI Agent 的工程化方法论（四机制：Inform/Constrain/Verify/Correct）| @.iflow/ecosystem/concept/execution-mode/harness-engineering.md |
| **知识基座** | 让 AI 越用越懂业务的团队经验实践 | @.iflow/ecosystem/concept/token-economics/knowledge-base.md |
| **三宫六院** | AI 协作的决策中枢与执行体系 | @.iflow/ecosystem/concept/three-palaces-six-courts/three-palaces-six-courts.md |
| **AI-AI协作** | 多AI实例间的交接、并行、编排协议 | @.iflow/ecosystem/concept/ai-collaboration/ai-to-ai-collaboration.md |
| **协作边界** | 目录边界、确认vs执行边界、优先级冲突、红线 | @.iflow/ecosystem/concept/ai-collaboration/collaboration-boundaries.md |

---

## 概念分类

| 类别 | L1 目录 | 核心概念 | 触发场景 |
|------|--------|---------|---------|
| **AI协作** | `ai-collaboration/` | 复用、沉淀、幻觉、500=404、AI-AI协作、协作边界 | 协作过程中 |
| **执行模式** | `execution-mode/` | 工作流/对话模式、冷启动 | 设计流程时 |
| **Token经济学** | `token-economics/` | 三层模型、教知识、效果等价 | 设计Skill时 |
| **三宫六院** | `three-palaces-six-courts/` | 三宫（规划/审核/调度）、六院、钦天监 | 规划/执行/监控时 |

---

## 概念关系图

```
复合工程（方法论体系）
├── AI协作概念
│   ├── 复用 → 沉淀 → 经验固化
│   ├── 幻觉 → 防止 → 质量保证
│   ├── 500=404 + AI Rules → 灵活执行
│   └── 协作边界 → 目录/确认/优先级/红线
├── Token经济学
│   ├── 三层信息模型 → 渐进读取
│   ├── 教知识 > 注册 API → Skill设计
│   └── 效果等价 → 降低负担
├── 执行模式
│   └── 冷启动 → 四层防御
└── 三宫六院（协作架构）
    ├── 三宫 → 决策中枢（规划/审核/调度）
    ├── 六院 → 执行机构（理解/执行/协同/反馈/审校/沉淀）
    └── 钦天监 → 监控机构（观天象/测吉凶/记史实）
```

---

## 概念→行为映射

> **核心原则**: 知道概念 ≠ 按概念行动。每个概念必须有明确的"如果X，则做Y"行为规则。

| 概念 | 触发场景 | AI必须执行的行为 |
|------|---------|-----------------|
| **复用** | 执行任务前 | 先搜索 deposition-records.md 和已有代码，不重复造轮子 |
| **沉淀** | 踩坑/用户纠正/发现更好方法 | 写入 deposition-records.md（场景标签+描述+方案），固化后删除 |
| **幻觉** | 输出"已完成"/没有具体证据 | 必须输出文件名+行号，不说空话 |
| **500=404** | 遇到无法解决的问题 | 聚焦能解决的部分，不阻塞整体流程 |
| **Application Legibility** | 编写/审查代码 | 代码对Agent可读：命名清晰、结构规范、注释充分 |
| **三层信息模型** | 设计新文档/Skill | L0核心→L1详情→L2参考，按需加载 |
| **教知识 > 注册 API** | 设计Skill | 用自然语言指令教AI，而非注册复杂API |
| **效果等价** | 选择实现方式 | 形式可不同，效果必须相同；选负担最小的 |
| **冷启动** | 新项目/新AI | 读取 start.md → endPoint.md → Cache |
| **SDD流程** | 需求→开发 | 用Spec文档作契约，先Spec后Code |
| **Harness Engineering** | 设计AI协作架构 | Inform → Constrain → Verify → Correct |
| **知识基座** | 团队经验共享 | 信号驱动沉淀，一人踩坑→全团队受益 |
| **三宫六院** | 复杂任务规划/执行 | 三宫决策+六院执行+钦天监监控 |
| **AI-AI协作** | 多AI实例协作 | 上下文交接+分区执行+冲突检测 |
| **协作边界** | 任何操作前 | 目录边界不越界+修改前确认+优先级冲突高覆盖低+红线不触碰 |

---

**版本**: v5.1
**设计**: L0 核心要点索引 + L1 概念详情文件 + L2 规范引用
