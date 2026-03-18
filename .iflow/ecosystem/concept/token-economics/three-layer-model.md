# 三层信息模型

> **定位**: Token 效率最大化的分层信息注入
> **L2 引用**: @.iflow/ecosystem/skills/SKILLS_SPEC.md

---

## 定义

通过分层信息注入实现 Token 效率最大化，先粗筛再精选。

## 三层架构

| 层级 | 内容 | 加载时机 | Token 消耗 |
|------|------|---------|-----------|
| **L0 概览** | name + description | 启动时加载所有 | ~30 Token/技能 |
| **L1 Body** | SKILL.md 主体 | 激活时加载 | ~500-2000 Token |
| **L2 详细** | references/ 文档 | 按需加载 | ~1000-5000 Token |

## Token 节省效果

```
一次性全部加载：SKILL.md + 详细文档 ≈ 7000 tokens
渐进加载（只需概览）：description → ~50 tokens
节省：~99%
```

## 使用场景

- AI 启动时：加载所有技能的 L0（概览）
- AI 识别需求后：加载特定技能的 L1（Body）
- AI 需要详细操作时：加载 L2（详细文档）

## L2 详细规范

- 详细规范：@.iflow/ecosystem/skills/SKILLS_SPEC.md（渐进式披露章节）
