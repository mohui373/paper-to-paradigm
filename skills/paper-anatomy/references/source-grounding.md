# 来源准备与精确定位

## 目的

把 PDF 页码、章节、图、表、内嵌图片和材料范围写入独立的 `source_bundle.json`。ABC 主报告只使用紧凑证据指针，不复制整页文本，也不把定位清单塞进正文。

## 准备流程

收到 PDF 时先运行：

```bash
python scripts/prepare_paper.py PAPER.pdf -o source_bundle.json
```

需要逐页视觉检查时可增加：

```bash
python scripts/prepare_paper.py PAPER.pdf -o source_bundle.json --render-pages rendered_pages
```

`--render-pages` 需要系统可调用 `pdftoppm`。文本提取依赖 `pypdf`，精确坐标和内嵌图片清单优先使用 `pdfplumber`。

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
