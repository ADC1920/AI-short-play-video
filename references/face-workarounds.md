# Seedance 人脸审核规避五法（路线 C）

## 五法速查

| # | 方法 | 一句话原理 | 对面部影响 |
|---|---|---|---|
| 1 | 墨镜遮挡三视图 | 戴墨镜生成三视图绕过检测 | **最小（首选）** |
| 2 | 网格遮挡面部 | 图片编辑工具给面部加网格 | 小，模型会自动修复面部 |
| 3 | 无五官三视图 | 去掉五官，五官单独展示在图下方 | 中 |
| 4 | 服装+头部三视图组合 | 服饰图与头部三视图分开过审，生成时组合 | 中 |
| 5 | 多次风格转绘「洗图」 | AI 风格转绘重复三次改变图像特征 | 次数多了会崩坏 |

## 方法 1：面部遮挡的三视图（墨镜，首选）

AI 生图提示词：

> 给人物带上墨镜后生成正面、侧面、背面的全身三视图，保持人物五官、服饰、发型、画面风格不变。

使用时，视频提示词中**必须加**去除遮挡的说明，可直接具体到物品：

> 视频制作时去除人物面部墨镜

## 方法 2：网格遮挡面部

用任意图片编辑工具在人物面部添加网格即可绕过检测。**网格间隔不能过密也不能过稀疏**；不必担心遮挡导致面部与原图不同，生成时大模型会对面部进行修复。

视频提示词中加：

> 视频制作时去除人物面部网格遮挡，视频中不得出现红色网格

（后半句必须有，防止网格乱入到视频里。）

## 方法 3：无五官人物三视图

AI 生图提示词：

> 去除该人物面部五官后，制作正面、背面、侧面的全身三视图。并将人物的五官在图片正下方展示，正下方只展示五官。图片中其他元素保持不变。

视频制作时直接 @ 使用，无需额外说明。

## 方法 4：服装与头部三视图组合

把完整人物图拆成「服饰正反图 + 头部三视图」两件素材分别过审，生成时再组合。

**第 1 步，提取服饰**（英文提示词原文照录）：

```
Use the reference image as the outfit and accessories anchor. Extract the visible clothing, styling, accessories, bag, shoes, and layering details from the reference, but do not show the person. Instead, present the full look in a clean neutral gray studio as if it is being worn by an invisible model. The garments should keep a realistic worn silhouette and natural body-supported structure, but no visible human body parts should appear at all: no face, no skin, no hair, no hands, no legs, no neck. Only the outfit itself should be visible, shaped by an unseen human form. Show the complete look from both the front and the back, arranged as a clean two-view fashion presentation. Keep the front view and back view consistent in scale, styling, and garment details so the outfit can be clearly examined from both sides. Preserve the exact design language from the reference image: the same clothing items, colors, materials, tailoring, proportions, layering, hardware, accessory placement, bag style, shoe design, and overall styling logic. Do not replace items, do not simplify the look, and do not invent new fashion elements. Place everything in a premium studio setup with a smooth gray background, controlled soft lighting, and clean shadow definition so the fabric texture, structure, drape, and silhouette are easy to read. Make it feel like a luxury fashion e-commerce or editorial product presentation with high realism and sharp material fidelity. Keep the result minimal, polished, and professional. Do not add any watermark, logo, subtitles, UI elements, borders, QR codes, signatures, or extra text.
```

**第 2 步，制作头部三视图**：截取人物面部上传，用以下提示词：

> 根据该人物面部，制作出只显示头部的正面、侧面、背面三视图，三视图只展示面部和头部。不做多余显示，空白背景，其余元素保持不变。图片比例16:9

**第 3 步，组合**：视频提示词中写：

> 让参考图1中人物穿着参考图2中的衣服后作为主人公

（只用人脸参考时同理：「…后作为女主人公」等。）

卡审核时：**去掉头部三视图中人物脖子部分后重试**。

## 方法 5：多次风格转绘「洗图」

用支持风格转绘的 AI 工具：上传图片 → 风格转绘 → 下载结果 → 重新上传，**重复三次**。转绘后即绕开人脸检测。

视频提示词中要**固定画面风格**，例如：

> 将参考图1转化为写实风格后作为主人公
> 样貌使用参考图1转化为写实风格后的形象

坑点：转绘次数不宜更多，否则人物主体崩坏、性别错乱；推荐彩铅等对人物细节影响较小的风格。

## 通用经验

1. 有面部遮挡的方法，视频提示词要写明去除遮挡物，且可直接具体到是什么物品。
2. 避免使用名气高的人物、IP 作品作参考——图片可能过审，但做出的视频会被拦截。
3. 图片是否过审与提示词无关，别在「用提示词蒙骗模型」上花功夫。
4. 人脸过审不确定性很大：同一张图可尝试不同方法，甚至今天能过、明天不能用。
