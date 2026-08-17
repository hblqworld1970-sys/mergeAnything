# lq-experiment-analysis · 医学实验数据分析

梁晴的医学实验分析工作空间。文献、统计、作图、写稿与报告规范审查走仓库内的 [MedSci Skills](https://github.com/Aperivue/medsci-skills)（当前 vendored 版本 v5.25.0）。

## 已确定

- 用途：对医学数据实验结果进行分析
- 不需要 Web 应用（no app）
- 技能接入：59 个上游技能放在本仓库 `lq-experiment-analysis/.cursor/skills/`，拉代码即生效，不必每人本机再装
- 没有默认流水线：每一步先确认当前阶段再动手
- 文献结论、引用、统计数字、图表解读、投稿动作若不确定，先问再写

## 目录

```
lq-experiment-analysis/
├── .cursor/
│   ├── rules/medsci-skills.mdc   # 本项目转向规则（不确定先问）
│   └── skills/                   # MedSci Skills（拉代码即生效）
├── keti/                         # 课题原始材料
├── answer/                       # 思路 / 分析文字产出
├── pp/                           # 机制图
├── data/                         # 分析用数据（可识别个人信息不提交）
├── analysis/                     # 统计代码、表、图
├── manuscript/                   # 稿件
└── qc/                           # 规范审查与引用核查
```

`keti/`、`answer/`、`pp/` 保持原样。`data/`、`analysis/`、`manuscript/`、`qc/` 给后续统计和稿件用。

## 如何使用

1. 拉取本仓库后用 Cursor 打开。技能在 `lq-experiment-analysis/.cursor/skills/`，**不必**再跑 `npx medsci-skills install`。
2. 在 `lq-experiment-analysis/` 里做医学研究相关工作时，按 rule 选用 `search-lit`、`analyze-stats`、`make-figures`、`write-paper`、`check-reporting` 等技能。
3. 没有说清要做哪一步时，agent 会先问你，不会自行跑完整投稿流水线。
4. 第一次拉到这些技能后，重启一次 Cursor 再测。

更新上游技能时，把新版本拷进 `.cursor/skills/` 后提交，全员拉代码即可同步。不要改成只装在某人本机 `~/.claude/skills/`。

## 待确认

- 具体分析方法（描述性统计 / 组间比较 / 生存分析 / 诊断试验评估 / 回归分析等）
- 数据格式与典型字段
