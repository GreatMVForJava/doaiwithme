# Markdown格式规范

## 规则 30：Markdown格式

**规则内容**：编写 Markdown 文档时，代码块必须使用三个反引号+空格+语言标识符的格式 → 思想：正确的格式支持语法高亮，提高文档可读性

## 为什么需要规范格式

正确的代码块格式可以：
- 支持语法高亮，提高可读性
- 统一文档风格，便于维护
- 避免 Markdown 渲染器解析错误

## 常用语言标识符

| 标识符 | 用途 | 示例 |
|--------|------|------|
| `text` | 纯文本（默认） | 普通文本、日志、配置片段 |
| `java` | Java代码 | 类、方法、代码片段 |
| `bash` | Shell命令 | 命令行操作、脚本 |
| `yaml` | YAML配置 | 配置文件 |
| `json` | JSON数据 | 数据结构、API响应 |
| `xml` | XML配置 | Spring配置、Maven配置 |
| `sql` | SQL语句 | 数据库查询 |
| `mermaid` | 流程图 | 架构图、流程图 |
| `markdown` | Markdown示例 | 文档说明 |

## 正确示例

### 示例1：纯文本

``` text
确认 → 规划 → 执行 → 自检 → 沉淀
```

### 示例2：Java代码

``` java
public class UserService {
    private final UserRepository userRepository;
    
    public User getUserById(Long userId) {
        return userRepository.findById(userId);
    }
}
```

### 示例3：Shell命令

``` bash
mvn clean install -DskipTests
```

### 示例4：YAML配置

``` yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/mydb
    username: root
    password: secret
```

### 示例5：Mermaid流程图

``` mermaid
graph TD
    A[开始] --> B[执行]
    B --> C[结束]
```

## 错误示例

### 错误1：缺少空格

````text
❌ 错误：
```java
public class User {}
```

✅ 正确：
``` java
public class User {}
```
````

**问题**：三个反引号后缺少空格，部分渲染器无法正确识别语言标识符。

### 错误2：缺少语言标识符

````text
❌ 错误：
```
public class User {}
```

✅ 正确：
``` java
public class User {}
```
````

**问题**：缺少语言标识符，无法启用语法高亮。

### 错误3：使用错误的标识符

````text
❌ 错误：
``` code
public class User {}
```

✅ 正确：
``` java
public class User {}
```
````

**问题**：`code` 不是有效的语言标识符，无法启用语法高亮。

## 如何检查

### 检查清单
- [ ] 代码块是否使用了三个反引号开头？
- [ ] 三个反引号后是否有空格？
- [ ] 空格后是否有语言标识符？
- [ ] 语言标识符是否正确？

### 检查命令

``` bash
# 检查缺少空格的代码块
grep -rn '^```[a-z]' --include="*.md" | grep -v '^.*:``` [a-z]'

# 检查缺少语言标识符的代码块
grep -rn '^```$' --include="*.md"
```

## 常见误区

1. **以为 ` ```text ` 和 ` ```text ` 一样**：必须有空格
2. **以为可以省略语言标识符**：应该始终指定，默认使用 `text`
3. **以为所有渲染器都兼容**：不同渲染器对格式要求不同，规范格式最通用

## 最佳实践

### 实践1：统一使用 text 作为默认标识符

当内容不属于特定编程语言时，使用 `text` 标识符：

``` text
确认 → 规划 → 执行 → 自检 → 沉淀
```

### 实践2：Mermaid 图表统一使用 mermaid 标识符

``` mermaid
graph TD
    A[开始] --> B[结束]
```

### 实践3：配置文件使用对应标识符

- YAML 配置 → ` ``` yaml `
- JSON 数据 → ` ``` json `
- XML 配置 → ` ``` xml `
- Properties 配置 → ` ``` properties `
