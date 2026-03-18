# 效果等价

> **定位**: 形式不同但效果相同，降低认知负担
> **L2 引用**: @.iflow/ecosystem/skills/SKILLS_SPEC.md

---

## 定义

形式不同但效果相同，降低认知负担。

## 核心原则

- 脚本不需要知道自己在沙箱里运行
- 它只看到一个正常的目录结构
- 实际上在一个精心隔离的沙箱里

## 使用场景

- 沙箱执行：脚本写 `open("out/report.txt")` 和 `open("$OUTPUT_DIR/report.txt")` 效果相同
- 符号链接：`out/` 指向 `$OUTPUT_DIR`，脚本无感知
- 降低学习成本：不需要学习沙箱的特殊路径

## 示例

```
# 沙箱中的效果等价
脚本视角：我在 skills/pdf/ 目录，写文件到 out/report.txt
实际视角：文件被符号链接到 /tmp/ws_xxx/out/report.txt

# 脚本代码（无需感知沙箱）
with open("out/report.txt", "w") as f:  # 形式：相对路径
    f.write(content)
# 效果：写入沙箱的输出目录
```

## L2 详细规范

- 详细规范：@.iflow/ecosystem/skills/SKILLS_SPEC.md
