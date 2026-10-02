# manju-video · AI 漫剧制作技能

把一句话剧情或完整剧本，变成可执行的漫剧（动态漫）视频工程：分镜蓝图、宫格分镜图、逐镜视频提示词一条龙。适用于 Claude Code / ZCode 等 Agent 的 Skill 机制（SKILL.md + 按需加载的 references）。

## 技能结构

| 文件 | 说明 |
|---|---|
| `SKILL.md` | 三条路线决策、触发示例、铁律与核心公式、平台硬约束、排障速查、多集工作流 |
| `references/agent-prompt.md` | 「短剧分镜架构师」系统提示词全文（可直接粘贴）+ 配套操作流程 + 实战范例 |
| `references/grid-storyboard.md` | 宫格分镜直生：25/9 宫格 JSON 提示词、后处理链、分镜模板捷径 |
| `references/face-workarounds.md` | 人脸审核规避五法（墨镜遮挡 / 网格遮挡 / 无五官三视图 / 服装+头部组合 / 风格转绘） |
| `scripts/validate_storyboard.py` | 分镜 JSON 机检：数量 / 词数 / 必含排除词 / 禁用句式 |
| `scripts/make_grid.py` | 本地拼九宫格（3×3，也支持 25 张拼 5×5），依赖 Pillow |

## 三条路线

- **路线 A 漫剧智能体**：系统提示词 + 剧本 → 工程级分镜蓝图（镜号 / 时长 / 转场 / 声音设计）→ 逐镜生成，尾帧接力保连贯。
- **路线 B 宫格分镜直生**：剧情一句话 → 分镜 JSON（可机检）→ 宫格分镜图 → 一张图直出 15s 连贯片段。
- **路线 C 人脸审核规避五法**：人物参考图被人脸检测拦截时的五种替代方案，各带生成与使用提示词。

另有：多集长剧工作流（分集 → 每集项目目录 → 素材全剧共用）、平台硬约束核对表、7 类常见故障首修表、首镜 2 秒钩子法则。

## 安装

把 `manju-video/` 整个目录复制到 Agent 的技能根目录（如 `~/.agents/skills/` 或 `~/.claude/skills/`）。触发话术示例见 SKILL.md 的「触发示例」一节。

## 脚本自检

```bash
python scripts/validate_storyboard.py --selftest
python scripts/make_grid.py --selftest   # 需要 pip install pillow
```

## License

MIT
