# Custom Design Specification Guide (design.md)
# 自定义 PPT 设计规范指导文件 (design.md 样例与规范)

当用户在第一阶段选择“不使用内置 Default 模板，而是提供/编写自定义 `design.md`”时，可以参考或直接使用本文件作为规范。

---

## 1. 基础元数据 (Deck Metadata)
- **Deck Title (PPT 主标题)**: e.g. 高德美 AART 眶周精细化抗衰实战分享
- **Subtitle (副标题)**: e.g. 动态自然美学与两步法临床病例报告
- **Speaker / Institution (讲者与机构)**: e.g. 刘志昱 医生 / 某某医疗美容医院
- **Target Audience (目标受众)**: e.g. 资深皮肤科/微整形主诊医师、全国学术交流研讨会
- **Target Slide Count (预期页数)**: e.g. 15-20 页
- **Aspect Ratio (屏幕比例)**: 16:9 (标准宽屏 13.33 x 7.50 英寸)

---

## 2. 视觉与品牌色彩系统 (Brand & Palette Tokens)
可在此处指定品牌定制色（如高德美海蓝系、艾尔建紫金系、极简黑白高级灰系等）：

```yaml
theme:
  style_name: "Galderma Executive Navy" # 风格名称
  primary_color: "#0F2C59"             # 核心学术主色 (深海蓝，用于封面标题与重点强调)
  secondary_color: "#00A3C4"           # 辅助高亮色 (科技青蓝，用于点位箭头、序号高亮)
  accent_color: "#C5A880"              # 贵雅点缀色 (香槟金，用于局部高亮框与关键标签)
  card_bg_color: "#F8F9FA"             # 卡片背景底色 (极浅灰白，提升图文层次感)
  card_border_color: "#E2E8F0"         # 卡片边框色 (超细浅灰描边)
  text_primary: "#1A202C"              # 一级标题与主要正文字体色 (炭黑色)
  text_muted: "#718096"                # 辅助注释与参数字体色 (冷灰色)
  font_family_cn: "PingFang SC, Microsoft YaHei, SimHei" # 中文字体推荐
  font_family_en: "Helvetica Neue, Arial, Montserrat"    # 英文字体推荐
```

---

## 3. 页面模块与结构编排 (Slide Outline & Sections)
用户可以在此列出自定义的幻灯片页面清单及排版布局指令：

```markdown
### 模块一：背景与学术理念 (Slides 1-3)
- Slide 1: [Layout: Dark Navy Hero Cover] 全屏深色封面，居左大标题，右下讲者信息，底部会议保密声明
- Slide 2: [Layout: Two-Column Text+Cards] 东方人眶周衰老解剖特质与传统打法痛点分析
- Slide 3: [Layout: Evidence Comparison Table] 既有文献证据等级与主流共识打法对比表

### 模块二：术式与技术拆解 (Slides 4-6)
- Slide 4: [Layout: Left-Image Right-Grid] 左侧解剖图/布点图，右侧 3 个参数卡（进针点、层次、流变学选型）
- Slide 5: [Layout: Step-by-Step Flow] 术式两步法操作流程（深层骨相定点 + 浅层羽毛状铺展）

### 模块三：临床病例实战与多维度对比 (Slides 7-12)
- Slide 7: [Layout: Patient Profile Card] 模特 Momo（39岁）基线特征、主诉与术前 FAS 评分
- Slide 8: [Layout: Left-Mapping Right-DoseTable] 术前画线布点照片与左右侧精细注射剂量表
- Slide 9: [Layout: 2-Up Comparative Grid] 术前 vs 术后即刻正面高清对齐对比
- Slide 10: [Layout: 3-Up Angle Grid] 术后即刻 45° 斜位与 90° 侧位多角度对比
- Slide 11: [Layout: Dynamic Smile Verification] 术前静动态 vs 术后静动态大笑对比（证明无条索、无香肠眼）
- Slide 12: [Layout: Follow-up Timeline] 术前 -> 术后即刻 -> 3个月 -> 6个月 随访时间走廊

### 模块四：思考、合规与致谢 (Slides 13-14)
- Slide 13: [Layout: Key Takeaways 3-Cards] 3 条医生临床实践心得与并发症规避技巧
- Slide 14: [Layout: Dark Navy Closing] 感谢聆听、答疑互动、底部标准个案合规免责声明
```

---

## 4. 特殊排版与内容偏好 (Special Guidelines)
- **前后对比图排版要求**：必须保持相同缩放比例与头部角度，照片底部必须带阶段名称标签。
- **免责声明要求**：全套 PPT 必须包含官方合规声明。
- **是否需要动画**：静态高质感排版（无需复杂动画，利于医学学术研讨与投影）。
