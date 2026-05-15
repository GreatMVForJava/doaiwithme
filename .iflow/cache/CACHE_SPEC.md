# Cache 规范（L0 入口）

> **定位**: 状态层，四层防御体系的 Level 0
> **读取策略**: 本文件为 L0 入口，始终读取；L1/L2 按需读取

## 核心要点（L0，必须记住）

- Cache 是状态层，解决"我做到哪里了"的问题
- 预检阶段：总是读取；自检阶段：总是读取；任务完成：必须删除
- 每次询问用户时，都必须执行 Cache 操作

## 按需读取导航

| 场景 | 读取文件 | 层级 |
|------|---------|------|
| 理解Cache定位与冷启动关系 | `@.iflow/cache/l1-lifecycle.md` 一、Cache与冷启动 | L1 |
| 需要写入Cache | `@.iflow/cache/l1-lifecycle.md` 二、AI执行生命周期 | L1 |
| 判断何时写入/不写入 | `@.iflow/cache/l1-lifecycle.md` 三、Cache调用时机 | L1 |
| 查看文件格式 | `@.iflow/cache/l2-reference.md` 五、文件格式 | L2 |
| 查看目录结构 | `@.iflow/cache/l2-reference.md` 四、目录结构 | L2 |
| Loop模式 | `@.iflow/cache/l2-reference.md` 六、Loop模式 | L2 |
| 协作规范传递者 | `@.iflow/cache/l2-reference.md` 七、协作规范传递者 | L2 |
| 注意事项 | `@.iflow/cache/l2-reference.md` 八、注意事项 | L2 |
| 需要交互闭环 | `@.iflow/cache/l2-reference.md` 九、强制交互机制 | L2 |

---

**版本**: 5.0
**创建日期**: 2026-03-09
**更新日期**: 2026-04-30
**维护者**: AI + 人类
**适用对象**: 所有 AI 实例