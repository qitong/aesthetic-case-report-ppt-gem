#!/usr/bin/env python3
"""
Aesthetic Case Report Deck Generator
医美学术与临床病例汇报 PPTX 自动化生成引擎

基于 python-pptx 自动构建 16:9 高端医美学术幻灯片，覆盖：
- 封面与目录
- 临床痛点与文献解剖机理
- 面部划线布点与左右侧剂量表 (Treatment Mapping)
- 术前 vs 术后即刻标准化对比 (Before / After Matrix)
- 动态表情对比 (Static vs Dynamic Smile)
- 全程时光走廊 (Longitudinal Patient Journey Timeline)
- 医生临床体会与官方合规免责声明
"""

import os
import sys
import json
import argparse
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# 导入样式与工具
from pptx_builder_utils import (
    NAVY_PRIMARY, NAVY_DARK, TEAL_ACCENT, GOLD_ACCENT, CARD_BG, CARD_BORDER,
    TEXT_DARK, TEXT_MUTED, TEXT_LIGHT, WHITE, GREEN_ACCENT,
    FONT_HEADING, FONT_BODY, FONT_EN,
    SLIDE_WIDTH_INCHES, SLIDE_HEIGHT_INCHES,
    DEFAULT_DISCLAIMER_CONFIDENTIAL, DEFAULT_DISCLAIMER_CASE,
    set_slide_background, add_header, add_disclaimer, add_card_shape, add_image_or_placeholder
)

