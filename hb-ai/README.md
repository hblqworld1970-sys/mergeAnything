# hb-ai · AI 剧本创作工作空间

一个用 AI agent 辅助编辑剧本的工作空间：剧本正文用普通 Markdown 文件编辑，短剧/漫剧产线由 [`drama-skills`](./.cursor/skills/drama-skills/SKILL.md) 按 [Drama Skills](https://github.com/worldwonderer/drama-skills) 自动路由。

## 目录结构

```
hb-ai/
├── .cursor/
│   └── skills/
│       └── drama-skills/        # 短剧/漫剧产线入口（自动生效）
└── scripts/                     # 剧本正文，一个剧本一个文件夹
    ├── _template/                # 新建剧本时复制此模板
    └── <剧本名>/
        ├── characters.md
        ├── outline.md
        └── draft.md
```

## 如何使用

1. 在 `scripts/` 下复制 `_template/` 文件夹，重命名为新剧本的名字；也可直接说「初始化一个……短剧」，由 `drama-skills` 建目录。
2. 在 `hb-ai/` 里做短剧/漫剧相关工作时，`drama-skills` 会自动生效，按产线路由到分集剧本、资产、分镜、提示词与审查。不必二次配置，也不必点名。
3. 生成内容由你确认后再写入对应的 `.md` 文件。

推荐顺序：初始化 →（可选原著分析）→ 故事开发 → 分集剧本 → 资产 → 图片提示词 / 分镜 → 视频提示词 → 确认后投产 → 审查。详见 [scripts/README.md](./scripts/README.md)。

## Agent

| Agent | 职责 | 触发方式 |
| --- | --- | --- |
| [`drama-skills`](./.cursor/skills/drama-skills/SKILL.md) | 短剧/漫剧产线入口：初始化、路由、资产/分镜/提示词/审查 | 处理 `hb-ai/` 时自动生效 |

该 skill 放在 `hb-ai/.cursor/skills/`，只对 hb-ai 自动生效，不会带到 `lq-experiment-analysis`。
