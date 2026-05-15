# Skills 参考内容（L2）

> **定位**: Skills 详细参考，仅在需要时读取
> **上级入口**: `@.iflow/ecosystem/skills/SKILLS_SPEC.md`

---

## 四、渐进式披露（强制调用规则）

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

#### 规则2：使用 Skill 时按需读取

```
AI 识别需求
     ↓
匹配 description 中的触发关键词（元数据层）
     ↓
是否需要详细步骤？
     ├─ 是 → 主动读取 SKILL.md 主体（指令层）
     └─ 否 → 仅使用元数据执行
     ↓
是否需要参考资料？
     ├─ 是 → 主动读取 references/（资源层）
     └─ 否 → 完成
```

#### 规则3：@ 引用强制读取

**当用户或文档使用 `@文件路径` 引用时，AI 必须主动读取该文件。**

### 4.4 渐进式披露检查表

**AI 在每个阶段必须输出**：

``` text
### 渐进式披露检查

| 检查项 | 状态 | 证据 |
|-------|------|------|
| 元数据匹配 | ✅/❌ | 匹配到哪个 skill 的 description？ |
| 指令层读取 | ✅/❌ | 是否需要读取 SKILL.md 主体？ |
| 资源层读取 | ✅/❌ | 是否需要读取 references/？ |
| @ 引用处理 | ✅/❌ | 是否识别并读取了 @ 引用的文件？ |
```

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
3. 主动读取 SKILL.md 主体
      ↓
4. 执行实现步骤
      ↓
5. 返回结果
```

---

## 八、创建新 Skills（强制流程）

> **关键**：创建 Skill 时，AI **必须**先调用 `@.iflow/ecosystem/skills/skill-creator-skill.md`

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

**单文件**：`skills/new-skill.md`

**目录结构**：`skills/new-skill/` + `SKILL.md` + `scripts/` + `references/`

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

---

## 十一、Skills 关系管理

> **原则**：每个 Skill 独立，不在 Skill 内部引用其他 Skill。

### 规范与执行的关系

| 文件 | 定位 | 内容 | 使用时机 |
|------|------|------|---------|
| **SKILLS_SPEC.md** | 规范标准（L0入口） | 定义格式、验证规则 | AI 需要了解规范时读取 |
| **l1-skills-core.md** | 核心内容（L1） | 格式定义、验证规范 | 创建/使用Skill时读取 |
| **l2-skills-reference.md** | 参考内容（L2） | 工具组合、联动 | 需要详细参考时读取 |

### Skills 边界区分

| skill | 核心场景 | 输入 | 输出 | 典型表达 |
|-------|---------|------|------|---------|
| **web-search-skill** | 搜索外部信息 | 查询词 | 链接摘要 | "搜索xx"、"了解xx" |
| **context-search-skill** | 搜索内部知识 | 查询词 | 项目文档 | "项目内搜索"、"规范在哪" |
| **skill-creator-skill** | 创建技能 | 技能定义 | skill文件 | "创建skill"、"验证skill" |

### Skills 组合使用场景

| 场景 | 推荐组合 | 说明 |
|------|---------|------|
| "了解项目规范" | context-search | 只需内部搜索 |
| "创建新技能" | skill-creator | 创建时必须调用 |

---

## 十三、工具清单索引

> **来源**: OpenClaw Skills 完全指南 + 当前系统可用工具

### 13.1 搜索类工具

| 工具 | 功能 | 国内可用 | API Key | Skill 应用 |
|------|------|---------|---------|-----------|
| `web_search` | 网页搜索 | 需代理 | Brave API Key | web-search-skill |
| `firecrawl` | JS渲染网页抓取 | ✅ 直接可用 | Firecrawl API Key | 复杂网页解析 |
| `tavily` | AI优化搜索 | 需代理 | Tavily API Key | 搜索增强 |

### 13.2 网页操作类工具

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
    ├─ 静态内容 → browsy 或 web_fetch
    ├─ 需要JS渲染 → agent-browser
    ├─ 需要复杂交互 → browser + playwright-cli
    └─ 需要结构化采集 → web-scraper
```

### 13.3 文件处理类工具

| 工具 | 功能 | 复杂度 | 适用场景 | 与其他工具组合 |
|------|------|--------|---------|---------------|
| `nano-pdf` | PDF自然语言编辑 | ⭐⭐ | 页面合并、拆分、水印 | + web_fetch → 下载后编辑 |
| `pdf-processor` | PDF处理工具集 | ⭐⭐ | OCR、文本提取 | + ocr → 扫描版PDF |
| `excel-handler` | Excel读写操作 | ⭐⭐ | 数据表格、报表 | + web-scraper → 数据导出 |
| `csv-data-summarizer` | CSV数据分析 | ⭐ | 数据统计、聚合 | + code_execution → 复杂分析 |
| `file-manager` | 文件系统管理 | ⭐ | 文件操作、目录管理 | + shell → 批量操作 |

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

### 14.2 文件处理组合

| 组合 | 产生的 Skill 类型 | 示例场景 |
|------|------------------|---------|
| `pdf-processor` + `code_execution` | PDF数据分析 | 提取数据并分析 |
| `excel-handler` + `db-query` | 数据同步 | Excel数据入库 |
| `file-manager` + `shell` | 批量文件操作 | 批量重命名、移动 |

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

> **核心**: Skill 不是孤立的，而是复合工程六层体系中的一层

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

### 15.3 Skill 与 Cache 的联动

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
3. `@.iflow/ecosystem/skills/skill-creator-skill.md` - 技能创建技能（创建/更新/验证技能）
4. `@.iflow/ecosystem/skills/self-improvement-skill/` - 自我改进技能（触发机制 + 记录流程）
   - `SKILL.md` - 技能主体
5. `@.iflow/ecosystem/skills/three-palaces-six-courts-skill/` - 三宫六院协作技能（Cache绑定 + 自指检查）
   - `SKILL.md` - 技能主体

---

**版本**: 14.0-L2
**上级入口**: `@.iflow/ecosystem/skills/SKILLS_SPEC.md`