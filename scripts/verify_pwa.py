"""
PWA配置验证脚本
检查心动积分系统的PWA配置是否正确
"""
import os
import json
import sys
from pathlib import Path

# 颜色输出
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}✓{Colors.END} {msg}")

def print_error(msg):
    print(f"{Colors.RED}✗{Colors.END} {msg}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠{Colors.END} {msg}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ{Colors.END} {msg}")

def check_file_exists(file_path, description):
    """检查文件是否存在"""
    if os.path.exists(file_path):
        print_success(f"{description} 存在: {file_path}")
        return True
    else:
        print_error(f"{description} 不存在: {file_path}")
        return False

def check_manifest():
    """检查manifest.json配置"""
    print("\n" + "="*60)
    print("检查 Manifest 配置")
    print("="*60)

    manifest_path = "frontend/static/manifest.json"

    if not check_file_exists(manifest_path, "Manifest文件"):
        return False

    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)

        # 检查必需字段
        required_fields = ['name', 'short_name', 'start_url', 'display', 'icons']
        for field in required_fields:
            if field in manifest:
                print_success(f"包含必需字段: {field}")
            else:
                print_error(f"缺少必需字段: {field}")

        # 检查图标配置
        if 'icons' in manifest:
            icon_count = len(manifest['icons'])
            print_info(f"配置了 {icon_count} 个图标")

            # 检查关键尺寸
            sizes = [icon['sizes'] for icon in manifest['icons']]
            required_sizes = ['192x192', '512x512']
            for size in required_sizes:
                if size in sizes:
                    print_success(f"包含关键尺寸: {size}")
                else:
                    print_warning(f"建议添加尺寸: {size}")

        # 检查主题色
        if 'theme_color' in manifest:
            print_success(f"主题色: {manifest['theme_color']}")

        if 'background_color' in manifest:
            print_success(f"背景色: {manifest['background_color']}")

        return True

    except json.JSONDecodeError as e:
        print_error(f"Manifest JSON格式错误: {e}")
        return False
    except Exception as e:
        print_error(f"读取Manifest失败: {e}")
        return False

