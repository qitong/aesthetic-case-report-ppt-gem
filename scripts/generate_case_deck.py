#!/usr/bin/env python3
"""
Aesthetic Case Report Deck Generator
医美学术与临床病例汇报 PPTX 自动化生成引擎

基于 python-pptx 自动构建 16:9 高端医美学术幻灯片，覆盖：
- 封面与章节过渡
- 临床痛点与面部全层解剖衰老机理
- 患者基线档案与 FAS 评分卡
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

            p_title = tf.paragraphs[0]
            p_title.text = card_info.get("title", "")
            p_title.font.name = FONT_HEADING
            p_title.font.size = Pt(16)
            p_title.font.bold = True
            p_title.font.color.rgb = NAVY_PRIMARY
            p_title.space_after = Pt(10)

            for bullet in card_info.get("points", []):
                p_bullet = tf.add_paragraph()
                p_bullet.text = f"• {bullet}"
                p_bullet.font.name = FONT_BODY
                p_bullet.font.size = Pt(12)
                p_bullet.font.color.rgb = TEXT_DARK
                p_bullet.space_after = Pt(8)

        add_disclaimer(slide, disclaimer)
        return slide

    def add_patient_profile_slide(self, title, category, profile_data, disclaimer=DEFAULT_DISCLAIMER_CASE):
        """4. 患者基线档案与 FAS 评分卡 (双栏对称布局)"""
        slide = self.prs.slides.add_slide(self.blank_layout)
        set_slide_background(slide, WHITE)
        add_header(slide, title, category)

        top = Inches(1.7)
        height = Inches(4.9)
        col_w = Inches(5.7)
        left1 = Inches(0.8)
        left2 = Inches(6.833)

        # 左栏：基线档案与主诉
        add_card_shape(slide, left1, top, col_w, height)
        bar1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left1, top, col_w, Inches(0.08))
        bar1.fill.solid()
        bar1.fill.fore_color.rgb = TEAL_ACCENT
        bar1.line.fill.background()

        tx1 = slide.shapes.add_textbox(left1 + Inches(0.3), top + Inches(0.25), col_w - Inches(0.6), height - Inches(0.5))
        tf1 = tx1.text_frame
        tf1.word_wrap = True

        p1_h = tf1.paragraphs[0]
        p1_h.text = f"👤 求美者基本特征档案"
        p1_h.font.name = FONT_HEADING
        p1_h.font.size = Pt(16)
        p1_h.font.bold = True
        p1_h.font.color.rgb = NAVY_PRIMARY
        p1_h.space_after = Pt(12)

        items = [
            ("代称与年龄", f"{profile_data.get('name', '')}，{profile_data.get('age', '')} 岁"),
            ("核心主诉", profile_data.get('complaints', '')),
            ("既往医美史", profile_data.get('history', '')),
            ("期望诉求", profile_data.get('expectations', ''))
        ]
        for label, val in items:
            p_lbl = tf1.add_paragraph()
            p_lbl.text = f"📌 {label}："
            p_lbl.font.name = FONT_HEADING
            p_lbl.font.size = Pt(13)
            p_lbl.font.bold = True
            p_lbl.font.color.rgb = TEAL_ACCENT
            
            p_val = tf1.add_paragraph()
            p_val.text = val
            p_val.font.name = FONT_BODY
            p_val.font.size = Pt(11.5)
            p_val.font.color.rgb = TEXT_DARK
            p_val.space_after = Pt(8)

        # 右栏：FAS 术前面部美学评分
        add_card_shape(slide, left2, top, col_w, height)
        bar2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left2, top, col_w, Inches(0.08))
        bar2.fill.solid()
        bar2.fill.fore_color.rgb = GOLD_ACCENT
        bar2.line.fill.background()

        tx2 = slide.shapes.add_textbox(left2 + Inches(0.3), top + Inches(0.25), col_w - Inches(0.6), height - Inches(0.5))
        tf2 = tx2.text_frame
        tf2.word_wrap = True

        p2_h = tf2.paragraphs[0]
        p2_h.text = f"📊 FAS 术前面部量化评估 (Facial Assessment Scale)"
        p2_h.font.name = FONT_HEADING
        p2_h.font.size = Pt(16)
        p2_h.font.bold = True
        p2_h.font.color.rgb = NAVY_PRIMARY
        p2_h.space_after = Pt(14)

        fas_scores = profile_data.get('fas_scores', {})
        for area, score in fas_scores.items():
            p_f = tf2.add_paragraph()
            p_f.text = f"🎯 {area}："
            p_f.font.name = FONT_HEADING
            p_f.font.size = Pt(13)
            p_f.font.bold = True
            p_f.font.color.rgb = NAVY_PRIMARY

            p_fs = tf2.add_paragraph()
            p_fs.text = f"    • 评估等级: {score}"
            p_fs.font.name = FONT_BODY
            p_fs.font.size = Pt(12)
            p_fs.font.color.rgb = TEXT_DARK
            p_fs.space_after = Pt(8)

        p_note = tf2.add_paragraph()
        p_note.text = "💡 评估结论：中面部深层骨膜与容积严重支撑不足，牵拉眶下韧带外露，需先深层复位支撑再行精细修饰。"
        p_note.font.name = FONT_BODY
        p_note.font.size = Pt(11)
        p_note.font.color.rgb = TEXT_MUTED

        add_disclaimer(slide, disclaimer)
        return slide

    def add_mapping_and_dose_slide(self, title, category, patient_summary, mapping_img_path, dose_items, disclaimer=DEFAULT_DISCLAIMER_CASE):
        """5. 面部画线布点与剂量明细页 (左图右表)"""
        slide = self.prs.slides.add_slide(self.blank_layout)
        set_slide_background(slide, WHITE)
        add_header(slide, title, category)

        img_left = Inches(0.8)
        img_top = Inches(1.6)
        img_w = Inches(4.5)
        img_h = Inches(5.0)
        add_image_or_placeholder(slide, mapping_img_path, img_left, img_top, img_w, img_h, "术前画线布点设计图")

        if patient_summary:
            tag_box = slide.shapes.add_textbox(img_left, img_top + img_h + Inches(0.05), img_w, Inches(0.35))
            tf_tag = tag_box.text_frame
            p_tag = tf_tag.paragraphs[0]
            p_tag.text = patient_summary
            p_tag.font.name = FONT_BODY
            p_tag.font.size = Pt(10)
            p_tag.font.bold = True
            p_tag.font.color.rgb = NAVY_PRIMARY

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
            detail_str = f"  • 层次/工具: {item.get('layer', '')} | {item.get('tool', '')}\n  • 剂量分配: Left {item.get('left_dose', '-')} / Right {item.get('right_dose', '-')}\n  • 选用材料: {item.get('product', '')}"
            p_detail.text = detail_str
            p_detail.font.name = FONT_BODY
            p_detail.font.size = Pt(11)
            p_detail.font.color.rgb = TEXT_DARK
            p_detail.space_after = Pt(8)

        add_disclaimer(slide, disclaimer)
        return slide

    def add_comparison_2up_slide(self, title, category, img_before, img_after, label_before="术前 (Before)", label_after="术后即刻 (Immediate After)", observation_notes="", disclaimer=DEFAULT_DISCLAIMER_CASE):
        """6. 经典 2-Up 对比页 (术前 vs 术后)"""
        slide = self.prs.slides.add_slide(self.blank_layout)
        set_slide_background(slide, WHITE)
        add_header(slide, title, category)

        top = Inches(1.6)
        img_w = Inches(4.3)
        img_h = Inches(4.8)
        left1 = Inches(0.8)
        left2 = Inches(5.4)

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

        notes_left = Inches(10.0)
        notes_w = Inches(2.533)
        add_card_shape(slide, notes_left, top, notes_w, img_h + Inches(0.43))
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
        """7. 患者时光走廊与就诊旅程页 (Patient Journey Timeline)"""
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

            add_image_or_placeholder(slide, stage.get("img_path", ""), left, top, col_w, img_h, stage.get("label", ""))

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
        """8. 医生临床思考与心得总结页"""
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
        """9. 结语与致谢页"""
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

def build_deck_from_config(cfg, output_file="Aesthetic_Case_Report.pptx"):
    """根据结构化配置构建完整医学 Case Report PPTX"""
    builder = AestheticDeckBuilder(output_file)

    meta = cfg.get("deck_meta", {})
    builder.add_cover_slide(
        title=meta.get("title", "Medical Aesthetics Case Report"),
        subtitle=meta.get("subtitle", "临床个案汇报"),
        speaker_info=meta.get("speaker", "主讲医生"),
        institution=meta.get("institution", "学术研讨会"),
        disclaimer=meta.get("disclaimer_cover", DEFAULT_DISCLAIMER_CONFIDENTIAL)
    )

    sc = cfg.get("slides_content", {})

    # 章节 1
    builder.add_section_divider_slide(1, "抗衰理念与全层解剖机制", "Aging Philosophy & Multi-layer Anatomy")
    if "anatomy_cards" in sc:
        builder.add_cards_slide(
            title="面部全层衰老认知与传统注射痛点",
            category="01 解剖机制与美学评估",
            cards_data=sc["anatomy_cards"],
            disclaimer=meta.get("disclaimer_content", DEFAULT_DISCLAIMER_CASE)
        )

    # 章节 2
    builder.add_section_divider_slide(2, "病例档案与个体化治疗方案", "Patient Profile & Treatment Plan")
    if "patient_profile" in sc:
        builder.add_patient_profile_slide(
            title="患者基线画像与 FAS 美学评估",
            category="02 病例档案",
            profile_data=sc["patient_profile"],
            disclaimer=meta.get("disclaimer_content", DEFAULT_DISCLAIMER_CASE)
        )
    if "treatment_mapping" in sc:
        tm = sc["treatment_mapping"]
        builder.add_mapping_and_dose_slide(
            title="首期注射方案规划与精细剂量分配",
            category="02 治疗方案与布点",
            patient_summary=tm.get("patient_summary", ""),
            mapping_img_path=tm.get("mapping_photo", ""),
            dose_items=tm.get("dose_items", []),
            disclaimer=meta.get("disclaimer_content", DEFAULT_DISCLAIMER_CASE)
        )

    # 章节 3
    builder.add_section_divider_slide(3, "首期治疗效果与多维对比", "Immediate Post-op & Comparative Matrix")
    if "comparisons" in sc:
        comp = sc["comparisons"]
        builder.add_comparison_2up_slide(
            title="首期治疗前后对比：正面平视静态",
            category="03 术后即刻临床评价",
            img_before=comp.get("baseline_photo", ""),
            img_after=comp.get("immediate_photo", ""),
            label_before="术前基线 (Baseline)",
            label_after="术后即刻 (Immediate After)",
            observation_notes=comp.get("notes", ""),
            disclaimer=meta.get("disclaimer_content", DEFAULT_DISCLAIMER_CASE)
        )

    # 章节 4
    builder.add_section_divider_slide(4, "二期微调与全程就诊旅程", "2nd Treatment & Longitudinal Patient Journey")
    if "timeline_stages" in sc:
        builder.add_timeline_journey_slide(
            title="全程时光走廊与长期维养 (Patient Journey)",
            category="04 纵向长期随访",
            stages_data=sc["timeline_stages"],
            disclaimer=meta.get("disclaimer_content", DEFAULT_DISCLAIMER_CASE)
        )

    # 章节 5
    builder.add_section_divider_slide(5, "临床思考与心得总结", "Clinical Insights & Key Takeaways")
    if "doctor_insights" in sc:
        builder.add_doctor_insights_slide(
            title="临床思考与核心心得 (Doctor's Key Takeaways)",
            category="05 专家观点",
            insights=sc["doctor_insights"],
            disclaimer=meta.get("disclaimer_content", DEFAULT_DISCLAIMER_CASE)
        )

    # 致谢
    builder.add_closing_slide(
        thank_you_text="Thank You",
        doctor_name=meta.get("speaker", ""),
        disclaimer=meta.get("disclaimer_cover", DEFAULT_DISCLAIMER_CONFIDENTIAL)
    )

    builder.save()

def main():
    parser = argparse.ArgumentParser(description="Aesthetic Case Report Deck Generator")
    parser.add_argument("--demo", action="store_true", help="Generate a comprehensive demo case deck")
    parser.add_argument("--config", type=str, help="Path to JSON configuration file for custom deck")
    parser.add_argument("--output", type=str, default="Aesthetic_Case_Report.pptx", help="Output PPTX path")

    args = parser.parse_args()

    if args.config:
        with open(args.config, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        build_deck_from_config(cfg, args.output)
    else:
        # demo mode
        print("Generating comprehensive Aesthetic Case Report Demo deck...")
        # fallback to simple demo
        with open("test_data/case_config.json", "r", encoding="utf-8") as f:
            cfg = json.load(f)
        build_deck_from_config(cfg, args.output)

if __name__ == "__main__":
    main()
