# start.md - AI 行为启动入口

> **定位**: AI 与人类程序员协作的核心入口，定义强制流程和目录索引
> **使用者**: AI + 人类共用
> **使用方式**: 每次任务请求附带 "依照@.iflow/start.md（你的行为规范）"

---

## 核心思想

本目录（`.iflow/`）和 `app-demand/` 是 AI 与人类程序员交互的核心内容，内容包括概念、规范、流程、rule、skill 等。

**协作内容分类**（详见 `@.iflow/context/concept/GLOBAL_CONCEPTS.md `）：

| 分类 | 使用者 | 核心特征 | 典型文件 |
|------|--------|---------|---------|
| **AI专用** | AI | 跨AI模型可用、人类不需关心 | `cold-start.md`, `*-skill.md` |
| **共用** | AI + 人类 | 人类可全链路指导、追踪AI行为 | `start.md`, `RULE_SPEC.md` |
| **人类专用** | 人类 | 简单明了、程序员间沟通 | `需求冷启动.md`, `测试问题.md` |

**核心原则**：共用内容是最重要的核心，AI每次行为后检查是否需要沉淀更新。

---

## 一、强制启动流程

**AI 收到任何任务时，必须依次执行，每步必须有输出物：**

``` text
预检 → 确认 → 规划 → 执行 → 自检 → 沉淀
```

### 1.0 预检

**核心问题：是否有概念阻塞？这是什么类型的操作？需要读取哪些文件？**

**执行顺序**：
1. **概念阻塞检查**：是否有不理解的概念？→ 先读取 `@.iflow/context/concept/GLOBAL_CONCEPTS.md `
2. **意图判断**：根据理解的需求，判断操作意图
3. **文件读取**：根据意图映射必须读取的文件列表

**意图-文件映射表**：

| 操作意图 | 必须读取的文件 |
|---------|---------------|
| 修改规范文件 | `@.iflow/start.md `, `@.iflow/endPoint.md `, 相关规范文件 |
| 修改代码文件 | `@.iflow/context/rule/ai-coding/CODING_SPEC.md `, 相关代码文件 |
| 沉淀经验 | `@.iflow/context/experience/collaboration-method.md `, `@.iflow/context/experience/EXPERIENCE_SPEC.md ` |
| 创建文档 | 检查规则8，确认是否允许 |

**输出格式**：
```
## 预检
- 概念阻塞：[无 / 有，概念：xxx，已读取：@GLOBAL_CONCEPTS.md，已理解：xxx]
- 操作意图：[修改规范/修改代码/沉淀经验/创建文档]
- 必须读取：
  - @.iflow/context/xxx/xxx.md 
  - @.iflow/context/xxx/xxx.md 
- 已读取摘要：  - @文件1：核心内容概述
  - @文件2：核心内容概述
```

**强制要求**：
- 必须先检查概念阻塞，有阻塞先消除（读取 GLOBAL_CONCEPTS.md）
- 必须先判断意图，再输出文件列表
- 必须实际读取文件，不能省略
- 必须输出文件内容摘要，证明已读取
- 文件路径必须是全路径+@前缀+空格结尾
- 未输出摘要或未消除阻塞视为流程未完成

### 1.1 规则清单

**核心问题：本次任务需要遵守哪些规则？**

**必须输出**：读取 `@.iflow/context/rule/ai-coding/CODING_SPEC.md ` 和 `@.iflow/context/rule/ai-collaboration/AI_COLLABORATION_SPEC.md `，输出适用规则清单

**输出格式**：
```
## 规则清单

已读取规则文件：
- @.iflow/context/rule/ai-coding/CODING_SPEC.md 
- @.iflow/context/rule/ai-collaboration/AI_COLLABORATION_SPEC.md 

适用规则（根据操作类型判断）：
| 规则编号 | 规则名称 | 是否适用 | 判断依据 |
|---------|---------|---------|---------|
| 规则4 | 联动完整性 | 是/否 | 本次是否涉及任何修改操作 |
| 规则9 | 修改后自检 | 是/否 | 本次是否涉及代码修改 |
| ... | ... | ... | ... |
```

**强制要求**：
- 必须实际读取规则文件，不能省略
- 必须根据操作类型判断是否适用
- 未读取规则文件视为流程未完成

