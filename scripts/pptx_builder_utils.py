"""
Aesthetic Case Report PPTX Builder Utilities
医美学术与临床病例 PPTX 自动化排版核心样式与工具函数库
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# -------------------------------------------------------------
# 1. 颜色常数定义 (Aesthetic & Medical Color Palette)
# -------------------------------------------------------------
NAVY_PRIMARY = RGBColor(15, 44, 89)      # #0F2C59 高德美深海蓝 / 学术主色
NAVY_DARK = RGBColor(10, 25, 47)         # #0A192F 深邃夜幕底色
TEAL_ACCENT = RGBColor(0, 163, 196)      # #00A3C4 医美科技青 / 强调色
GOLD_ACCENT = RGBColor(197, 168, 128)    # #C5A880 香槟雅金 / 点缀色
CARD_BG = RGBColor(248, 249, 250)        # #F8F9FA 卡片极浅灰白底
CARD_BORDER = RGBColor(226, 232, 240)    # #E2E8F0 超细边框灰
TEXT_DARK = RGBColor(26, 32, 44)         # #1A202C 主要文字炭黑
TEXT_MUTED = RGBColor(113, 128, 150)     # #718096 辅助注释冷灰
TEXT_LIGHT = RGBColor(247, 250, 252)     # #F7FAFC 浅色文字
WHITE = RGBColor(255, 255, 255)
GREEN_ACCENT = RGBColor(46, 133, 64)     # 绿色/获益标注
GRAY_PLACEHOLDER = RGBColor(230, 235, 240)

FONT_HEADING = "Microsoft YaHei"
FONT_BODY = "Microsoft YaHei"
FONT_EN = "Arial"

SLIDE_WIDTH_INCHES = 13.333
SLIDE_HEIGHT_INCHES = 7.500

DEFAULT_DISCLAIMER_CONFIDENTIAL = "（非公开）会议资料，仅供临床学术探讨与专业交流，请勿外传。"
DEFAULT_DISCLAIMER_CASE = "以上为临床个案分享，仅供本次会议学术讨论；不同医疗器械/药品的具体使用，应参见国家药品监督管理局获批的中文产品说明书及相关临床诊疗指南。"

# -------------------------------------------------------------
# 2. 基础容器与几何绘制工具
# -------------------------------------------------------------
def set_slide_background(slide, color):
    """设置页面纯色背景"""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_header(slide, title_text, category_text=None, is_dark=False):
    """添加标准化页面顶栏标题"""
    top = Inches(0.45)
    left = Inches(0.8)
    width = Inches(11.7)
    height = Inches(0.9)

    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0)
    tf.margin_top = Inches(0)

    # 类别/面包屑小标 (例如: 03 解剖与机制 / SECTION)
    if category_text:
        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = FONT_EN
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = TEAL_ACCENT if is_dark else TEAL_ACCENT
        p_cat.space_after = Pt(4)
        p_title = tf.add_paragraph()
    else:
        p_title = tf.paragraphs[0]

    p_title.text = title_text
    p_title.font.name = FONT_HEADING
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = WHITE if is_dark else NAVY_PRIMARY

def add_disclaimer(slide, text=DEFAULT_DISCLAIMER_CASE, is_dark=False):
    """添加页面底部合规免责声明"""
    left = Inches(0.8)
    top = Inches(7.05)
    width = Inches(11.733)
    height = Inches(0.35)

    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0)
    tf.margin_top = Inches(0)
    p = tf.paragraphs[0]
    p.text = text
    p.font.name = FONT_BODY
    p.font.size = Pt(8.5)
    p.font.color.rgb = RGBColor(160, 174, 192) if is_dark else TEXT_MUTED

def add_card_shape(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
    """在幻灯片上绘制带有极细边框的卡片底板"""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()
    return card

def add_image_or_placeholder(slide, img_path, left, top, width, height, placeholder_label=""):
    """安全添加图片；如果图片不存在，则优雅绘制占位框"""
    if img_path and os.path.isfile(img_path):
        try:
            return slide.shapes.add_picture(img_path, left, top, width, height)
        except Exception as e:
            print(f"Warning: Failed to load picture {img_path}: {e}")

    # 占位框
    rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    rect.fill.solid()
    rect.fill.fore_color.rgb = GRAY_PLACEHOLDER
    rect.line.color.rgb = RGBColor(203, 213, 225)
    rect.line.width = Pt(1)

    tf = rect.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = f"📷 待替换照片\n{placeholder_label}"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(100, 116, 139)
    return rect