def check_service_worker():
    """检查Service Worker配置"""
    print("\n" + "="*60)
    print("检查 Service Worker")
    print("="*60)

    sw_path = "frontend/static/sw.js"

    if not check_file_exists(sw_path, "Service Worker文件"):
        return False

    try:
        with open(sw_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查关键代码
        checks = [
            ('CACHE_VERSION', '缓存版本号'),
            ('addEventListener(\'install\'', 'install事件监听'),
            ('addEventListener(\'activate\'', 'activate事件监听'),
            ('addEventListener(\'fetch\'', 'fetch事件监听'),
            ('caches.open', '缓存API使用'),
        ]

        for keyword, description in checks:
            if keyword in content:
                print_success(f"包含{description}")
            else:
                print_error(f"缺少{description}")

        # 提取版本号
        import re
        version_match = re.search(r"CACHE_VERSION\s*=\s*['\"]([^'\"]+)['\"]", content)
        if version_match:
            version = version_match.group(1)
            print_info(f"当前版本: {version}")

        return True

    except Exception as e:
        print_error(f"读取Service Worker失败: {e}")
        return False

def check_icons():
    """检查图标文件"""
    print("\n" + "="*60)
    print("检查 PWA 图标")
    print("="*60)

    icons_dir = "frontend/static/icons"

    if not os.path.exists(icons_dir):
        print_error(f"图标目录不存在: {icons_dir}")
        print_info("运行以下命令生成图标:")
        print_info("  python scripts/generate_pwa_icons.py")
        return False

    # 检查必需的图标尺寸
    required_icons = [
        'icon-72x72.png',
        'icon-96x96.png',
        'icon-128x128.png',
        'icon-144x144.png',
        'icon-152x152.png',
        'icon-192x192.png',
        'icon-384x384.png',
        'icon-512x512.png',
    ]

    missing_icons = []
    for icon in required_icons:
        icon_path = os.path.join(icons_dir, icon)
        if os.path.exists(icon_path):
            print_success(f"图标存在: {icon}")
        else:
            print_error(f"图标缺失: {icon}")
            missing_icons.append(icon)

    if missing_icons:
        print_warning(f"缺少 {len(missing_icons)} 个图标")
        print_info("运行以下命令生成图标:")
        print_info("  python scripts/generate_pwa_icons.py")
        return False

    return True

def check_template():
    """检查模板集成"""
    print("\n" + "="*60)
    print("检查 模板集成")
    print("="*60)

    template_path = "frontend/templates/base_new.html"

    if not check_file_exists(template_path, "基础模板"):
        return False

    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查PWA相关代码
        checks = [
            ('<link rel="manifest"', 'Manifest链接'),
            ('<meta name="theme-color"', '主题色meta标签'),
            ('serviceWorker.register', 'Service Worker注册'),
            ('beforeinstallprompt', '安装提示监听'),
            ('apple-mobile-web-app-capable', 'iOS PWA支持'),
        ]

        for keyword, description in checks:
            if keyword in content:
                print_success(f"包含{description}")
            else:
                print_warning(f"可能缺少{description}")

        return True

    except Exception as e:
        print_error(f"读取模板失败: {e}")
        return False

def check_dependencies():
    """检查依赖"""
    print("\n" + "="*60)
    print("检查 Python 依赖")
    print("="*60)

    try:
        import flask
        print_success(f"Flask 已安装 (版本 {flask.__version__})")
    except ImportError:
        print_error("Flask 未安装")
        return False

    try:
        import fastapi
        print_success(f"FastAPI 已安装 (版本 {fastapi.__version__})")
    except ImportError:
        print_error("FastAPI 未安装")
        return False

    try:
        from PIL import Image
        print_success("Pillow 已安装 (用于图标生成)")
    except ImportError:
        print_warning("Pillow 未安装 (图标生成需要)")

    return True

def check_structure():
    """检查项目结构"""
    print("\n" + "="*60)
    print("检查 项目结构")
    print("="*60)

    required_dirs = [
        'frontend',
        'frontend/templates',
        'frontend/static',
        'backend',
        'backend/api',
        'scripts',
        'data',
    ]

    all_exist = True
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print_success(f"目录存在: {dir_path}")
        else:
            print_error(f"目录缺失: {dir_path}")
            all_exist = False

    return all_exist

def print_summary(results):
    """打印检查摘要"""
    print("\n" + "="*60)
    print("检查摘要")
    print("="*60)

    total = len(results)
    passed = sum(results.values())

    print(f"\n总计: {total} 项检查")
    print(f"通过: {Colors.GREEN}{passed}{Colors.END} 项")
    print(f"失败: {Colors.RED}{total - passed}{Colors.END} 项")

    if passed == total:
        print(f"\n{Colors.GREEN}🎉 所有检查通过！PWA配置正确。{Colors.END}")
        print("\n下一步:")
        print("  1. 运行 start_pwa.bat 启动服务")
        print("  2. 访问 http://localhost:5000")
        print("  3. 使用Chrome DevTools检查PWA功能")
        print("  4. 尝试安装到主屏幕")
        return True
    else:
        print(f"\n{Colors.YELLOW}⚠ 发现问题，请修复后重试。{Colors.END}")
        print("\n建议:")
        print("  1. 检查上述错误信息")
        print("  2. 运行 python scripts/generate_pwa_icons.py 生成图标")
        print("  3. 确保所有文件都已正确创建")
        print("  4. 重新运行此脚本验证")
        return False

def main():
    """主函数"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}心动积分 PWA 配置验证工具 v2.1{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")

    # 检查当前目录
    if not os.path.exists('frontend') or not os.path.exists('backend'):
        print_error("请在项目根目录运行此脚本")
        sys.exit(1)

    # 执行各项检查
    results = {
        '项目结构': check_structure(),
        'Python依赖': check_dependencies(),
        'Manifest配置': check_manifest(),
        'Service Worker': check_service_worker(),
        'PWA图标': check_icons(),
        '模板集成': check_template(),
    }

    # 打印摘要
    success = print_summary(results)

    # 返回状态码
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
