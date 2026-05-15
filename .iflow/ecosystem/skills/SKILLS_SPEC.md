# Skills 规范（L0 入口）

> **定位**: 专业技能的抽象，将专业知识、工作流程、工具使用方式封装成可复用的模块
> **读取策略**: 本文件为 L0 入口，始终读取；L1/L2 按需读取
> **借鉴来源**: [Agent Skills Specification](https://agentskills.io/specification)

## 核心要点（L0，必须记住）

- Skills 是专业技能的抽象，指导 AI 如何使用 Tools
- 按需读取：元数据启动时主动读取，主体激活时主动读取
- 文件命名：`{name}-skill.md` 或目录结构 `{name}/SKILL.md`
- frontmatter 必须包含 `name` 和 `description`
- **创建 Skill 时必须先读取 skill-creator-skill.md**

## Skill 执行模式

| 模式 | 核心机制 | 适用场景 |
|------|---------|---------|
| **纯 Prompt 注入** | 注入 body 到 system prompt | 教规范/风格 |
| **脚本执行** | 预制脚本 + skill_run | 操作文件格式 |
| **库调用** | LLM 写代码 import 库 | 灵活组合 API |
| **渐进读取** | 路由表 + 按需读取文档 | 知识量大 |
| **编排型** | 多阶段工作流 + 子 Agent | 复杂流程 |

**执行力公式**：Skill 执行力 = SKILL.md body 质量 × (Agent 基础工具 + skill_run 沙箱能力)
- SKILL.md body 是"灵魂"——决定 LLM 能否理解任务、选对方法
- skill_run 是"手脚"——提供在隔离沙箱中执行命令的能力

## 按需读取导航

| 场景 | 读取文件 |
|------|---------|
| Skill格式与验证规范 | `@.iflow/ecosystem/skills/l1-skills-core.md` |
| 创建新Skill与高级规范 | `@.iflow/ecosystem/skills/l2-skills-reference.md` |

---

**版本**: 16.0
**更新日期**: 2026-05-15
**维护者**: AI + 人类