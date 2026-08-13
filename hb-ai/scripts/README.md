# 剧本目录

每个剧本一个独立文件夹，命名建议使用剧本标题的拼音或英文简写，例如 `midnight-store/`。

新建剧本时，复制 `_template/` 文件夹并重命名，包含三个文件：

| 文件 | 用途 | 对应 agent |
| --- | --- | --- |
| `characters.md` | 人物设定 | `character-designer` |
| `outline.md` | 故事大纲 | `outline-writer` |
| `draft.md` | 剧本正文草稿/定稿 | `dialogue-writer` / `script-reviser` / `formatter` |

## 建议的创作流程

1. 用 `character-designer` 设计人物 → 写入 `characters.md`
2. 用 `outline-writer` 构思大纲 → 写入 `outline.md`
3. 用 `dialogue-writer` 逐场写对白 → 写入 `draft.md`
4. 用 `script-reviser` 通读检查逻辑与人物一致性，按建议修改
5. 用 `formatter` 整理成标准剧本格式，得到定稿

在 Cursor 中直接说明"用 {agent 名} 帮我做 xxx"即可调用对应 agent。
