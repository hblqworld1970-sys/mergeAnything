# hb-ai · AI 剧本创作工作空间

一个用 AI agent 辅助编辑剧本的工作空间：`剧本正文用普通 Markdown 文件编辑，创作/修订过程由若干专职 Cursor Agent Skill 辅助完成。

## 目录结构

```
hb-ai/
├── .cursor/
│   └── skills/                  # 剧本创作用的 AI agent（Cursor Agent Skills）
│       ├── character-designer/  # 人物设定
│       ├── outline-writer/      # 大纲构思
│       ├── dialogue-writer/     # 对白创作
│       ├── script-reviser/      # 整体润色/修订
│       └── formatter/           # 标准格式排版
└── scripts/                     # 剧本正文，一个剧本一个文件夹
    ├── _template/                # 新建剧本时复制此模板
    └── <剧本名>/
        ├── characters.md
        ├── outline.md
        └── draft.md
```

## 如何使用

1. 在 `scripts/` 下复制 `_template/` 文件夹，重命名为新剧本的名字
2. 在 Cursor 中直接对话，按名字调用对应 agent，例如：
   - "用 `character-designer` 帮我设计这个剧本的主角"
   - "用 `outline-writer` 帮我构思大纲，题材是悬疑，讲一个……"
   - "用 `dialogue-writer` 帮我写场景 3 的对白"
   - "用 `script-reviser` 检查一下 `draft.md` 有没有逻辑问题"
   - "用 `formatter` 把这份草稿整理成标准剧本格式"
3. agent 生成的内容由你确认后写入对应的 `.md` 文件

推荐的创作顺序：人物设定 → 大纲 → 分场对白草稿 → 修订 → 排版定稿。详见 [scripts/README.md](./scripts/README.md)。

## 各 agent 一览

| Agent | 职责 | 触发方式 |
| --- | --- | --- |
| [`character-designer`](./.cursor/skills/character-designer/SKILL.md) | 设计角色档案：身份、性格、目标、人物弧光 | 显式命名调用 |
| [`outline-writer`](./.cursor/skills/outline-writer/SKILL.md) | 构思故事大纲与分场情节结构 | 显式命名调用 |
| [`dialogue-writer`](./.cursor/skills/dialogue-writer/SKILL.md) | 撰写/润色角色对白 | 显式命名调用 |
| [`script-reviser`](./.cursor/skills/script-reviser/SKILL.md) | 通读草稿，给出逻辑/节奏/一致性修订意见 | 显式命名调用 |
| [`formatter`](./.cursor/skills/formatter/SKILL.md) | 整理为标准剧本格式（场景/动作/对白排版） | 显式命名调用 |

这些 agent 均设置为**仅在被明确点名时才触发**（`disable-model-invocation: true`），不会在你做其他事情时意外介入。如果需要新增专职 agent（比如"分镜脚本 agent"），可参考现有 skill 的结构新建一个。
