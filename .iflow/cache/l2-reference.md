# Cache 参考内容（L2）— 简化版

> **定位**: Cache 详细参考，仅在需要时读取
> **上级入口**: `@.iflow/cache/CACHE_SPEC.md`
> **说明**: 本文件为简化版，移除了与 `l1-lifecycle.md` 及 `identity.md` 重复的内容，仅保留 L2 独有的参考信息。

---

## 四、目录结构

```text
.iflow/cache/
├── CACHE_SPEC.md        # Cache 规范（L0入口）
├── l1-lifecycle.md      # Cache 生命周期核心内容（L1）
├── l2-reference.md      # Cache 参考内容（L2，本文件）
├── pending-tasks.json   # 待确认任务
├── skipped-tasks.json   # 跳过的任务
├── task-progress.json   # 任务进度
```

| 文件 | 用途 | 管理方式 |
|------|------|---------|
| pending-tasks.json | 待确认任务 | 按 5.1 格式 |
| skipped-tasks.json | 跳过的任务 | 按 5.2 格式 |
| task-progress.json | 任务进度 | 按 5.3 格式 |

> **注意**: `progress/` 目录是运行时临时文件，任务结束后必须删除

---

## 五、文件格式

### 5.1 pending-tasks.json

```json
{
  "version": "1.0",
  "updated_at": "",
  "tasks": [
    {
      "id": "task-001",
      "type": "confirm",
      "content": "是否修复 xxx？",
      "proposed_action": "具体操作描述",
      "status": "pending",
      "created_at": "",
      "confirmed_at": null
    }
  ]
}
```

### 5.2 skipped-tasks.json

```json
{
  "version": "1.0",
  "updated_at": "",
  "tasks": [
    {
      "id": "task-002",
      "type": "confirm",
      "content": "是否修改 xxx？",
      "proposed_action": "具体操作描述",
      "status": "skipped",
      "created_at": "",
      "skip_reason": "跳过原因",
      "skip_at": ""
    }
  ]
}
```

### 5.3 task-progress.json

```json
{
  "version": "1.0",
  "current_task": {
    "id": "main-task-001",
    "boundary": {
      "include": ["任务包含范围"],
      "exclude": ["任务排除范围"]
    },
    "completion_conditions": [
      {"id": "cond-001", "content": "完成条件1", "status": "done"},
      {"id": "cond-002", "content": "完成条件2", "status": "pending"}
    ],
    "current_progress": "1/2",
    "status": "in_progress",
    "created_at": "",
    "updated_at": ""
  },
  "completed_tasks": []
}
```

---

## 六、Loop 模式（摘要）

> **详细内容**: `@.iflow/cache/l1-lifecycle.md`

核心原则：AI 不执行任何实质性操作，除非获得人类确认。用户可回答：Y/执行、n/修改方案、跳过、讨论。

---

## 七、强制询问机制（核心）

> **核心原则**：没有用户回答时，必须强制调用 ask_user_question tool，至少询问三次

### 触发条件

| 场景 | 判断标准 | AI 行为 |
|------|---------|---------|
| **没有用户回答** | 用户输入为空或无关内容 | 强制调用 ask_user_question |
| **回答不明确** | 用户回答模糊，如"随便"、"都行" | 强制调用 ask_user_question |
| **需要决策** | 多个选项需要用户选择 | 强制调用 ask_user_question |
| **方案确认** | 执行前需要用户确认 | 强制调用 ask_user_question |

### 询问流程

```text
AI 输出方案 → 等待用户回答
├─ 明确回答 → 执行 → 更新 Cache
└─ 无回答 → 强制询问（第1次）
    ├─ 回答 → 执行
    └─ 无回答 → 强制询问（第2次，提供更多背景）
        ├─ 回答 → 执行
        └─ 无回答 → 强制询问（第3次，说明将记录到 pending）
            ├─ 回答 → 执行
            └─ 无回答 → 写入 pending-tasks.json → 等待下次对话
```

### 询问规范

| 规范 | 说明 |
|------|------|
| **至少询问三次** | 没有明确回答时，必须至少询问三次 |
| **每次询问不同** | 每次询问应提供不同角度或更多信息 |
| **最后一次说明** | 第三次询问后仍无回答，说明将记录到 pending-tasks.json |
| **写入 pending** | 三次询问后仍无回答，写入 pending-tasks.json |

### 询问模板

**第1次**：我需要您确认才能继续执行：[问题/选项]。请选择或提供您的想法。

**第2次**：我还在等待您的确认：[问题/选项]。为了帮您更好地决策，我可以提供更多背景信息。您需要吗？

**第3次**：这是最后一次询问：[问题/选项]。如果您暂时无法决定，我将记录到待办任务，稍后再处理。这样可以吗？

### Cache 操作配合

| 询问次数 | Cache 操作 |
|---------|-----------|
| 第1次询问前 | 写入当前问题到 task-progress.json |
| 第2次询问前 | 更新询问次数 |
| 第3次询问前 | 更新询问次数 |
| 第3次后仍无回答 | 写入 pending-tasks.json |

---

## 已移除内容索引

| 原章节 | 移除原因 | 替代位置 |
|--------|---------|---------|
| 9.1 交互闭环 | 与 L1 重复 | l1-lifecycle.md |
| 9.2-9.5 强制写入/历史/输出/三宫六院 | 与 L1 或其他文件重复 | l1-lifecycle.md / three-palaces-six-courts-skill |
| 9.7 交互闭环完整流程 | 与 9.1 重复 | l1-lifecycle.md |
| 协作规范传递者 | 已在 identity.md 中定义 | identity.md |
| 注意事项 | 与 L1 核心原则重复 | l1-lifecycle.md |

---

**版本**: 5.0-L2（简化版）
**上级入口**: `@.iflow/cache/CACHE_SPEC.md`
