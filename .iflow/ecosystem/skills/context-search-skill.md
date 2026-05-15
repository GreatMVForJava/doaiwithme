---
name: context-search-skill
description: 项目内搜索技能。当用户需要**内部知识**时使用。典型场景：搜索规范、查找经验、定位文档。明确限定：用户明确指定搜索范围为项目内部时使用。
allowed-tools: search_file_content, glob, read_file
---

# Context Search Skill

## 使用场景

| 场景 | 用户意图 | 示例 |
|------|---------|------|
| 搜索规范 | 查找项目规范 | "规范在哪"、"怎么写代码" |
| 查找经验 | 复用历史经验 | "之前怎么处理的"、"经验沉淀在哪" |
| 定位文档 | 找到具体文件 | "项目结构是什么"、"某个文件在哪" |
| 明确限定 | 项目内部搜索 | "项目内搜索"、"在规范里找" |

## 触发条件

- 用户明确指定搜索范围为项目内部
- 用户需要查找项目规范、经验、文档
- 用户说"项目内搜索"、"规范在哪"

## 工具接口定义

### search_file_content

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| pattern | string | ✅ | 正则表达式模式或字面字符串 |
| path | string | ❌ | 搜索路径，默认当前工作目录 |
| include | string | ❌ | 文件过滤，如 `*.md`、`*.java` |
| case_sensitive | boolean | ❌ | 是否区分大小写，默认 false |
| fixed_strings | boolean | ❌ | 是否作为字面字符串而非正则，默认 false |
| context | number | ❌ | 显示匹配前后各多少行 |
| before | number | ❌ | 显示匹配前多少行 |
| after | number | ❌ | 显示匹配后多少行 |

**调用示例**：
```
search_file_content(
  pattern="HealthReportProcess",
  path="/Users/code/your-project",
  include="*.java"
)
```

### glob

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| pattern | string | ✅ | glob 模式，如 `**/*.md`、`src/**/*.java` |
| path | string | ❌ | 搜索路径，默认根目录 |
| case_sensitive | boolean | ❌ | 是否区分大小写，默认 false |
| respect_git_ignore | boolean | ❌ | 是否尊重 .gitignore，默认 true |

**调用示例**：
```
glob(
  pattern="**/*Service*.java",
  path="/Users/code/your-project"
)
```

### read_file

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| absolute_path | string | ✅ | 文件绝对路径，如 `/Users/code/project/file.txt` |
| limit | number | ❌ | 最大读取行数（与 offset 配合分页） |
| offset | number | ❌ | 起始行号，0-based（与 limit 配合分页） |

**调用示例**：
```
read_file(
  absolute_path="/Users/code/your-project/IFLOW.md"
)
```

## 工具边界与组合方式

### 工具职责

| 工具 | 职责 | 输入 | 输出 | 何时使用 |
|------|------|------|------|---------|
| `search_file_content` | 内容搜索 | 正则模式 | 匹配行 + 文件路径 + 行号 | 搜索文件内容 |
| `glob` | 文件查找 | glob 模式 | 文件路径列表 | 按文件名/路径查找 |
| `read_file` | 读取内容 | 文件绝对路径 | 文件内容 | 获取完整文件内容 |

### 调用模式

**可独立使用，也可顺序组合**：

```
┌──────────────────┐
│    glob          │ ──→ 按文件名查找
│  （文件定位）     │
└──────────────────┘

┌──────────────────┐
│ search_file_     │ ──→ 按内容查找
│   content        │
│  （内容搜索）     │
└──────────────────┘

┌──────────────────┐
│   read_file      │ ──→ 获取详情
│  （内容读取）     │
└──────────────────┘
```

### 决策树

```
用户需要内部知识
       │
       ▼
┌──────────────────────┐
│ 知道文件名特征？      │
└──────────────────────┘
       │
       ├── 是 → glob 查找文件
       │
       └── 否 → search_file_content 搜索内容
                    │
                    ▼
              ┌──────────────────────┐
              │ 是否需要完整内容？    │
              └──────────────────────┘
                    │
                    ├── 是 → read_file 读取详情
                    │
                    └── 否 → 输出搜索结果
```

### 组合场景

| 场景 | 调用方式 | 说明 |
|------|---------|------|
| 按文件名找文件 | `glob` only | 知道文件名特征 |
| 按内容找文件 | `search_file_content` only | 知道内容关键词 |
| 找到后读取详情 | `search_file_content` → `read_file` | 顺序调用 |
| 找文件后读内容 | `glob` → `read_file` | 顺序调用 |

### 并行可能性

| 工具对 | 可否并行 | 原因 |
|-------|---------|------|
| `glob` + `search_file_content` | ✅ 可并行 | 无依赖关系 |
| `search_file_content` + `read_file` | ❌ 不可并行 | read_file 需要搜索结果的路径 |
| `glob` + `read_file` | ❌ 不可并行 | read_file 需要 glob 结果的路径 |

## 输入参数

- `query`：搜索查询（必填）
- `path`：搜索路径（可选，默认为项目根目录）
- `file_type`：文件类型过滤（可选）

## 输出结果

- 返回搜索结果的摘要
- 包含文件路径、行号、匹配内容

## 实现步骤

### 步骤 1：识别用户意图

判断用户是否需要内部知识

### 步骤 2：构建搜索查询

将用户意图转化为有效的搜索查询

### 步骤 3：调用搜索工具

```bash
# 使用 search_file_content 搜索文件内容
search_file_content --pattern="{query}" --path="{path}"

# 或使用 glob 查找文件
glob --pattern="**/*{keyword}*"
```

### 步骤 4：筛选和总结

筛选最相关的结果，总结关键信息

## 注意事项

1. **明确限定触发**：只有用户明确指定项目内部时才使用
2. **搜索范围默认**：默认搜索是当前项目工程下的所有内容，包括目录名称、文件名称和文件内容（文件内容主要是文字内容，不包含图片内容等其他文件内容）
3. **结果整理**：输出时包含文件路径和行号，方便定位

---

**最后更新**：2026-03-18
**版本**：4.0
