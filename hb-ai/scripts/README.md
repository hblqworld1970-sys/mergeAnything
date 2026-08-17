# 剧本目录

每个剧本一个独立文件夹，命名建议使用剧本标题的拼音或英文简写，例如 `midnight-store/`。

新建剧本时，复制 `_template/` 文件夹并重命名，或让 `drama-skills` 初始化。模板含三个文学稿；产线后续阶段会按需追加制作文件。

| 文件 | 用途 |
| --- | --- |
| `characters.md` | 人物设定 |
| `outline.md` | 故事大纲 / 分集地图摘要 |
| `draft.md` | 剧本正文草稿/定稿 |
| `project.md` | 制作形态、视觉方向、当前阶段（初始化后写入） |
| `assets.md` | 人物造型、地点、道具 |
| `image-prompts.md` | 参考图与 Lookdev 提示词 |
| `storyboard.md` | 分镜与关键帧 |
| `video-prompts.md` | 视频提示词 |
| `review.md` | 审查记录 |

## 建议的创作流程

1. 初始化剧目（标题、画幅、语言）
2. 可选：原著抽样快评
3. 故事开发 / 分集地图 → `outline.md`
4. 写单集可拍剧本 → `draft.md`，人物写入 `characters.md`
5. 拆资产 → `assets.md`
6. 图片提示词与分镜（可并行）
7. 视频提示词
8. 确认后投产
9. 审查 → `review.md`

全部由自动生效的 `drama-skills` 路由。详见 [drama-skills/SKILL.md](../.cursor/skills/drama-skills/SKILL.md)。
