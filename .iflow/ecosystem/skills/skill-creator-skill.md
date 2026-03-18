---
name: skill-creator-skill
description: 技能创建技能，用于创建、更新、验证 Skills 规范文件。触发关键词：创建技能、新建skill、验证skill、技能规范、SKILL.md。
allowed-tools: read_file, write_file, search_file_content, glob
---

# Skill Creator Skill

## 技能描述
技能创建技能：帮助 AI 创建、更新、验证 Skills 规范文件，确保符合 Agent Skills 标准。

## 触发条件
- 需要创建新的 Skill
- 需要更新现有 Skill 的格式
- 需要验证 Skill 是否符合规范

## 工具接口定义

### read_file

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| absolute_path | string | ✅ | 文件绝对路径 |
| limit | number | ❌ | 最大读取行数（与 offset 配合分页） |
| offset | number | ❌ | 起始行号，0-based |

**调用示例**：
```
read_file(
  absolute_path="/Users/code/dhealth-agent-server/.iflow/ecosystem/skills/web-search-skill.md"
)
```

### write_file

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file_path | string | ✅ | 文件绝对路径 |
| content | string | ✅ | 文件内容 |

**调用示例**：
```
write_file(
  file_path="/Users/code/dhealth-agent-server/.iflow/ecosystem/skills/new-skill.md",
  content="---\nname: new-skill\n..."
)
```

### search_file_content

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| pattern | string | ✅ | 正则表达式模式或字面字符串 |
| path | string | ❌ | 搜索路径，默认当前工作目录 |
| include | string | ❌ | 文件过滤，如 `*.md` |

**调用示例**：
```
search_file_content(
  pattern="name:.*skill",
  path="/Users/code/dhealth-agent-server/.iflow/ecosystem/skills",
  include="*.md"
)
```

### glob

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| pattern | string | ✅ | glob 模式，如 `**/*-skill.md` |
| path | string | ❌ | 搜索路径，默认根目录 |

**调用示例**：
```
glob(
  pattern="**/*-skill.md",
  path="/Users/code/dhealth-agent-server/.iflow/ecosystem/skills"
)
```

## 工具边界与组合方式

### 工具职责

| 工具 | 职责 | 输入 | 输出 | 何时使用 |
|------|------|------|------|---------|
| `read_file` | 读取现有 Skill | 文件绝对路径 | Skill 内容 | 验证/更新时 |
| `write_file` | 创建/更新 Skill | 文件路径 + 内容 | 操作结果 | 创建/更新时 |
| `search_file_content` | 搜索现有 Skill | 正则模式 | 匹配列表 | 检查重复 |
| `glob` | 查找 Skill 文件 | glob 模式 | 文件列表 | 检查现有 Skill |

### 调用模式

**顺序调用为主**：

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  glob / search   │ ──→ │   read_file      │ ──→ │   write_file     │
│  （查找现有）     │     │  （读取内容）     │     │  （创建/更新）    │
└──────────────────┘     └──────────────────┘     └──────────────────┘
```

### 决策树

```
用户请求创建/更新/验证 Skill
              │
              ▼
┌─────────────────────────────┐
│ 检查现有 Skill 是否存在？    │
│ (glob 或 search_file_content)│
└───────────┬─────────────────┘
            │
    ┌───────┴───────┐
    │ 存在          │ 不存在
    ▼               ▼
┌─────────────┐  ┌─────────────┐
│ read_file   │  │ 直接创建    │
│ 读取内容    │  │ write_file  │
└──────┬──────┘  └─────────────┘
       │
       ▼
