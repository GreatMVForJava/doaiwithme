---
name: skill-creator-skill
description: 技能创建技能，用于创建、更新、验证 Skills 规范文件。触发关键词：创建技能、新建skill、验证skill、技能规范、SKILL.md。
allowed-tools: read_file, write_file, search_file_content, glob
---

# Skill Creator Skill

## 技能描述
技能创建技能：帮助 AI 创建、更新、验证 Skills 规范文件，确保符合 Agent Skills 标准。

## 触发条件
- 需要创建新的 Skill
- 需要更新现有 Skill 的格式
- 需要验证 Skill 是否符合规范

## 输入参数
- `action`：操作类型（create / update / validate）
- `name`：技能名称
- `content`：技能内容（create 时必填）

## 输出结果
- 操作结果
- 验证报告（validate 时）

## 实现步骤

### 步骤 1：确定操作类型

根据用户请求确定操作类型：
- `create`：创建新技能
- `update`：更新现有技能
- `validate`：验证技能规范

### 步骤 2：执行操作

**创建技能**：
1. 验证 name 符合规范（小写字母、数字、连字符）
2. 生成 frontmatter（name + description + 触发关键词）
3. 生成主体内容框架
4. 写入文件 `{name}-skill.md`

**更新技能**：
1. 读取现有技能文件
2. 更新 frontmatter（添加触发关键词）
3. 更新主体内容
4. 验证更新后符合规范

**验证技能**：
1. 读取技能文件
2. 验证 frontmatter 格式
3. 验证 name 一致性
4. 验证 description 包含触发关键词
5. 输出验证报告

### 步骤 3：输出结果

输出操作结果或验证报告。

## 验证规范

### frontmatter 验证

| 检查项 | 规则 | 通过条件 |
|-------|------|---------|
| name 格式 | 小写字母、数字、连字符 | 符合正则 `^[a-z0-9][a-z0-9-]*[a-z0-9]$` |
| name 长度 | 1-64字符 | `len(name) <= 64` |
| name 一致性 | 与文件名一致 | `{name}-skill.md` 或 `{name}/SKILL.md` |
| description 长度 | 1-1024字符 | `len(description) <= 1024` |
| description 关键词 | 包含触发关键词 | 包含"触发关键词：" |

### 内容验证

| 检查项 | 规则 | 通过条件 |
|-------|------|---------|
| 章节完整 | 包含必要章节 | 包含"技能描述"、"触发条件" |
| 步骤可执行 | 步骤具体 | 包含"步骤"字样 |

## 示例输出

### 验证报告

```markdown
## Skills 验证报告

### web-search-skill.md
| 检查项 | 结果 | 说明 |
|-------|------|------|
| name 格式 | ✅ | web-search-skill |
| name 一致性 | ✅ | 文件名匹配 |
| description 关键词 | ✅ | 包含"触发关键词" |
| 章节完整 | ✅ | 包含必要章节 |

### context-search-skill.md
| 检查项 | 结果 | 说明 |
|-------|------|------|
| name 格式 | ✅ | context-search-skill |
| name 一致性 | ✅ | 文件名匹配 |
| description 关键词 | ✅ | 包含"触发关键词" |
| 章节完整 | ✅ | 包含必要章节 |

**验证结果**：全部通过 ✅
```

## 注意事项

1. **name 命名规范**：必须符合小写字母、数字、连字符规范
2. **description 触发关键词**：必须包含触发关键词，帮助 AI 识别
3. **向后兼容**：现有 `{name}-skill.md` 格式保持不变
4. **目录结构**：复杂技能可使用 `{name}/SKILL.md` 目录结构

---

**最后更新**：2026-03-11
**版本**：1.0
