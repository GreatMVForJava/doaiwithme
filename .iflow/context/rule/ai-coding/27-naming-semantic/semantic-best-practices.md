# 命名语义最佳实践

## 规则 23：命名语义规范

**规则内容**：命名应该反映领域语义，避免混淆 → 使用成对命名，区分常量和变量命名 → 思想：命名是代码的一部分，提高可读性和维护性

## 命名规范范围

命名规范适用于所有命名元素：
- **文件名**：资源文件（.md, .yml 等）、代码文件
- **目录名**：Java 包目录、资源目录
- **类名**：Java 类、接口、枚举类
- **枚举值**：枚举常量的名称
- **变量名**：成员变量、局部变量、参数
- **常量名**：static final 字段

## 命名混淆案例

### 案例 1：START 节点和 startNodeId 参数混淆

**问题描述**：
- **START 节点**：工作流的生命周期节点，负责初始化工作流上下文
- **startNodeId 参数**：在 `continueWorkflow` 方法中，指定从哪个节点开始继续执行
- **混淆原因**：两者都包含 "start"，容易混淆

**解决方案**：
- 将 `START` 节点改名为 `BEGIN`
- `BEGIN` 节点和 `END` 节点形成一对，语义更清晰
- `startNodeId` 参数可以保持不变，因为它是"从哪个节点开始继续执行"的语义
- 避免了混淆

### 案例 2：文件名与占位符命名不一致

**问题描述**：
- **文件名**：`content.md`
- **占位符**：`{{markdownTemplate}}`
- **混淆原因**：文件名和占位符不一致，导致开发维护时需要记忆映射关系

**解决方案**：
- 将文件名改为 `markdownTemplate.md`，与占位符保持一致
- 命名是代码的一部分，需要符合 DDD 规范和 AI 上下文管理
- 提高代码可读性和维护性

**代码示例**：

``` java
// 修改前
private static String loadContentTemplate(String domain, String node) {
    String filePath = buildFilePath(domain, node, "content");  // 文件名与占位符不一致
    return loadFromFile(filePath);
}

// 修改后
private static String loadContentTemplate(String domain, String node) {
    String filePath = buildFilePath(domain, node, "markdownTemplate");  // 文件名与占位符一致
    return loadFromFile(filePath);
}
```

**文件结构变化**：
```
prompt/health/{domain}/{node}/
├── systemprompt.md
├── userprompt.md         # 包含 {{markdownTemplate}} 占位符
└── markdownTemplate.md   # 修改前：content.md
```

## 命名规范

### 1. 成对命名

使用成对命名提高可读性：
- ✅ BEGIN/END（开始/结束）
- ✅ START/STOP（启动/停止）
- ✅ OPEN/CLOSE（打开/关闭）
- ✅ SUCCESS/FAILURE（成功/失败）

### 2. 领域语义

命名应该反映领域语义，避免使用容易混淆的词汇：
- ✅ 使用领域术语（如 `workflowExecutionId`、`nodeDefinition`）
- ❌ 避免使用通用术语（如 `id`、`name`、`value`）

### 3. 区分常量和变量

- **常量**：使用大写和下划线（如 `MAX_RETRIES`、`DEFAULT_TIMEOUT`）
- **变量**：使用驼峰命名（如 `workflowExecutionId`、`nodeDefinition`）

### 4. 避免重复

避免在同一个上下文中使用相似的词汇：
- ✅ `workflowExecutionId`、`nodeDefinition`、`caseId`
- ❌ `id`、`definition`、`caseId`（容易混淆）

## 示例

### 正确示例

``` java
// 成对命名
BEGIN/END 节点，startNodeId 参数

// 领域语义
workflowExecutionId, nodeDefinition, caseId

// 常量和变量
private static final int MAX_RETRIES = 3;
private String workflowExecutionId;
```

### 错误示例

``` java
// 命名混淆
START/END 节点，startNodeId 参数（容易混淆）

// 缺乏领域语义
id, name, value

// 常量和变量混淆
private static final int maxRetries = 3;  // 应该使用大写
private String WorkflowExecutionId;       // 应该使用驼峰命名
```

## 命名检查清单

在编写代码时，检查以下问题：

1. [ ] 命名是否反映领域语义？
2. [ ] 是否存在命名混淆？
3. [ ] 是否使用了成对命名？
4. [ ] 常量和变量是否区分清楚？
5. [ ] 是否存在重复的命名？