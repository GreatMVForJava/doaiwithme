# 并发安全

## 规则 25：并发安全

**规则内容**：在多线程环境下确保共享资源的线程安全 → 优先使用局部变量而非实例变量，避免使用单例模式管理可变状态，禁止使用无界队列/缓存/Map（必须设置容量上限和过期策略），优先使用不可变对象（值对象），ThreadLocal 必须在 finally 里 remove()；思想：优先使用局部变量而非实例变量，避免使用单例模式管理可变状态，防止内存溢出和数据串线，降低并发成本

## 为什么需要确保并发安全

防止内存溢出和数据串线，降低并发成本，确保数据一致性，提高系统稳定性。

## 项目中的实际案例

### 案例1：WorkflowCallbackServiceImpl 使用静态存储避免循环依赖

**实现方式**：
``` java
@Service
@RequiredArgsConstructor
public class WorkflowCallbackServiceImpl implements WorkflowCallbackService {
    
    /**
     * 工作流上下文缓存（静态）
     * 创建原因：避免循环依赖，使用静态存储
     * 注意：使用 ConcurrentHashMap 确保线程安全
     */
    private static final Map<String, Object> CONTEXT_CACHE = new ConcurrentHashMap<>();
    
    /**
     * 节点定义缓存（静态）
     * 创建原因：避免循环依赖，使用静态存储
     * 注意：使用 ConcurrentHashMap 确保线程安全
     */
    private static final Map<String, Object> NODE_DEFINITIONS_CACHE = new ConcurrentHashMap<>();
    
    /**
     * 工作流完成后清理缓存，避免内存泄漏
     * 创建原因：工作流完成后清理缓存，避免内存泄漏
     * 对应边界：必须在工作流完成后调用
     */
    @Override
    public void clearCache(String workflowExecutionId) {
        CONTEXT_CACHE.remove(workflowExecutionId);
        NODE_DEFINITIONS_CACHE.remove(workflowExecutionId);
    }
}
```

**并发安全措施**：
- 使用 `ConcurrentHashMap` 确保线程安全
- 工作流完成后清理缓存，避免内存泄漏
- 使用 `workflowExecutionId` 作为 key，避免数据串线

### 案例2：PromptBuilder 使用局部变量

**实现方式**：
``` java
@Data
@Builder
public class PromptBuilder {
    
    /**
     * 构建Prompt（公共方法）
     * 创建原因：buildSystemPrompt 和 buildUserPrompt 有大量重复代码，提取公共方法
     * 使用场景：构建 System 或 User Prompt
     * 设计思想：统一构建逻辑，减少代码重复
     *
     * @param templates 模板列表
     * @return Prompt字符串
     */
    private String buildPrompt(List<PromptTemplate> templates) {
        if (templates == null || templates.isEmpty()) {
            return "";
        }

        // 使用局部变量，避免并发问题
        StringBuilder sb = new StringBuilder();
        Map<String, Object> mergedContext = prepareContext();

        for (PromptTemplate template : templates) {
            if (shouldIncludeTemplate(template)) {
                String content = buildTemplate(template, mergedContext);
                if (!content.isEmpty()) {
                    appendWithSeparator(sb, content);
                }
            }
        }

        return sb.toString();
    }
}
```

**并发安全措施**：
- 使用局部变量 `sb` 和 `mergedContext`，避免并发问题
- 每次调用都创建新的局部变量，不共享状态

### 案例3：LlmTaskEntity 使用不可变字段

**实现方式**：
``` java
@Data
@TableName("llm_call_record")
public class LlmTaskEntity {
    
    /**
     * 任务ID（不可变）
     * 创建原因：封装LLM任务的数据结构，用于持久化LLM调用状态
     */
    private String taskId;
    
    /**
     * 节点ID（不可变）
     */
    private String nodeId;
    
    /**
     * 工作流执行ID（不可变）
     */
    private String workflowExecutionId;
    
    // ... 其他字段
}
```

