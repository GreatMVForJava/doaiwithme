# start.md - AI 行为启动入口

> **定位**: 入口索引，告诉 AI "要做什么"（首位，易记住）
> **详细规范**: `@.iflow/endPoint.md`（末位，兜底检查）
> **设计原理**: AI 记忆规律是"前后记忆，中间遗忘"，start.md 在首位确保核心要点被记住

---

## 核心要点（必须记住）

- **流程**: 预检 → 确认 → 规划 → 执行 → 自检 → 沉淀
- **四层防御**: Cache状态层 → 项目级冷启动 → 需求级冷启动 → 任务级执行清单
- **三层保证**: 技术层（system prompt）→ 设计层（触发条件）→ 协作层（用户监督），**用户监督是最可靠的保证**
- **三层信息模型**: L0 概览 → L1 Body → L2 详细文档，渐进式披露，Token 效率最大化
- **身份确认**: 每次预检必须读取 identity.md / soul.md / user.md
- **强制输出**: 每步必须输出表格证据，否则视为未完成
- **交互规则**: 只在需要人类补充数据时才询问，否则默认执行下一阶段
- **防止幻觉**: 证据必须具体，不能只写"已完成"
- **方法论**: 预检用笛卡尔、确认用乔哈里窗、规划用联动检查、执行用删除评估、沉淀用固化判断
- **方法论强制**: 方法论贯穿整个协作过程，每个阶段必须执行对应方法
- **Skill设计**: 教知识 > 注册 API，效果等价 > 形式等价

---

## 分类触发表（按需加载）

| 触发场景 | 读取文件 |
|---------|---------|
| 新项目/新AI | `@.iflow/ecosystem/experience/cold-start.md` |
| 需要方法论 | `@.iflow/ecosystem/experience/collaboration-method.md` |
| AI犯错/不确定 | `@.iflow/ecosystem/experience/deposition-records.md`（先看场景标签索引） |
| **概念触发** | `@.iflow/ecosystem/concept/CONCEPT_SPEC.md`（查看具体场景→概念映射） |
| 查找经验 | `@.iflow/ecosystem/experience/EXPERIENCE_SPEC.md` |
| 创建/使用Skill | `@.iflow/ecosystem/skills/SKILLS_SPEC.md` |
| 修改规范/代码 | `@.iflow/ecosystem/rule/RULE_SPEC.md` |
| 身份相关 | `@.iflow/ecosystem/identity/IDENTITY_SPEC.md` |

**概念触发原则**：不是模糊的"概念对齐"，而是具体场景触发。详见 `@.iflow/ecosystem/concept/CONCEPT_SPEC.md` 的触发条件映射。

---

## 用户检查清单（快速验证）

| 阶段 | 用户检查项 | 合格标准 |
|------|-----------|---------|
| **预检** | AI 是否输出了"四层防御检查"表格？ | 有表格 + 有检查结果 |
| **确认** | AI 是否输出了"任务边界"？ | 有任务描述 + 有完成条件 |
| **规划** | AI 是否输出了"修改文件列表"？ | 有文件列表 + 有原因 |
| **执行** | AI 是否输出了"修改内容摘要"？ | 有修改摘要 + 有文件路径 |
| **自检** | AI 是否输出了"规则检查表"？ | 有表格 + 有检查结果 |
| **沉淀** | AI 是否输出了"经验沉淀"？ | 有场景标签 + 解决方案 |

**用户反馈**：✅ 合格→"继续" | ❌ 不合格→"缺少xxx"或"重做xxx"

---

## 目录索引

| 目录 | 用途 |
|------|------|
| `@.iflow/cache/` | 任务缓存 |
| `@.iflow/ecosystem/identity/` | 人格定义 |
| `@.iflow/ecosystem/experience/` | 经验沉淀 |
| `@.iflow/ecosystem/rule/` | 规则目录 |
| `@.iflow/ecosystem/skills/` | 技能目录 |
| `@.iflow/ecosystem/concept/` | 概念定义 |

---

**版本**: v6.0
**更新日期**: 2026-03-16
**维护者**: AI + 人类
