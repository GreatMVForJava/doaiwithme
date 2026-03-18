---
name: web-content-extraction
description: Web内容解析策略技能。指导AI根据页面特征选择合适的解析方式。触发关键词：解析网页、抓取文章、网页内容、Playwright、爬虫策略。
allowed-tools: web_fetch, run_shell_command, image_read, write_file, read_file
---

# Web Content Extraction Skill

## 核心要点（必须记住）

- **输入是URL**：本技能处理的是具体 URL，不是搜索查询
- **策略优先级**：curl → web_fetch → Chrome DevTools → Playwright（优先选简单）
- **快速判断**：微信公众号 → Playwright；静态页面 → web_fetch；调试API → curl
- **工具选择**：curl 用 run_shell_command；静态页面用 web_fetch；复杂交互用 Playwright

## 工具接口定义

### web_fetch

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| url | string | ✅ | 目标 URL，必须以 http:// 或 https:// 开头 |
| prompt | string | ✅ | 处理指令，告诉 AI 如何解析内容 |

**调用示例**：
```
web_fetch(
  url="https://example.com/article",
  prompt="提取文章标题、作者、发布时间和正文内容"
)
```

### run_shell_command

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| command | string | ✅ | 要执行的 bash 命令 |
| description | string | ✅ | 命令描述（5-10词） |
| dir_path | string | ❌ | 执行目录，默认项目根目录 |
| timeout | number | ❌ | 超时时间（秒），默认 120 |
| run_in_bg | boolean | ❌ | 是否后台运行，默认 false |

**curl 调用示例**：
```
run_shell_command(
  command='curl -L "https://example.com/api"',
  description="检查API响应状态"
)
```

**Playwright 调用示例**：
```
run_shell_command(
  command='python3 scripts/parse_wechat_article.py "https://mp.weixin.qq.com/xxx"',
  description="解析微信公众号文章"
)
```

### image_read

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| image_input | string | ✅ | 图片绝对路径或 base64 数据 |
| prompt | string | ✅ | 图片分析指令 |
| input_type | string | ❌ | 输入类型：`file_path` 或 `base64`，默认 `file_path` |
| mime_type | string | ❌ | MIME 类型（base64 时需要），如 `image/png` |
| task_brief | string | ❌ | 任务简介（CLI 显示用） |

**调用示例**：
```
image_read(
  image_input="/Users/code/downloads/screenshot.png",
  prompt="提取图片中的文字内容"
)
```

### read_file

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| absolute_path | string | ✅ | 文件绝对路径 |
| limit | number | ❌ | 最大读取行数 |
| offset | number | ❌ | 起始行号，0-based |

### write_file

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file_path | string | ✅ | 文件绝对路径 |
| content | string | ✅ | 文件内容 |

## 工具边界与组合方式

### 工具职责

| 工具 | 职责 | 输入 | 输出 | 何时使用 |
|------|------|------|------|---------|
| `web_fetch` | 抓取静态页面 | URL | 结构化内容 | 静态页面、无JS渲染 |
| `run_shell_command` | 执行 curl/Playwright | 命令 | 命令输出 | 调试API、复杂交互 |
| `image_read` | 解析图片 | 图片路径/base64 | 图片描述 | 解析网页中的图片 |
| `read_file` | 读取脚本 | 文件路径 | 脚本内容 | 执行 Playwright 脚本前 |
| `write_file` | 保存结果 | 路径+内容 | 操作结果 | 保存解析结果 |

### 调用模式

**互斥策略选择**（选其一）：

```
                    ┌─────────────────┐
                    │   用户需求      │
                    │  (解析URL)      │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
       ┌───────────┐  ┌───────────┐  ┌───────────┐
       │   curl    │  │ web_fetch │  │ Playwright│
       │  (调试)   │  │  (静态)   │  │  (复杂)   │
       └───────────┘  └───────────┘  └───────────┘
              │              │              │
              └──────────────┼──────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   write_file    │
                    │   (保存结果)    │
                    └─────────────────┘
```

### 决策树（简化版）

