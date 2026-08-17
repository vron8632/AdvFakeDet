# 图片生成指南

> 用于生成 paper/figures/ 下的占位图

## 已准备好的 Prompt 文件
- `paper/FIGURE_PROMPTS_中文.md` — 包含 fig1 和 fig2 的完整英文 prompt

## 生成方式

### 方式 1：手动用 gpt-image-2 / DALL-E
直接打开 `paper/FIGURE_PROMPTS_中文.md`，复制英文 prompt 到图像生成工具。

### 方式 2：用 pi 的 skill（如果支持 image generation）
```
请根据 paper/FIGURE_PROMPTS_中文.md 的描述生成 fig1 和 fig2
```

### 方式 3：手绘 + LaTeX overlay
1. 手绘流程框图（draw.io / Keynote / PPT）
2. 导出为 PDF
3. 放到 `paper/figures/` 覆盖占位图

## 需要生成的图
| 文件 | 内容 | 说明 |
|---|---|---|
| fig1_teaser_placeholder.png → fig1_teaser.png | 动机图（3栏：原图→遮蔽→水印） | 论文开篇卖点 |
| fig2_framework_placeholder.png → fig2_framework.png | 方法框架图（5阶段流水线） | 核心方法概览 |

## 已有的真实数据图（不需要重新生成）
| 文件 | 内容 |
|---|---|
| fig3_qualitative.png | 定性对比（遮蔽/水印/原始对比） |
| fig4_main_results.png | 主结果表/图 |
| fig5_jpeg_robustness.png | JPEG 鲁棒性分析 |
| fig6_ber_curve.png | BER 阈值曲线 |

## 生成后
1. 替换 `paper/figures/` 下的占位 PNG
2. 如果改名，同步修改 main.tex 中的 `\includegraphics{}` 引用
3. 编译 PDF 确认无报错