class AestheticDeckBuilder:
    def __init__(self, output_path="Aesthetic_Case_Report.pptx"):
        self.output_path = output_path
        self.prs = Presentation()
        self.prs.slide_width = Inches(SLIDE_WIDTH_INCHES)
        self.prs.slide_height = Inches(SLIDE_HEIGHT_INCHES)
        self.blank_layout = self.prs.slide_layouts[6]  # 空白版式

    def add_cover_slide(self, title, subtitle, speaker_info, institution, disclaimer=DEFAULT_DISCLAIMER_CONFIDENTIAL):
        """1. 封面页：深海蓝学术高奢背景"""
        slide = self.prs.slides.add_slide(self.blank_layout)
        set_slide_background(slide, NAVY_DARK)

        # 装饰性光晕/青蓝强调色条
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(2.2), Inches(0.12), Inches(2.8))
        bar.fill.solid()
        bar.fill.fore_color.rgb = TEAL_ACCENT
        bar.line.fill.background()

        # 标题区域
        tx_box = slide.shapes.add_textbox(Inches(1.2), Inches(2.0), Inches(10.5), Inches(3.2))
        tf = tx_box.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(36)
        p1.font.bold = True
        p1.font.color.rgb = WHITE
        p1.space_after = Pt(14)

        p2 = tf.add_paragraph()
        p2.text = subtitle
        p2.font.name = FONT_HEADING
        p2.font.size = Pt(18)
        p2.font.color.rgb = GOLD_ACCENT

        # 讲者与单位
        tx_info = slide.shapes.add_textbox(Inches(1.2), Inches(5.4), Inches(8.0), Inches(1.0))
        tf_info = tx_info.text_frame
        p_spk = tf_info.paragraphs[0]
        p_spk.text = f"{speaker_info}  |  {institution}"
        p_spk.font.name = FONT_BODY
        p_spk.font.size = Pt(14)
        p_spk.font.color.rgb = TEXT_LIGHT

        add_disclaimer(slide, disclaimer, is_dark=True)
        return slide

    def add_section_divider_slide(self, section_num, title_cn, title_en):
        """2. 章节过渡页"""
        slide = self.prs.slides.add_slide(self.blank_layout)
        set_slide_background(slide, NAVY_PRIMARY)

        # 大号序号
        tx_num = slide.shapes.add_textbox(Inches(1.2), Inches(2.2), Inches(3.0), Inches(1.2))
        tf_num = tx_num.text_frame
        p_num = tf_num.paragraphs[0]
        p_num.text = str(section_num).zfill(2)
        p_num.font.name = FONT_EN
        p_num.font.size = Pt(64)
        p_num.font.bold = True
        p_num.font.color.rgb = TEAL_ACCENT

        # 章节标题
        tx_title = slide.shapes.add_textbox(Inches(1.2), Inches(3.5), Inches(10.0), Inches(2.0))
        tf_title = tx_title.text_frame
        p_cn = tf_title.paragraphs[0]
        p_cn.text = title_cn
        p_cn.font.name = FONT_HEADING
        p_cn.font.size = Pt(32)
        p_cn.font.bold = True
        p_cn.font.color.rgb = WHITE
        p_cn.space_after = Pt(8)

        p_en = tf_title.add_paragraph()
        p_en.text = title_en.upper()
        p_en.font.name = FONT_EN
        p_en.font.size = Pt(14)
        p_en.font.color.rgb = GOLD_ACCENT

        add_disclaimer(slide, DEFAULT_DISCLAIMER_CONFIDENTIAL, is_dark=True)
        return slide

    def add_cards_slide(self, title, category, cards_data, disclaimer=DEFAULT_DISCLAIMER_CASE):
        """3. 多卡片分析页 (2或3列卡片，用于痛点、解剖、分型、量表)"""
        slide = self.prs.slides.add_slide(self.blank_layout)
        set_slide_background(slide, WHITE)
        add_header(slide, title, category)

        num_cards = len(cards_data)
        margin_x = Inches(0.8)
        top = Inches(1.7)
        height = Inches(4.9)
        spacing = Inches(0.3)
        available_width = Inches(11.733) - (spacing * (num_cards - 1))
        card_w = available_width / num_cards

        for i, card_info in enumerate(cards_data):
            left = margin_x + i * (card_w + spacing)
            add_card_shape(slide, left, top, card_w, height)

            # 顶部强调条
            accent_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, card_w, Inches(0.08))
            accent_bar.fill.solid()
            accent_bar.fill.fore_color.rgb = TEAL_ACCENT if i % 2 == 0 else GOLD_ACCENT
            accent_bar.line.fill.background()

            tx_box = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), card_w - Inches(0.5), height - Inches(0.4))
            tf = tx_box.text_frame
            tf.word_wrap = True

            # 卡片标题
            p_title = tf.paragraphs[0]
            p_title.text = card_info.get("title", "")
            p_title.font.name = FONT_HEADING
            p_title.font.size = Pt(16)
            p_title.font.bold = True
            p_title.font.color.rgb = NAVY_PRIMARY
            p_title.space_after = Pt(10)

            # 卡片要点
            for bullet in card_info.get("points", []):
                p_bullet = tf.add_paragraph()
                p_bullet.text = f"• {bullet}"
                p_bullet.font.name = FONT_BODY
                p_bullet.font.size = Pt(12)
                p_bullet.font.color.rgb = TEXT_DARK
                p_bullet.space_after = Pt(8)

        add_disclaimer(slide, disclaimer)
        return slide

    def add_mapping_and_dose_slide(self, title, category, patient_summary, mapping_img_path, dose_items, disclaimer=DEFAULT_DISCLAIMER_CASE):
        """4. 面部画线布点与剂量明细页 (左图右表)"""
        slide = self.prs.slides.add_slide(self.blank_layout)
        set_slide_background(slide, WHITE)
        add_header(slide, title, category)

        # 左侧：画线/布点照片
        img_left = Inches(0.8)
        img_top = Inches(1.6)
        img_w = Inches(4.5)
        img_h = Inches(5.0)
        add_image_or_placeholder(slide, mapping_img_path, img_left, img_top, img_w, img_h, "术前画线布点设计图")

        # 患者信息标注
        if patient_summary:
            tag_box = slide.shapes.add_textbox(img_left, img_top + img_h + Inches(0.05), img_w, Inches(0.35))
            tf_tag = tag_box.text_frame
            p_tag = tf_tag.paragraphs[0]
            p_tag.text = patient_summary
            p_tag.font.name = FONT_BODY
            p_tag.font.size = Pt(10)
            p_tag.font.bold = True
            p_tag.font.color.rgb = NAVY_PRIMARY

        # 右侧：解剖靶区与剂量分配卡片
        right_left = Inches(5.6)
        right_w = Inches(6.933)
        add_card_shape(slide, right_left, img_top, right_w, img_h)

        tx_right = slide.shapes.add_textbox(right_left + Inches(0.3), img_top + Inches(0.2), right_w - Inches(0.6), img_h - Inches(0.4))
        tf_r = tx_right.text_frame
        tf_r.word_wrap = True

        p_h = tf_r.paragraphs[0]
        p_h.text = "解剖靶区注射方案与精细剂量 (Treatment Parameters)"
        p_h.font.name = FONT_HEADING
        p_h.font.size = Pt(15)
        p_h.font.bold = True
        p_h.font.color.rgb = NAVY_PRIMARY
        p_h.space_after = Pt(12)

        for item in dose_items:
            p_item = tf_r.add_paragraph()
            p_item.text = f"📍 {item.get('site', '')}"
            p_item.font.name = FONT_HEADING
            p_item.font.size = Pt(13)
            p_item.font.bold = True
            p_item.font.color.rgb = TEAL_ACCENT

            p_detail = tf_r.add_paragraph()
            detail_str = f"  • 层次/工具: {item.get('layer', '')} | {item.get('tool', '')}\n  • 剂量分配: Left {item.get('left_dose', '-')} / Right {item.get('right_dose', '-')}\n  • 选用产品: {item.get('product', '')}"
            p_detail.text = detail_str
            p_detail.font.name = FONT_BODY
            p_detail.font.size = Pt(11)
            p_detail.font.color.rgb = TEXT_DARK
            p_detail.space_after = Pt(8)

        add_disclaimer(slide, disclaimer)
        return slide

    def add_comparison_2up_slide(self, title, category, img_before, img_after, label_before="术前 (Before)", label_after="术后即刻 (Immediate After)", observation_notes="", disclaimer=DEFAULT_DISCLAIMER_CASE):
        """5. 经典 2-Up 对比页 (术前 vs 术后)"""
        slide = self.prs.slides.add_slide(self.blank_layout)
        set_slide_background(slide, WHITE)
        add_header(slide, title, category)

        top = Inches(1.6)
        img_w = Inches(4.3)
        img_h = Inches(4.8)
        left1 = Inches(0.8)
        left2 = Inches(5.4)

        # 术前图片
        add_image_or_placeholder(slide, img_before, left1, top, img_w, img_h, label_before)
        tag1 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left1, top + img_h + Inches(0.08), img_w, Inches(0.35))
        tag1.fill.solid()
        tag1.fill.fore_color.rgb = CARD_BG
        tag1.line.color.rgb = CARD_BORDER
        tag1.text_frame.text = label_before
        tag1.text_frame.paragraphs[0].font.name = FONT_BODY
        tag1.text_frame.paragraphs[0].font.size = Pt(11)
        tag1.text_frame.paragraphs[0].font.bold = True
        tag1.text_frame.paragraphs[0].font.color.rgb = NAVY_PRIMARY
        tag1.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

        # 术后图片
        add_image_or_placeholder(slide, img_after, left2, top, img_w, img_h, label_after)
        tag2 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left2, top + img_h + Inches(0.08), img_w, Inches(0.35))
        tag2.fill.solid()
        tag2.fill.fore_color.rgb = CARD_BG
        tag2.line.color.rgb = TEAL_ACCENT
        tag2.text_frame.text = label_after
        tag2.text_frame.paragraphs[0].font.name = FONT_BODY
        tag2.text_frame.paragraphs[0].font.size = Pt(11)
        tag2.text_frame.paragraphs[0].font.bold = True
        tag2.text_frame.paragraphs[0].font.color.rgb = TEAL_ACCENT
        tag2.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

        # 右侧：临床观察笔记卡片
        notes_left = Inches(10.0)
        notes_w = Inches(2.533)
        notes_card = add_card_shape(slide, notes_left, top, notes_w, img_h + Inches(0.43))
        tx_notes = slide.shapes.add_textbox(notes_left + Inches(0.15), top + Inches(0.2), notes_w - Inches(0.3), img_h)
        tf_n = tx_notes.text_frame
        tf_n.word_wrap = True

        p_nh = tf_n.paragraphs[0]
        p_nh.text = "🔍 临床观察要点"
        p_nh.font.name = FONT_HEADING
        p_nh.font.size = Pt(13)
        p_nh.font.bold = True
        p_nh.font.color.rgb = NAVY_PRIMARY
        p_nh.space_after = Pt(8)

        p_nb = tf_n.add_paragraph()
        p_nb.text = observation_notes if observation_notes else "• 容积凹陷精准填平\n• 组织平滑过渡，无边界感\n• 颧部高光点立体上移\n• 动态表情自然无紧绷"
        p_nb.font.name = FONT_BODY
        p_nb.font.size = Pt(11)
        p_nb.font.color.rgb = TEXT_DARK

        add_disclaimer(slide, disclaimer)
        return slide

    def add_timeline_journey_slide(self, title, category, stages_data, disclaimer=DEFAULT_DISCLAIMER_CASE):
        """6. 患者时光走廊与就诊旅程页 (Patient Journey Timeline)"""
        slide = self.prs.slides.add_slide(self.blank_layout)
        set_slide_background(slide, WHITE)
        add_header(slide, title, category)

        num_stages = len(stages_data)
        margin_x = Inches(0.8)
        top = Inches(1.6)
        spacing = Inches(0.25)
        available_width = Inches(11.733) - (spacing * (num_stages - 1))
        col_w = available_width / num_stages
        img_h = Inches(4.2)

        for i, stage in enumerate(stages_data):
            left = margin_x + i * (col_w + spacing)

            # 图片
            add_image_or_placeholder(slide, stage.get("img_path", ""), left, top, col_w, img_h, stage.get("label", ""))

            # 底部时间轴卡片
            tag_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top + img_h + Inches(0.1), col_w, Inches(0.95))
            tag_card.fill.solid()
            tag_card.fill.fore_color.rgb = CARD_BG
            tag_card.line.color.rgb = CARD_BORDER

            tf = tag_card.text_frame
            tf.word_wrap = True
            p_time = tf.paragraphs[0]
            p_time.text = stage.get("time", "")
            p_time.font.name = FONT_EN
            p_time.font.size = Pt(10)
            p_time.font.bold = True
            p_time.font.color.rgb = TEAL_ACCENT

            p_lbl = tf.add_paragraph()
            p_lbl.text = stage.get("label", "")
            p_lbl.font.name = FONT_BODY
            p_lbl.font.size = Pt(10)
            p_lbl.font.bold = True
            p_lbl.font.color.rgb = NAVY_PRIMARY

            if stage.get("note", ""):
                p_nt = tf.add_paragraph()
                p_nt.text = stage.get("note", "")
                p_nt.font.name = FONT_BODY
                p_nt.font.size = Pt(8.5)
                p_nt.font.color.rgb = TEXT_MUTED

        add_disclaimer(slide, disclaimer)
        return slide

    def add_doctor_insights_slide(self, title, category, insights, disclaimer=DEFAULT_DISCLAIMER_CASE):
        """7. 医生临床思考与心得总结页"""
        slide = self.prs.slides.add_slide(self.blank_layout)
        set_slide_background(slide, WHITE)
        add_header(slide, title, category)

        top = Inches(1.7)
        card_h = Inches(4.9)
        margin_x = Inches(0.8)
        card_w = Inches(3.64)
        spacing = Inches(0.4)

        for i, item in enumerate(insights[:3]):
            left = margin_x + i * (card_w + spacing)
            add_card_shape(slide, left, top, card_w, card_h)

            # 序号小徽标
            badge = slide.shapes.add_shape(MSO_SHAPE.OVAL, left + Inches(0.3), top + Inches(0.3), Inches(0.5), Inches(0.5))
            badge.fill.solid()
            badge.fill.fore_color.rgb = NAVY_PRIMARY
            badge.line.fill.background()
            badge.text_frame.text = str(i + 1)
            badge.text_frame.paragraphs[0].font.name = FONT_EN
            badge.text_frame.paragraphs[0].font.size = Pt(14)
            badge.text_frame.paragraphs[0].font.bold = True
            badge.text_frame.paragraphs[0].font.color.rgb = WHITE
            badge.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

            tx = slide.shapes.add_textbox(left + Inches(0.3), top + Inches(1.0), card_w - Inches(0.6), card_h - Inches(1.2))
            tf = tx.text_frame
            tf.word_wrap = True

            p_h = tf.paragraphs[0]
            p_h.text = item.get("title", "")
            p_h.font.name = FONT_HEADING
            p_h.font.size = Pt(16)
            p_h.font.bold = True
            p_h.font.color.rgb = NAVY_PRIMARY
            p_h.space_after = Pt(10)

            p_b = tf.add_paragraph()
            p_b.text = item.get("desc", "")
            p_b.font.name = FONT_BODY
            p_b.font.size = Pt(12)
            p_b.font.color.rgb = TEXT_DARK

        add_disclaimer(slide, disclaimer)
        return slide

    def add_closing_slide(self, thank_you_text="Thank You", doctor_name="", disclaimer=DEFAULT_DISCLAIMER_CASE):
        """8. 结语与致谢页"""
        slide = self.prs.slides.add_slide(self.blank_layout)
        set_slide_background(slide, NAVY_DARK)

        tx_box = slide.shapes.add_textbox(Inches(1.0), Inches(2.6), Inches(11.333), Inches(2.5))
        tf = tx_box.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.alignment = PP_ALIGN.CENTER
        p1.text = thank_you_text
        p1.font.name = FONT_EN
        p1.font.size = Pt(44)
        p1.font.bold = True
        p1.font.color.rgb = WHITE
        p1.space_after = Pt(12)

        if doctor_name:
            p2 = tf.add_paragraph()
            p2.alignment = PP_ALIGN.CENTER
            p2.text = f"{doctor_name} · 临床个案精研"
            p2.font.name = FONT_HEADING
            p2.font.size = Pt(18)
            p2.font.color.rgb = GOLD_ACCENT

        add_disclaimer(slide, disclaimer, is_dark=True)
        return slide

    def save(self):
        os.makedirs(os.path.dirname(os.path.abspath(self.output_path)), exist_ok=True)
        self.prs.save(self.output_path)
        print(f"✅ Aesthetic Case Report PPTX successfully created at: {self.output_path}")

