# 协作内容分类

> **定位**: 目录内容按使用者分类
> **L2 引用**: @.iflow/ecosystem/experience/collaboration-method.md

---

## 定义

目录内容按使用者分类：AI 专用、共用、人类专用。AI 每次行为后检查共用内容是否需要沉淀。

## 分类表

| 分类 | 使用者 | 核心特征 | 典型文件 |
|------|--------|---------|---------|
| **AI 专用** | AI | 跨 AI 模型可用、人类不需关心 | cold-start.md, *-skill.md |
| **共用** | AI + 人类 | 人类可全链路指导、追踪 AI 行为 | start.md, RULE_SPEC.md |
| **人类专用** | 人类 | 简单明了、程序员间沟通 | 需求冷启动.md, 产品需求.md |

## 判断方法

```
问：这个文件谁会主动打开阅读？
答：只有 AI 打开 → AI 专用
答：AI 和人类都会打开 → 共用
答：只有人类打开 → 人类专用
```

## L2 详细规范

- 详细规范：@.iflow/ecosystem/experience/collaboration-method.md
