# 论文配图生成 Prompt（gpt-image-2 用，文字请用英文）

> 生成后替换 paper/figures/fig1_teaser_placeholder.png 和 fig2_framework_placeholder.png
> 图片比例 16:9，画布内文字一律英文（以下中文是给你看的说明）

---

## 图 1：Teaser 动机图（fig1_teaser_placeholder.png）

**画面布局（左→右，共 3 栏 + 中间箭头连接）**：

- 第 1 栏：一张清晰的人脸照片（正面、中性表情、半身），下方标注 `Original Face`
- 第 2 栏：同一张脸，肉眼几乎看不出变化，但加了一层极淡的噪点质感，下方标注 `Cloaked (Fawkes)`，右上角小标签 `FR: Not Recognized ✗`（打叉的绿色识别框）
- 第 3 栏：同一张脸，视觉上与第 2 栏几乎相同，但在面部轮廓外圈有淡蓝色半透明"水印波纹"示意层，下方标注 `Cloaked + Watermarked`，右上角小标签 `FR: Not Recognized ✗` + 左下角 `Watermark: Verified ✓`
- 底部一行小字：`Privacy preserved + Provenance verifiable`

**风格**：学术论文 teaser，浅色背景（白/浅灰），干净扁平，人物写实。3 栏用浅色圆角卡片分隔，中间用箭头连接（→）。
**英文文字**（务必用这些）：
- `Original Face`
- `Cloaked (Fawkes)`
- `Cloaked + Watermarked`
- `FR: Not Recognized`
- `Watermark: Verified`
- `Privacy preserved + Provenance verifiable`

---

## 图 2：方法框架图（fig2_framework_placeholder.png）

**画面布局（流水线，从左到右 4 个阶段，每个阶段一个浅色圆角卡片，卡片间用箭头连接）**：

1. **阶段 1（输入）**：人脸照片缩略图，标注 `Clean Face x`，旁边一个小的锁/隐私图标
2. **阶段 2（遮蔽）**：同一人脸 + 淡噪点，标注 `Fawkes Cloaking`，下方小公式 `min ||f(c(x)) - f_target||`，卡片右上角小标签 `FR: Evaded`
3. **阶段 3（安全区域图）**：人脸 + 叠加的暖色热力图（眼睛/鼻子区域红黄，脸颊冷色），标注 `Safety Map R (FR sensitivity)`，下方小公式 `S = 1 - R`
4. **阶段 4（水印嵌入）**：人脸 + 面部轮廓外的淡蓝色波纹，标注 `WAM Embedding`，下方小公式 `y = c(x) + β·S·Δ`
5. **阶段 5（输出 + 验证）**：最终人脸图，标注 `Watermarked Cloaked Image y`，右侧一个"对勾"徽章标注 `Detect: BER ≤ θ`

**底部一条横向时间轴**：从阶段 2 到阶段 5 的流水线箭头，标注 `Sequential Pipeline`

**风格**：学术论文方法图，浅色背景，扁平化 2D 图标风格，暖色热力图 + 冷色水印对比，公式用等宽/衬线字体。
**英文文字**（务必用这些）：
- `Clean Face x`
- `Fawkes Cloaking` / `min ||f(c(x)) − f_target||` / `FR: Evaded`
- `Safety Map R (FR sensitivity)` / `S = 1 − R`
- `WAM Embedding` / `y = c(x) + β·S·Δ`
- `Watermarked Cloaked Image y` / `Detect: BER ≤ θ`
- `Sequential Pipeline`

---

## 生成后处理
1. 图片保存到 `paper/figures/` 覆盖占位图（同名即可，LaTeX 会自动引用）
2. 建议分辨率 1920×1080 以上，PNG
3. 如果 gpt-image-2 无法保证英文文字正确，可接受轻微瑕疵，之后手动修图
