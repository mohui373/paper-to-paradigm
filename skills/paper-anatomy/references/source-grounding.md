# 来源准备与精确定位

## 目的

把 PDF 页码、章节、图、表、内嵌图片和材料范围写入独立的 `source_bundle.json`。ABC 主报告只使用紧凑证据指针，不复制整页文本，也不把定位清单塞进正文。

## 准备流程

收到 PDF 时先运行：

```bash
python scripts/prepare_paper.py PAPER.pdf -o source_bundle.json
```

若 PDF 是会议集、论文集或合订本，并且用户指定了其中一篇，可用论文序号、`paper_id`、DOI 或唯一标题短语选择：

```bash
python scripts/prepare_paper.py PROCEEDINGS.pdf -o source_bundle.json --article "HyperCare"
```

可重复使用 `--article` 选择多篇。没有提供 `--article` 时，脚本将 `selection.mode` 记为 `all_default`，后续默认阅读识别出的全部论文；选择词不存在或同时命中多篇时立即报错，不猜测目标。

需要逐页视觉检查时可增加：

```bash
python scripts/prepare_paper.py PAPER.pdf -o source_bundle.json --render-pages rendered_pages
```

`--render-pages` 需要系统可调用 `pdftoppm`。文本提取依赖 `pypdf`，精确坐标和内嵌图片清单优先使用 `pdfplumber`。

## 合格索引的读取顺序

先读取 `document_index`，不要先把 `pages[].text` 全部送入模型：

1. 查看 `document_type` 与 `paper_count`，先判断是单篇论文还是多论文集合；`front_matter` 与 `back_matter` 单独记录目录、序言或作者索引等集合级页面，不把它们误算进某篇论文。
2. 对会议集/论文集，核对每个 `paper_id`、标题、DOI 候选和起止 PDF 页；按用户指定目标读取，未指定则依次读取全部论文。
3. 对每篇论文查看 `canonical_sections`，按固定顺序定位：
   - `abstract`：摘要；
   - `introduction_theory`：前言、研究背景、理论与文献综述；
   - `research_design`：研究设计、方法、样本、程序、材料与测量；
   - `results_analysis`：结果、数据处理与统计分析；
   - `discussion_value`：讨论、结论、贡献、启示、局限与文章价值。
4. 只把当前分析所需的页码范围从 `pages` 带入上下文；需要核对图表时再加载对应页及相邻解释页。
5. 某一类显示 `not_detected` 时，表示自动索引没有识别到明确标题，不等于论文没有该内容。此时检查 `raw_sections`、页面文本或渲染页，并在报告中说明人工校正。

`document_index` 是导航层，不是论文摘要，也不替代逐页证据核查。自动识别依赖版面标题；扫描件、非常规排版或没有 Abstract 标题的论文集需要 OCR 或人工校正边界。

## 三种证据状态

- `page-grounded`：大多数页面可提取文字，可定位到 PDF 页码、章节、图表和图片坐标。
- `mixed-page-grounded`：只有部分页面可提取文字；可使用页码，但缺字页面必须视觉检查或 OCR。
- `image-page-grounded`：只能确认 PDF 页与图片范围，不能在 OCR 前声称已经读懂页面文字。
- 只有摘要、网页片段或二手描述而没有 PDF 时，不运行脚本，在报告中标为 `source-limited`，不得猜页码。

## 定位格式

正文结论优先在句末使用：

- `[Paper: PDF p. 7]`
- `[Paper: PDF p. 7, Fig. 2]`
- `[Paper: PDF p. 9, Table 1]`
- `[Supplement: PDF p. 3, Appendix A]`
- `[OSF: Materials/Instructions.docx, p. 2]`

PDF 页码始终指文件从第一页开始计算的页序；若印刷页码不同，可写成 `[Paper: PDF p. 7; printed p. 3]`。不要只写“见结果部分”或“见图”，也不要把推断绑定到不存在的精确位置。

## 主报告中的最小定位要求

1. B4 每条关键结果至少有一个页码指针；结果主要来自图或表时同时给图表编号。
2. C1 每条核心解释指向结果/讨论所在页；作者解释与本 Skill 判断分别定位。
3. “最终判断”中的每个实质性结论都有至少一个来源指针；同一来源支撑连续两句时可合并一次。
4. 若正文、图、表、附录或补充材料互相矛盾，保留双方指针并标记 `矛盾证据`，不得静默选择更方便的一方。
5. `source_bundle.json` 作为定位侧车文件单独保存，不新增 D/E 顶级章节，不挤压 ABC 主体分析。

`source_bundle.json` 可能包含论文逐页文本，`rendered_pages/` 可能包含整页图像。它们默认是本地分析产物，不应提交到公开仓库；只有在版权、许可、隐私和研究伦理允许时才能再分发。

## 材料范围纪律

脚本只会把实际输入的主 PDF 标为 `inspected`。Supplement、附录、OSF、预注册、数据与代码即使在正文里出现链接，也只能标为“发现链接但尚未读取”；必须实际打开后才能进入已读取范围。