**并发安全措施**：
- 使用 Lombok 的 `@Data` 注解，但字段本身是线程安全的（String, Long 等）
- 通过数据库主键确保数据一致性

## 常见错误案例

### 错误1：使用实例变量管理可变状态

``` java
@Service
public class UserService {
    // 实例变量，线程不安全
    private List<User> userList = new ArrayList<>();

    public void addUser(User user) {
        userList.add(user); // 线程不安全
    }
}
```

**问题**：使用实例变量管理可变状态，线程不安全。

### 错误2：使用无界队列

``` java
@Service
public class MessageService {
    // 无界队列，可能导致内存溢出
    private Queue<Message> messageQueue = new LinkedList<>();

    public void addMessage(Message message) {
        messageQueue.add(message); // 无界队列，可能导致内存溢出
    }
}
```

**问题**：使用无界队列，可能导致内存溢出。

### 错误3：ThreadLocal 未在 finally 里 remove()

``` java
public class UserContext {
    private static final ThreadLocal<User> USER_CONTEXT = new ThreadLocal<>();

    public static void setUser(User user) {
        USER_CONTEXT.set(user);
    }

    public static User getUser() {
        return USER_CONTEXT.get();
    }

    // 忘记在 finally 里 remove()
    public static void clearUser() {
        USER_CONTEXT.remove();
    }
}
```

**问题**：ThreadLocal 未在 finally 里 remove()，可能导致内存泄漏。

## 如何检查

### 检查清单
- [ ] 是否使用了实例变量管理可变状态？
- [ ] 是否使用了无界队列/缓存/Map？
- [ ] ThreadLocal 是否在 finally 里 remove()？
- [ ] 是否优先使用局部变量而非实例变量？
- [ ] 是否优先使用不可变对象？

### 检查方法

#### 方法1：检查实例变量
检查是否使用了实例变量管理可变状态，应该改为局部变量。

#### 方法2：检查队列/缓存/Map
检查队列/缓存/Map 是否设置了容量上限和过期策略。

#### 方法3：检查 ThreadLocal
检查 ThreadLocal 是否在 finally 里 remove()。

## 常见误区

1. **以为实例变量线程安全**：实例变量在多线程环境下不安全
2. **以为无界队列没问题**：无界队列可能导致内存溢出
3. **以为 ThreadLocal 不需要 remove()**：ThreadLocal 必须在 finally 里 remove()

## 最佳实践

### 实践1：优先使用局部变量

``` java
@Service
public class UserService {
    public void addUser(User user) {
        // 使用局部变量
        List<User> userList = new ArrayList<>();
        userList.add(user);
        // ... 处理 userList
    }
}
```

### 实践2：使用有界队列

``` java
@Service
public class MessageService {
    // 有界队列，设置容量上限
    private final BlockingQueue<Message> messageQueue = new LinkedBlockingQueue<>(1000);

    public void addMessage(Message message) throws InterruptedException {
        messageQueue.put(message); // 有界队列，队列满时阻塞
    }
}
```

### 实践3：ThreadLocal 在 finally 里 remove()

``` java
public class UserContext {
    private static final ThreadLocal<User> USER_CONTEXT = new ThreadLocal<>();

    public static void execute(Runnable task) {
        try {
            task.run();
        } finally {
            USER_CONTEXT.remove(); // 在 finally 里 remove()
        }
    }
}
```

### 实践4：优先使用不可变对象

``` java
// 不可变对象（值对象）
public class UserId {
    private final Long id;

    public UserId(Long id) {
        this.id = id;
    }

    public Long getId() {
        return id;
    }
}
```

### 实践5：使用线程安全的集合

``` java
// 使用线程安全的集合
private static final Map<String, Object> CACHE = new ConcurrentHashMap<>();

private static final List<String> LIST = new CopyOnWriteArrayList<>();
```