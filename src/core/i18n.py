"""
国际化(i18n)核心模块
提供多语言支持功能
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from PyQt6.QtCore import QSettings, QLocale, QObject, pyqtSignal

logger = logging.getLogger(__name__)


class I18nManager(QObject):
    """
    国际化管理器 - 单例模式
    负责加载、管理和切换应用程序的多语言翻译
    """
    
    # 语言切换信号
    language_changed = pyqtSignal(str)  # 参数为新语言代码
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """单例模式实现"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """初始化国际化管理器"""
        if self._initialized:
            return
            
        super().__init__()
        
        # 语言文件目录
        self.locale_dir = Path(__file__).parent.parent.parent / "resources" / "i18n" / "locales"
        
        # 应用设置
        self.settings = QSettings('ChangoSoft', 'ChangoEditor')
        
        # 翻译数据
        self._translations: Dict[str, Any] = {}
        self._current_locale: str = "zh_CN"
        self._fallback_locale: str = "zh_CN"  # 设置简体中文为默认后备语言
        
        # 缺失翻译键记录
        self._missing_keys: set = set()
        
        # 标记已初始化
        self._initialized = True
        
        # 加载语言
        self._load_locale()
        
        logger.info(f"I18n manager initialized with locale: {self._current_locale}")
    
    def _load_locale(self):
        """加载语言文件"""
        # 1. 从设置读取用户选择的语言
        saved_locale = self.settings.value('language', None)
        
        # 2. 如果没有保存，则自动检测系统语言
        if not saved_locale:
            system_locale = QLocale.system().name()  # 如 "zh_CN"
            logger.info(f"Detected system locale: {system_locale}")
            
            # 检查系统语言文件是否存在
            if self._locale_exists(system_locale):
                saved_locale = system_locale
            else:
                # 尝试只匹配语言代码（忽略国家/地区）
                lang_code = system_locale.split('_')[0]  # 如 "zh"
                
                # 查找匹配的语言文件
                for locale_file in self.locale_dir.glob(f"{lang_code}_*.json"):
                    saved_locale = locale_file.stem
                    logger.info(f"Found matching locale: {saved_locale}")
                    break
                else:
                    # 使用后备语言
                    saved_locale = self._fallback_locale
                    logger.info(f"Using fallback locale: {saved_locale}")
        
        # 3. 加载语言文件
        self.set_locale(saved_locale)
    
    def _locale_exists(self, locale: str) -> bool:
        """检查语言文件是否存在"""
        return (self.locale_dir / f"{locale}.json").exists()
    
    def set_locale(self, locale: str):
        """
        设置当前语言
        
        Args:
            locale: 语言代码，如 "zh_CN", "en_US", "ja_JP"
        """
        locale_file = self.locale_dir / f"{locale}.json"
        fallback_file = self.locale_dir / f"{self._fallback_locale}.json"
        
        try:
            # 加载主语言文件
            if locale_file.exists():
                with open(locale_file, 'r', encoding='utf-8') as f:
                    self._translations = json.load(f)
                
                old_locale = self._current_locale
                self._current_locale = locale
                self.settings.setValue('language', locale)
                
                logger.info(f"Locale changed from {old_locale} to {locale}")
                
                # 发出语言切换信号
                self.language_changed.emit(locale)
            else:
                logger.warning(f"Locale file not found: {locale_file}")
                
                # 加载后备语言
                if fallback_file.exists():
                    with open(fallback_file, 'r', encoding='utf-8') as f:
                        self._translations = json.load(f)
                    self._current_locale = self._fallback_locale
                    logger.info(f"Loaded fallback locale: {self._fallback_locale}")
                else:
                    logger.error(f"Fallback locale file not found: {fallback_file}")
                    self._translations = {}
                    
        except Exception as e:
            logger.error(f"Error loading locale {locale}: {e}")
            self._translations = {}
    
    def tr(self, key: str, **kwargs) -> str:
        """
        翻译函数
        
        Args:
            key: 翻译键，使用点号分隔的层级结构，如 "menu.file.new"
            **kwargs: 格式化参数，如 filename="test.py", error="File not found"
        
        Returns:
            翻译后的文本，如果找不到翻译则返回键名
        
        Examples:
            >>> tr("menu.file.new")
            "新建"
            
            >>> tr("message.file_saved_as", filename="test.py")
            "文件已另存为：test.py"
        """
        keys = key.split('.')
        value = self._translations
        
        # 递归查找键值
        try:
            for k in keys:
                value = value[k]
            
            # 支持参数格式化
            if kwargs and isinstance(value, str):
                return value.format(**kwargs)
            
            return str(value)
            
        except (KeyError, TypeError) as e:
            # 记录缺失的翻译键
            if key not in self._missing_keys:
                self._missing_keys.add(key)
                logger.debug(f"Missing translation key: {key}")
            
            # 返回键名作为后备
            return key
        except Exception as e:
            logger.error(f"Error translating key '{key}': {e}")
            return key
    
    def get_available_locales(self) -> Dict[str, str]:
        """
        获取所有可用语言
        
        Returns:
            字典，键为语言代码，值为语言名称
            例如：{"zh_CN": "简体中文", "en_US": "English"}
        """
        locales = {}
        
        try:
            for file in self.locale_dir.glob("*.json"):
                locale_code = file.stem
                
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        language_name = data.get('meta', {}).get('language', locale_code)
                        locales[locale_code] = language_name
                except Exception as e:
                    logger.error(f"Error reading locale file {file}: {e}")
                    
        except Exception as e:
            logger.error(f"Error scanning locale directory: {e}")
        
        return locales
    
    def get_current_locale(self) -> str:
        """
        获取当前语言代码
        
        Returns:
            当前语言代码，如 "zh_CN"
        """
        return self._current_locale
    
    def get_current_locale_name(self) -> str:
        """
        获取当前语言名称
        
        Returns:
            当前语言名称，如 "简体中文"
        """
        return self._translations.get('meta', {}).get('language', self._current_locale)
    
    def export_missing_keys(self, output_file: str = "missing_translations.txt"):
        """
        导出缺失的翻译键到文件
        
        Args:
            output_file: 输出文件路径
        """
        if not self._missing_keys:
            logger.info("No missing translation keys")
            return
        
        try:
            output_path = Path(output_file)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"# Missing Translation Keys ({len(self._missing_keys)} total)\n")
                f.write(f"# Current locale: {self._current_locale}\n\n")
                
                for key in sorted(self._missing_keys):
                    f.write(f"{key}\n")
            
            logger.info(f"Exported {len(self._missing_keys)} missing keys to {output_path}")
            
        except Exception as e:
            logger.error(f"Error exporting missing keys: {e}")
    
    def clear_missing_keys(self):
        """清空缺失翻译键记录"""
        self._missing_keys.clear()
        logger.debug("Cleared missing translation keys")


# ============================================================================
# 全局单例实例和便捷函数
# ============================================================================

_i18n: Optional[I18nManager] = None


def get_i18n_manager() -> I18nManager:
    """
    获取国际化管理器单例
    
    Returns:
        I18nManager实例
    """
    global _i18n
    if _i18n is None:
        _i18n = I18nManager()
    return _i18n


def tr(key: str, **kwargs) -> str:
    """
    全局翻译函数（便捷方法）
    
    Args:
        key: 翻译键
        **kwargs: 格式化参数
    
    Returns:
        翻译后的文本
    
    Examples:
        >>> from src.core.i18n import tr
        >>> tr("menu.file.new")
        "新建"
    """
    return get_i18n_manager().tr(key, **kwargs)


def set_language(locale: str):
    """
    设置语言（便捷方法）
    
    Args:
        locale: 语言代码
    """
    get_i18n_manager().set_locale(locale)


def get_available_languages() -> Dict[str, str]:
    """
    获取可用语言列表（便捷方法）
    
    Returns:
        可用语言字典
    """
    return get_i18n_manager().get_available_locales()


def get_current_language() -> str:
    """
    获取当前语言代码（便捷方法）
    
    Returns:
        当前语言代码
    """
    return get_i18n_manager().get_current_locale()


def get_current_language_name() -> str:
    """
    获取当前语言名称（便捷方法）
    
    Returns:
        当前语言名称
    """
    return get_i18n_manager().get_current_locale_name()


# ============================================================================
# 初始化
# ============================================================================

# 自动初始化（导入时创建单例）
_i18n = I18nManager()

logger.info("I18n module loaded successfully")

