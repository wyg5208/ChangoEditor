"""
测试翻译键是否正确加载
"""

import sys
from pathlib import Path

# 添加src到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.i18n import get_i18n_manager, tr

def test_translations():
    """测试翻译功能"""
    i18n = get_i18n_manager()
    
    print("=" * 60)
    print("🔍 翻译键测试")
    print("=" * 60)
    
    # 测试键列表
    test_keys = [
        "menu.file.title",
        "menu.file.new.text",
        "menu.file.new.tip",
        "menu.file.open.text",
        "menu.file.open.tip",
        "menu.file.open_folder.text",
        "menu.file.open_folder.tip",
        "menu.file.save.text",
        "menu.file.save.tip",
        "menu.file.save_as.text",
        "menu.file.save_as.tip",
    ]
    
    # 测试三种语言
    for locale in ["zh_CN", "en_US", "ja_JP"]:
        print(f"\n📋 测试语言: {locale} ({i18n.get_available_locales().get(locale, '未知')})")
        print("-" * 60)
        
        i18n.set_locale(locale)
        
        for key in test_keys:
            value = tr(key)
            # 检查是否是原始键（表示翻译缺失）
            if value == key:
                print(f"  ❌ {key:30s} = [缺失翻译]")
            else:
                print(f"  ✅ {key:30s} = {value}")
    
    print("\n" + "=" * 60)
    print("✅ 测试完成")
    print("=" * 60)

if __name__ == "__main__":
    test_translations()

