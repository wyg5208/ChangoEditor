"""
图标提供器 - 使用Font Awesome风格的SVG图标
提供现代化、清晰的矢量图标
"""

from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtSvg import QSvgRenderer
import base64


class IconProvider:
    """图标提供器类 - 提供SVG格式的现代化图标"""
    
    # Font Awesome风格的SVG图标路径数据
    SVG_ICONS = {
        # 文件操作图标
        'file-new': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><path fill="currentColor" d="M224 136V0H24C10.7 0 0 10.7 0 24v464c0 13.3 10.7 24 24 24h336c13.3 0 24-10.7 24-24V160H248c-13.2 0-24-10.8-24-24zm65.2 204.1l-64 64c-4.7 4.7-12.3 4.7-17 0l-64-64c-4.7-4.7-4.7-12.3 0-17l17-17c4.7-4.7 12.3-4.7 17 0l23 23V224c0-6.6 5.4-12 12-12h24c6.6 0 12 5.4 12 12v105.1l23-23c4.7-4.7 12.3-4.7 17 0l17 17c4.7 4.7 4.7 12.3 0 17zM377 105L279.1 7c-4.5-4.5-10.6-7-17-7H256v128h128v-6.1c0-6.3-2.5-12.4-7-16.9z"/></svg>''',
        
        'folder-open': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path fill="currentColor" d="M572.6 270.3l-96 192C471.2 473.2 460.1 480 447.1 480H64c-35.35 0-64-28.66-64-64V96c0-35.34 28.65-64 64-64h117.5c16.97 0 33.25 6.742 45.26 18.75L275.9 96H416c35.35 0 64 28.66 64 64v32h-48V160c0-8.824-7.178-16-16-16H256L192.8 84.69C189.8 81.66 185.8 80 181.5 80H64C55.18 80 48 87.18 48 96v288l71.16-142.3C124.6 230.8 135.7 224 147.8 224h396.2C567.7 224 583.2 249 572.6 270.3z"/></svg>''',
        
        'folder': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="currentColor" d="M464 128H272l-64-64H48C21.49 64 0 85.49 0 112v288c0 26.51 21.49 48 48 48h416c26.51 0 48-21.49 48-48V176c0-26.51-21.49-48-48-48z"/></svg>''',
        
        'save': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path fill="currentColor" d="M433.941 129.941l-83.882-83.882A48 48 0 0 0 316.118 32H48C21.49 32 0 53.49 0 80v352c0 26.51 21.49 48 48 48h352c26.51 0 48-21.49 48-48V163.882a48 48 0 0 0-14.059-33.941zM272 80v80H144V80h128zm122 352H54a6 6 0 0 1-6-6V86a6 6 0 0 1 6-6h36v104c0 13.255 10.745 24 24 24h176c13.255 0 24-10.745 24-24V83.882l78.243 78.243a6 6 0 0 1 1.757 4.243V426a6 6 0 0 1-6 6zM224 232c-48.523 0-88 39.477-88 88s39.477 88 88 88 88-39.477 88-88-39.477-88-88-88zm0 128c-22.056 0-40-17.944-40-40s17.944-40 40-40 40 17.944 40 40-17.944 40-40 40z"/></svg>''',
        
        'times-circle': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="currentColor" d="M256 8C119 8 8 119 8 256s111 248 248 248 248-111 248-248S393 8 256 8zm121.6 313.1c4.7 4.7 4.7 12.3 0 17L338 377.6c-4.7 4.7-12.3 4.7-17 0L256 312l-65.1 65.6c-4.7 4.7-12.3 4.7-17 0L134.4 338c-4.7-4.7-4.7-12.3 0-17l65.6-65-65.6-65.1c-4.7-4.7-4.7-12.3 0-17l39.6-39.6c4.7-4.7 12.3-4.7 17 0l65 65.7 65.1-65.6c4.7-4.7 12.3-4.7 17 0l39.6 39.6c4.7 4.7 4.7 12.3 0 17L312 256l65.6 65.1z"/></svg>''',
        
        'folder-times': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="currentColor" d="M464 128H272l-54.63-54.63c-6-6-14.14-9.37-22.63-9.37H48C21.49 64 0 85.49 0 112v288c0 26.51 21.49 48 48 48h416c26.51 0 48-21.49 48-48V176c0-26.51-21.49-48-48-48zm-83.48 143.99l-17.98 17.98c-4.69 4.69-12.28 4.69-16.97 0L304 248.41l-41.57 41.56c-4.69 4.69-12.28 4.69-16.97 0l-17.98-17.98c-4.69-4.69-4.69-12.28 0-16.97L269.04 214l-41.56-41.57c-4.69-4.69-4.69-12.28 0-16.97l17.98-17.98c4.69-4.69 12.28-4.69 16.97 0L304 179.04l41.57-41.56c4.69-4.69 12.28-4.69 16.97 0l17.98 17.98c4.69 4.69 4.69 12.28 0 16.97L338.96 214l41.56 41.57c4.69 4.68 4.69 12.28 0 16.97z"/></svg>''',
        
        # 编辑操作图标
        'undo': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="currentColor" d="M255.545 8c-66.269.119-126.438 26.233-170.86 68.685L48.971 40.971C33.851 25.851 8 36.559 8 57.941V192c0 13.255 10.745 24 24 24h134.059c21.382 0 32.09-25.851 16.971-40.971l-41.75-41.75c30.864-28.899 70.801-44.907 113.23-45.273 92.398-.798 170.283 73.977 169.484 169.442C423.236 348.009 349.816 424 256 424c-41.127 0-79.997-14.678-110.63-41.556-4.743-4.161-11.906-3.908-16.368.553L89.34 422.659c-4.872 4.872-4.631 12.815.482 17.433C133.798 479.813 192.074 504 256 504c136.966 0 247.999-111.033 248-247.998C504.001 119.193 392.354 7.755 255.545 8z"/></svg>''',
        
        'redo': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="currentColor" d="M256.455 8c66.269.119 126.437 26.233 170.859 68.685l35.715-35.715C478.149 25.851 504 36.559 504 57.941V192c0 13.255-10.745 24-24 24H345.941c-21.382 0-32.09-25.851-16.971-40.971l41.75-41.75c-30.864-28.899-70.801-44.907-113.23-45.273-92.398-.798-170.283 73.977-169.484 169.442C88.764 348.009 162.184 424 256 424c41.127 0 79.997-14.678 110.629-41.556 4.743-4.161 11.906-3.908 16.368.553l39.662 39.662c4.872 4.872 4.631 12.815-.482 17.433C378.202 479.813 319.926 504 256 504 119.034 504 8.001 392.967 8 256.002 7.999 119.193 119.646 7.755 256.455 8z"/></svg>''',
        
        'trash': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path fill="currentColor" d="M432 32H312l-9.4-18.7A24 24 0 0 0 281.1 0H166.8a23.72 23.72 0 0 0-21.4 13.3L136 32H16A16 16 0 0 0 0 48v32a16 16 0 0 0 16 16h416a16 16 0 0 0 16-16V48a16 16 0 0 0-16-16zM53.2 467a48 48 0 0 0 47.9 45h245.8a48 48 0 0 0 47.9-45L416 128H32z"/></svg>''',
        
        'check-circle': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="currentColor" d="M504 256c0 136.967-111.033 248-248 248S8 392.967 8 256 119.033 8 256 8s248 111.033 248 248zM227.314 387.314l184-184c6.248-6.248 6.248-16.379 0-22.627l-22.627-22.627c-6.248-6.249-16.379-6.249-22.628 0L216 308.118l-70.059-70.059c-6.248-6.248-16.379-6.248-22.628 0l-22.627 22.627c-6.248 6.248-6.248 16.379 0 22.627l104 104c6.249 6.249 16.379 6.249 22.628.001z"/></svg>''',
        
        'copy': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path fill="currentColor" d="M320 448v40c0 13.255-10.745 24-24 24H24c-13.255 0-24-10.745-24-24V120c0-13.255 10.745-24 24-24h72v296c0 30.879 25.121 56 56 56h168zm0-344V0H152c-13.255 0-24 10.745-24 24v368c0 13.255 10.745 24 24 24h272c13.255 0 24-10.745 24-24V128H344c-13.2 0-24-10.8-24-24zm120.971-31.029L375.029 7.029A24 24 0 0 0 358.059 0H352v96h96v-6.059a24 24 0 0 0-7.029-16.97z"/></svg>''',
        
        'paste': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><path fill="currentColor" d="M336 64h-80c0-35.3-28.7-64-64-64s-64 28.7-64 64H48C21.5 64 0 85.5 0 112v352c0 26.5 21.5 48 48 48h288c26.5 0 48-21.5 48-48V112c0-26.5-21.5-48-48-48zM192 40c13.3 0 24 10.7 24 24s-10.7 24-24 24-24-10.7-24-24 10.7-24 24-24zm144 418c0 3.3-2.7 6-6 6H54c-3.3 0-6-2.7-6-6V118c0-3.3 2.7-6 6-6h42v36c0 6.6 5.4 12 12 12h168c6.6 0 12-5.4 12-12v-36h42c3.3 0 6 2.7 6 6z"/></svg>''',
        
        # 搜索图标
        'search': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="currentColor" d="M505 442.7L405.3 343c-4.5-4.5-10.6-7-17-7H372c27.6-35.3 44-79.7 44-128C416 93.1 322.9 0 208 0S0 93.1 0 208s93.1 208 208 208c48.3 0 92.7-16.4 128-44v16.3c0 6.4 2.5 12.5 7 17l99.7 99.7c9.4 9.4 24.6 9.4 33.9 0l28.3-28.3c9.4-9.4 9.4-24.6.1-34zM208 336c-70.7 0-128-57.2-128-128 0-70.7 57.2-128 128-128 70.7 0 128 57.2 128 128 0 70.7-57.2 128-128 128z"/></svg>''',
        
        'exchange': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="currentColor" d="M0 168v-16c0-13.255 10.745-24 24-24h360V80c0-21.367 25.899-32.042 40.971-16.971l80 80c9.372 9.373 9.372 24.569 0 33.941l-80 80C409.956 271.982 384 261.456 384 240v-48H24c-13.255 0-24-10.745-24-24zm488 152H128v-48c0-21.314-25.862-32.08-40.971-16.971l-80 80c-9.372 9.373-9.372 24.569 0 33.941l80 80C102.057 463.997 128 453.437 128 432v-48h360c13.255 0 24-10.745 24-24v-16c0-13.255-10.745-24-24-24z"/></svg>''',
        
        # 文件浏览器图标
        'level-up': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path fill="currentColor" d="M34.9 289.5l-22.2-22.2c-9.4-9.4-9.4-24.6 0-33.9L207 39c9.4-9.4 24.6-9.4 33.9 0l194.3 194.3c9.4 9.4 9.4 24.6 0 33.9L413 289.4c-9.5 9.5-25 9.3-34.3-.4L264 168.6V456c0 13.3-10.7 24-24 24h-32c-13.3 0-24-10.7-24-24V168.6L69.2 289.1c-9.3 9.7-24.8 9.9-34.3.4z"/></svg>''',
        
        'sync': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="currentColor" d="M440.65 12.57l4 82.77A247.16 247.16 0 0 0 255.83 8C134.73 8 33.91 94.92 12.29 209.82A12 12 0 0 0 24.09 224h49.05a12 12 0 0 0 11.67-9.26 175.91 175.91 0 0 1 317-56.94l-101.46-4.86a12 12 0 0 0-12.57 12v47.41a12 12 0 0 0 12 12H500a12 12 0 0 0 12-12V12a12 12 0 0 0-12-12h-47.37a12 12 0 0 0-11.98 12.57zM255.83 432a175.61 175.61 0 0 1-146-77.8l101.8 4.87a12 12 0 0 0 12.57-12v-47.4a12 12 0 0 0-12-12H12a12 12 0 0 0-12 12V500a12 12 0 0 0 12 12h47.35a12 12 0 0 0 12-12.6l-4.15-82.57A247.17 247.17 0 0 0 255.83 504c121.11 0 221.93-86.92 243.55-201.82a12 12 0 0 0-11.8-14.18h-49.05a12 12 0 0 0-11.67 9.26A175.86 175.86 0 0 1 255.83 432z"/></svg>''',
        
        'angle-double-down': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512"><path fill="currentColor" d="M143 256.3L7 120.3c-9.4-9.4-9.4-24.6 0-33.9l22.6-22.6c9.4-9.4 24.6-9.4 33.9 0l96.4 96.4 96.4-96.4c9.4-9.4 24.6-9.4 33.9 0L313 86.3c9.4 9.4 9.4 24.6 0 33.9l-136 136c-9.4 9.5-24.6 9.5-34 .1zm34 192l136-136c9.4-9.4 9.4-24.6 0-33.9l-22.6-22.6c-9.4-9.4-24.6-9.4-33.9 0L160 352.1l-96.4-96.4c-9.4-9.4-24.6-9.4-33.9 0L7 278.3c-9.4 9.4-9.4 24.6 0 33.9l136 136c9.4 9.5 24.6 9.5 34 .1z"/></svg>''',
        
        'angle-double-up': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512"><path fill="currentColor" d="M177 255.7l136 136c9.4 9.4 9.4 24.6 0 33.9l-22.6 22.6c-9.4 9.4-24.6 9.4-33.9 0L160 351.9l-96.4 96.4c-9.4 9.4-24.6 9.4-33.9 0L7 425.7c-9.4-9.4-9.4-24.6 0-33.9l136-136c9.4-9.5 24.6-9.5 34-.1zm-34-192L7 199.7c-9.4 9.4-9.4 24.6 0 33.9l22.6 22.6c9.4 9.4 24.6 9.4 33.9 0l96.4-96.4 96.4 96.4c9.4 9.4 24.6 9.4 33.9 0l22.6-22.6c9.4-9.4 9.4-24.6 0-33.9l-136-136c-9.4-9.5-24.6-9.5-34-.1z"/></svg>''',
        
        # 彩色的"全选+复制"组合图标
        'select-copy': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
            <!-- 背景圆形 -->
            <circle cx="256" cy="256" r="240" fill="#0078d4" opacity="0.15"/>
            <!-- 选择框（蓝色） -->
            <rect x="120" y="120" width="180" height="180" rx="8" fill="none" stroke="#0078d4" stroke-width="20" stroke-dasharray="20,10"/>
            <!-- 对勾（绿色） -->
            <path d="M140 200 L180 240 L260 160" fill="none" stroke="#28a745" stroke-width="20" stroke-linecap="round" stroke-linejoin="round"/>
            <!-- 复制页面（橙色） -->
            <rect x="220" y="220" width="160" height="200" rx="8" fill="#ffffff" stroke="#ff6b35" stroke-width="16"/>
            <rect x="240" y="240" width="120" height="10" rx="4" fill="#ff6b35"/>
            <rect x="240" y="270" width="120" height="10" rx="4" fill="#ff6b35"/>
            <rect x="240" y="300" width="120" height="10" rx="4" fill="#ff6b35"/>
            <rect x="240" y="330" width="90" height="10" rx="4" fill="#ff6b35"/>
        </svg>''',
    }
    
    @staticmethod
    def create_icon(icon_name: str, color: str = "#ffffff", size: int = 32, keep_colors: bool = False) -> QIcon:
        """
        创建SVG图标
        
        Args:
            icon_name: 图标名称
            color: 图标颜色（十六进制格式）
            size: 图标尺寸
            keep_colors: 是否保持原始颜色（用于彩色图标）
            
        Returns:
            QIcon对象
        """
        if icon_name not in IconProvider.SVG_ICONS:
            # 如果图标不存在，返回空图标
            return QIcon()
        
        # 获取SVG数据
        svg_data = IconProvider.SVG_ICONS[icon_name]
        
        # 如果不是彩色图标，则替换颜色
        if not keep_colors:
            svg_data = svg_data.replace('currentColor', color)
        
        # 创建SVG渲染器
        svg_renderer = QSvgRenderer(svg_data.encode('utf-8'))
        
        # 创建像素图
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        # 渲染SVG到像素图
        painter = QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()
        
        return QIcon(pixmap)
    
    @staticmethod
    def get_icon_names():
        """获取所有可用的图标名称"""
        return list(IconProvider.SVG_ICONS.keys())


# 预定义常用图标（白色，适用于深色主题）
class Icons:
    """常用图标集合"""
    
    @staticmethod
    def init_icons(color: str = "#ffffff", size: int = 18):
        """
        初始化图标集合
        
        Args:
            color: 图标颜色
            size: 图标尺寸（默认18×18）
        """
        Icons.FILE_NEW = IconProvider.create_icon('file-new', color, size)
        Icons.FOLDER_OPEN = IconProvider.create_icon('folder-open', color, size)
        Icons.FOLDER = IconProvider.create_icon('folder', color, size)
        Icons.SAVE = IconProvider.create_icon('save', color, size)
        Icons.TIMES_CIRCLE = IconProvider.create_icon('times-circle', color, size)
        Icons.FOLDER_TIMES = IconProvider.create_icon('folder-times', color, size)
        Icons.UNDO = IconProvider.create_icon('undo', color, size)
        Icons.REDO = IconProvider.create_icon('redo', color, size)
        Icons.TRASH = IconProvider.create_icon('trash', color, size)
        Icons.CHECK_CIRCLE = IconProvider.create_icon('check-circle', color, size)
        Icons.COPY = IconProvider.create_icon('copy', color, size)
        Icons.PASTE = IconProvider.create_icon('paste', color, size)
        Icons.SEARCH = IconProvider.create_icon('search', color, size)
        Icons.EXCHANGE = IconProvider.create_icon('exchange', color, size)
        
        # 彩色的"全选+复制"组合图标（保持原始颜色）
        Icons.SELECT_COPY = IconProvider.create_icon('select-copy', color, size, keep_colors=True)
        
        # 文件浏览器图标
        Icons.LEVEL_UP = IconProvider.create_icon('level-up', color, size)
        Icons.SYNC = IconProvider.create_icon('sync', color, size)
        Icons.ANGLE_DOUBLE_DOWN = IconProvider.create_icon('angle-double-down', color, size)
        Icons.ANGLE_DOUBLE_UP = IconProvider.create_icon('angle-double-up', color, size)


