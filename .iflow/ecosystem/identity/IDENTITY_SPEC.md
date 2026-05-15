# IDENTITY_SPEC.md - 身份目录规范（L0 入口）

> **定位**: identity 目录的指导手册，定义身份体系结构和使用方式
> **读取策略**: 本文件为 L0 入口，始终读取；L1/L2 按需读取
> **借鉴来源**: OpenClaw 分层身份设计

---

## 核心要点（L0，必须记住）

- **三层身份体系**：IDENTITY（身份）→ SOUL（人格）→ USER（用户）
- **读取顺序**：IDENTITY → SOUL → USER（身份优先）
- **初始化触发**：检测到 `[待初始化]` 或新项目时，主动询问
- **身份生效**：user.md 初始化后，AI 行为根据用户偏好调整
- **人格文件位置**：三宫六院人格文件在 `skills/three-palaces-six-courts-skill/souls/`

---

## 按需读取导航

| 场景 | 读取文件 |
|------|---------|
| 身份定义 | `@.iflow/ecosystem/identity/identity.md` |
| 协作人格 | `@.iflow/ecosystem/identity/identity.md`（协作人格章节） |
| 用户画像 | `@.iflow/ecosystem/identity/user.md` |
| 三宫六院人格文件 | `@.iflow/ecosystem/skills/three-palaces-six-courts-skill/souls/` |

## 初始化机制

| 触发条件 | AI 行为 |
|---------|--------|
| user.md 不存在 | 创建并询问初始化信息 |
| user.md 含 `[待初始化]` | 询问初始化信息 |
| 新项目/新 AI 实例 | 读取 `cold-start.md` + 触发初始化 |

**初始化流程**：AI 检测到需初始化 → 输出询问（角色/技术栈/协作偏好/当前项目）→ 用户回答 → 更新 user.md → 身份生效

**身份生效后的 AI 行为**：

| 身份要素 | 生效后的 AI 行为 |
|---------|-----------------|
| Role = 程序员 | 输出代码为主，技术细节深入 |
| Tech Stack = Java | 使用 Java 语法和框架 |
| 协作偏好 = 理解优先 | 先输出"我理解您需要..."，等待确认 |

---

**版本**: v2.1
**更新日期**: 2026-05-15
**维护者**: AI + 人类