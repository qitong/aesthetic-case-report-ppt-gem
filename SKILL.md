---
name: aesthetic-case-report-ppt-gem
description: Generate professional medical aesthetics (医美) clinical case report PPT presentations, featuring patient journeys, facial multi-layer anatomy, injection mappings (dosage, layer, cannula/needle), before-and-after photographic comparisons (static & dynamic smile), longitudinal follow-ups, and optional clinical paper literature appraisal. Use when the user asks to create an aesthetic case report PPT, patient journey presentation, aesthetic clinical slides, literature-backed case deck, or mentions "医美case report", "病例PPT", "病程做PPT", "patient journey PPT", or "高德美案例汇报".
---

# Aesthetic Case Report PPT Generator (医美临床病例与学术就诊旅程 PPT 生成器)

用于将医美临床病程记录、治疗参数、前后对比影像以及（可选的）医学文献，转化为具备国际顶级学术会议（如 AMWC, IMCAS, 高德美 AART 研讨会）水准的 16:9 Case Report PPTX 幻灯片。

本 Skill 深度总结并融合了两大权威案例范式：
1. **范式 A（文献机理精读 + 临床验证型）**：参考《The Blending Technique: A New Approach for Tear Trough Correction》及配套精读 PPT，适合“有论文支撑”的前沿术式与解剖机制攻坚。
2. **范式 B（纵向面部全层抗衰 Patient Journey 型）**：参考《Aesthetic Lives Dr Jovi Liu Edition》，适合“纯临床实战”，聚焦面部整体化全层评估（Bone to Dermis）、首期治疗、阶段随访、二期演进与跨年度长期维养。

---

## 核心交互流水线 (5-Phase Interactive Pipeline)

无论用户的原始输入是简要一句话还是详实病历，必须严格执行以下交互与生成流水线：

```
[ Phase 1: 输入盘点与资产识别 ]
              ↓
[ Phase 2: 模板确认 (Default 模板 vs. 自定义 design.md) ]
              ↓
[ Phase 3: 病程与医学参数结构化提取 & 逐页大纲确认 ]
              ↓
[ Phase 4: 幻灯片自动化构建与 PPTX 渲染 ]
              ↓
[ Phase 5: 成果交付与迭代指导 ]
```

---

### Phase 1: 输入资产盘点与需求问询 (Input Intake & Discovery)

当用户发起创建医美 Case Report 的需求时，主动询问并澄清以下 4 项关键输入：

1. **是否有参考论文 / 文献？**
   - *有*：用户提供 PDF 文件路径、PubMed ID、DOI 或论文摘要（将启用 **Default 模板 A: 文献机理+临床验证型**）。
   - *无*：纯临床实战病例汇报（将启用 **Default 模板 B: 纵向 Patient Journey 型**）。