| 步骤 | 必须输出 | 规范依据 |
|------|---------|---------|
| **预检** | 操作意图 + 必须读取文件列表 + 已读取摘要 | 本节 1.0 |
| **规则清单** | 适用规则清单 | 本节 1.1 |
| **确认** | 需求理解复述 + 理解边界 | `@.iflow/endPoint.md ` |
| **规划** | 联动检查清单 + 执行计划 | `@.iflow/context/experience/collaboration-method.md ` |
| **执行** | 修改文件列表 + 编译结果 | `@.iflow/endPoint.md ` |
| **自检** | 检查表 | `@.iflow/endPoint.md ` |
| **沉淀** | 文档更新路径 | `@.iflow/endPoint.md ` |

**详细流程**: `@.iflow/endPoint.md `
**AI协作规范**: `@.iflow/context/rule/RULE_SPEC.md `
**编码规范**: `@.iflow/context/rule/ai-coding/CODING_SPEC.md `
**协作方法**: `@.iflow/context/experience/collaboration-method.md `

---

## 二、目录索引

### 2.1 .iflow/ 目录（AI 协作配置）

| 文件/目录 | 使用者 | 命名类型 | 用途 |
|----------|--------|-------|------|
| `start.md` | 共用 | 驼峰 | AI 行为启动入口 |
| `endPoint.md` | 共用 | 驼峰 | 执行流程详细规范 |
| `备忘录.md` | 人类 | 中文 | 人类备忘录 |
| `context/` | AI | - | 上下文知识库 |
| ├─ `concept/` | AI | - | 概念定义 |
| │   └─ `GLOBAL_CONCEPTS.md` | 共用 | 大写下划线 | 全局概念定义 |
| ├─ `experience/` | AI | - | 经验沉淀 |
| │   ├─ `EXPERIENCE_SPEC.md` | AI | 大写下划线 | 经验快速入口 |
| │   ├─ `infrastructure.md` | AI | 小写短横杠 | 目录设计、Skills设计 |
| │   ├─ `cold-start.md` | AI | 小写短横杠 | 三层防御体系 |
| │   └─ `collaboration-method.md` | AI | 小写短横杠 | 乔哈里窗、苏格拉底、联动检查 |
| ├─ `issues/` | AI | - | 问题孵化器 |
| │   └─ `ISSUES_SPEC.md` | AI | 大写下划线 | issues目录规范 |
| ├─ `rule/` | AI | - | 规则目录 |
| │   ├─ `RULE_SPEC.md` | 共用 | 大写下划线 | 规则总入口 |
| │   ├─ `ai-collaboration/` | AI | - | AI协作规范 |
| │   │   ├─ `AI_COLLABORATION_SPEC.md` | 共用 | 大写下划线 | AI协作规范（核心准则） |
| │   │   ├─ `04-linkage-integrity/` | 共用 | 编号-简写 | 规则4详解 |
| │   │   ├─ `05-comprehensive-analysis/` | 共用 | 编号-简写 | 规则5详解 |
| │   │   ├─ `07-markdown-format/` | 共用 | 编号-简写 | 规则7详解 |
| │   │   └─ `09-post-modification-check/` | 共用 | 编号-简写 | 规则9详解 |
| │   └─ `ai-coding/` | AI | - | 编码规范 |
| │       ├─ `CODING_SPEC.md` | 共用 | 大写下划线 | 编码规范（核心准则） |
| │       ├─ `17-javadoc-comment/` | 共用 | 编号-简写 | 规则17详解 |
| │       ├─ `20-database-idempotence/` | 共用 | 编号-简写 | 规则20详解 |
| │       ├─ `22-method-consistency/` | 共用 | 编号-简写 | 规则22详解 |
| │       ├─ `23-modification-completeness/` | 共用 | 编号-简写 | 规则23详解 |
| │       ├─ `25-concurrency-safety/` | 共用 | 编号-简写 | 规则25详解 |
| │       ├─ `26-interface-parameter-validation/` | 共用 | 编号-简写 | 规则26详解 |
| │       └─ `27-naming-semantic/` | 共用 | 编号-简写 | 规则27详解 |
| └─ `skills/` | AI | - | 技能目录 |
|     ├─ `SKILLS_SPEC.md` | AI | 大写下划线 | Skills规范 |
|     └─ `*-skill.md` | AI | 小写短横杠 | 具体技能定义 |

### 2.2 app-demand/ 目录（业务需求管理）

| 文件/目录 | 使用者 | 命名类型 | 用途 |
|----------|--------|---------|------|
| `APP_DEMAND_SPEC.md` | 共用 | 大写下划线 | 需求目录规范 |
| `requirementsGuidelines.md` | 共用 | 驼峰 | 需求编写准则 |
| `requirementsTemplate.md` | 共用 | 驼峰 | 需求文档模板 |
| `YYYY-MM-DD/` | 共用 | 日期 | 按日期组织的需求 |
| ├─ `需求冷启动.md` | 人类 | 中文 | 该需求的冷启动文档 |
| ├─ `产品/` | 人类 | 中文 | 产品需求文档 |
| │   └─ `产品需求.md` | 人类 | 中文 | 具体产品需求 |
| └─ `测试/` | 人类 | 中文 | 测试相关文档 |
|     └─ `测试问题.md` | 人类 | 中文 | 测试问题记录 |