```
已有 URL 需要解析
       │
       ▼
┌──────────────────────┐
│ 是否只需要检查响应？  │
└──────────────────────┘
       │
       ├── 是 → run_shell_command (curl)
       │
       └── 否 → ┌──────────────────────┐
                 │ 是否需要JS渲染？      │
                 └──────────────────────┘
                         │
                         ├── 否 → web_fetch
                         │
                         └── 是 → run_shell_command (Playwright)
                                   或 read_file + 执行脚本
```

### 组合场景

| 场景 | 调用方式 | 说明 |
|------|---------|------|
| 检查API响应 | `run_shell_command` (curl) | 单独使用 |
| 抓取静态文章 | `web_fetch` | 单独使用 |
| 抓取并保存 | `web_fetch` → `write_file` | 顺序调用 |
| 解析微信公众号 | `read_file` → `run_shell_command` (执行脚本) | 顺序调用 |
| 解析网页图片 | `web_fetch` → `image_read` | 顺序调用 |
| 复杂交互页面 | `run_shell_command` (Playwright) → `write_file` | 顺序调用 |

### 并行可能性

| 工具对 | 可否并行 | 原因 |
|-------|---------|------|
| `web_fetch` + `image_read` | ❌ 不可并行 | image_read 需要 web_fetch 的图片URL |
| `curl` + `web_fetch` | ❌ 不需要 | 策略互斥，选其一 |
| `read_file` + `run_shell_command` | ❌ 不可并行 | 执行需要脚本内容 |
| 多个 URL 的 `web_fetch` | ✅ 可并行 | 无依赖关系 |

## 技能描述

Web内容解析策略技能：帮助AI根据页面特征选择最优的解析方式，平衡效率、复杂度和可靠性。

## 四种策略对比

| 策略 | 复杂度 | 工具类型 | 适用场景 | 优势 | 劣势 |
|------|--------|---------|---------|------|------|
| **curl** | ⭐ | HTTP工具 | 原始HTTP请求、API调用、检查响应 | 轻量、可控、调试方便 | 返回原始数据，需自行解析 |
| **web_fetch** | ⭐⭐ | 抓取工具 | 静态页面、无JS渲染 | 自动解析、返回结构化内容 | 无法处理动态内容 |
| **Chrome DevTools** | ⭐⭐⭐ | 浏览器协议 | JS渲染页面、SPA应用 | 可获取动态内容 | 需要Chrome环境 |
| **Playwright** | ⭐⭐⭐⭐ | 自动化框架 | 复杂交互、登录态、动态加载 | 最强大、可编程 | 依赖重、速度慢 |

### 工具层次关系

```
┌─────────────────────────────────────────────────────────────┐
│                      工具复杂度金字塔                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                      Playwright (⭐⭐⭐⭐)                     │
│                     完整浏览器自动化框架                       │
│                    （交互、登录、动态加载）                     │
│                           ▲                                 │
│                           │ 升级                             │
│                           │                                 │
│                 Chrome DevTools (⭐⭐⭐)                       │
│                    浏览器调试协议                              │
│                  （JS渲染，无交互）                            │
│                           ▲                                 │
│                           │ 升级                             │
│                           │                                 │
│                     web_fetch (⭐⭐)                          │
│                    高级网页抓取工具                            │
│                  （自动解析，静态页面）                         │
│                           ▲                                 │
│                           │ 升级                             │
│                           │                                 │
│                       curl (⭐)                              │
│                    原始HTTP请求工具                           │
│                  （原始响应，需自行解析）                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 决策框架

### 决策树

```
用户需要解析网页内容（已有URL）
              │
              ▼
┌─────────────────────────────┐
│ 是否只需要检查响应状态？      │
│ (调试API、下载文件、检查可访问)│
└───────────┬─────────────────┘
            │
    ┌───────┴───────┐
    │ 是            │ 否
    ▼               ▼
  curl        ┌─────────────────────────────┐
              │ 页面是否需要JS渲染？          │
              │ (微信公众号、SPA、动态加载)   │
              └───────────┬─────────────────┘
                          │
                  ┌───────┴───────┐
                  │ 否            │ 是
                  ▼               ▼
            web_fetch      ┌─────────────────────────────┐
                           │ 是否需要复杂交互？            │
                           │ (点击、滚动、登录、等待)       │
                           └───────────┬─────────────────┘
                                       │
                               ┌───────┴───────┐
                               │ 否            │ 是
                               ▼               ▼
                         Chrome DevTools    Playwright
