# Drama Skills 产线

上游仓库：[worldwonderer/drama-skills](https://github.com/worldwonderer/drama-skills)（MIT）。本文件只作路由对照，细则以该仓库各 `SKILL.md` 为准。

## 十个上游技能

```text
原著分析 ─┐
          ▼
      故事开发 ──可选──► 分集剧本 ──► 资产
                                      /      \
                             图片提示词      分镜 ──► 视频提示词
                                      \      /
                                   确认后生产
                                        │
                                      审查 ──► 文本交付
```

| 上游技能 | 职责 | hb-ai 落点 |
|---|---|---|
| `short-drama` | 初始化、路由、视觉方向、Look Development、状态、交付 | `project.md`；本 skill 承担入口 |
| `short-drama-novel-analyze` | 原著抽样快评、章节索引、改编价值与分集候选 | 分析记录写入剧目目录，不改原著 |
| `short-drama-develop` | 改编契约、故事引擎、分集地图、导演阐述 | `outline.md` + `project.md` |
| `short-drama-write` | 单集目标、因果节拍、可拍剧本 | `draft.md` |
| `short-drama-assets` | 人物/造型、地点/视图、道具/状态 | `assets.md`；人物摘要同步 `characters.md` |
| `short-drama-image-prompts` | Lookdev 风格帧、角色/场景/道具参考图提示词 | `image-prompts.md` |
| `short-drama-storyboard` | 场次视觉计划、镜头、冻结关键帧 | `storyboard.md` |
| `short-drama-video-prompts` | 单镜动作、表演、摄影、声音、时间线音乐规格 | `video-prompts.md` |
| `short-drama-produce` | 展示有界 job，确认后经外部 adapter 执行 | 不默认执行；需上游安装与用户确认 |
| `short-drama-review` | 结构/内容审查与修订结论 | `review.md` |

三条单帧提示词不要混用：项目级 Lookdev 检验视觉方向；资产提示词固定可复用事实；分镜关键帧只投影本镜 start（必要时另做 end 帧）。三者都只写文本规格。
