# 增量哈希优化

> **定位**: 通过哈希值避免重复计算
> **L2 引用**: @.iflow/ecosystem/skills/SKILLS_SPEC.md

---

## 定义

通过哈希值判断内容是否变化，避免重复计算/拷贝。

## 核心原理

```
1. compute_dir_digest(skill_root) → 计算目录哈希
2. 如果哈希没变 → 直接跳过（零开销）
3. 如果哈希变了 → 执行完整操作
4. 更新元数据，记录新哈希
```

## 使用场景

- skill_run 多次调用：第 2-4 次调用跳过目录拷贝
- Cache 检查：判断任务状态是否变化
- 任何需要避免重复操作的场景

## 效果

每次调用节省 ~100ms IO 时间

## L2 详细规范

- 详细规范：@.iflow/ecosystem/skills/SKILLS_SPEC.md
