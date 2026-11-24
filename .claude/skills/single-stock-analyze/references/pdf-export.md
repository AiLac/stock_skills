# 导出单股报告为 PDF

把已完成的 Markdown 报告交给渲染器即可生成 A4 PDF。第一页有可点击的目录，正文沿用报告的 13 个章节。表格、列表和网页来源链接随报告一起输出。

## 安装和运行

使用 Python 3.10+、Pandoc 3.x、WeasyPrint 69 和覆盖报告文字的系统字体。中文推荐安装 Noto Sans CJK SC 和 Noto Serif CJK SC。按平台安装 [Pandoc](https://pandoc.org/installing.html) 和 [WeasyPrint 所需系统库](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation)，在已激活的 Python 虚拟环境中安装 PDF 引擎：

```sh
python -m pip install "weasyprint==69.0"
pandoc --version
weasyprint --version
```

从本技能目录执行以下命令。输入和输出路径均可指向仓库外，例如用户保存报告的目录：

```sh
python scripts/render_report_pdf.py "/path/to/report.md" "/path/to/report.pdf"
```

要打印空白报告，从同一目录执行：

```sh
python scripts/render_report_pdf.py assets/pdf/report-blank.md "/path/to/blank.pdf"
```

也可复制[可编辑的空白报告](../assets/pdf/report-blank.md)，填写后再导出。填表时删掉不适用的空行，保留财报实际列出的内部抵销项目。

工具从 PATH 查找两个命令。自定义安装路径可通过 `--pandoc`、`--weasyprint` 指定。英文报告可加 `--lang en` 切换目录与页首标签。版式文件在 `assets/pdf/report.html`，纸张、字体、表格及分页样式在 `assets/pdf/report.css`。

## 准备报告和图表

使用 [报告内容模板](../assets/stock-verdict-template.md) 的标题层级和顺序。一条数据占一个表格单元格，计量单位放在列名或邻近正文，数值用小数或百分比。报告期、证据等级、计算假设以及原始来源链接应写在成稿中。

| 报告位置 | 可自动绘图的列 | 图形的读法 |
|---|---|---|
| 评分卡 | 因子、评分(0-5) | 每个评分对照同一条 0–5 分刻度 |
| 公司介绍 | 分部 / 业务、占合并收入% | 各分部占合并收入的比例；同层级分部合计应约为 100% |
| 最近财报重点 | 报表科目、占营收%（适用时） | 每项成本或费用占营收多少，所有项目使用同一分母 |

图紧跟对应原表。没有可比数值、含「其中」或抵销行的表直接以表格呈现。应保留这些行及其披露口径。渲染器按原表数值制图，所需百分比须在报告中给出。