---

## 三、命名规范

| 类型 | 命名规范 | 示例 | 用途 |
|------|---------|------|------|
| AI专用-核心准则 | 全大写+下划线+上下文 | `SKILLS_SPEC.md`, `EXPERIENCE_SPEC.md` | 规范当前目录层级 |
| AI专用-执行帮助 | 全小写+短横杠 | `cold-start.md`, `context-search-skill.md` | AI执行行为的帮助 |
| 共用文件 | 首字母小写驼峰 | `start.md`, `endPoint.md`, `requirementsGuidelines.md` | 人机交互形式 |
| 人类专用 | 中文命名 | `需求冷启动.md`, `测试问题.md` | 仅在 app-demand/需求目录中 |
| 规则详解目录 | `{编号}-{英文简写}` | `12-javadoc-comment/` | 规则详解目录命名 |

**案例**：`prompt.md` 曾被AI误认为是共用文件（因为使用了驼峰命名），但实际它是人类专用文件。正确命名应为 `备忘录.md`。

---

## 四、沉淀路径

**核心原则**：issues 是孵化器，不是墓地。问题必须流动，成熟后必须固化。

### 问题生命周期

``` text
发现问题 → 记录分析 → 验证成熟 → 固化迁移 → 清理删除
```

| 阶段 | 操作 | 沉淀路径 |
|------|------|---------|
| **发现问题** | 记录到 issues | `@.iflow/context/issues/YYYY-MM-DD-问题关键词.md ` |
| **验证成熟** | 预防措施验证有效 | 在 issues 文件中记录验证结果 |
| **固化迁移** | 迁移到规则或方法论 | 更新 `@.iflow/context/rule/RULE_SPEC.md ` 或 `@.iflow/context/experience/collaboration-method.md ` |
| **清理删除** | 问题已固化 | 删除对应的 issues 文件 |

### 固化目标对照

| 问题类型 | 固化目标 | 示例 |
|---------|---------|------|
| 每次必须检查 | `@.iflow/context/rule/RULE_SPEC.md ` | 规则0、规则4、规则6 |
| 方法论层面 | `@.iflow/context/experience/collaboration-method.md ` | 联动检查方法论、乔哈里窗 |
| 经验层面 | `@.iflow/context/experience/*.md ` | 冷启动最佳实践 |

### 其他沉淀场景

| 场景 | 沉淀路径 | 示例 |
|------|---------|------|
| 提炼经验 | `@.iflow/context/experience/*.md ` | 更新 `@.iflow/context/experience/collaboration-method.md ` |
| 更新索引 | `@.iflow/context/experience/EXPERIENCE_SPEC.md ` | 添加新经验条目 |
| 需求相关 | `@app-demand/YYYY-MM-DD/需求名称/需求冷启动.md ` | 记录新发现 |

### 场景标签格式（情境记忆法）

**使用场景**：沉淀经验、记录问题时，必须使用场景标签格式

``` text
## 场景标签
- 触发条件：什么时候会遇到这个场景？
- 问题类型：这是什么类型的问题？

## 场景描述
描述具体的业务场景和上下文

## 解决方案
描述如何解决这个问题

## 关联经验
链接到相关的经验文档
```

**详细说明**：`@.iflow/context/experience/collaboration-method.md ` 

---

## 五、快速参考

**AI 执行任务时**:
1. 读取 `@.iflow/start.md ` → 确认流程
2. 读取 `@.iflow/endPoint.md ` → 了解详细步骤
3. 读取 `@.iflow/context/rule/RULE_SPEC.md ` → 遵守AI协作规范（**必须同时读取 ai-coding/CODING_SPEC.md**）
4. 读取 `@.iflow/context/rule/ai-coding/CODING_SPEC.md ` → 遵守编码规范
5. 读取 `@.iflow/context/experience/collaboration-method.md ` → 应用联动检查

**人类创建需求时**:
1. 参考 `@app-demand/requirementsGuidelines.md `
2. 使用 `@app-demand/requirementsTemplate.md `
3. 创建 `@app-demand/YYYY-MM-DD/需求名称/需求冷启动.md `

---

**版本**: v1.5
**创建日期**: 2026-02-25
**更新日期**: 2026-03-04
**维护者**: AI + 人类
