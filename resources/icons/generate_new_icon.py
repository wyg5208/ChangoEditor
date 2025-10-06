"""
ChangoEditor Icon Generator
Design: Highlight C and G letters with modern gradient colors
"""

from PIL import Image, ImageDraw, ImageFont
import os
import sys

# Set UTF-8 encoding for console output
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def create_chango_icon(size=512):
    """创建突出C和G字母的现代图标"""
    
    # 创建画布，使用透明背景
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 定义颜色方案 - 现代科技风格
    bg_color = (45, 55, 72, 255)  # 深蓝灰色背景
    gradient_start = (99, 102, 241, 255)  # 紫蓝色
    gradient_end = (139, 92, 246, 255)  # 紫色
    accent_color = (236, 72, 153, 255)  # 粉红色强调
    text_color = (255, 255, 255, 255)  # 白色文字
    
    # 绘制圆角矩形背景
    corner_radius = size // 8
    draw.rounded_rectangle(
        [(0, 0), (size, size)],
        radius=corner_radius,
        fill=bg_color
    )
    
    # 绘制渐变背景效果
    for i in range(size):
        ratio = i / size
        r = int(gradient_start[0] + (gradient_end[0] - gradient_start[0]) * ratio)
        g = int(gradient_start[1] + (gradient_end[1] - gradient_start[1]) * ratio)
        b = int(gradient_start[2] + (gradient_end[2] - gradient_start[2]) * ratio)
        alpha = int(180 * (1 - ratio * 0.7))  # 渐变透明度
        
        draw.line([(0, i), (size, i)], fill=(r, g, b, alpha), width=1)
    
    # 绘制装饰圆圈
    circle_size = size // 6
    draw.ellipse(
        [(size - circle_size - 20, 20), (size - 20, 20 + circle_size)],
        fill=accent_color
    )
    
    # 创建字母 C 和 G 的形状（使用几何图形绘制，不依赖字体）
    # 字母尺寸
    letter_size = size // 2
    stroke_width = size // 20
    center_x = size // 2
    center_y = size // 2
    
    # 绘制字母 C（左侧）
    c_x = center_x - letter_size // 3
    c_radius = letter_size // 3
    
    # C 的外圆
    draw.arc(
        [(c_x - c_radius, center_y - c_radius),
         (c_x + c_radius, center_y + c_radius)],
        start=45, end=315,
        fill=text_color,
        width=stroke_width
    )
    
    # 绘制字母 G（右侧）
    g_x = center_x + letter_size // 3
    g_radius = letter_size // 3
    
    # G 的外圆
    draw.arc(
        [(g_x - g_radius, center_y - g_radius),
         (g_x + g_radius, center_y + g_radius)],
        start=45, end=315,
        fill=text_color,
        width=stroke_width
    )
    
    # G 的横线
    horizontal_line_y = center_y
    draw.rectangle(
        [(g_x - stroke_width // 2, horizontal_line_y - stroke_width // 2),
         (g_x + g_radius, horizontal_line_y + stroke_width // 2)],
        fill=text_color
    )
    
    # G 的竖线
    draw.rectangle(
        [(g_x + g_radius - stroke_width, horizontal_line_y - stroke_width // 2),
         (g_x + g_radius, center_y + stroke_width)],
        fill=text_color
    )
    
    # 添加底部装饰线
    line_y = size - 40
    draw.line(
        [(40, line_y), (size - 40, line_y)],
        fill=accent_color,
        width=4
    )
    
    # 添加小点装饰
    dot_size = 8
    for i in range(3):
        x = 50 + i * 30
        draw.ellipse(
            [(x, line_y - dot_size // 2), (x + dot_size, line_y + dot_size // 2)],
            fill=accent_color
        )
    
    return img


def create_alternative_icon(size=512):
    """创建另一个设计方案 - 交叉的C和G"""
    
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 定义颜色 - 编辑器风格
    bg_color = (30, 41, 59, 255)  # 深色背景
    c_color = (34, 211, 238, 255)  # 青色 C
    g_color = (251, 191, 36, 255)  # 橙色 G
    border_color = (148, 163, 184, 255)  # 边框
    
    # 绘制圆角矩形背景
    corner_radius = size // 8
    draw.rounded_rectangle(
        [(0, 0), (size, size)],
        radius=corner_radius,
        fill=bg_color
    )
    
    # 绘制边框
    draw.rounded_rectangle(
        [(10, 10), (size - 10, size - 10)],
        radius=corner_radius - 5,
        outline=border_color,
        width=3
    )
    
    # 参数
    center_x = size // 2
    center_y = size // 2
    letter_radius = size // 3
    stroke_width = size // 18
    
    # 绘制大号字母 C
    draw.arc(
        [(center_x - letter_radius - 30, center_y - letter_radius),
         (center_x + letter_radius - 30, center_y + letter_radius)],
        start=45, end=315,
        fill=c_color,
        width=stroke_width
    )
    
    # 绘制大号字母 G
    # G 的外圆
    draw.arc(
        [(center_x - letter_radius + 30, center_y - letter_radius),
         (center_x + letter_radius + 30, center_y + letter_radius)],
        start=45, end=315,
        fill=g_color,
        width=stroke_width
    )
    
    # G 的横线和竖线
    g_center_x = center_x + 30
    horizontal_y = center_y
    
    draw.rectangle(
        [(g_center_x - stroke_width // 2, horizontal_y - stroke_width // 2),
         (g_center_x + letter_radius, horizontal_y + stroke_width // 2)],
        fill=g_color
    )
    
    draw.rectangle(
        [(g_center_x + letter_radius - stroke_width, horizontal_y - stroke_width // 2),
         (g_center_x + letter_radius, horizontal_y + letter_radius // 2)],
        fill=g_color
    )
    
    # 添加代码符号装饰 < >
    bracket_size = 40
    bracket_y = size - 80
    draw.text((40, bracket_y), "</>", fill=c_color, font=None)
    
    return img


def create_minimalist_icon(size=512):
    """创建极简风格图标 - CG字母组合"""
    
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 渐变背景 - 从深蓝到深紫
    for i in range(size):
        ratio = i / size
        r = int(59 + (88 - 59) * ratio)
        g = int(130 + (28 - 130) * ratio)
        b = int(246 + (135 - 246) * ratio)
        draw.line([(0, i), (size, i)], fill=(r, g, b, 255), width=1)
    
    # 圆角遮罩
    corner_radius = size // 8
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle(
        [(0, 0), (size, size)],
        radius=corner_radius,
        fill=255
    )
    img.putalpha(mask)
    
    draw = ImageDraw.Draw(img)
    
    # 绘制超大 CG 字母
    center_x = size // 2
    center_y = size // 2
    letter_size = size // 2.2
    stroke = size // 15
    
    # C 字母
    c_x = center_x - letter_size // 3.5
    draw.arc(
        [(c_x - letter_size // 2, center_y - letter_size // 2),
         (c_x + letter_size // 2, center_y + letter_size // 2)],
        start=50, end=310,
        fill=(255, 255, 255, 255),
        width=stroke
    )
    
    # G 字母
    g_x = center_x + letter_size // 3.5
    draw.arc(
        [(g_x - letter_size // 2, center_y - letter_size // 2),
         (g_x + letter_size // 2, center_y + letter_size // 2)],
        start=50, end=310,
        fill=(255, 255, 255, 255),
        width=stroke
    )
    
    # G 的特征线
    h_line_y = center_y
    draw.rectangle(
        [(g_x - stroke // 2, h_line_y - stroke // 2),
         (g_x + letter_size // 2, h_line_y + stroke // 2)],
        fill=(255, 255, 255, 255)
    )
    
    draw.rectangle(
        [(g_x + letter_size // 2 - stroke, h_line_y),
         (g_x + letter_size // 2, h_line_y + letter_size // 3)],
        fill=(255, 255, 255, 255)
    )
    
    # 添加光晕效果
    glow_size = size // 4
    glow = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse(
        [(center_x - glow_size, center_y - glow_size),
         (center_x + glow_size, center_y + glow_size)],
        fill=(255, 255, 255, 30)
    )
    img = Image.alpha_composite(img, glow)
    
    return img


def main():
    """生成所有尺寸的图标"""
    
    # 获取图标目录
    icon_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 生成三种设计方案
    designs = {
        'chango_editor_v1': create_chango_icon,
        'chango_editor_v2': create_alternative_icon,
        'chango_editor_v3': create_minimalist_icon
    }
    
    for design_name, create_func in designs.items():
        print(f"\nGenerating design: {design_name}")
        
        # 生成主图标 (512x512)
        main_icon = create_func(512)
        png_path = os.path.join(icon_dir, f'{design_name}.png')
        main_icon.save(png_path, 'PNG')
        print(f"  Saved: {design_name}.png (512x512)")
        
        # Generate ICO file with multiple sizes
        ico_path = os.path.join(icon_dir, f'{design_name}.ico')
        sizes = [16, 32, 48, 64, 128, 256]
        icon_images = []
        
        for size in sizes:
            resized = main_icon.resize((size, size), Image.Resampling.LANCZOS)
            icon_images.append(resized)
        
        icon_images[0].save(
            ico_path,
            format='ICO',
            sizes=[(s, s) for s in sizes],
            append_images=icon_images[1:]
        )
        print(f"  Saved: {design_name}.ico (multi-size)")
    
    print("\n" + "="*60)
    print("Icon generation completed!")
    print("="*60)
    print("\nThree design options:")
    print("  1. chango_editor_v1.png/ico - Modern gradient style, CG letters")
    print("  2. chango_editor_v2.png/ico - Dark editor style, colorful CG")
    print("  3. chango_editor_v3.png/ico - Minimalist style, white CG letters")
    print("\nPlease check and choose your favorite design!")
    print("="*60)


if __name__ == '__main__':
    main()

