# CQRS 解耦

> **定位**: 命令查询分离，写入方和读取方解耦
> **L2 引用**: @.iflow/ecosystem/skills/SKILLS_SPEC.md

---

## 定义

写入方和读取方通过中间状态解耦，各自独立演化。

## 核心架构

```
写入方（命令）  →  state_delta（中间状态）  →  读取方（查询）
skill_load()                              SkillsRequestProcessor
skill_select_docs()                       _build_docs_text()
skill_run()
```

## 使用场景

- Cache 机制：写入 pending-tasks.json，读取时检查进度
- Skill 系统：skill_load 写入状态，RequestProcessor 读取状态注入 prompt
- 任何需要解耦写入和读取的场景

## 优势

- 写入方不关心读取方如何使用数据
- 读取方可以按需组合数据
- 中间状态可作为调试检查点

## L2 详细规范

- 详细规范：@.iflow/ecosystem/skills/SKILLS_SPEC.md
