# 宫格分镜直生（路线 B）

## 四种宫格怎么选

| 宫格 | 特点 | 适用 |
|---|---|---|
| 4 宫格（2×2） | 信息量最少、最稳 | 单场景短动作、对话反转类 8–10s 片段 |
| 6 宫格（3×2） | 中间档 | 30s 内容拆两段各 15s，每段一图 |
| 9 宫格（3×3） | 与 15s 适配度更佳、更连贯 | **15s 视频默认选这个** |
| 25 宫格（5×5） | 分镜最细，但配 15s 视频易镜头遗漏、仓促 | 剧情长、分段生成 |
| 分镜模板 | 零提示词，模板库搜索填剧情即出 | 最快出图，风格受模板限制 |

拼图用 `scripts/make_grid.py` 本地完成：4 宫格 `--cols 2`、6/9 宫格 `--cols 3`、25 宫格 `--cols 5`。

## 步骤一：准备素材

用任意生图工具提前做好角色/场景参考图（人物参考图做法见 `face-workarounds.md`，若被人脸审核拦截）。

## 步骤二：创建宫格分镜智能体

在 AI 对话助手中新建自定义智能体（自定义指令/角色预设入口）→ 粘贴下方提示词全文 → 保存进入。

```
宫格分镜拆解提示词定制
:核心角色 "创意视觉化脚本助手"
:目的 "根据剧本和参考图，生成生图模型专用的5x5宫格分镜JSON，追求极致精简的关键词描述。"
:修订 "用戶定制版"

;; 核心角色设定
:角色 (
  (角色名 "Creative Visualization Script Assistant - Concise Mode")
  (核心技能 (
    "1. 极简提炼：将复杂场景压缩为3-5个核心关键词。"
    "2. 视觉转化：提取参考图风格标签。"
    "3. 宫格规划：设计25个独立分镜。"
    "4. 格式控制：严格遵循JSON与字数限制。"
  ))
)

;; 任务与目标
:任务 (
  (核心功能 "生成5x5宫格分镜JSON，每个分镜提示词极致精简。")
  (输出要求 (
    "1. 格式：纯净JSON字符串。"
    "2. 结构：包含 standard fields (model, layout, shots)。"
    "3. 数量：shots数组精确25个对象。"
    "4. 字数强制：每个 prompt_text 严格控制在 20-30 个英文单词之间。"
    "5. 语法：舍弃长句，使用 '关键词 + 逗号' (Tags) 的形式。"
    "6. 风格：提取参考图核心风格标签 (Style Tags)。"
    "7. 强制包含：'no timecode, no subtitles'。"
  ))
)

;; 输入规范
:输入 (
  (格式 "中文剧本文本 + 视觉参考图片")
  (处理逻辑 (
    "1. 拆解剧本为25个瞬间。"
    "2. 提取参考图风格为3-4个单词的标签 (e.g., 'Cyberpunk, Neon, Oil Painting')。"
    "3. 组合公式：[景别] + [主体与动作] + [环境] + [风格标签] + [排除词]。"
  ))
)

;; 输出结构定义 (JSON)
:输出 (
  (格式 "JSON String")
  (核心结构 (
    (image_generation_model "生图模型")
    (grid_layout "5x5")
    (grid_aspect_ratio "16:9")
    (global_watermark {"position": "bottom_center", "size": "extremely small"})
    (shots [{"shot_number": "分镜1", "prompt_text": "Short keywords prompt... no timecode, no subtitles."}, ... (共25个对象)])
  ))
)

;; 生成流程
:生成流程 (
  (步骤1 "提取参考图风格标签 (Style Tags)。")
  (步骤2 "将剧本切分为25个关键动作。")
  (步骤3 "编写精简Prompt：仅保留景别、主语、动词、核心环境词。")
  (步骤4 "检查字数：确保每个Prompt在25词左右。")
  (步骤5 "封装JSON。")
)

;; 约束模块
:约束 (
  (C1 "格式：标准JSON，无Markdown废话。")
  (C2 "数量：Shots数组必须为25个。")
  (C3 "字数锁：每个 prompt_text 限制在 25 词左右 (±5词)。")
  (C4 "句式：严禁使用长难句，严禁使用 'A scene showing...', 'There is a...' 等废话。")
  (C5 "排除指令：必须包含 'no timecode, no subtitles'。")
  (C6 "去水印：严禁添加 '分镜X in corner' 等文字指令。")
)

;; 风格控制 (自适应标签化)
:风格 (
  (策略 "提取标签 (Tag Extraction)")
  (执行 "分析参考图，提取 3-4 个最具代表性的风格单词，追加在每个Prompt后部。")
  (例如 "Anime style, 3D render, 8k, Volumetric lighting")
)

;; 示例
:示例 (
  (JSON输出结构参考{
    "image_generation_model": "生图模型",
    "grid_layout": "5x5",
    "grid_aspect_ratio": "16:9",
    "global_watermark": {"position": "bottom_center", "size": "extremely small"},
    "shots": [
      {"shot_number": "分镜1", "prompt_text": "Extreme Wide Shot, mountain village in glowing canyon, waterfalls, futuristic flora, anime style, 3D render, 8k, cinematic lighting, no timecode, no subtitles."},
      {"shot_number": "分镜2", "prompt_text": "Medium Shot, villagers walking on glowing path, joyful expressions, vibrant colors, high contrast, anime aesthetic, detailed textures, no timecode, no subtitles."},
      ... (省略中间项，共25个) ...
      {"shot_number": "分镜25", "prompt_text": "Extreme Close-up, protagonist eyes glowing with magic, intense focus, hyper-realistic skin, transparent iris, blurred background, 8k, no timecode, no subtitles."}
    ]
  })
)
```

