# SPIC 投稿操作手册（逐步操作版）

> 按照本文档一步步操作即可完成投稿。
> 目标期刊：Signal Processing: Image Communication (Elsevier)
> 投稿系统：Editorial Manager

---

## 第零步：投稿前准备（投之前必须全部完成）

### 0.1 确认论文文件已就绪

在 `paper/` 目录下执行编译，确认生成 PDF 无报错：

```bash
cd paper
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

编译成功后，`paper/main.pdf` 就是你要上传的论文 PDF。

### 0.2 确认以下文件已准备好

| 文件 | 位置 | 说明 |
|---|---|---|
| 论文 PDF | `paper/main.pdf` | 编译好的最终版 |
| LaTeX 源码 | `paper/main.tex` + `paper/elsevier_template/` | 打包成 zip |
| Cover Letter | `docs/SUBMISSION_PACKAGE.md` 中的草稿 → 转成 PDF | 给编辑的信 |
| 图片源文件 | `paper/figures/fig*.png` | 所有图的高清版 |

### 0.3 你还需要自己准备的信息

| 信息 | 说明 | 你的情况 |
|---|---|---|
| 通讯作者邮箱 | 注册 EM 账号用 | 18818351620@163.com |
| 所有作者信息 | 姓名、单位、邮箱、ORCID | 已填入 main.tex |
| 推荐审稿人 2-3 人 | 不同机构、无合作、近 3 年有相关发表 | **你需要找** |
| 基金信息 | 项目名称+编号（如有） | **你需要填** |
| Highlights | 3-5 条，每条 ≤85 字符 | 已备好（见下文） |
| 关键词 | 3-6 个 | 已备好（见下文） |

---

## 第一步：注册 Editorial Manager 账号

### 1.1 打开投稿系统

浏览器打开：**https://www.editorialmanager.com/spic/**

### 1.2 注册账号（首次投稿必须）

1. 点击页面右侧 **"Register"** 按钮
2. 填写注册信息：
   - **Title**: 选你的称谓（Dr./Prof./Mr./Ms.）
   - **First Name**: Junlin（通讯作者名）
   - **Last Name**: Ouyang
   - **Email**: 18818351620@163.com（必须用这个邮箱）
   - **Password**: 自己设一个密码
   - **Institution**: Hunan University of Science and Technology
   - **Department**: School of Computer Science and Engineering
   - **Country**: China
3. 点击 **"Register"** 完成注册
4. 去邮箱查收验证邮件，点击链接激活账号

### 1.3 登录系统

用注册的邮箱和密码登录：https://www.editorialmanager.com/spic/

---

## 第二步：开始新投稿

### 2.1 进入投稿界面

登录后，点击左侧菜单 **"Author"** → **"Submit New Manuscript"**

### 2.2 选择文章类型

在 "Article Type Selection" 页面：
- 选择 **"Research Paper"**（研究论文）
- 点击 **"Continue"**

---

## 第三步：上传文件

### 3.1 上传论文主体

在 "Manuscript Data" 页面的 **"Attach Files"** 区域：

1. 点击 **"Browse"** 或 **"Choose File"**
2. 选择 `paper/main.pdf`（编译好的 PDF）
3. **Article Type**: 选择 **"Manuscript"**
4. 点击 **"Upload"**
5. 确认文件出现在列表中，状态为 ✅

### 3.2 上传 Cover Letter

1. 点击 **"Browse"** 选择你的 Cover Letter PDF
2. **Article Type**: 选择 **"Cover Letter"**
3. 点击 **"Upload"**

### 3.3 上传图片文件

1. 逐个上传 `paper/figures/` 下的 fig*.png 文件
2. 每个图的 **Article Type**: 选择 **"Figure"**
3. 上传的图文件：fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8

### 3.4 上传 LaTeX 源码（可选但建议）

1. 将 `paper/main.tex` + `paper/elsevier_template/` + 图文件打包成 zip
2. **Article Type**: 选择 **"LaTeX File"**
3. 上传 zip 文件

### 3.5 确认文件列表

上传完成后，检查文件列表：
- [ ] Manuscript (main.pdf) ✅
- [ ] Cover Letter ✅
- [ ] Figure files (fig1-fig8) ✅
- [ ] LaTeX source (zip) ✅（可选）

点击 **"Continue"** 进入下一步。

---

## 第四步：填写论文信息

### 4.1 General Information

| 字段 | 填写内容 |
|---|---|
| **Title** | Provenance-Verifiable Privacy Cloaking for Face Images: Safety-Region-Guided Neural Watermarking with JPEG-Robust Detection |
| **Abstract** | 复制 main.tex 中 `\begin{abstract}` 到 `\end{abstract}` 之间的内容（纯文本，去掉 LaTeX 命令） |
| **Keywords** | 依次输入：`Face recognition`, `privacy cloaking`, `neural watermarking`, `JPEG robustness`, `provenance` |

### 4.2 Authors

点击 **"Add Author"** 添加作者：

**作者 1（一作）：**
| 字段 | 内容 |
|---|---|
| Title | Mr. |
| First Name | Pan |
| Last Name | Ouyang |
| Email | 393974615@qq.com |
| ORCID | 0009-0003-3995-0847 |
| Institution | Hunan University of Science and Technology |
| Department | School of Computer Science and Engineering |
| Country | China |
| Corresponding Author | **不要勾选** |

**作者 2（通讯）：**
| 字段 | 内容 |
|---|---|
| Title | Dr. |
| First Name | Junlin |
| Last Name | Ouyang |
| Email | 18818351620@163.com |
| ORCID | 0000-0001-7155-2732 |
| Institution | Hunan University of Science and Technology |
| Department | School of Computer Science and Engineering |
| Country | China |
| Corresponding Author | **勾选 ✅** |

### 4.3 Highlights

在 "Highlights" 区域，逐条输入（每条 ≤85 字符含空格）：

1. `JPEG recompression collapses WAM decoding on cloaked faces (6% TPR@95%)`
2. `Safety-region guidance restores cloaking retention (36.1% to 42.1%)`
3. `Strength calibration + BER detection: 93-99% JPEG-robust decode at 0-0.8% FPR`
4. `Sequential cloak-then-watermark keeps PSR 93.5%; reverse drops to 70-81.5%`
5. `SOTA InvisMark fails under JPEG on same protocol; our method maintains 93-100%`

### 4.4 Additional Information

| 字段 | 填写内容 |
|---|---|
| **Article Type** | Research Paper |
| **Manuscript Number** | （系统自动分配，留空） |
| **Suggested Reviewers** | 见第五步 |
| **Exclude Reviewers** | 可留空 |
| **Funding** | 填你的基金信息（如有） |
| **Conflict of Interest** | The authors declare no conflict of interest. |
| **Ethics Statement** | This study used publicly available datasets (LFW) and did not require IRB approval. |
| **Data Availability** | 见第六步 |
| **Author Contributions** | Pan Ouyang: Methodology, Experiments, Writing. Junlin Ouyang: Supervision, Writing, Funding Acquisition. |

---

## 第五步：推荐审稿人

### 5.1 为什么要推荐

SPIC 要求（非强制但强烈建议）提供 2-3 名推荐审稿人。编辑会优先从你推荐的人中选择。

### 5.2 审稿人要求

- ❌ 不能是你同一单位的同事
- ❌ 不能是近 3 年有合作论文的人
- ✅ 必须是真实存在的学者
- ✅ 近 3 年发表过相关论文
- ✅ 用机构邮箱（非 gmail/163）
- ✅ 不同国家更好

### 5.3 怎么找审稿人

1. 去 Google Scholar 搜索相关论文（搜 "face privacy cloaking watermark" "adversarial face protection" "neural watermarking JPEG"）
2. 找近 3 年发表过类似方向论文的作者
3. 查看他们的单位和邮箱
4. 确认你和他们没有合作过

### 5.4 填写审稿人信息

在 "Suggested Reviewers" 区域，点击 "Add Reviewer"，逐个填写：

| 字段 | 说明 |
|---|---|
| First Name | 审稿人名 |
| Last Name | 审稿人姓 |
| Email | 机构邮箱 |
| Institution | 审稿人单位 |
| Country | 审稿人国家 |

**你需要自己找 2-3 个真实审稿人填入。**

---

## 第六步：填写声明和数据可用性

### 6.1 Data Availability Statement

在 "Data Availability" 字段中粘贴：

```
The LFW dataset used in this study is publicly available at
http://vis-www.cs.umass.edu/lfw/. The Fawkes implementation is available at
https://sandlab.cs.uchicago.edu/fawkes/. The WAM watermarking code and our
experimental scripts will be made available upon acceptance.
```

### 6.2 Declaration of Interest

```
The authors declare that they have no known competing financial interests
or personal relationships that could have appeared to influence the work
reported in this paper.
```

### 6.3 CRediT Author Statement

```
Pan Ouyang: Methodology, Software, Validation, Investigation, Writing - Original Draft.
Junlin Ouyang: Conceptualization, Supervision, Writing - Review & Editing, Funding Acquisition.
```

---

## 第七步：检查并提交

### 7.1 最终检查

在提交前，确认以下所有项：

- [ ] 论文 PDF 已上传
- [ ] Cover Letter 已上传
- [ ] 所有图文件已上传
- [ ] Title 正确
- [ ] Abstract 完整（150-250 词）
- [ ] Keywords 已填（3-6 个）
- [ ] Highlights 已填（3-5 条，每条 ≤85 字符）
- [ ] 所有作者信息正确（姓名、邮箱、ORCID、单位）
- [ ] 通讯作者已勾选
- [ ] 推荐审稿人已填（2-3 人）
- [ ] 数据可用性声明已填
- [ ] 利益冲突声明已填
- [ ] 作者贡献声明已填

### 7.2 构建 PDF 预览

点击 **"Build PDF"** 按钮，系统会生成投稿预览 PDF。
下载预览 PDF，检查：
- 所有图都显示正常
- 参考文献格式正确
- 没有乱码或缺失内容

### 7.3 正式提交

确认无误后，点击 **"Submit"** 按钮。

**提交后会收到确认邮件**，标题类似：
"Your manuscript [编号] has been submitted to Signal Processing: Image Communication"

---

## 第八步：投稿后

### 8.1 跟踪状态

登录 https://www.editorialmanager.com/spic/ ，在 "Author" → "Manuscripts with Decisions" 或 "Submissions Being Processed" 中查看状态。

### 8.2 常见状态

| 状态 | 含义 | 你需要做什么 |
|---|---|---|
| With Editor | 编辑在审阅 | 等待 |
| Under Review | 同行评审中 | 等待（2-3 个月） |
| Required Reviews Complete | 评审完成 | 编辑即将做决定 |
| Decision in Process | 编辑在做决定 | 等待 |
| Revise | 需要修改 | 按审稿意见修改后重新提交 |
| Accepted | 接受 | 等待校对邮件 |

### 8.3 如果收到修改意见

1. 下载审稿意见 PDF
2. 逐条回复（写 Response Letter）
3. 修改论文（用红色标注修改处）
4. 在 EM 系统中上传修改版 + Response Letter
5. 在截止日期前提交（通常给 30-60 天）

---

## 附录 A：Cover Letter 模板

在 `docs/SUBMISSION_PACKAGE.md` 中有完整草稿。核心结构：

```
Dear Editor,

