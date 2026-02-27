# 删除未使用代码同步原则

## 规则 15：删除未使用代码同步原则

**规则内容**：删除接口方法后必须同步删除实现类中的方法、相关依赖注入字段和 import 语句；思想：@Override 注解强制接口与实现同步，避免编译错误和代码冗余

## 为什么需要同步删除

避免编译错误和代码冗余，保持代码一致性，提高代码可读性，降低维护成本。

## 项目中的实际案例

### 案例1：删除 RAG 相关服务

**背景**：项目不再使用 RAG 功能，需要删除 RAG 相关的所有代码

**删除的文件**：
- `RAGService.java` - RAG 服务接口
- `RAGServiceImpl.java` - RAG 服务实现
- `RAGSearchRequest.java` - RAG 搜索请求
- `RAGVectorizeRequest.java` - RAG 向量化请求
- `RAGSearchResponse.java` - RAG 搜索响应
- `RAGVectorizeResponse.java` - RAG 向量化响应

**同步删除的内容**：
- 删除接口中的所有方法声明
- 删除实现类中的所有方法实现
- 删除依赖注入字段（如 `RAGService ragService`）
- 删除所有 import 语句
- 删除所有调用代码

**结果**：代码编译通过，没有编译错误和警告。

### 案例2：删除 PromptTemplateEntity 和 PromptTemplateMapper

**背景**：提示词管理改为文件系统管理，不再使用数据库存储

**删除的文件**：
- `PromptTemplateEntity.java` - 提示词模板实体
- `PromptTemplateMapper.java` - 提示词模板 Mapper

**同步删除的内容**：
- 删除实体类和 Mapper 类
- 删除依赖注入字段
- 删除所有 import 语句
- 删除所有数据库操作代码

**结果**：代码编译通过，提示词管理改为文件系统管理。

## 常见错误案例

### 错误1：删除接口方法后未删除实现类方法

``` java
// 删除接口方法后
public interface UserRepository {
    // deleteUserById 方法已被删除
}

// 但实现类中仍然存在
@Repository
public class UserRepositoryImpl implements UserRepository {
    @Override
    public void deleteUserById(Long userId) {
        userRepository.deleteById(userId);
    }
}
```

**问题**：实现类中的方法无法编译通过。

### 错误2：删除方法后未删除 import 语句

``` java
// 方法已被删除，但 import 仍然存在
import com.example.utils.StringUtils;

public class UserService {
    // deleteUser 方法已被删除，但 import 仍然存在
}
```

**问题**：import 语句无用，造成代码冗余。

### 错误3：删除接口后未删除依赖注入字段

``` java
// RAGService 接口已被删除
@Service
@RequiredArgsConstructor
public class UserService {
    private final RAGService ragService; // 依赖注入字段仍然存在
}
```

**问题**：编译错误，因为 RAGService 不存在。

## 如何检查

### 检查清单
- [ ] 删除接口方法后是否同步删除了实现类中的方法？
- [ ] 删除方法后是否同步删除了未使用的 import 语句？
- [ ] 删除接口后是否同步删除了依赖注入字段？
- [ ] 是否运行编译检查确保没有编译错误？

### 检查步骤

#### 步骤1：编译检查
运行 `mvn compile` 检查是否有编译错误。

#### 步骤2：检查实现类
检查实现类中是否有无法编译的方法。

#### 步骤3：检查 import 语句
检查 import 语句是否有未使用的。

#### 步骤4：检查依赖注入字段
检查依赖注入字段是否有未使用的。

## 常见误区

1. **以为实现类中的方法可以保留**：必须同步删除
2. **以为 import 语句可以保留**：必须同步删除
3. **以为依赖注入字段可以保留**：必须同步删除
4. **以为可以通过注释的方式保留**：未使用的代码必须彻底删除

## 最佳实践

### 实践1：使用 IDE 的自动删除功能
IDE 通常会提示未使用的 import 语句和方法，可以直接使用 IDE 的自动删除功能。

### 实践2：编译验证
删除代码后必须运行编译检查，确保没有编译错误。

### 实践3：完整性检查
删除代码后必须进行完整性检查，确保没有遗留未使用的代码。

### 实践4：批量删除
如果删除的是整个功能模块（如 RAG），应该：
1. 删除所有相关的类文件
2. 搜索所有引用并删除
3. 删除所有 import 语句
4. 删除所有依赖注入字段
5. 运行编译检查