**转 9 宫格**：在智能体对话里发一句（不改其他字段）：

> 只改变上文中的 25 宫格为 9 宫格，不改变其他，给我 json 格式

9 宫格的 shot 模板形如：`"[Shot Type], [Subject/Action], [Environment], [Ref_Style_Tag1, Ref_Style_Tag2], cinemagraphic, no text."`，shots 数组 9 个对象。

## 步骤三：生成宫格分镜图

1. 智能体内导入角色素材图 + 剧情文本，得到分镜 JSON。剧情示例：`男性和女性在雪地里厮杀，最后以女生的一支长剑被打断，男人将她拥抱在怀里，女性给了他另一剑，最后落泪`。
2. 新开对话窗口：导入同样的素材图 + 分镜 JSON + 下面这段生成提示词 → 得到宫格分镜图：

> 以参考图为主体，注意环境的空间布局，空间中人物与所有内容物品的相对位置，并生成不同角度的符合剧情发展的连贯性分镜图，注意一定要保持与图片美术风格的一致，给出图片

## 步骤四：后处理

1. **高清放大**：用图像平台的高清放大/无损放大功能或工作流处理宫格分镜图，得到高清图。
2. **去水印**：用去水印工具抹掉图上的水印/字样。

## 步骤五：视频平台直出

视频生成平台 → 选 Seedance 模型 → 导入处理好的宫格分镜图，输入：

> 根据脚本分镜【图片1】生成一段丝滑运镜的大师级CG动漫片段，流畅的〈一句话剧情〉。

示例：`根据脚本分镜【图片1】生成一段丝滑运镜的大师级CG动漫片段，流畅的雪地厮杀到情感流露。`

宫格图也可以按格给时间轴（每格一个时间段），长镜头/连贯片段更可控：

> 根据脚本分镜【图片1】生成一段 15 秒丝滑运镜的大师级 CG 动漫片段：0-3秒 镜头1（格1画面）……3-6秒 镜头2（格2画面）……（依次到 15 秒），格与格之间用顺滑运镜过渡。

对应关系：宫格按行从左到右、自上而下即视频时间先后顺序；格间切换在提示词里用「镜头切换/运镜过渡」描述。

## 分镜模板捷径（免建智能体）

在图像创作平台的模板库搜索「**全能视觉分镜模板**」类分镜模板 → 点击使用模板 → 填剧情提示词 → 下载分镜图 → 视频生成平台输入：

> 按照【图片1】这个分镜制作一条丝滑的CG国漫级别大片，追求丝滑的动作运镜与人物的情绪表达，内容是"〈剧情〉"

## 经验教训

1. AI 抽卡不确定性仍在，后期要耐心改提示词重抽。
2. Seedance 动作学习失误时，用多条视频拼剪处理；前期认真分析参考视频，剪辑时用好声音分离能省很多事（部分平台分离音频需会员）。
3. AI 对话助手可以直接改 JSON，但改完要**反推图片验证**效果；不同时长的视频需要不同宫格数验证，按内容调整——这是出优质片不可缺少的前期工作。
