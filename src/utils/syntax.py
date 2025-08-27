"""
语法高亮器 - Chango Editor

主要功能：
- 基于Pygments的语法高亮
- 支持多种编程语言
- 可切换的配色方案
- 实时高亮更新
"""

import re
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt6.QtCore import Qt

try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name, guess_lexer
    from pygments.formatters import NullFormatter
    from pygments.token import Token
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False
    print("警告: Pygments未安装，将使用基础语法高亮")


class SyntaxHighlighter(QSyntaxHighlighter):
    """语法高亮器"""
    
    def __init__(self, document=None):
        super().__init__(document)
        
        # 当前语言
        self.language = 'text'
        
        # Pygments相关
        self.lexer = None
        self.use_pygments = PYGMENTS_AVAILABLE
        
        # 高亮格式
        self.formats = {}
        
        # 初始化格式
        self._init_formats()
        
        # 设置默认语言
        self.set_language('python')
        
        print(f"语法高亮器初始化完成 (Pygments: {PYGMENTS_AVAILABLE})")
    
    def _init_formats(self):
        """初始化高亮格式"""
        # 基础格式
        self.formats = {
            # 关键字
            'keyword': self._create_format(QColor(86, 156, 214), bold=True),
            # 字符串
            'string': self._create_format(QColor(206, 145, 120)),
            # 注释
            'comment': self._create_format(QColor(106, 153, 85), italic=True),
            # 数字
            'number': self._create_format(QColor(181, 206, 168)),
            # 函数
            'function': self._create_format(QColor(220, 220, 170)),
            # 类
            'class': self._create_format(QColor(78, 201, 176)),
            # 操作符
            'operator': self._create_format(QColor(212, 212, 212)),
            # 内置函数
            'builtin': self._create_format(QColor(86, 156, 214)),
            # 错误
            'error': self._create_format(QColor(244, 71, 71)),
            # 装饰器
            'decorator': self._create_format(QColor(255, 198, 109)),
        }
        
        # Pygments token映射
        if PYGMENTS_AVAILABLE:
            self.token_formats = {
                Token.Keyword: self.formats['keyword'],
                Token.Keyword.Constant: self.formats['keyword'],
                Token.Keyword.Declaration: self.formats['keyword'],
                Token.Keyword.Namespace: self.formats['keyword'],
                Token.Keyword.Pseudo: self.formats['keyword'],
                Token.Keyword.Reserved: self.formats['keyword'],
                Token.Keyword.Type: self.formats['keyword'],
                
                Token.String: self.formats['string'],
                Token.String.Char: self.formats['string'],
                Token.String.Doc: self.formats['string'],
                Token.String.Double: self.formats['string'],
                Token.String.Escape: self.formats['string'],
                Token.String.Heredoc: self.formats['string'],
                Token.String.Interpol: self.formats['string'],
                Token.String.Other: self.formats['string'],
                Token.String.Regex: self.formats['string'],
                Token.String.Single: self.formats['string'],
                Token.String.Symbol: self.formats['string'],
                
                Token.Comment: self.formats['comment'],
                Token.Comment.Hashbang: self.formats['comment'],
                Token.Comment.Multiline: self.formats['comment'],
                Token.Comment.Preproc: self.formats['comment'],
                Token.Comment.PreprocFile: self.formats['comment'],
                Token.Comment.Single: self.formats['comment'],
                Token.Comment.Special: self.formats['comment'],
                
                Token.Number: self.formats['number'],
                Token.Number.Bin: self.formats['number'],
                Token.Number.Float: self.formats['number'],
                Token.Number.Hex: self.formats['number'],
                Token.Number.Integer: self.formats['number'],
                Token.Number.Long: self.formats['number'],
                Token.Number.Oct: self.formats['number'],
                
                Token.Name.Function: self.formats['function'],
                Token.Name.Function.Magic: self.formats['function'],
                
                Token.Name.Class: self.formats['class'],
                
                Token.Operator: self.formats['operator'],
                Token.Operator.Word: self.formats['operator'],
                
                Token.Name.Builtin: self.formats['builtin'],
                Token.Name.Builtin.Pseudo: self.formats['builtin'],
                
                Token.Error: self.formats['error'],
                
                Token.Name.Decorator: self.formats['decorator'],
            }
    
    def _create_format(self, color, bold=False, italic=False):
        """创建文本格式"""
        format = QTextCharFormat()
        format.setForeground(color)
        if bold:
            format.setFontWeight(QFont.Weight.Bold)
        if italic:
            format.setFontItalic(True)
        return format
    
    def set_language(self, language):
        """设置高亮语言"""
        self.language = language.lower()
        
        if PYGMENTS_AVAILABLE:
            try:
                # 扩展的语言别名映射
                language_aliases = {
                    'javascript': 'javascript',
                    'js': 'javascript',
                    'typescript': 'typescript',
                    'ts': 'typescript',
                    'csharp': 'csharp',
                    'c#': 'csharp',
                    'cplusplus': 'cpp',
                    'c++': 'cpp',
                    'c': 'c',
                    'h': 'c',
                    'hpp': 'cpp',
                    'java': 'java',
                    'python': 'python',
                    'py': 'python',
                    'pyw': 'python',
                    'html': 'html',
                    'htm': 'html',
                    'css': 'css',
                    'scss': 'scss',
                    'sass': 'sass',
                    'less': 'less',
                    'json': 'json',
                    'xml': 'xml',
                    'yaml': 'yaml',
                    'yml': 'yaml',
                    'markdown': 'markdown',
                    'md': 'markdown',
                    'sql': 'sql',
                    'php': 'php',
                    'go': 'go',
                    'rust': 'rust',
                    'rs': 'rust',
                    'ruby': 'ruby',
                    'rb': 'ruby',
                    'bash': 'bash',
                    'sh': 'bash',
                    'powershell': 'powershell',
                    'ps1': 'powershell',
                    'batch': 'batch',
                    'bat': 'batch',
                    'perl': 'perl',
                    'pl': 'perl',
                    'lua': 'lua',
                    'swift': 'swift',
                    'kotlin': 'kotlin',
                    'kt': 'kotlin',
                    'scala': 'scala',
                    'r': 'r',
                    'matlab': 'matlab',
                    'm': 'matlab',
                }
                
                lexer_name = language_aliases.get(self.language, self.language)
                self.lexer = get_lexer_by_name(lexer_name)
                print(f"设置Pygments词法分析器: {lexer_name}")
            except Exception as e:
                print(f"无法设置Pygments词法分析器 {self.language}: {e}")
                self.lexer = None
                # 降级到正则表达式高亮
                print("降级使用正则表达式高亮")
        
        # 重新高亮整个文档
        self.rehighlight()
    
    def highlightBlock(self, text):
        """高亮代码块"""
        if not text.strip():
            return
        
        if self.use_pygments and self.lexer:
            self._highlight_with_pygments(text)
        else:
            self._highlight_with_regex(text)
    
    def _highlight_with_pygments(self, text):
        """使用Pygments进行高亮"""
        try:
            # 获取tokens
            tokens = list(self.lexer.get_tokens(text))
            
            # 应用高亮
            start = 0
            for token_type, value in tokens:
                if value.strip():  # 忽略空白字符
                    length = len(value)
                    format = self.token_formats.get(token_type)
                    
                    if format:
                        self.setFormat(start, length, format)
                
                start += len(value)
                
        except Exception as e:
            print(f"Pygments高亮失败: {e}")
            self._highlight_with_regex(text)
    
    def _highlight_with_regex(self, text):
        """使用正则表达式进行基础高亮"""
        language = self.language.lower()
        
        if language in ['python', 'py', 'pyw']:
            self._highlight_python(text)
        elif language in ['javascript', 'js']:
            self._highlight_javascript(text)
        elif language in ['typescript', 'ts']:
            self._highlight_typescript(text)
        elif language in ['html', 'htm']:
            self._highlight_html(text)
        elif language in ['css', 'scss', 'sass', 'less']:
            self._highlight_css(text)
        elif language in ['java']:
            self._highlight_java(text)
        elif language in ['c', 'h']:
            self._highlight_c(text)
        elif language in ['cpp', 'c++', 'hpp', 'cplusplus']:
            self._highlight_cpp(text)
        elif language in ['csharp', 'c#']:
            self._highlight_csharp(text)
        elif language in ['json']:
            self._highlight_json(text)
        elif language in ['xml']:
            self._highlight_xml(text)
        elif language in ['markdown', 'md']:
            self._highlight_markdown(text)
        elif language in ['sql']:
            self._highlight_sql(text)
        elif language in ['bash', 'sh']:
            self._highlight_bash(text)
        else:
            self._highlight_generic(text)
    
    def _highlight_python(self, text):
        """Python语法高亮"""
        # 关键字
        keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'exec', 'finally', 'for',
            'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
            'not', 'or', 'pass', 'print', 'raise', 'return', 'try',
            'while', 'with', 'yield', 'True', 'False', 'None'
        ]
        
        # 高亮关键字
        for keyword in keywords:
            pattern = r'\b' + keyword + r'\b'
            for match in re.finditer(pattern, text):
                self.setFormat(match.start(), match.end() - match.start(), 
                             self.formats['keyword'])
        
        # 高亮字符串
        string_patterns = [
            r'""".*?"""',  # 三引号字符串
            r"'''.*?'''",  # 三引号字符串
            r'"[^"\\]*(\\.[^"\\]*)*"',  # 双引号字符串
            r"'[^'\\]*(\\.[^'\\]*)*'"   # 单引号字符串
        ]
        
        for pattern in string_patterns:
            for match in re.finditer(pattern, text, re.DOTALL):
                self.setFormat(match.start(), match.end() - match.start(), 
                             self.formats['string'])
        
        # 高亮注释
        comment_pattern = r'#.*$'
        for match in re.finditer(comment_pattern, text, re.MULTILINE):
            self.setFormat(match.start(), match.end() - match.start(), 
                         self.formats['comment'])
        
        # 高亮数字
        number_pattern = r'\b\d+\.?\d*\b'
        for match in re.finditer(number_pattern, text):
            self.setFormat(match.start(), match.end() - match.start(), 
                         self.formats['number'])
        
        # 高亮函数定义
        function_pattern = r'\bdef\s+(\w+)'
        for match in re.finditer(function_pattern, text):
            self.setFormat(match.start(1), match.end(1) - match.start(1), 
                         self.formats['function'])
        
        # 高亮类定义
        class_pattern = r'\bclass\s+(\w+)'
        for match in re.finditer(class_pattern, text):
            self.setFormat(match.start(1), match.end(1) - match.start(1), 
                         self.formats['class'])
        
        # 高亮装饰器
        decorator_pattern = r'@\w+'
        for match in re.finditer(decorator_pattern, text):
            self.setFormat(match.start(), match.end() - match.start(), 
                         self.formats['decorator'])
    
    def _highlight_javascript(self, text):
        """JavaScript语法高亮"""
        # 关键字
        keywords = [
            'break', 'case', 'catch', 'class', 'const', 'continue', 'debugger',
            'default', 'delete', 'do', 'else', 'export', 'extends', 'finally',
            'for', 'function', 'if', 'import', 'in', 'instanceof', 'let', 'new',
            'return', 'super', 'switch', 'this', 'throw', 'try', 'typeof', 'var',
            'void', 'while', 'with', 'yield', 'true', 'false', 'null', 'undefined'
        ]
        
        # 高亮关键字
        for keyword in keywords:
            pattern = r'\b' + keyword + r'\b'
            for match in re.finditer(pattern, text):
                self.setFormat(match.start(), match.end() - match.start(), 
                             self.formats['keyword'])
        
        # 高亮字符串
        string_patterns = [
            r'`[^`\\]*(\\.[^`\\]*)*`',   # 模板字符串
            r'"[^"\\]*(\\.[^"\\]*)*"',  # 双引号字符串
            r"'[^'\\]*(\\.[^'\\]*)*'"   # 单引号字符串
        ]
        
        for pattern in string_patterns:
            for match in re.finditer(pattern, text, re.DOTALL):
                self.setFormat(match.start(), match.end() - match.start(), 
                             self.formats['string'])
        
        # 高亮注释
        comment_patterns = [
            r'//.*$',        # 单行注释
            r'/\*.*?\*/'     # 多行注释
        ]
        
        for pattern in comment_patterns:
            for match in re.finditer(pattern, text, re.MULTILINE | re.DOTALL):
                self.setFormat(match.start(), match.end() - match.start(), 
                             self.formats['comment'])
        
        # 高亮数字
        number_pattern = r'\b\d+\.?\d*\b'
        for match in re.finditer(number_pattern, text):
            self.setFormat(match.start(), match.end() - match.start(), 
                         self.formats['number'])
    
    def _highlight_html(self, text):
        """HTML语法高亮"""
        # HTML标签
        tag_pattern = r'<[^>]+>'
        for match in re.finditer(tag_pattern, text):
            self.setFormat(match.start(), match.end() - match.start(), 
                         self.formats['keyword'])
        
        # HTML注释
        comment_pattern = r'<!--.*?-->'
        for match in re.finditer(comment_pattern, text, re.DOTALL):
            self.setFormat(match.start(), match.end() - match.start(), 
                         self.formats['comment'])
    
    def _highlight_css(self, text):
        """CSS语法高亮"""
        # CSS选择器
        selector_pattern = r'[#.]?[a-zA-Z][a-zA-Z0-9_-]*\s*(?=\{)'
        for match in re.finditer(selector_pattern, text):
            self.setFormat(match.start(), match.end() - match.start(), 
                         self.formats['class'])
        
        # CSS属性
        property_pattern = r'[a-zA-Z-]+\s*(?=:)'
        for match in re.finditer(property_pattern, text):
            self.setFormat(match.start(), match.end() - match.start(), 
                         self.formats['keyword'])
        
        # CSS注释
        comment_pattern = r'/\*.*?\*/'
        for match in re.finditer(comment_pattern, text, re.DOTALL):
            self.setFormat(match.start(), match.end() - match.start(), 
                         self.formats['comment'])
    
    def _highlight_typescript(self, text):
        """TypeScript语法高亮"""
        # TypeScript关键字
        keywords = [
            'abstract', 'any', 'as', 'break', 'case', 'catch', 'class', 'const', 
            'continue', 'debugger', 'declare', 'default', 'delete', 'do', 'else', 
            'enum', 'export', 'extends', 'false', 'finally', 'for', 'from', 
            'function', 'get', 'if', 'implements', 'import', 'in', 'instanceof', 
            'interface', 'is', 'keyof', 'let', 'module', 'namespace', 'never', 
            'new', 'null', 'number', 'object', 'package', 'private', 'protected', 
            'public', 'readonly', 'return', 'set', 'static', 'string', 'super', 
            'switch', 'this', 'throw', 'true', 'try', 'type', 'typeof', 'undefined', 
            'var', 'void', 'while', 'with', 'yield'
        ]
        
        self._highlight_keywords(text, keywords)
        self._highlight_strings(text)
        self._highlight_comments(text, [r'//.*$', r'/\*.*?\*/'])
        self._highlight_numbers(text)
    
    def _highlight_java(self, text):
        """Java语法高亮"""
        keywords = [
            'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 
            'char', 'class', 'const', 'continue', 'default', 'do', 'double', 
            'else', 'enum', 'extends', 'final', 'finally', 'float', 'for', 
            'goto', 'if', 'implements', 'import', 'instanceof', 'int', 'interface', 
            'long', 'native', 'new', 'package', 'private', 'protected', 'public', 
            'return', 'short', 'static', 'strictfp', 'super', 'switch', 
            'synchronized', 'this', 'throw', 'throws', 'transient', 'try', 
            'void', 'volatile', 'while', 'true', 'false', 'null'
        ]
        
        self._highlight_keywords(text, keywords)
        self._highlight_strings(text)
        self._highlight_comments(text, [r'//.*$', r'/\*.*?\*/'])
        self._highlight_numbers(text)
    
    def _highlight_c(self, text):
        """C语言语法高亮"""
        keywords = [
            'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 
            'do', 'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 
            'if', 'int', 'long', 'register', 'return', 'short', 'signed', 
            'sizeof', 'static', 'struct', 'switch', 'typedef', 'union', 
            'unsigned', 'void', 'volatile', 'while'
        ]
        
        self._highlight_keywords(text, keywords)
        self._highlight_strings(text)
        self._highlight_comments(text, [r'//.*$', r'/\*.*?\*/'])
        self._highlight_numbers(text)
    
    def _highlight_cpp(self, text):
        """C++语法高亮"""
        keywords = [
            'alignas', 'alignof', 'and', 'and_eq', 'asm', 'auto', 'bitand', 
            'bitor', 'bool', 'break', 'case', 'catch', 'char', 'char16_t', 
            'char32_t', 'class', 'compl', 'const', 'constexpr', 'const_cast', 
            'continue', 'decltype', 'default', 'delete', 'do', 'double', 
            'dynamic_cast', 'else', 'enum', 'explicit', 'export', 'extern', 
            'false', 'float', 'for', 'friend', 'goto', 'if', 'inline', 'int', 
            'long', 'mutable', 'namespace', 'new', 'noexcept', 'not', 'not_eq', 
            'nullptr', 'operator', 'or', 'or_eq', 'private', 'protected', 
            'public', 'register', 'reinterpret_cast', 'return', 'short', 
            'signed', 'sizeof', 'static', 'static_assert', 'static_cast', 
            'struct', 'switch', 'template', 'this', 'thread_local', 'throw', 
            'true', 'try', 'typedef', 'typeid', 'typename', 'union', 'unsigned', 
            'using', 'virtual', 'void', 'volatile', 'wchar_t', 'while', 'xor', 'xor_eq'
        ]
        
        self._highlight_keywords(text, keywords)
        self._highlight_strings(text)
        self._highlight_comments(text, [r'//.*$', r'/\*.*?\*/'])
        self._highlight_numbers(text)
    
    def _highlight_csharp(self, text):
        """C#语法高亮"""
        keywords = [
            'abstract', 'as', 'base', 'bool', 'break', 'byte', 'case', 'catch', 
            'char', 'checked', 'class', 'const', 'continue', 'decimal', 'default', 
            'delegate', 'do', 'double', 'else', 'enum', 'event', 'explicit', 
            'extern', 'false', 'finally', 'fixed', 'float', 'for', 'foreach', 
            'goto', 'if', 'implicit', 'in', 'int', 'interface', 'internal', 
            'is', 'lock', 'long', 'namespace', 'new', 'null', 'object', 
            'operator', 'out', 'override', 'params', 'private', 'protected', 
            'public', 'readonly', 'ref', 'return', 'sbyte', 'sealed', 'short', 
            'sizeof', 'stackalloc', 'static', 'string', 'struct', 'switch', 
            'this', 'throw', 'true', 'try', 'typeof', 'uint', 'ulong', 
            'unchecked', 'unsafe', 'ushort', 'using', 'virtual', 'void', 
            'volatile', 'while'
        ]
        
        self._highlight_keywords(text, keywords)
        self._highlight_strings(text)
        self._highlight_comments(text, [r'//.*$', r'/\*.*?\*/'])
        self._highlight_numbers(text)
    
    def _highlight_json(self, text):
        """JSON语法高亮"""
        # JSON字符串
        string_pattern = r'"[^"\\]*(\\.[^"\\]*)*"'
        for match in re.finditer(string_pattern, text):
            self.setFormat(match.start(), match.end() - match.start(), 
                         self.formats['string'])
        
        # JSON数字
        number_pattern = r'\b-?\d+\.?\d*([eE][+-]?\d+)?\b'
        for match in re.finditer(number_pattern, text):
            self.setFormat(match.start(), match.end() - match.start(), 
                         self.formats['number'])
        
        # JSON关键字
        keywords = ['true', 'false', 'null']
        self._highlight_keywords(text, keywords)
    
    def _highlight_xml(self, text):
        """XML语法高亮"""
        # XML标签
        tag_pattern = r'<[^>]+>'
        for match in re.finditer(tag_pattern, text):
            self.setFormat(match.start(), match.end() - match.start(), 
                         self.formats['keyword'])
        
        # XML注释
        comment_pattern = r'<!--.*?-->'
        for match in re.finditer(comment_pattern, text, re.DOTALL):
            self.setFormat(match.start(), match.end() - match.start(), 
                         self.formats['comment'])
    
    def _highlight_markdown(self, text):
        """Markdown语法高亮"""
        # 标题
        header_pattern = r'^#{1,6}\s+.*$'
        for match in re.finditer(header_pattern, text, re.MULTILINE):
            self.setFormat(match.start(), match.end() - match.start(), 
                         self.formats['keyword'])
        
        # 代码块
        code_pattern = r'`[^`]+`'
        for match in re.finditer(code_pattern, text):
            self.setFormat(match.start(), match.end() - match.start(), 
                         self.formats['string'])
        
        # 粗体
        bold_pattern = r'\*\*[^*]+\*\*'
        for match in re.finditer(bold_pattern, text):
            self.setFormat(match.start(), match.end() - match.start(), 
                         self.formats['function'])
    
    def _highlight_sql(self, text):
        """SQL语法高亮"""
        keywords = [
            'SELECT', 'FROM', 'WHERE', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 
            'DROP', 'ALTER', 'TABLE', 'INDEX', 'DATABASE', 'VIEW', 'PROCEDURE', 
            'FUNCTION', 'TRIGGER', 'JOIN', 'INNER', 'LEFT', 'RIGHT', 'FULL', 
            'OUTER', 'ON', 'AS', 'AND', 'OR', 'NOT', 'NULL', 'IS', 'IN', 
            'BETWEEN', 'LIKE', 'ORDER', 'BY', 'GROUP', 'HAVING', 'LIMIT', 
            'OFFSET', 'DISTINCT', 'COUNT', 'SUM', 'AVG', 'MAX', 'MIN'
        ]
        
        # SQL不区分大小写
        for keyword in keywords:
            pattern = r'\b' + keyword + r'\b'
            for match in re.finditer(pattern, text, re.IGNORECASE):
                self.setFormat(match.start(), match.end() - match.start(), 
                             self.formats['keyword'])
        
        self._highlight_strings(text)
        self._highlight_comments(text, [r'--.*$', r'/\*.*?\*/'])
        self._highlight_numbers(text)
    
    def _highlight_bash(self, text):
        """Bash语法高亮"""
        keywords = [
            'if', 'then', 'else', 'elif', 'fi', 'case', 'esac', 'for', 'in', 
            'while', 'until', 'do', 'done', 'function', 'return', 'local', 
            'export', 'unset', 'readonly', 'declare', 'typeset', 'echo', 
            'printf', 'read', 'test', 'true', 'false'
        ]
        
        self._highlight_keywords(text, keywords)
        self._highlight_strings(text)
        self._highlight_comments(text, [r'#.*$'])
        self._highlight_numbers(text)
    
    # 辅助方法
    def _highlight_keywords(self, text, keywords):
        """高亮关键字"""
        for keyword in keywords:
            pattern = r'\b' + keyword + r'\b'
            for match in re.finditer(pattern, text):
                self.setFormat(match.start(), match.end() - match.start(), 
                             self.formats['keyword'])
    
    def _highlight_strings(self, text):
        """高亮字符串"""
        string_patterns = [
            r'"[^"\\]*(\\.[^"\\]*)*"',  # 双引号字符串
            r"'[^'\\]*(\\.[^'\\]*)*'"   # 单引号字符串
        ]
        
        for pattern in string_patterns:
            for match in re.finditer(pattern, text):
                self.setFormat(match.start(), match.end() - match.start(), 
                             self.formats['string'])
    
    def _highlight_comments(self, text, patterns):
        """高亮注释"""
        for pattern in patterns:
            flags = re.MULTILINE
            if r'\*' in pattern:  # 多行注释
                flags |= re.DOTALL
            
            for match in re.finditer(pattern, text, flags):
                self.setFormat(match.start(), match.end() - match.start(), 
                             self.formats['comment'])
    
    def _highlight_numbers(self, text):
        """高亮数字"""
        number_pattern = r'\b\d+\.?\d*\b'
        for match in re.finditer(number_pattern, text):
            self.setFormat(match.start(), match.end() - match.start(), 
                         self.formats['number'])
    
    def _highlight_generic(self, text):
        """通用语法高亮"""
        # 高亮字符串（通用）
        self._highlight_strings(text)
        # 高亮数字
        self._highlight_numbers(text)
    
    def set_color_scheme(self, scheme='dark'):
        """设置配色方案"""
        if scheme == 'dark':
            # 暗色主题（默认）
            self.formats['keyword'] = self._create_format(QColor(86, 156, 214), bold=True)
            self.formats['string'] = self._create_format(QColor(206, 145, 120))
            self.formats['comment'] = self._create_format(QColor(106, 153, 85), italic=True)
            self.formats['number'] = self._create_format(QColor(181, 206, 168))
            self.formats['function'] = self._create_format(QColor(220, 220, 170))
            self.formats['class'] = self._create_format(QColor(78, 201, 176))
            self.formats['operator'] = self._create_format(QColor(212, 212, 212))
            self.formats['builtin'] = self._create_format(QColor(86, 156, 214))
            self.formats['error'] = self._create_format(QColor(244, 71, 71))
            self.formats['decorator'] = self._create_format(QColor(255, 198, 109))
        elif scheme == 'light':
            # 亮色主题
            self.formats['keyword'] = self._create_format(QColor(0, 0, 255), bold=True)
            self.formats['string'] = self._create_format(QColor(163, 21, 21))
            self.formats['comment'] = self._create_format(QColor(0, 128, 0), italic=True)
            self.formats['number'] = self._create_format(QColor(9, 134, 88))
            self.formats['function'] = self._create_format(QColor(121, 94, 38))
            self.formats['class'] = self._create_format(QColor(43, 145, 175))
            self.formats['operator'] = self._create_format(QColor(0, 0, 0))
            self.formats['builtin'] = self._create_format(QColor(0, 0, 255))
            self.formats['error'] = self._create_format(QColor(255, 0, 0))
            self.formats['decorator'] = self._create_format(QColor(128, 128, 0))
        
        # 更新Pygments映射
        if PYGMENTS_AVAILABLE:
            self._init_formats()
        
        # 重新高亮
        self.rehighlight()
        print(f"设置配色方案: {scheme}")
