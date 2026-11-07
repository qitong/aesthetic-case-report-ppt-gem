# Clinical Case Record & Photo Input Guide
# 医美病程记录与照片输入规范指南

为了生成高质量、专业严谨的医美 Case Report PPT，建议用户按以下结构提供病程记录与照片素材。如果资料不完全，Skill 会自动补充合理的医学逻辑并在对应位置预留标注。

---

## 1. 结构化病程记录（文本输入模板）

用户可以直接复制并填写以下文本发给 Skill：

```markdown
### 1. 患者基本信息 (Patient Profile)
- 代称/化名：[例如：模特 Momo / Cherry]
- 性别与年龄：[例如：女，39 岁]
- 主诉 (Chief Complaints)：[例如：眼周凹陷显疲惫，泪沟明显，苹果肌下垂，中面部扁平，伴有轻度法令纹]
- 既往史 (Aesthetic History)：[例如：1年前曾行光子嫩肤，无眼周注射史]
- 求美期望 (Expectations)：[例如：希望改善疲惫老态，改善黑眼圈与眼下凹陷，追求自然灵动、不僵硬、无明显充气感]

### 2. 治疗方案与参数明细 (Treatment Plan & Parameters)
- 靶向解剖区域与层次：
  * 区域 1: [例如：颧弓韧带支撑 (Zygomatic arch) - 骨膜上层 - 锐针 27G 垂直定点 - 左 0.3ml / 右 0.4ml - 材料: 高 G' 玻尿酸]
  * 区域 2: [例如：深层内侧颊 (DMCFP / Maxilla) - 深层骨相与间隙 - 钝针 25G - 左 0.7ml / 右 0.6ml]
  * 区域 3: [例如：眶轮匝肌支持韧带浅层融合 (Tear trough blending) - 眶隔前浅层 - 钝针 27G 微量扇形 - 左 0.2ml / 右 0.2ml - 材料: 低吸水微交联玻尿酸]
  * 区域 4 (如有二期微调): [例如：6个月后二期治疗，下颏延伸 3.0ml，法令纹精细平铺 0.5ml/0.5ml]

### 3. 就诊旅程节点 (Patient Journey Timeline)
- Baseline: [例如：2024.01 术前评估]
- Stage 1: [例如：2024.01 首期注射术后即刻]
- Follow-up 1: [例如：2024.07 术后 6 个月随访，组织融合自然]
- Stage 2: [例如：2025.01 二期微调治疗术后即刻]
- Follow-up 2: [例如：2025.04 二期术后 3 个月随访]
- Long-term: [例如：2026 跨年度长期维护状态]

### 4. 医生评估与临床心得 (Doctor's Notes)
- 美学评分改变 (FAS / GAIS)：[例如：术后 GAIS 评定为 Very Much Improved，眼周及中面部饱满度明显提升]
- 重点关注的动态表现：[例如：做大笑与微笑表情时下睑平整自然，未出现条索或香肠样隆起]
- 医生临床体会：[例如：先深后浅，先骨相后皮相；眶周治疗重在深层打底与浅层微量融合，不可盲目单层大量推注]
```

---

## 2. 照片素材准备与命名规范 (Photo Naming Conventions)

建议将患者照片存放在一个文件夹中（例如 `case_photos/`），并推荐采用标准化命名，以便 Skill 自动识别并匹配到对应的 PPT 页面中：

### 推荐命名规则：`[时间节点]_[视角]_[表情/状态].[扩展名]`

- **时间节点标签**：
  - `baseline` / `pre` / `before` : 术前基线
  - `immediate` / `post_immediate` : 术后即刻
  - `1m` / `3m` / `6m` / `1y` : 术后随访（1个月、3个月、6个月、1年等）
  - `stage2_pre` / `stage2_immediate` : 二期术前、二期术后即刻
- **视角标签**：
  - `front` / `frontal` : 正面平视
  - `oblique_left` / `oblique_right` / `45L` / `45R` : 左右 45° 斜位
  - `profile_left` / `profile_right` / `90L` / `90R` : 左右 90° 侧位
  - `upgaze` : 向上看（评估眼袋与泪沟分离度）
  - `smile` / `dynamic` : 微笑/大笑动态表情
  - `mapping` / `marking` : 术前画线设计与布点图

### 命名示例：
- `baseline_front_static.jpg` (术前正面静态)
- `baseline_front_smile.jpg` (术前正面大笑)
- `baseline_oblique_left.jpg` (术前左侧 45°)
- `mapping_front.jpg` (术前面部画线布点)
- `immediate_front_static.jpg` (术后即刻正面静态)
- `immediate_oblique_left.jpg` (术后即刻左侧 45°)
- `6m_front_static.jpg` (术后 6 个月随访正面)
- `timeline_2024.jpg`, `timeline_2025.jpg`, `timeline_2026.jpg` (年度对比照片)

> **注**：如果用户的照片没有规范命名，只需告知照片文件夹路径，并在病程记录中说明对应关系即可。