2. **病程记录与治疗信息 (Clinical Case Record)**：
   - 是否已有现成的文字病历/记录单？（包含主诉、面部评估诊断、解剖靶区、注射层次、进针工具、左右侧注射剂量 ml、选用材料等）。
   - 若用户无格式文本，提示参考 [case_record_prompt_guide.md](file:///Users/qitonghu/Desktop/1118%20%E9%AB%98%E5%BE%B7%E7%BE%8E/aesthetic-case-report-ppt-gem/templates/case_record_prompt_guide.md) 直接输入关键数据。
3. **患者照片所在文件夹与时序 (Photos & Timepoints)**：
   - 询问照片存放文件夹路径（例如 `case_photos/`），以及包含哪些视角与时序（如 术前基线、术后面部布点、术后即刻、3个月/6个月随访、正面/斜位/侧位、静态与大笑动态等）。
4. **讲者与会议背景**：
   - 医生姓名、执业单位、分享主题名称、会议场合与日期。

---

### Phase 2: 模板与设计路线选择 (Template & Design Strategy)

在盘点好输入之后，向用户明确询问模板策略：

- **选项 1：使用内置 Default 模板 (推荐)**
  - **模式 A (学术文献双核型)**：针对**有论文**输入。结构为：临床痛点与文献背景 -> 面部全层解剖与间隙机制 -> 临床分型与决策树 -> 术式步骤与流变学匹配 -> 典型病例基线与布点 -> 术后即刻/动态验证 -> 随访稳固度 -> 中国人群本土化实践与批判。详细页面大纲参见 [default_template_A_academic.md](file:///Users/qitonghu/Desktop/1118%20%E9%AB%98%E5%BE%B7%E7%BE%8E/aesthetic-case-report-ppt-gem/templates/default_template_A_academic.md)。
  - **模式 B (纵向抗衰旅程型)**：针对**无论文**输入。结构为：全层衰老哲学 (Bone to Epidermis) -> FAS 美学评估量表 -> 病例基线画像 -> 1st 治疗方案与布点剂量表 -> 术后即刻正面/斜位/侧位多维矩阵 -> 6个月随访 -> 2nd 治疗演化方案 -> 多年时光走廊 (Longitudinal Timeline) -> 医生临床心得与合规声明。详细页面大纲参见 [default_template_B_journey.md](file:///Users/qitonghu/Desktop/1118%20%E9%AB%98%E5%BE%B7%E7%BE%8E/aesthetic-case-report-ppt-gem/templates/default_template_B_journey.md)。
- **选项 2：提供或自定义 `design.md`**
  - 用户若有指定的视觉品牌色（如高德美蓝、学术黑白、典雅暖金）、特定版式布局或页数要求，可提供 `design.md`。
  - 参考规范范本：[design_sample.md](file:///Users/qitonghu/Desktop/1118%20%E9%AB%98%E5%BE%B7%E7%BE%8E/aesthetic-case-report-ppt-gem/templates/design_sample.md)。

---

### Phase 3: 医学参数提取与逐页大纲审批 (Parsing & Outline Review)

在确定模板后，系统应首先梳理出清晰的结构化数据，并输出完整的 PPT 逐页大纲供用户预览和确认：

1. **核心医学参数提取表**：
   - **患者基线**：代称、年龄、主诉、FAS 术前面部美学评分。
   - **解剖靶区与剂量矩阵**：
     | 解剖靶位 (Site) | 解剖层次 (Layer) | 操作工具 (Tool) | 左侧剂量 (Left) | 右侧剂量 (Right) | 材料与流变学特点 |
     | :--- | :--- | :--- | :--- | :--- | :--- |
     | Zygomatic arch (颧弓) | Layer 5 骨膜上 | 锐针 27G 垂直点推 | 0.3 ml | 0.4 ml | 高 G'、强深层支撑 |
     | Maxilla / DMCFP (深颊) | Layer 5 骨相/间隙 | 钝针 25G 扇形平铺 | 0.7 ml | 0.6 ml | 容积复位重塑 |
     | Tear Trough (泪沟融合) | Layer 2-4 穿透韧带 | 钝针 27G 浅层微滴 | 0.2 ml | 0.2 ml | 微交联极低吸水率 |
     | Chin (下颏 - 二期) | Layer 5 骨膜上 | 锐针垂直注射 | - | 3.0 ml | 轮廓延展塑形 |
2. **输出 Slide Outline**：逐页标注 Slide 编号、页面标题、版式类型（如 `COVER`, `TEXT_CARDS`, `MAPPING_DOSE`, `COMPARISON_2UP`, `TIMELINE` 等）、对应的图片路径、文字要点。
3. **用户微调与确认**：用户确认大纲后，进入代码自动构建。

---

### Phase 4: 幻灯片自动化构建与 PPTX 渲染 (Execution & Automation)

Skill 内置完整的 Python 自动化生成工具：
- 渲染脚本：`scripts/generate_case_deck.py`
- 视觉排版工具库：`scripts/pptx_builder_utils.py`

#### 脚本执行方式：
```bash
python3 scripts/generate_case_deck.py --config config.json --output "output/My_Aesthetic_Case_Report.pptx"
```
或者直接使用内置的 Python 类 `AestheticDeckBuilder` 动态生成。

#### 关键页面排版规范：
- **画线布点与剂量表 (Treatment Mapping)**：左侧 40% 放置高保真面部划线设计图；右侧 60% 绘制圆角卡片，列出每个解剖靶区的层次、针规、左右剂量对比表。
- **前后对比矩阵 (Before / After 2-Up & 3-Up)**：成对严谨对齐，照片下方附带胶囊型状态标签（`Baseline 术前`、`Immediate After 术后即刻`）；右侧附带 4 条临床观察笔记。
- **动态大笑对比 (Static vs Dynamic)**：对比静态与大笑表情，突出“无条索隆起、无香肠眼、表情自然灵动”。
- **全周期时光走廊 (Longitudinal Timeline)**：4-5 列横向时间流动卡片，自左向右跨越 2-3 年（Baseline -> Tx1 -> 6M -> Tx2 -> Long-term Maintenance）。
- **官方合规声明**：全套 PPT 底部统一部署高德美与行业合规标注：
  - *“以上为临床个案分享，仅供本次会议学术讨论；不同医疗器械/药品的具体使用，应参见国家药品监督管理局获批的中文产品说明书及相关临床诊疗指南。”*

---

## 资源索引与参考知识库

- **解剖学、流变学与术式专业词汇库**：[anatomy_and_injection_vocabulary.md](file:///Users/qitonghu/Desktop/1118%20%E9%AB%98%E5%BE%B7%E7%BE%8E/aesthetic-case-report-ppt-gem/references/anatomy_and_injection_vocabulary.md)
- **医美学术案例汇报黄金法则**：[aesthetic_case_best_practices.md](file:///Users/qitonghu/Desktop/1118%20%E9%AB%98%E5%BE%B7%E7%BE%8E/aesthetic-case-report-ppt-gem/references/aesthetic_case_best_practices.md)
- **病程记录与照片输入指南**：[case_record_prompt_guide.md](file:///Users/qitonghu/Desktop/1118%20%E9%AB%98%E5%BE%B7%E7%BE%8E/aesthetic-case-report-ppt-gem/templates/case_record_prompt_guide.md)
- **默认模板 A (文献+病例双核型)**：[default_template_A_academic.md](file:///Users/qitonghu/Desktop/1118%20%E9%AB%98%E5%BE%B7%E7%BE%8E/aesthetic-case-report-ppt-gem/templates/default_template_A_academic.md)
- **默认模板 B (纵向抗衰旅程型)**：[default_template_B_journey.md](file:///Users/qitonghu/Desktop/1118%20%E9%AB%98%E5%BE%B7%E7%BE%8E/aesthetic-case-report-ppt-gem/templates/default_template_B_journey.md)
- **自定义 design.md 规范范例**：[design_sample.md](file:///Users/qitonghu/Desktop/1118%20%E9%AB%98%E5%BE%B7%E7%BE%8E/aesthetic-case-report-ppt-gem/templates/design_sample.md)
