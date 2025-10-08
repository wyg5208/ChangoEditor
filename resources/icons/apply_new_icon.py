"""
Quick script to apply new icon design
"""

import shutil
import os

def apply_icon(version='v2'):
    """
    Apply selected icon version as the main icon
    
    Args:
        version: v1, v2, or v3
    """
    icon_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define file paths
    old_png = os.path.join(icon_dir, 'chango_editor.png')
    old_ico = os.path.join(icon_dir, 'chango_editor.ico')
    
    new_png = os.path.join(icon_dir, f'chango_editor_{version}.png')
    new_ico = os.path.join(icon_dir, f'chango_editor_{version}.ico')
    
    backup_png = os.path.join(icon_dir, 'chango_editor_old.png')
    backup_ico = os.path.join(icon_dir, 'chango_editor_old.ico')
    
    # Check if new icon exists
    if not os.path.exists(new_png) or not os.path.exists(new_ico):
        print(f"Error: Icon version {version} not found!")
        print(f"Available versions: v1, v2, v3")
        return False
    
    print(f"\n{'='*60}")
    print(f"Applying icon design: chango_editor_{version}")
    print(f"{'='*60}\n")
    
    # Backup old icons
    if os.path.exists(old_png):
        shutil.copy2(old_png, backup_png)
        print(f"Backed up: chango_editor.png -> chango_editor_old.png")
    
    if os.path.exists(old_ico):
        shutil.copy2(old_ico, backup_ico)
        print(f"Backed up: chango_editor.ico -> chango_editor_old.ico")
    
    # Apply new icons
    shutil.copy2(new_png, old_png)
    print(f"Applied: chango_editor_{version}.png -> chango_editor.png")
    
    shutil.copy2(new_ico, old_ico)
    print(f"Applied: chango_editor_{version}.ico -> chango_editor.ico")
    
    print(f"\n{'='*60}")
    print(f"Icon successfully applied!")
    print(f"{'='*60}\n")
    print("Next steps:")
    print("1. Rebuild the executable: python build_exe.py")
    print("2. The new icon will be used in the compiled application")
    print("\nTo restore old icon:")
    print("  Copy chango_editor_old.png/ico back to chango_editor.png/ico")
    print(f"{'='*60}\n")
    
    return True


def preview_icons():
    """Show available icon options"""
    print("\n" + "="*60)
    print("ChangoEditor Icon Options")
    print("="*60 + "\n")
    
    print("Available designs:\n")
    print("  [v1] Modern gradient style")
    print("       - Purple-blue gradient background")
    print("       - White CG letters")
    print("       - Pink accent dot\n")
    
    print("  [v2] Dark editor style (RECOMMENDED)")
    print("       - Dark background")
    print("       - Cyan C + Orange G")
    print("       - Code symbol decoration\n")
    
    print("  [v3] Minimalist gradient style")
    print("       - Blue-purple gradient")
    print("       - Large white CG letters")
    print("       - Center glow effect\n")
    
    print("="*60 + "\n")


if __name__ == '__main__':
    import sys
    
    preview_icons()
    
    if len(sys.argv) < 2:
        print("Usage: python apply_new_icon.py [v1|v2|v3]")
        print("Example: python apply_new_icon.py v2")
        print("\nRecommendation: v2 (best for code editor)")
        sys.exit(0)
    
    version = sys.argv[1].lower()
    if version not in ['v1', 'v2', 'v3']:
        print(f"Error: Invalid version '{version}'")
        print("Please choose: v1, v2, or v3")
        sys.exit(1)
    
    success = apply_icon(version)
    sys.exit(0 if success else 1)





