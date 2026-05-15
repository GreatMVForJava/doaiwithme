# 沉淀（Deposition）

> **定位**: AI 将经验沉淀到相应目录，减少后续沟通成本
> **L2 引用**: @.iflow/ecosystem/methodology/method-index.md

---

## 定义

AI 在编码完成后，将经验沉淀到相应目录，减少后续沟通成本。

## 使用场景

- AI 将经验沉淀到 experience/ 目录
- AI 将问题记录到 issues/ 目录
- AI 将解决方案固化到规则中

## 示例

```
AI：我已经将 LLM 集成的经验沉淀到 experience/ 中了
```

## L2 详细规范

- 详细规范：@.iflow/ecosystem/methodology/method-index.md
- 相关概念：@.iflow/ecosystem/concept/ai-collaboration/reuse.md

---

## AI 执行检查

| 检查项 | 合格标准 | 不合格示例 |
|-------|---------|-----------|
| **沉淀位置** | 明确写入文件路径 | "已经沉淀了"、"记录好了" |
| **沉淀内容** | 输出沉淀的内容片段 | 只说"沉淀了经验" |
| **沉淀索引** | 在deposition-records.md登记 | 未登记 |

**AI自检模板**：

```text
### 沉淀检查
| 检查项 | 是否合格 | 说明 |
|-------|---------|------|
| 位置明确 | ✅/❌ | 文件路径: ... |
| 内容输出 | ✅/❌ | 沉淀内容: ... |
| 索引登记 | ✅/❌ | deposition-records.md 序号: ... |
```
