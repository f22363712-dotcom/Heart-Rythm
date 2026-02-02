"""
PWA图标生成脚本
生成心动积分系统所需的各种尺寸的PWA图标
"""
from PIL import Image, ImageDraw, ImageFont
import os

# 图标尺寸列表
ICON_SIZES = [72, 96, 128, 144, 152, 192, 384, 512]
SHORTCUT_SIZE = 96

# 颜色配置（玫瑰腮红主题）
ROSE_BLUSH = '#e891a9'
ROSE_MAUVE = '#d47a9e'
ROSE_DAWN = '#f4b6c2'
BG_COLOR = '#faf5f7'

def create_heart_icon(size, output_path):
    """创建心形图标"""
    # 创建图像
    img = Image.new('RGBA', (size, size), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 计算心形的位置和大小
    padding = size * 0.15
    heart_size = size - 2 * padding

    # 绘制渐变背景圆形
    for i in range(int(size/2)):
        alpha = int(255 * (1 - i / (size/2)))
        color = tuple(int(ROSE_BLUSH.lstrip('#')[j:j+2], 16) for j in (0, 2, 4)) + (alpha,)
        draw.ellipse([i, i, size-i, size-i], fill=color)

    # 绘制心形（使用emoji或简化的心形）
    # 这里使用简化的心形路径
    center_x = size / 2
    center_y = size / 2

    # 心形的上半部分（两个圆）
    circle_radius = heart_size / 4
    left_circle_x = center_x - circle_radius
    right_circle_x = center_x + circle_radius
    circle_y = center_y - circle_radius / 2

    # 绘制左圆
    draw.ellipse([
        left_circle_x - circle_radius, circle_y - circle_radius,
        left_circle_x + circle_radius, circle_y + circle_radius
    ], fill=ROSE_MAUVE)

    # 绘制右圆
    draw.ellipse([
        right_circle_x - circle_radius, circle_y - circle_radius,
        right_circle_x + circle_radius, circle_y + circle_radius
    ], fill=ROSE_MAUVE)

    # 绘制心形的下半部分（三角形）
    triangle_points = [
        (center_x - heart_size/2 + padding, circle_y),
        (center_x + heart_size/2 - padding, circle_y),
        (center_x, center_y + heart_size/2)
    ]
    draw.polygon(triangle_points, fill=ROSE_MAUVE)

    # 添加文字（仅在大图标上）
    if size >= 192:
        try:
            # 尝试使用系统字体
            font_size = int(size * 0.15)
            font = ImageFont.truetype("msyh.ttc", font_size)  # 微软雅黑
            text = "心动"

            # 获取文字边界框
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # 在底部绘制文字
            text_x = (size - text_width) / 2
            text_y = size - text_height - padding

            # 绘制文字阴影
            draw.text((text_x + 2, text_y + 2), text, fill=(0, 0, 0, 100), font=font)
            # 绘制文字
            draw.text((text_x, text_y), text, fill='white', font=font)
        except:
            pass  # 如果字体加载失败，跳过文字

    # 保存图标
    img.save(output_path, 'PNG')
    print(f"✓ 生成图标: {output_path} ({size}x{size})")

def create_simple_icon(size, output_path, emoji="💕"):
    """创建简单的emoji图标（备用方案）"""
    img = Image.new('RGBA', (size, size), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 绘制圆形背景
    margin = size * 0.1
    draw.ellipse([margin, margin, size-margin, size-margin],
                 fill=ROSE_BLUSH, outline=ROSE_MAUVE, width=int(size*0.02))

    # 尝试添加emoji（需要支持emoji的字体）
    try:
        font_size = int(size * 0.5)
        # Windows 10/11 的 Segoe UI Emoji 字体
        font = ImageFont.truetype("seguiemj.ttf", font_size)

        # 获取文字边界框
        bbox = draw.textbbox((0, 0), emoji, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # 居中绘制emoji
        text_x = (size - text_width) / 2
        text_y = (size - text_height) / 2
        draw.text((text_x, text_y), emoji, font=font, embedded_color=True)
    except Exception as e:
        print(f"  警告: 无法加载emoji字体，使用纯色图标 ({e})")

    img.save(output_path, 'PNG')
    print(f"✓ 生成图标: {output_path} ({size}x{size})")

def main():
    """主函数"""
    # 获取项目根目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    icons_dir = os.path.join(project_root, 'frontend', 'static', 'icons')

    # 确保目录存在
    os.makedirs(icons_dir, exist_ok=True)

    print("🎨 开始生成PWA图标...")
    print(f"📁 输出目录: {icons_dir}\n")

    # 生成主图标
    for size in ICON_SIZES:
        output_path = os.path.join(icons_dir, f'icon-{size}x{size}.png')
        create_simple_icon(size, output_path, "💕")

    # 生成快捷方式图标
    print("\n🔖 生成快捷方式图标...")
    create_simple_icon(SHORTCUT_SIZE,
                      os.path.join(icons_dir, 'shortcut-record.png'),
                      "✨")
    create_simple_icon(SHORTCUT_SIZE,
                      os.path.join(icons_dir, 'shortcut-reward.png'),
                      "🎁")

    # 生成badge图标
    print("\n🏷️  生成badge图标...")
    create_simple_icon(72,
                      os.path.join(icons_dir, 'badge-72x72.png'),
                      "💗")

    print("\n✅ 所有图标生成完成！")
    print(f"📊 共生成 {len(ICON_SIZES) + 3} 个图标文件")
    print("\n💡 提示: 如果图标显示不正常，可以使用在线工具生成更精美的图标：")
    print("   - https://realfavicongenerator.net/")
    print("   - https://www.pwabuilder.com/imageGenerator")

if __name__ == '__main__':
    main()
