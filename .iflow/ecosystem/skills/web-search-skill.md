---
name: web-search-skill
description: 网络搜索技能。当用户需要**外部知识**时使用。典型场景：了解新概念、研究技术、查找公开资料、参考外部实践。默认行为：用户未明确指定搜索范围时，优先使用网络搜索。
allowed-tools: web_search, web_fetch
---

# Web Search Skill

## 使用场景

| 场景 | 用户意图 | 示例 |
|------|---------|------|
| 了解新概念 | 学习未知领域 | "研究龙虾"、"了解 Spring Boot" |
| 查找公开资料 | 获取外部信息 | "找一下最佳实践"、"参考官方文档" |
| 基于外部知识 | 引用外部依据 | "根据 xxx 思想"、"基于 xxx 原则" |
| 默认搜索 | 未指定范围 | "搜索一下"、"查查这个" |

## 触发条件

- 用户需要**项目外部**的知识
- 用户需要**最新**的技术趋势和实践
- 用户**未明确指定**搜索范围

## 优先搜索源

以下来源的专业知识更准确，搜索时应优先考虑：

| 优先级 | 来源 | 适用领域 | 搜索方式 |
|--------|------|---------|---------|
| ⭐⭐⭐ | **Perplexity** | AI搜索、深度研究、带引用回答 | `site:perplexity.ai` |
| ⭐⭐⭐ | **OpenAI** | AI、LLM、编程 | `site:openai.com` |
| ⭐⭐⭐ | **Anthropic** | AI安全、Claude | `site:anthropic.com` |
| ⭐⭐⭐ | **Google** | 通用技术 | `site:developers.google.com` |
| ⭐⭐ | **every.to** | 技术深度文章 | `site:every.to` |
| ⭐⭐ | **GitHub** | 开源项目、代码 | `site:github.com` |
| ⭐⭐ | **Stack Overflow** | 编程问题 | `site:stackoverflow.com` |

**Perplexity 特点**：
- AI 驱动的搜索引擎，提供带引用的回答
- 支持追问和深入探索
- 适合研究、技术对比、概念理解

**使用方式**：
```
# 优先搜索示例
web_search --query="GPT-4 API best practices site:openai.com"
web_search --query="Claude prompt engineering site:anthropic.com"
web_search --query="RAG implementation best practices site:perplexity.ai"
```

## 工具接口定义

### web_search

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| query | string | ✅ | 搜索查询词，支持搜索引擎语法 |
| intent | string | ✅ | 搜索意图，说明为什么搜索 |
| expected | string | ✅ | 期望结果，说明想获取什么信息 |
| num | number | ❌ | 返回结果数量，默认 15 |
| tbs | string | ❌ | 时间过滤，如 `qdr:d7`（过去7天）、`qdr:m1`（过去1月） |

**调用示例**：
```
web_search(
  query="GPT-4 API best practices site:openai.com",
  intent="学习 GPT-4 API 最佳实践",
  expected="官方文档中的 API 使用建议和示例代码"
)
```

### web_fetch

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| url | string | ✅ | 目标 URL，必须以 http:// 或 https:// 开头 |
| prompt | string | ✅ | 处理指令，告诉 AI 如何解析内容 |

**调用示例**：
```
web_fetch(
  url="https://openai.com/docs/gpt-4",
  prompt="提取 GPT-4 API 的主要参数说明和使用示例"
)
```

## 工具边界与组合方式

### 工具职责

| 工具 | 职责 | 输入 | 输出 | 何时使用 |
|------|------|------|------|---------|
| `web_search` | 发现 | 查询词 + 意图 + 期望 | 链接列表 + 摘要 | 不知道去哪找 |
| `web_fetch` | 深入 | URL + 处理指令 | 完整内容 | 已有链接，需要详情 |

### 调用模式

**必须顺序调用，不可并行**：

```
┌─────────────┐     ┌─────────────┐
│ web_search  │ ──→ │  web_fetch  │
│  (发现)     │     │  (深入)     │
└─────────────┘     └─────────────┘
     ↓                    ↓
  链接列表            完整内容
```

### 决策树

```
用户需要外部知识
       │
       ▼
┌──────────────────┐
│ 是否已有 URL？    │
└──────────────────┘
       │
       ├── 是 → 直接 web_fetch
       │
       └── 否 → web_search
                    │
                    ▼
              ┌──────────────────┐
              │ 摘要是否足够？    │
              └──────────────────┘
                    │
                    ├── 是 → 结束，总结结果
                    │
                    └── 否 → web_fetch 获取详情
```

### 组合场景

| 场景 | 调用顺序 | 说明 |
|------|---------|------|
| 快速了解 | `web_search` only | 摘要足够，无需深入 |
| 深度研究 | `web_search` → `web_fetch` | 先找链接，再深入内容 |
| 已知来源 | `web_fetch` only | 用户已提供 URL |

## 输入参数

- `query`：搜索查询（必填）
- `num`：返回结果数量（可选，默认为 10）

## 输出结果

- 返回搜索结果的摘要
- 包含标题、链接、日期

## 实现步骤

### 步骤 1：识别用户意图

判断用户是否需要外部知识

### 步骤 2：构建搜索查询

将用户意图转化为有效的搜索查询

### 步骤 3：调用 web_search 工具

```bash
web_search --query="{query}" --num={num}
```

### 步骤 4：筛选和总结

筛选最相关的结果，总结关键信息

## 注意事项

1. **优先判断场景**：先判断用户是否需要外部知识
2. **优先搜索源**：AI、编程类问题优先搜索 OpenAI、Anthropic、Google
3. **默认行为**：用户未指定范围时，网络搜索是默认选择

---

**最后更新**：2026-03-18
**版本**：6.0
