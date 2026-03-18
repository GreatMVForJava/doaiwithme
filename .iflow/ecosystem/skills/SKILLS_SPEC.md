# Skills 规范

> **定位**: 专业技能的抽象，将专业知识、工作流程、工具使用方式封装成可复用的模块
> **借鉴来源**: [Agent Skills Specification](https://agentskills.io/specification)

---

## 核心要点（必须记住）

- Skills 是专业技能的抽象，指导 AI 如何使用 Tools
- Skills 按需加载：元数据启动时加载，主体激活时加载
- **三层信息模型**: 概念见 `@.iflow/ecosystem/concept/token-economics/three-layer-model.md`，实现见本文件第四节
- **Token 效率**: 元数据精简、指令聚焦、资源分离，避免一次性加载全部内容
- 文件命名：`{name}-skill.md`（向后兼容）或目录结构 `{name}/SKILL.md`
- frontmatter 必须包含 `name` 和 `description`
- **创建 Skill 时必须先读取 skill-creator-skill.md**

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

### 4.3 强制调用规则（必须遵守）

**核心原则**：渐进式披露要求 AI 在对应步骤强制调用对应文件，不得跳过。

#### 规则1：创建 Skill 时强制调用

```
用户请求：创建新 Skill
     ↓
AI 识别意图 → 必须读取 @.iflow/ecosystem/skills/skill-creator-skill.md
     ↓
按照 skill-creator-skill 的步骤执行
     ↓
输出验证报告
```

**检查点**：
- [ ] 是否读取了 skill-creator-skill.md？
- [ ] 是否按照其步骤执行？
- [ ] 是否输出了验证报告？

#### 规则2：使用 Skill 时按需加载

```
AI 识别需求
     ↓
匹配 description 中的触发关键词（元数据层）
     ↓
是否需要详细步骤？
     ├─ 是 → 加载 SKILL.md 主体（指令层）
     └─ 否 → 仅使用元数据执行
     ↓
是否需要参考资料？
     ├─ 是 → 加载 references/（资源层）
     └─ 否 → 完成
```

**检查点**：
- [ ] 是否先匹配了 description？
- [ ] 是否按需加载了指令层？
- [ ] 是否只在需要时加载资源层？

#### 规则3：@ 引用强制加载

**当用户或文档使用 `@文件路径` 引用时，AI 必须读取该文件。**

```
用户输入："依照 @.iflow/endPoint.md 执行"
     ↓
AI 识别 @ 引用
     ↓
必须读取 @.iflow/endPoint.md
     ↓
按照文件内容执行
```

**检查点**：
- [ ] 是否识别了 @ 引用？
- [ ] 是否实际读取了文件？
- [ ] 是否输出了文件内容摘要？

### 4.4 渐进式披露检查表

**AI 在每个阶段必须输出**：

``` text
### 渐进式披露检查

| 检查项 | 状态 | 证据 |
|-------|------|------|
| 元数据匹配 | ✅/❌ | 匹配到哪个 skill 的 description？ |
| 指令层加载 | ✅/❌ | 是否需要加载 SKILL.md 主体？ |
| 资源层加载 | ✅/❌ | 是否需要加载 references/？ |
| @ 引用处理 | ✅/❌ | 是否识别并读取了 @ 引用的文件？ |
```

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

## 八、创建新 Skills（强制流程）

> **关键**：创建 Skill 时，AI **必须**先调用 `@.iflow/ecosystem/skills/skill-creator-skill.md`，按照其步骤执行。

### 8.1 强制执行流程

```
用户请求创建 Skill
         │
         ▼
┌─────────────────────────────────────┐
│ 步骤1：识别意图                       │
│ AI 输出："检测到创建 Skill 需求"        │
└─────────────────┬───────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│ 步骤2：强制读取 skill-creator-skill   │
│ AI 输出："正在读取 @.iflow/ecosystem/   │
│ skills/skill-creator-skill.md"       │
└─────────────────┬───────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│ 步骤3：按照 skill-creator-skill 执行  │
│ - 确定 action 类型                    │
│ - 验证 name 规范                      │
│ - 生成 frontmatter                   │
│ - 编写主体内容                        │
│ - 输出验证报告                        │
└─────────────────┬───────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│ 步骤4：输出验证报告                    │
│ 格式参照 skill-creator-skill 示例     │
└─────────────────────────────────────┘
```

### 8.2 检查点（必须输出）

**创建 Skill 时，AI 必须输出**：

``` text
### Skill 创建检查

| 检查项 | 状态 | 证据 |
|-------|------|------|
| 是否读取了 skill-creator-skill.md | ✅/❌ | 输出文件内容摘要 |
| name 格式验证 | ✅/❌ | 符合规范/不符合规范原因 |
| description 包含触发关键词 | ✅/❌ | 包含哪些关键词 |
| allowed-tools 定义 | ✅/❌ | 包含哪些工具 |
| 验证报告输出 | ✅/❌ | 是否输出了验证报告 |
```

### 8.3 禁止行为

**创建 Skill 时，AI 禁止**：

| 禁止行为 | 原因 |
|---------|------|
| 跳过 skill-creator-skill 直接创建 | 会导致格式不规范 |
| 不输出验证报告 | 无法确认是否符合规范 |
| 在 Skill 内部引用其他 Skill | 破坏 Skill 独立性 |

### 8.4 步骤概要（快速参考）

1. **强制**：读取 `@.iflow/ecosystem/skills/skill-creator-skill.md`
2. 确定技能类型和名称
3. 创建文件或目录
4. 编写 frontmatter（name + description + 触发关键词）
5. 编写主体内容
6. 输出验证报告

### 8.5 示例

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

## 十一、Skills 关系管理

> **原则**：每个 Skill 独立，不在 Skill 内部引用其他 Skill。所有 Skill 之间的关系由本文件（SKILLS_SPEC.md）统一管理。

### 规范与执行的关系

| 文件 | 定位 | 内容 | 使用时机 |
|------|------|------|---------|
| **SKILLS_SPEC.md** | 规范标准 | 定义格式、验证规则、创建步骤 | AI 需要了解规范时读取 |
| **skill-creator-skill** | 执行工具 | 具体执行创建/更新/验证 | **AI 创建新 skill 时必须调用** |

**强制规则**：创建 skill 时，AI **必须**先调用 `@.iflow/ecosystem/skills/skill-creator-skill.md`。

### Skills 边界区分

| skill | 核心场景 | 输入 | 输出 | 典型表达 |
|-------|---------|------|------|---------|
| **web-search-skill** | 搜索外部信息 | 查询词 | 链接摘要 | "搜索xx"、"了解xx" |
| **web-content-extraction-skill** | 解析页面内容 | URL | 完整内容 | "解析网页"、"抓取文章" |
| **context-search-skill** | 搜索内部知识 | 查询词 | 项目文档 | "项目内搜索"、"规范在哪" |
| **skill-creator-skill** | 创建技能 | 技能定义 | skill文件 | "创建skill"、"验证skill" |

### Skills 组合使用场景

| 场景 | 推荐组合 | 说明 |
|------|---------|------|
| "研究龙虾思想" | web-search → web-content-extraction | 先搜索找到链接，再解析完整内容 |
| "解析微信公众号文章" | web-content-extraction | 直接使用，无需搜索 |
| "了解项目规范" | context-search | 只需内部搜索 |
| "创建新技能" | skill-creator | 创建时必须调用 |

### 协作链参考图

```
用户需求：获取外部信息
         │
         ▼
┌─────────────────────────────┐
│ 阶段1：搜索信息              │
│ 使用：web-search-skill       │
│ 输入：查询词                  │
│ 输出：链接列表                │
└─────────────┬───────────────┘
               │ 如需完整内容
               ▼
┌─────────────────────────────┐
│ 阶段2：解析页面              │
│ 使用：web-content-extraction │
│ 输入：URL                    │
│ 输出：完整内容                │
└─────────────────────────────┘

用户需求：获取内部信息
         │
         ▼
┌─────────────────────────────┐
│ 使用：context-search-skill   │
│ 输入：查询词                  │
│ 输出：项目文档                │
└─────────────────────────────┘
```

## 十三、工具清单索引

> **来源**: OpenClaw Skills 完全指南 + 当前系统可用工具
> **目的**: 为 Skill 设计提供工具参考，帮助 AI 选择合适的工具组合

### 13.1 搜索类工具

| 工具 | 功能 | 国内可用 | API Key | Skill 应用 |
|------|------|---------|---------|-----------|
| `web_search` | 网页搜索 | 需代理 | Brave API Key | web-search-skill |
| `web_fetch` | 网页抓取 | ✅ 直接可用 | 无需 | web-content-extraction |
| `firecrawl` | JS渲染网页抓取 | ✅ 直接可用 | Firecrawl API Key | 复杂网页解析 |
| `tavily` | AI优化搜索 | 需代理 | Tavily API Key | 搜索增强 |

### 13.2 网页操作类工具（重点）

| 工具 | 功能 | 复杂度 | 适用场景 | 与其他工具组合 |
|------|------|--------|---------|---------------|
| `browser` | Playwright完整自动化 | ⭐⭐⭐⭐ | 复杂交互、登录态、动态加载 | + screenshot → 截图报告 |
| `agent-browser` | 无头浏览器控制 | ⭐⭐⭐ | JS渲染、无复杂交互 | + web_fetch → 混合策略 |
| `browsy` | 轻量网页浏览 | ⭐⭐ | 静态内容、快速抓取 | 单独使用即可 |
| `playwright-cli` | Playwright CLI封装 | ⭐⭐⭐ | 命令行自动化 | + shell → 脚本化 |
| `web-scraper` | 结构化数据采集 | ⭐⭐⭐ | 表格、列表、多页数据 | + excel-handler → 导出 |
| `screenshot-skill` | 网页截图 | ⭐ | 页面快照、报告截图 | + browser → 全页截图 |

**网页工具选择决策树**：

```
需要处理网页
    │
    ├─ 只需截图 → screenshot-skill
    │
    ├─ 静态内容 → browsy 或 web_fetch
    │
    ├─ 需要JS渲染 → agent-browser
    │
    ├─ 需要复杂交互 → browser + playwright-cli
    │
    └─ 需要结构化采集 → web-scraper
```

### 13.3 文件处理类工具（重点）

| 工具 | 功能 | 复杂度 | 适用场景 | 与其他工具组合 |
|------|------|--------|---------|---------------|
| `nano-pdf` | PDF自然语言编辑 | ⭐⭐ | 页面合并、拆分、水印 | + web_fetch → 下载后编辑 |
| `pdf-processor` | PDF处理工具集 | ⭐⭐ | OCR、文本提取 | + ocr → 扫描版PDF |
| `excel-handler` | Excel读写操作 | ⭐⭐ | 数据表格、报表 | + web-scraper → 数据导出 |
| `csv-data-summarizer` | CSV数据分析 | ⭐ | 数据统计、聚合 | + code_execution → 复杂分析 |
| `file-manager` | 文件系统管理 | ⭐ | 文件操作、目录管理 | + shell → 批量操作 |

**文件工具选择决策树**：

```
需要处理文件
    │
    ├─ PDF编辑 → nano-pdf
    │
    ├─ PDF解析 → pdf-processor
    │
    ├─ Excel操作 → excel-handler
    │
    ├─ CSV分析 → csv-data-summarizer
    │
    └─ 文件管理 → file-manager
```

### 13.4 代码执行类工具

| 工具 | 功能 | 适用场景 |
|------|------|---------|
| `code_execution` | Python执行 | 数据分析、脚本执行 |
| `shell` | Shell命令 | 系统操作、脚本调用 |
| `docker-skill` | Docker管理 | 容器操作、部署 |

### 13.5 数据库类工具

| 工具 | 功能 | 适用场景 |
|------|------|---------|
| `mysql-skill` | MySQL操作 | 关系型数据库 |
| `db-query` | 统一数据库查询 | 多数据库支持 |
| `redis-skill` | Redis操作 | 缓存、键值存储 |

### 13.6 AI模型类工具

| 工具 | 功能 | 国内可用 | 适用场景 |
|------|------|---------|---------|
| `qwen-skill` | 通义千问 | ✅ | 通用LLM调用 |
| `deepseek-skill` | DeepSeek | ✅ | 性价比高、推理强 |
| `glm-skill` | 智谱GLM | ✅ | 开源可本地 |
| `kimi-skill` | Kimi长文本 | ✅ | 长文本处理 |

### 13.7 通讯类工具

| 工具 | 功能 | 国内可用 | 适用场景 |
|------|------|---------|---------|
| `feishu` | 飞书集成 | ✅ | 企业通知 |
| `wecom` | 企业微信 | ✅ | 企业通知 |
| `email` | 邮件发送 | ✅ | 报告发送 |

---

## 十四、工具组合价值表

> **核心思想**: 单个工具能力有限，组合后产生新能力

### 14.1 网页处理组合

| 组合 | 产生的 Skill 类型 | 示例场景 |
|------|------------------|---------|
| `web_fetch` + `image_read` | 图片解析工作流 | 解析网页中的图片 |
| `browser` + `screenshot-skill` | 网页截图报告 | 生成页面快照报告 |
| `web-scraper` + `excel-handler` | 数据采集导出 | 爬取数据导出Excel |
| `agent-browser` + `web_fetch` | 混合解析策略 | 先静态后动态 |
| `playwright-cli` + `shell` | 自动化脚本 | 定时自动化任务 |

### 14.2 文件处理组合

| 组合 | 产生的 Skill 类型 | 示例场景 |
|------|------------------|---------|
| `pdf-processor` + `code_execution` | PDF数据分析 | 提取数据并分析 |
| `excel-handler` + `db-query` | 数据同步 | Excel数据入库 |
| `file-manager` + `shell` | 批量文件操作 | 批量重命名、移动 |
| `nano-pdf` + `web_fetch` | 下载后编辑 | 下载PDF并编辑 |

### 14.3 搜索+处理组合

| 组合 | 产生的 Skill 类型 | 示例场景 |
|------|------------------|---------|
| `web_search` + `web_fetch` | 晨间简报 | 搜索→抓取→汇总 |
| `web_search` + `image_read` | 图片研究 | 搜索图片并分析 |
| `context-search` + `read_file` | 规范查找 | 搜索规范并读取详情 |

### 14.4 数据处理组合

| 组合 | 产生的 Skill 类型 | 示例场景 |
|------|------------------|---------|
| `code_execution` + `excel-handler` | 数据分析管道 | Python分析+Excel输出 |
| `db-query` + `code_execution` | 数据报表 | 查询+分析+可视化 |
| `csv-data-summarizer` + `email` | 数据报告 | 分析结果邮件发送 |

---

## 十五、Skill 与复合工程的联动

> **核心**: Skill 不是孤立的，而是复合工程六层体系中的一层，与其他层有联动关系

### 15.1 Skill 与 Tools 的联动

| 联动关系 | 说明 |
|---------|------|
| Skill 指导 Tool 使用 | Skill 告诉 AI 如何组合使用 Tools |
| Tool 组合产生新能力 | 单个工具能力有限，组合后产生新能力 |
| allowed-tools 定义 | frontmatter 中定义预批准的工具列表 |

### 15.2 Skill 与 Experience 的联动

| 联动关系 | 说明 |
|---------|------|
| 踩坑案例沉淀 | Skill 执行中的踩坑案例沉淀到 `experience/deposition-records.md` |
| 场景标签匹配 | 通过场景标签索引找到相关经验 |
| **不独立记忆** | Skill 不创建独立记忆机制，整合到 Experience |

**沉淀流程**：

```
Skill 执行发现踩坑案例
         │
         ▼
写入 experience/deposition-records.md
         │
         ├── 场景标签：{触发条件}
         ├── 场景描述：{具体场景}
         └── 解决方案：{如何避免}
```

### 15.3 Skill 与 Cache 的联动

| 联动关系 | 说明 |
|---------|------|
| 执行进度记录 | Skill 执行进度记录到 `cache/task-progress.json` |
| 跨对话恢复 | 通过 Cache 恢复中断的 Skill 执行 |
| 任务完成清理 | Skill 执行完成后清理 Cache |

**Cache 操作时机**：

| 阶段 | Cache 操作 |
|------|-----------|
| Skill 开始执行 | 写入任务边界和完成条件 |
| Skill 执行中 | 更新进度 |
| Skill 执行完成 | 清理 Cache |
| 用户说"稍后" | 写入 pending-tasks.json |
| 用户说"跳过" | 写入 skipped-tasks.json |

### 15.4 Skill 与 Concept 的联动

| 联动关系 | 说明 |
|---------|------|
| 概念定义在先 | Skill 使用概念先在 `concept/` 定义 |
| 触发条件映射 | 通过 `CONCEPT_SPEC.md` 找到触发条件 |
| 渐进式加载 | 概念是 L1 层，Skill 是规范层 |

### 15.5 Skill 与 Rule 的联动

| 联动关系 | 说明 |
|---------|------|
| 规则约束 Skill | `rule/ai-coding/CODING_SPEC.md` 约束 Skill 执行 |
| 验证规范 | Skill 验证规则在 `SKILLS_SPEC.md` 定义 |
| 创建规范 | 创建 Skill 时必须遵循 `skill-creator-skill` |

---

## 十六、文件列表

1. `@.iflow/ecosystem/skills/web-search-skill.md` - 网络搜索技能（外部知识、默认搜索）
2. `@.iflow/ecosystem/skills/context-search-skill.md` - 项目内搜索技能（内部知识、明确限定）
3. `@.iflow/ecosystem/skills/web-content-extraction/` - Web内容解析策略技能（目录结构）
   - `SKILL.md` - 技能主体
   - `scripts/parse_wechat_article.py` - 微信公众号解析脚本
4. `@.iflow/ecosystem/skills/skill-creator-skill.md` - 技能创建技能（创建/更新/验证技能）

---

**最后更新**：2026-03-18
**版本**：13.0
**借鉴来源**: [Agent Skills Specification](https://agentskills.io/specification)、OpenClaw Skills完全指南