┌─────────────────────────────┐
│ 更新: write_file            │
│ 验证: 输出验证报告           │
└─────────────────────────────┘
```

### 组合场景

| 场景 | 调用顺序 | 说明 |
|------|---------|------|
| 创建新 Skill | `glob` → `write_file` | 先检查是否已存在 |
| 更新 Skill | `read_file` → `write_file` | 先读取再更新 |
| 验证 Skill | `read_file` → 输出报告 | 只读取不修改 |
| 检查重复 | `search_file_content` | 搜索是否有类似 Skill |

### 并行可能性

| 工具对 | 可否并行 | 原因 |
|-------|---------|------|
| `glob` + `search_file_content` | ✅ 可并行 | 都是检查，无依赖 |
| `read_file` + `write_file` | ❌ 不可并行 | write 需要读取结果 |

## 输入参数
- `action`：操作类型（create / update / validate）
- `name`：技能名称
- `content`：技能内容（create 时必填）

## 输出结果
- 操作结果
- 验证报告（validate 时）

## 实现步骤

### 步骤 1：确定操作类型

根据用户请求确定操作类型：
- `create`：创建新技能
- `update`：更新现有技能
- `validate`：验证技能规范

### 步骤 2：执行操作

**创建技能**：
1. 验证 name 符合规范（小写字母、数字、连字符）
2. 生成 frontmatter（name + description + 触发关键词）
3. 生成主体内容框架
4. 写入文件 `{name}-skill.md`

**更新技能**：
1. 读取现有技能文件
2. 更新 frontmatter（添加触发关键词）
3. 更新主体内容
4. 验证更新后符合规范

**验证技能**：
1. 读取技能文件
2. 验证 frontmatter 格式
3. 验证 name 一致性
4. 验证 description 包含触发关键词
5. 输出验证报告

### 步骤 3：输出结果

输出操作结果或验证报告。

## 验证规范

### frontmatter 验证

| 检查项 | 规则 | 通过条件 |
|-------|------|---------|
| name 格式 | 小写字母、数字、连字符 | 符合正则 `^[a-z0-9][a-z0-9-]*[a-z0-9]$` |
| name 长度 | 1-64字符 | `len(name) <= 64` |
| name 一致性 | 与文件名一致 | `{name}-skill.md` 或 `{name}/SKILL.md` |
| description 长度 | 1-1024字符 | `len(description) <= 1024` |
| description 关键词 | 包含触发关键词 | 包含"触发关键词：" |

### 内容验证

| 检查项 | 规则 | 通过条件 |
|-------|------|---------|
| 章节完整 | 包含必要章节 | 包含"技能描述"、"触发条件" |
| 步骤可执行 | 步骤具体 | 包含"步骤"字样 |

## 示例输出

### 验证报告

```markdown
## Skills 验证报告

### web-search-skill.md
| 检查项 | 结果 | 说明 |
|-------|------|------|
| name 格式 | ✅ | web-search-skill |
| name 一致性 | ✅ | 文件名匹配 |
| description 关键词 | ✅ | 包含"触发关键词" |
| 章节完整 | ✅ | 包含必要章节 |

### context-search-skill.md
| 检查项 | 结果 | 说明 |
|-------|------|------|
| name 格式 | ✅ | context-search-skill |
| name 一致性 | ✅ | 文件名匹配 |
| description 关键词 | ✅ | 包含"触发关键词" |
| 章节完整 | ✅ | 包含必要章节 |

**验证结果**：全部通过 ✅
```

## 注意事项

1. **name 命名规范**：必须符合小写字母、数字、连字符规范
2. **description 触发关键词**：必须包含触发关键词，帮助 AI 识别
3. **向后兼容**：现有 `{name}-skill.md` 格式保持不变
4. **目录结构**：复杂技能可使用 `{name}/SKILL.md` 目录结构

---

## 踩坑清单模板

> **来源**: Anthropic 工程师实战经验
> **价值**: Skill 中信息密度最高的部分，告诉 AI 别踩哪些雷

### 创建 Skill 前必须检查

| 检查项 | 问题 | 正确做法 |
|-------|------|---------|
| **场景频率** | 该场景是否频繁出现？ | 频繁场景才值得创建 Skill |
| **已有覆盖** | 现有 Skill 是否已覆盖？ | 先检查现有 Skill，避免重复 |
| **工具组合** | 工具组合是否产生新能力？ | 组合价值高才值得封装 |
| **可复用性** | Skill 是否可被其他 AI 复用？ | 通用性是 Skill 的核心价值 |

### 常见踩坑案例

| 坑 | 表现 | 解决方案 |
|---|------|---------|
| **描述太抽象** | "用于搜索" | 描述具体场景："当用户需要**外部知识**时使用" |
| **触发关键词堆砌** | "搜索、查找、研究、了解、查询..." | 用场景区分，不要词汇堆砌 |
| **步骤不可执行** | "根据情况处理" | 具体到："调用 web_search 工具" |
| **缺少输入输出定义** | 没说需要什么、返回什么 | 必须定义 `输入参数` 和 `输出结果` |
| **工具列表不完整** | 只列了主要工具 | 列出所有可能用到的工具，包括辅助工具 |

### Skill 模板（含踩坑检查）

```markdown
---
name: {skill-name}
description: {功能描述}。当用户需要**{场景}**时使用。触发关键词：{关键词1}、{关键词2}。
allowed-tools: {tool1}, {tool2}, {tool3}
---

# {Skill 名称}

## 技能描述
{一句话描述功能和用途}

## 使用场景
| 场景 | 用户意图 | 示例 |
|------|---------|------|
| {场景1} | {意图1} | "{示例1}" |
| {场景2} | {意图2} | "{示例2}" |

## 触发条件
- {条件1}
- {条件2}

## 输入参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| {param} | {type} | ✅/❌ | {说明} |

## 输出结果
{输出格式描述}

## 实现步骤
### 步骤 1：{步骤名称}
{具体操作}

### 步骤 2：{步骤名称}
{具体操作}

## 踩坑清单（必须填写）
| 坑 | 解决方案 |
|---|---------|
| {常见问题1} | {解决方案1} |
| {常见问题2} | {解决方案2} |
```

---

**最后更新**：2026-03-18
**版本**：3.0