```

### 快速判断表

| 页面特征 | 推荐策略 | 理由 |
|---------|---------|------|
| API接口调用、检查HTTP响应 | `curl` | 原始HTTP请求，调试方便 |
| 下载文件、获取原始数据 | `curl` | 直接输出到文件 |
| 新闻文章、博客、文档 | `web_fetch` | 静态内容，自动解析 |
| 微信公众号文章 | `Playwright` | 需要JS渲染，内容动态加载 |
| SPA应用（Vue/React） | `Chrome` 或 `Playwright` | 需要JS渲染 |
| 需要登录的页面 | `Playwright` | 需要处理认证态 |
| 需要滚动加载更多 | `Playwright` | 需要模拟用户交互 |
| 需要点击展开内容 | `Playwright` | 需要模拟点击 |
| 简单动态页面 | `Chrome DevTools` | JS渲染，无需复杂交互 |
| 检查页面是否存在/可访问 | `curl` | 快速检查响应状态 |
| 解析网页图片 | `web_fetch` + `image_read` | 获取内容后解析图片 |

## 触发条件

- 用户提供了**具体的 URL** 需要解析
- 用户提到"抓取"、"爬取"、"解析网页"、"解析URL"
- 用户提到"Playwright"、"Selenium"、"无头浏览器"
- web_fetch 返回空内容或不完整内容

## 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `url` | string | ✅ | 目标网址 |
| `content_type` | string | ❌ | 内容类型（article/interactive/spa） |
| `requires_interaction` | boolean | ❌ | 是否需要交互（滚动/点击） |
| `requires_auth` | boolean | ❌ | 是否需要登录 |

## 输出结果

```json
{
  "strategy": "playwright",
  "reason": "微信公众号文章需要JS渲染",
  "content": {
    "title": "文章标题",
    "author": "作者",
    "publish_time": "发布时间",
    "text": "正文内容",
    "images": ["图片URL列表"]
  },
  "metadata": {
    "extraction_time": "耗时",
    "page_type": "页面类型"
  }
}
```

## 实现步骤

### 步骤 1：判断页面类型

**快速判断方法**：

1. **已知域名判断**：
   - `mp.weixin.qq.com` → 微信公众号 → Playwright
   - `weibo.com` → 微博 → Playwright（需登录）
   - `zhihu.com` → 知乎 → web_fetch（静态）或 Chrome（动态）

2. **未知域名判断**：
   - 先尝试 `web_fetch`
   - 如果返回内容不完整，升级到 `Playwright`

### 步骤 2：选择策略

根据决策树和判断表选择最优策略

### 步骤 3：执行解析

**curl 策略**（通过 run_shell_command）：
```bash
# 获取页面内容
curl -L "https://example.com/article"

# 检查响应状态
curl -I "https://example.com/article"
```

**web_fetch 策略**：
```
使用 web_fetch 工具，直接获取页面内容
```

**Playwright 策略**（通过 run_shell_command 执行 Python 脚本）：
```
参考 scripts/parse_wechat_article.py
```

### 步骤 4：验证结果

- 检查内容是否完整
- 检查是否有缺失的关键信息
- 如果不完整，考虑升级策略

## 注意事项

1. **优先选择简单策略**：curl → web_fetch → Chrome → Playwright
2. **curl 适合调试**：检查响应、调试API时优先用 curl
3. **web_fetch 适合内容**：需要正文内容时优先用 web_fetch
4. **图片解析**：配合 image_read 工具解析网页中的图片
5. **结果保存**：使用 write_file 保存解析结果
6. **考虑环境依赖**：Playwright 需要安装浏览器

---

**最后更新**：2026-03-18
**版本**：2.0
