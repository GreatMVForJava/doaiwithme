# 执行力公式

> **定位**: Skill 的执行力由文档质量和工具能力共同决定
> **L2 引用**: @.iflow/ecosystem/skills/SKILLS_SPEC.md

---

## 定义

Skill 的执行力由文档质量和工具能力共同决定。

## 公式

```
Skill 的执行力 = SKILL.md body 质量 × (Agent 基础工具 + skill_run 沙箱能力)
```

## 关键洞察

- SKILL.md 的 body 文本是"灵魂"——决定 LLM 能否理解任务、选对方法、写对代码
- skill_run 是"手脚"——提供在隔离沙箱中执行任意命令的能力
- Tools: 声明是"可选配件"——框架支持，但大多数场景不需要

## LLM 能力层级

```
开发者（理解 + 组合 + 创造）
    > 选择者（理解 + 选择）
    > 调用者（理解 + 执行）
    > 遵循者（理解 + 遵循）
```

## 使用场景

- Skill 设计：根据场景选择合适的模式
- Skill 评估：评估现有 Skill 的质量和执行力
- Skill 优化：提升 SKILL.md 质量 或 增强工具能力

## L2 详细规范

- 详细规范：@.iflow/ecosystem/skills/SKILLS_SPEC.md
