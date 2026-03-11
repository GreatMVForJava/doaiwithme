# Skills 规范

> **定位**: 专业技能的抽象，将专业知识、工作流程、工具使用方式封装成可复用的模块
> **借鉴来源**: [Agent Skills Specification](https://agentskills.io/specification)

---

## 核心要点（必须记住）

- Skills 是专业技能的抽象，指导 AI 如何使用 Tools
- Skills 按需加载：元数据启动时加载，主体激活时加载
- 文件命名：`{name}-skill.md`（向后兼容）或目录结构 `{name}/SKILL.md`
- frontmatter 必须包含 `name` 和 `description`

---

## 一、目录结构

### 1.1 单文件结构（向后兼容）

```
skills/
├── SKILLS_SPEC.md          # 规范文档
├── web-search-skill.md     # 单文件技能
└── context-search-skill.md # 单文件技能
```

### 1.2 目录结构（可选，用于复杂技能）

```
skills/
├── SKILLS_SPEC.md          # 规范文档
├── skill-creator/          # 复杂技能目录
│   ├── SKILL.md            # 技能主体
│   ├── scripts/            # 可执行脚本
│   │   └── validate.py
│   ├── references/         # 参考资料
│   │   └── REFERENCE.md
│   └── assets/             # 静态资源
│       └── template.md
```

### 1.3 目录说明

| 目录 | 用途 | 加载时机 |
|------|------|---------|
| `scripts/` | 可执行代码 | 按需加载 |
| `references/` | 参考文档 | 按需加载 |
| `assets/` | 静态资源 | 按需加载 |

---

## 二、SKILL.md 格式

### 2.1 frontmatter（必须）

```yaml
---
name: skill-name
description: 技能描述，包含功能和使用时机。触发关键词：xxx、xxx、xxx。
license: Apache-2.0                    # 可选
compatibility: 需要网络访问             # 可选
allowed-tools: web_search, web_fetch   # 可选
---
```

### 2.2 字段定义

| 字段 | 必填 | 约束 | 说明 |
|------|------|------|------|
| `name` | ✅ 是 | 1-64字符，小写字母、数字、连字符 | 技能标识，与文件名一致 |
| `description` | ✅ 是 | 1-1024字符 | 描述功能和触发条件，包含关键词 |
| `compatibility` | ❌ 否 | 1-500字符 | 环境要求（网络、系统包等） |
| `allowed-tools` | ❌ 否 | 空格分隔的工具列表 | 预批准的工具列表 |

### 2.3 name 字段规范

- 必须是 1-64 字符
- 只能包含小写字母（`a-z`）、数字（`0-9`）和连字符（`-`）
- 不能以连字符开头或结尾
- 不能包含连续连字符（`--`）
- 必须与文件名（不含 `-skill.md`）或目录名一致

### 2.4 description 字段规范

- 必须是 1-1024 字符
- 必须描述：**功能** + **触发条件**
- 必须包含：**触发关键词**
- 格式建议：`{功能描述}。触发关键词：{关键词1}、{关键词2}、{关键词3}。`

### 2.5 使用场景区分（核心原则）

**原则：用场景区分，而非词汇堆砌**

| skill | 核心场景 | 典型表达 | 默认行为 |
|-------|---------|---------|---------|
| web-search-skill | 需要**外部知识** | 研究xx、了解xx、根据xx、基于xx | 未指定范围时的默认选择 |
| context-search-skill | 需要**内部知识** | 项目内搜索、规范在哪、经验沉淀 | 需要明确限定才触发 |

**场景判断流程**：

```
用户输入
    ↓
用户是否明确指定"项目内/内部/规范/经验"？
    ├─ 是 → context-search-skill
    └─ 否 → web-search-skill（默认）
```

**组合使用场景**：

```
"根据龙虾的思想，内化为协作方式"
     ↓              ↓
 外部知识需求    内部知识需求
     ↓              ↓
 web-search    context-search
     ↓              ↓
   搜索龙虾思想   搜索协作规范
     ↓              ↓
        整合输出
```

**错误做法**：在 description 里堆砌关键词
```yaml
# 错误：只列举词汇，没有场景区分
description: ...触发关键词：搜索、查找、研究、了解、查询、根据、基于...
```

**正确做法**：描述场景和意图
```yaml
# web-search-skill
description: 网络搜索技能。当用户需要**外部知识**时使用。默认行为：用户未明确指定搜索范围时，优先使用网络搜索。

# context-search-skill
description: 项目内搜索技能。当用户需要**内部知识**时使用。明确限定：用户明确指定搜索范围为项目内部时使用。
```

---

## 三、主体内容

### 3.1 推荐章节

```markdown
# {技能名称} Skill

## 技能描述
简要描述技能的功能和用途

## 触发条件
在什么情况下应该调用这个技能

## 输入参数
技能需要的输入参数

## 输出结果
技能返回的结果格式

## 实现步骤
具体的实现步骤

## 注意事项
使用技能时的注意事项
```

### 3.2 内容规范

- 主体内容建议 < 5000 tokens
- 建议保持 SKILL.md < 500 行
- 详细参考材料应移至 `references/` 目录

---

## 四、渐进式披露

### 4.1 加载层级

| 层级 | 内容 | 加载时机 | Token 消耗 |
|------|------|---------|-----------|
| 元数据 | `name` + `description` | 启动时加载所有 | ~100 |
| 指令 | SKILL.md 主体 | 技能激活时加载 | ~1000 |
| 资源 | scripts/references/assets | 按需加载 | 按需 |

### 4.2 上下文效率原则

- **元数据精简**：description 包含触发关键词，帮助 AI 识别
- **指令聚焦**：主体内容聚焦核心步骤，避免冗余
- **资源分离**：详细参考移至 references/，按需加载

---

## 五、验证规范

### 5.1 frontmatter 验证

| 检查项 | 规则 |
|-------|------|
| name 格式 | 小写字母、数字、连字符，不超64字符 |
| name 一致性 | 必须与文件名或目录名一致 |
| description 长度 | 不超过1024字符 |
| description 关键词 | 必须包含触发关键词 |

### 5.2 文件验证

| 检查项 | 规则 |
|-------|------|
| 章节完整 | 包含必要章节 |
| 步骤可执行 | 实现步骤具体可执行 |
| 参数明确 | 输入参数定义清晰 |

---

## 六、Skills 类型

### 6.1 工具调用型

调用外部工具（如 web_search、web_fetch）

**示例**：`web-search-skill`

### 6.2 文档搜索型

搜索项目文档

**示例**：`context-search-skill`

### 6.3 任务执行型

执行特定任务

**示例**：`skill-creator`

---

## 七、调用流程

```text
1. AI 识别需求
      ↓
2. 匹配 description 中的触发关键词
      ↓
3. 加载 SKILL.md 主体
      ↓
4. 执行实现步骤
      ↓
5. 返回结果
```

---

## 八、创建新 Skills

### 8.1 步骤

1. 确定技能类型和名称
2. 创建文件或目录
3. 编写 frontmatter（name + description + 触发关键词）
4. 编写主体内容
5. 验证规范

### 8.2 示例

**单文件**：
```
skills/new-skill.md
```

**目录结构**：
```
skills/new-skill/
├── SKILL.md
├── scripts/
└── references/
```

---

## 九、沉淀原则

| 场景 | 沉淀动作 |
|------|---------|
| 发现新技能需求 | 创建新 skill 文件或目录 |
| 技能验证有效 | 更新描述和步骤 |
| 技能不再需要 | 标记废弃 |

**核心原则**：技能必须可复用，步骤必须可执行，沉淀必须持续迭代。

---

## 十、与 Agent Skills 的关系

| 维度 | Agent Skills | 当前 Skills |
|------|-------------|-------------|
| 定位 | 运行时框架 | 文档工程 |
| 目标 | Agent 自动调用 | AI 协作指导 |
| 触发 | description 自动匹配 | AI 主动识别 |
| 兼容性 | 完全兼容格式 | 可选采用 |

**关键**：当前 Skills 借鉴 Agent Skills 格式规范，但定位不同。Agent Skills 用于运行时自动调用，当前 Skills 用于协作指导传递。

---

## 十一、文件列表

1. `@.iflow/context/skills/web-search-skill.md` - 网络搜索技能（外部知识、默认搜索）
2. `@.iflow/context/skills/context-search-skill.md` - 项目内搜索技能（内部知识、明确限定）
3. `@.iflow/context/skills/skill-creator-skill.md` - 技能创建技能（创建/更新/验证技能）

---

**最后更新**：2026-03-11
**版本**：10.0
**借鉴来源**: [Agent Skills Specification](https://agentskills.io/specification)