We would like to submit our manuscript entitled "[论文标题]" for
consideration as a Research Paper in Signal Processing: Image Communication.

[1 段：研究背景和动机]

[1 段：4 点贡献，编号清晰]

[1 段：与已有工作的差异化]

[1 段：数据完整性说明]

We confirm that this manuscript has not been published elsewhere and is not
under consideration by another journal. All authors have approved the
manuscript and agree with its submission.

We suggest the following potential reviewers:
1. [姓名], [单位], [邮箱]
2. [姓名], [单位], [邮箱]
3. [姓名], [单位], [邮箱]

Thank you for considering our manuscript.

Sincerely,
[通讯作者姓名]
[单位]
[邮箱]
```

---

## 附录 B：投稿前最终 Checklist

### 论文内容
- [ ] 摘要 150-250 词，无 LaTeX 命令
- [ ] 关键词 3-6 个
- [ ] Highlights 3-5 条，每条 ≤85 字符
- [ ] 所有图/表在正文中有引用
- [ ] 参考文献格式统一（Numbered）
- [ ] 作者信息完整（姓名、单位、ORCID、邮箱）
- [ ] 致谢已填写（基金号等）
- [ ] 数据可用性声明已写

### 文件准备
- [ ] main.pdf 编译无报错
- [ ] 所有图文件高清（≥300dpi）
- [ ] Cover Letter 已写并转 PDF
- [ ] LaTeX 源码已打包 zip

### 投稿信息
- [ ] 推荐审稿人 2-3 人（真实、无合作、不同机构）
- [ ] 通讯作者邮箱正确
- [ ] 利益冲突声明已填
- [ ] 作者贡献声明已填

### 提交前
- [ ] Build PDF 预览无误
- [ ] 下载预览 PDF 检查
- [ ] 点击 Submit 正式提交
- [ ] 收到确认邮件
