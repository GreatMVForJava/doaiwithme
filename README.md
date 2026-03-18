# AI 复合工程使用手册

## 一、工程理念

1. 本工程的核心理念是复合工程
2. **本工程的目标**：让人类程序员和 AI 的每次交互都有价值，并通过沉淀的方式把这个价值，固定下来，分享给团队和给 AI使用；
3. **本工程的目的**：是为了 AI 和人类程序员更好的协作，不仅仅是规范 AI 的输入输出行为，AI 写的代码仅仅是结果产物之一；

## 二、使用方法

1. 下载：[https://github.com/GreatMVForJava/doaiwithme/tree/iflow1.0](https://github.com/GreatMVForJava/doaiwithme/tree/iflow1.0)
2. 粘贴：在工程目录下，粘贴.iflow/和app-demand/两个文件夹
3. 打开：使用自己顺手的 ide 和 AI 模型（工程例子来自于心流：[https://platform.iflow.cn/cli/quickstart](https://platform.iflow.cn/cli/quickstart)）
4. 使用：使用 `快速入门.md` 中的第二章

## 三、工程内容解析

1. 以目录和文档的形式组织，目录和文档名也同样属于上下文，也有核心含义；
2. 文档命名规范：
   1. 人类专用：中文命名，AI 参考，用来人类程序员和人类程序员之间的沟通；如：`快速入门.md`
   2. AI 专用：人类不需要关心，AI 行为规范，分为两种：目录级别沉淀落地规范（全大写+下划线,如：`EXPERIENCE_SPEC.md`），AI 行为指导规范（全小写+短横杠，如：`collaboration-method.md`）；前者基本不变，后者可以根据项目特性修改；
   3. 人和 AI 协作：首字母小写的驼峰规则，人类程序员重点关注，需要考究字段，逻辑，内容（可使用一些 prompt 技巧），最终和 AI 使用的交互入口，如工程中的 `start.md` 和 `endpoint.md`

**重要内容**

**工程结构概述：**

```
.iflow/
├── ecosystem                    # 上下文模块
│   ├── concept/
│   │   └── GLOBAL_CONCEPTS.md  # 全局概念定义文档（定义核心术语如智能人、协作模式等）
│   ├── experience/
│   │   ├── EXPERIENCE_SPEC.md  # 经验规范总入口（定义经验沉淀格式和分类）
│   │   ├── cold-start.md       # 冷启动方法
│   │   ├── collaboration-method.md  # 协作方法（乔哈里窗、苏格拉底等）
│   │   ├── collaboration-role.md    # 协作角色定义
│   │   └── infrastructure.md   # 基础设施设计
│   ├── issues/
│   │   ├── ISSUES_SPEC.md      # 问题规范总入口（定义问题分类和记录规范）
│   │   └── 2026-03-02-AI主动性不足.md  # 具体问题记录
│   ├── rule/
│   │   ├── RULE_SPEC.md        # 规则规范总入口（定义规则设计规范和分类导航）
│   │   ├── ai-coding/          # AI 编码规范
│   │   │   ├── CODING_SPEC.md  # 编码规范总入口（设计原则、代码架构、代码质量）
│   │   │   ├── 17-javadoc-comment/
│   │   │   ├── 20-database-idempotence/
│   │   │   ├── 22-method-consistency/
│   │   │   ├── 23-modification-completeness/
│   │   │   ├── 25-concurrency-safety/
│   │   │   ├── 26-interface-parameter-validation/
│   │   │   └── 27-naming-semantic/
│   │   └── ai-collaboration/   # AI 协作规范
│   │       ├── AI_COLLABORATION_SPEC.md  # 协作规范总入口（协作流程、Git规范、文档规范）
│   │       ├── 04-linkage-integrity/
│   │       ├── 05-comprehensive-analysis/
│   │       ├── 07-markdown-format/
│   │       ├── 09-post-modification-check/
│   │       ├── checkpoint/
│   │       │   └── CHECKPOINT_SPEC.md    # 检查点规范（关键操作的检查触发机制）
│   │       └── workflow/
│   │           └── WORKFLOW_SPEC.md      # 流程规范（预检→确认→规划→执行→自检→沉淀）
│   └── skills/
│       ├── SKILLS_SPEC.md      # 技能规范总入口（定义Skills元数据、调用流程、创建规范）
│       ├── context-search-skill.md
│       └── web-search-skill.md
├── start.md                    # AI 行为启动入口
├── endPoint.md                 # 执行流程规范
└── 备忘录.md                    # 人类备忘录

app-demand/                     # 应用需求模块
├── APP_DEMAND_SPEC.md          # 需求规范总入口（定义需求生命周期和协作模式）
├── requirementsGuidelines.md   # 需求编写准则
├── requirementsTemplate.md     # 需求文档模板
└── 2026-02-27/                 # 按日期组织的需求
    └── 支付 demo/
        ├── requirementColdStart.md  # 需求级冷启动（人与AI共用）
        ├── 产品/
        │   └── 支付 demo.md
        └── 测试/
            └── 支付 demo测试问题.md
```

> 其中.iflow/ecosystem/rule/ai-coding 是基于 JDK17 版本做的代码规范，可以不用！！！

## 四、核心概念

1. **智能人**：AI + 人的组合体，具备决策 + 执行的完整能力
2. **协作模式**：AI 自我理解、AI+人协作、人+人配合、智能人+智能人、AI+AI配合
3. 详细定义见 `.iflow/ecosystem/concept/GLOBAL_CONCEPTS.md`

## 五、复合工程相关

1. [认知重建：Speckit 用了三个月，我放弃了——走出工具很强但用不好的困境](https://mp.weixin.qq.com/s/CXx-0ar1EBf14vgQHHjU7A)
2. [Compound Engineering: How Every Codes With Agents](https://every.to/chain-of-thought/compound-engineering-how-every-codes-with-agents)
3. [GitHub - EveryInc/compound-engineering-plugin: Official Claude Code compound engineering plugin](https://github.com/EveryInc/compound-engineering-plugin)
4. [AI 工程化落地实践：推翻"完美架构"，回归提示词本质](https://mp.weixin.qq.com/s/PRLrVURRycKOhnFOGGdJYA)
