# 接口参数校验规范

## 规则 22：接口参数校验规范

**规则内容**：外部接口参数转换在 DTO 层处理 → DTO 提供规范化方法（如 getNormalizedStatus），Service 层使用规范化方法；思想：外部接口的参数格式不受控制，DTO 层负责参数转换和适配，Service 层使用规范化的参数，避免对外部接口的依赖过于严格

## 为什么需要接口参数校验规范

外部接口的参数格式不受控制，DTO 层负责参数转换和适配，Service 层使用规范化的参数，避免对外部接口的依赖过于严格，提高代码可维护性。

## 项目中的实际案例

### 案例1：OcrCallbackRequest 规范化 status

**实现方式**：
``` java
@Data
public class OcrCallbackRequest {
    
    /**
     * 状态
     * 创建原因：外部接口的 status 可能是小写（如 "success"），需要转换为大写（如 "SUCCESS"）
     * 对应边界：外部接口的 status 格式不受控制
     */
    private String status;
    
    /**
     * 获取规范化的状态
     * 创建原因：外部接口的 status 可能是小写，需要转换为大写
     * 使用场景：Service 层使用规范化方法获取状态
     * 设计思想：DTO 层负责参数转换和适配，Service 层使用规范化的参数
     *
     * @return 规范化的状态（大写）
     */
    public String getNormalizedStatus() {
        if (status == null || status.isEmpty()) {
            return null;
        }
        return status.toUpperCase();
    }
}
```

**使用方式**：
``` java
@Service
@RequiredArgsConstructor
public class OcrCallbackServiceImpl implements OcrCallbackService {
    
    @Override
    public void handleCallback(OcrCallbackRequest request) {
        // 使用规范化方法获取状态
        String status = request.getNormalizedStatus();
        
        // Service 层使用规范化的参数
        if ("SUCCESS".equals(status)) {
            // 处理成功
        } else if ("FAILED".equals(status)) {
            // 处理失败
        }
    }
}
```

**优点**：
- DTO 层负责参数转换和适配
- Service 层使用规范化的参数
- 避免对外部接口的依赖过于严格

### 案例2：LlmCallbackRequest 规范化 callbackType

**实现方式**：
``` java
@Data
public class LlmCallbackRequest {
    
    /**
     * 回调类型
     * 创建原因：外部接口的 callbackType 可能是多种格式，需要统一规范化
     */
    private String callbackType;
    
    /**
     * 获取规范化的回调类型
     * 创建原因：外部接口的 callbackType 可能是多种格式，需要统一规范化
     * 使用场景：Service 层使用规范化方法获取回调类型
     * 设计思想：DTO 层负责参数转换和适配，Service 层使用规范化的参数
     *
     * @return 规范化的回调类型
     */
    public String getNormalizedCallbackType() {
        if (callbackType == null || callbackType.isEmpty()) {
            return null;
        }
        return callbackType.toUpperCase();
    }
}
```

**使用方式**：
``` java
@Service
@RequiredArgsConstructor
public class LlmCallbackServiceImpl implements LlmCallbackService {
    
    @Override
    public void handleCallback(LlmCallbackRequest request) {
        // 使用规范化方法获取回调类型
        String callbackType = request.getNormalizedCallbackType();
        
        // Service 层使用规范化的参数
        if ("ASYNC".equals(callbackType)) {
            // 处理异步回调
        }
    }
}
```

## 常见错误案例

### 错误1：在 Service 层进行参数转换

``` java
@Service
@RequiredArgsConstructor
public class OcrCallbackServiceImpl implements OcrCallbackService {
    
    @Override
    public void handleCallback(OcrCallbackRequest request) {
        // 在 Service 层进行参数转换（错误）
        String status = request.getStatus();
        if (status != null) {
            status = status.toUpperCase();
        }
        
        // Service 层使用规范化的参数
        if ("SUCCESS".equals(status)) {
            // 处理成功
        }
    }
}
```

**问题**：在 Service 层进行参数转换，违反了分层原则。

### 错误2：对外部接口的依赖过于严格

``` java
@Service
@RequiredArgsConstructor
public class OcrCallbackServiceImpl implements OcrCallbackService {
    
    @Override
    public void handleCallback(OcrCallbackRequest request) {
        // 对外部接口的依赖过于严格，要求 status 必须是大写
        if ("SUCCESS".equals(request.getStatus())) {
            // 处理成功
        }
    }
}
```

**问题**：对外部接口的依赖过于严格，如果外部接口的 status 是小写，就会出错。

## 如何检查

### 检查清单
- [ ] DTO 层是否提供了规范化方法？
- [ ] Service 层是否使用了规范化方法？
- [ ] 是否在 Service 层进行了参数转换？
- [ ] 是否对外部接口的依赖过于严格？

### 检查方法

#### 方法1：检查 DTO 层
检查 DTO 层是否提供了规范化方法（如 getNormalizedStatus）。

#### 方法2：检查 Service 层
检查 Service 层是否使用了规范化方法，而不是直接使用原始参数。

## 常见误区

1. **以为可以在 Service 层进行参数转换**：应该在 DTO 层进行参数转换
2. **以为对外部接口的依赖越严格越好**：对外部接口的依赖过于严格会导致错误
3. **以为不需要规范化方法**：规范化方法可以提高代码可维护性

## 最佳实践

### 实践1：DTO 层提供规范化方法

``` java
@Data
public class CallbackRequest {
    private String status;
    
    /**
     * 获取规范化的状态
     * @return 规范化的状态（大写）
     */
    public String getNormalizedStatus() {
        if (status == null || status.isEmpty()) {
            return null;
        }
        return status.toUpperCase();
    }
}
```

### 实践2：Service 层使用规范化方法

``` java
@Service
@RequiredArgsConstructor
public class CallbackServiceImpl implements CallbackService {
    
    @Override
    public void handleCallback(CallbackRequest request) {
        // 使用规范化方法获取状态
        String status = request.getNormalizedStatus();
        
        // Service 层使用规范化的参数
        if ("SUCCESS".equals(status)) {
            // 处理成功
        }
    }
}
```

### 实践3：避免对外部接口的依赖过于严格

``` java
// 不推荐：对外部接口的依赖过于严格
if ("SUCCESS".equals(request.getStatus())) {
    // 处理成功
}

// 推荐：使用规范化方法
if ("SUCCESS".equals(request.getNormalizedStatus())) {
    // 处理成功
}
```

### 实践4：DTO 层负责参数转换和适配

DTO 层负责参数转换和适配，Service 层使用规范化的参数，这样可以：
- 提高代码可维护性
- 避免对外部接口的依赖过于严格
- 符合分层原则