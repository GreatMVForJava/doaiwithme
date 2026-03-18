# 教知识 > 注册 API

> **定位**: LLM 最强的能力是理解自然语言指令后自主解决问题
> **L2 引用**: @.iflow/ecosystem/skills/SKILLS_SPEC.md

---

## 定义

LLM 最强的能力是理解自然语言指令后自主解决问题，而非调用预定义 API。

## 对比

| 维度 | 注册 API | 教知识 |
|------|---------|--------|
| **思路** | 给 LLM 定义 API Schema | 给 LLM 写使用手册 |
| **Token 成本** | 8 个 API ≈ 1600-4000 Token | 1 个 skill_run ≈ 20 Token |
| **灵活性** | 只能调预定义函数 | 可写出第 9、10 种操作 |
| **适用场景** | 确定性操作 | 不确定性任务 |

## 为什么教知识更好

```
# 注册 API 的局限
pdf 技能注册了 8 个 function calling
→ LLM 只能在这 8 个中选

# 教知识的灵活
SKILL.md 教会 LLM 怎么用 pypdf 和 reportlab
→ LLM 可以写出第 9 种、第 10 种操作
→ 这些操作可能是 Skill 作者压根没想到的
```

## L2 详细规范

- 详细规范：@.iflow/ecosystem/skills/SKILLS_SPEC.md