def build_demo_deck(output_file="Aesthetic_Lives_Demo.pptx"):
    """创建基于 Jovi Liu Edition 与 Blending 精读的高阶范例演示 PPTX"""
    builder = AestheticDeckBuilder(output_file)

    # 1. 封面
    builder.add_cover_slide(
        title="Aging is a Privilege, Not a Predicament",
        subtitle="面部全层抗衰与眶周精细化两步融合技术 · 临床个案精研",
        speaker_info="Dr. Zhiyu Liu (刘志昱医生)",
        institution="高德美 AART 美学实践研讨会"
    )

    # 2. 章节 01
    builder.add_section_divider_slide(1, "抗衰理念与全层解剖机制", "Aging Philosophy & Multi-layer Anatomy")

    # 3. 痛点与衰老机制卡片
    builder.add_cards_slide(
        title="面部全层衰老认知与传统注射痛点",
        category="01 解剖机制与美学评估",
        cards_data=[
            {
                "title": "全层衰老演化 (Bone to Dermis)",
                "points": [
                    "骨吸收与退缩：眶下骨缘后退，梨状孔扩大",
                    "深层脂肪垫 (DMCFP/SOOF) 容积萎缩萎陷",
                    "真性支持韧带 (ORL/TTL) 张力减弱松弛",
                    "浅层脂肪室下垂堆积，真皮胶原降解变薄"
                ]
            },
            {
                "title": "传统眶周打法三大临床痛点",
                "points": [
                    "静态平整但微笑大笑时出现条索隆起（香肠样畸形）",
                    "注射层次过浅或产品吸水率高导致眶下迟发性水肿",
                    "微粒透光产生蓝灰色廷德尔现象（Tyndall Effect）",
                    "忽视深层骨相与中面部支撑，单点单层填充易移位"
                ]
            },
            {
                "title": "FAS 全面美学评估原则",
                "points": [
                    "分区量化：额颞、眶周、中面部、下颌轮廓",
                    "动静结合：静态平视 + Upgaze 向上看 + 微笑动态",
                    "以深促浅：先骨相复位，后皮相微量平铺融合"
                ]
            }
        ]
    )

    # 4. 章节 02
    builder.add_section_divider_slide(2, "病例档案与个体化治疗方案", "Patient Profile & Treatment Plan")

    # 5. 画线布点与剂量明细
    builder.add_mapping_and_dose_slide(
        title="个体化注射方案规划与精细剂量",
        category="02 治疗方案与布点",
        patient_summary="模特 Momo，39岁 | 主诉：中面部扁平凹陷、重度疲惫感、眼周泪沟明显",
        mapping_img_path="AI 参考素材/参考图.png",
        dose_items=[
            {
                "site": "Zygomatic arch (颧弓骨膜上支撑)",
                "layer": "Layer 5 骨膜上层",
                "tool": "锐针 27G 垂直点状注射",
                "left_dose": "0.3 ml",
                "right_dose": "0.4 ml",
                "product": "高 G' 强支撑力透明质酸 (Restylane Lyft)"
            },
            {
                "site": "Maxilla & DMCFP (深层内侧颊脂肪垫)",
                "layer": "Layer 5 深层间隙",
                "tool": "钝针 25G 扇形平铺",
                "left_dose": "0.7 ml",
                "right_dose": "0.6 ml",
                "product": "高弹性骨相重塑材料"
            },
            {
                "site": "Tear Trough Blending (泪沟浅层融合)",
                "layer": "Layer 2-4 穿透韧带眶隔前浅层",
                "tool": "钝针 27G 微量彗星状分散",
                "left_dose": "0.2 ml",
                "right_dose": "0.2 ml",
                "product": "微交联极低吸水率眼周专研材料 (Eyelight)"
            }
        ]
    )

    # 6. 术前 vs 术后即刻正面对比
    builder.add_comparison_2up_slide(
        title="首期治疗效果评估：正面平视静态对比",
        category="03 术后即刻临床评价",
        img_before="",
        img_after="",
        label_before="术前基线 (Baseline)",
        label_after="术后即刻 (Immediate After)",
        observation_notes="• 眶周泪沟与睑颧沟平整度极佳\n• 中面部高光点自然提升约 5mm\n• 苹果肌饱满且无充气僵硬感\n• 疲态感显著消除，眼神灵动"
    )

    # 7. 全程 Patient Journey 时间轴
    builder.add_timeline_journey_slide(
        title="全程就诊旅程与长期维养 (Patient Journey)",
        category="04 纵向长期随访",
        stages_data=[
            {
                "time": "2024.01",
                "label": "Baseline 术前基线",
                "note": "中面部容积流失\n泪沟深陷，疲态明显",
                "img_path": ""
            },
            {
                "time": "2024.01",
                "label": "1st Tx 术后即刻",
                "note": "深层骨膜支撑\n浅层泪沟无痕融合",
                "img_path": ""
            },
            {
                "time": "2024.07",
                "label": "6 Months Later",
                "note": "材料与自体组织深度融合\n面部平整度高度稳定",
                "img_path": ""
            },
            {
                "time": "2025.01",
                "label": "2nd Tx 二期微调",
                "note": "补充下颏延伸 3.0ml\n全脸年轻化轮廓紧致",
                "img_path": ""
            },
            {
                "time": "2026.01",
                "label": "2-Year Follow-up",
                "note": "跨年度动态自然\n维持青春态无位移",
                "img_path": ""
            }
        ]
    )

    # 8. 医生临床思考
    builder.add_doctor_insights_slide(
        title="临床思考与核心心得 (Doctor's Key Takeaways)",
        category="05 专家观点",
        insights=[
            {
                "title": "先骨相后皮相，分层递进",
                "desc": "中面部抗衰绝不能孤立处理某一条沟。先在深层骨膜上搭建好颧弓与深颊容积支架，浅层只需极微量流变学匹配材料即可实现平滑融合。"
            },
            {
                "title": "动静平衡是黄金检验标准",
                "desc": "术前必须评估 Innie/Outie 分型与 Upgaze 体位；术后务必让求美者做大笑表情，确保穿透韧带处无局限性条索与香肠样隆起。"
            },
            {
                "title": "纵向旅程优于一次性过度填充",
                "desc": "坚持 Longitudinal Patient Journey，分期分阶段微调。6-12 个月的随访与二次规划，能让组织获得最从容自然的逆龄修复。"
            }
        ]
    )

    # 9. 致谢与合规结尾
    builder.add_closing_slide(
        thank_you_text="Thank You",
        doctor_name="Dr. Zhiyu Liu"
    )

    builder.save()

def main():
    parser = argparse.ArgumentParser(description="Aesthetic Case Report Deck Generator")
    parser.add_argument("--demo", action="store_true", help="Generate a comprehensive demo case deck")
    parser.add_argument("--config", type=str, help="Path to JSON configuration file for custom deck")
    parser.add_argument("--output", type=str, default="Aesthetic_Case_Report.pptx", help="Output PPTX path")

    args = parser.parse_args()

    if args.demo or not args.config:
        print("Generating comprehensive Aesthetic Case Report Demo deck...")
        build_demo_deck(args.output)
    else:
        with open(args.config, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        print(f"Building deck from config: {args.config}")
        # 可根据自定义 config 执行类似逻辑

if __name__ == "__main__":
    main()
