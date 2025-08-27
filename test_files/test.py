#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chango Editor Python测试文件
展示Python语言的现代特性和最佳实践

作者: Chango Team
创建时间: 2024-01-15
版本: 1.0
"""

import asyncio
import logging
import json
import os
import sys
import time
import threading
from abc import ABC, abstractmethod
from collections import defaultdict, namedtuple
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from functools import wraps, lru_cache, singledispatch
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Protocol, TypeVar, Generic
from itertools import chain, combinations
import weakref

# 常量定义
APP_NAME = "Chango Editor"
APP_VERSION = "0.1.0"
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
SUPPORTED_EXTENSIONS = ['.py', '.js', '.ts', '.java', '.cpp', '.cs', '.go', '.rs', '.php', '.rb']

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chango_editor.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# 枚举类型
class Language(Enum):
    """编程语言枚举"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    CPP = "cpp"
    CSHARP = "csharp"
    GO = "go"
    RUST = "rust"
    PHP = "php"
    RUBY = "ruby"
    UNKNOWN = "unknown"
    
    @classmethod
    def from_extension(cls, extension: str) -> 'Language':
        """从文件扩展名获取语言类型"""
        extension_map = {
            '.py': cls.PYTHON,
            '.pyw': cls.PYTHON,
            '.js': cls.JAVASCRIPT,
            '.jsx': cls.JAVASCRIPT,
            '.ts': cls.TYPESCRIPT,
            '.tsx': cls.TYPESCRIPT,
            '.java': cls.JAVA,
            '.cpp': cls.CPP,
            '.cxx': cls.CPP,
            '.cc': cls.CPP,
            '.cs': cls.CSHARP,
            '.go': cls.GO,
            '.rs': cls.RUST,
            '.php': cls.PHP,
            '.rb': cls.RUBY,
        }
        return extension_map.get(extension.lower(), cls.UNKNOWN)
    
    def get_keywords(self) -> List[str]:
        """获取语言关键字"""
        keywords_map = {
            self.PYTHON: ['def', 'class', 'if', 'else', 'elif', 'for', 'while', 'try', 
                         'except', 'finally', 'import', 'from', 'as', 'with', 'lambda', 
                         'yield', 'return', 'pass', 'break', 'continue', 'async', 'await'],
            self.JAVASCRIPT: ['var', 'let', 'const', 'function', 'class', 'if', 'else',
                             'for', 'while', 'do', 'switch', 'case', 'default', 'try',
                             'catch', 'finally', 'return', 'break', 'continue', 'throw'],
            # 其他语言的关键字...
        }
        return keywords_map.get(self, [])

class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()

# 数据类
@dataclass
class FileInfo:
    """文件信息数据类"""
    path: Path
    name: str
    size: int
    lines: int
    language: Language
    encoding: str = "utf-8"
    checksum: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """后初始化处理"""
        if not self.checksum:
            self.checksum = self._calculate_checksum()
    
    def _calculate_checksum(self) -> str:
        """计算文件校验和"""
        import hashlib
        try:
            with open(self.path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            logger.warning(f"无法计算校验和: {e}")
            return "unknown"
    
    @classmethod
    def from_path(cls, file_path: Union[str, Path]) -> 'FileInfo':
        """从文件路径创建FileInfo实例"""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {path}")
        
        if not path.is_file():
            raise ValueError(f"路径不是文件: {path}")
        
        stat = path.stat()
        language = Language.from_extension(path.suffix)
        
        # 计算行数
        try:
            with open(path, 'r', encoding='utf-8') as f:
                lines = sum(1 for _ in f)
        except Exception:
            lines = 0
        
        return cls(
            path=path,
            name=path.name,
            size=stat.st_size,
            lines=lines,
            language=language,
            created_at=datetime.fromtimestamp(stat.st_ctime),
            modified_at=datetime.fromtimestamp(stat.st_mtime)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'path': str(self.path),
            'name': self.name,
            'size': self.size,
            'lines': self.lines,
            'language': self.language.value,
            'encoding': self.encoding,
            'checksum': self.checksum,
            'created_at': self.created_at.isoformat(),
            'modified_at': self.modified_at.isoformat(),
        }

# 命名元组
ProjectStats = namedtuple('ProjectStats', ['total_files', 'total_lines', 'total_size', 'languages'])

# 类型变量和泛型
T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

class Repository(Generic[T], ABC):
    """通用仓库抽象基类"""
    
    @abstractmethod
    def save(self, item: T) -> None:
        """保存项目"""
        pass
    
    @abstractmethod
    def find_by_id(self, item_id: str) -> Optional[T]:
        """根据ID查找项目"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[T]:
        """查找所有项目"""
        pass
    
    @abstractmethod
    def delete(self, item_id: str) -> bool:
        """删除项目"""
        pass

# 协议（Protocol）
class Processable(Protocol):
    """可处理协议"""
    
    def process(self) -> Any:
        """处理方法"""
        ...

# 自定义异常
class ChangoEditorError(Exception):
    """Chango Editor基础异常"""
    
    def __init__(self, message: str, error_code: int = 0, context: Optional[Dict] = None):
        super().__init__(message)
        self.error_code = error_code
        self.context = context or {}

class FileProcessingError(ChangoEditorError):
    """文件处理异常"""
    pass

class ValidationError(ChangoEditorError):
    """验证异常"""
    pass

# 装饰器
def timing_decorator(func):
    """计时装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            end_time = time.time()
            logger.info(f"{func.__name__} 执行时间: {end_time - start_time:.4f}秒")
    return wrapper

def retry(max_attempts: int = 3, delay: float = 1.0):
    """重试装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    logger.warning(f"{func.__name__} 第{attempt + 1}次尝试失败: {e}")
                    time.sleep(delay)
        return wrapper
    return decorator

def validate_file_size(max_size: int = MAX_FILE_SIZE):
    """文件大小验证装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(self, file_path: Path, *args, **kwargs):
            if file_path.stat().st_size > max_size:
                raise ValidationError(f"文件过大: {file_path} ({file_path.stat().st_size} bytes)")
            return func(self, file_path, *args, **kwargs)
        return wrapper
    return decorator

# 上下文管理器
@contextmanager
def file_lock(file_path: Path):
    """文件锁上下文管理器"""
    lock_file = file_path.with_suffix('.lock')
    try:
        if lock_file.exists():
            raise FileProcessingError(f"文件被锁定: {file_path}")
        lock_file.touch()
        logger.debug(f"获取文件锁: {file_path}")
        yield
    finally:
        if lock_file.exists():
            lock_file.unlink()
        logger.debug(f"释放文件锁: {file_path}")

@contextmanager
def temp_directory():
    """临时目录上下文管理器"""
    import tempfile
    import shutil
    
    temp_dir = Path(tempfile.mkdtemp())
    try:
        logger.debug(f"创建临时目录: {temp_dir}")
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir)
        logger.debug(f"删除临时目录: {temp_dir}")

# 主要类定义
class Task(ABC):
    """任务抽象基类"""
    
    def __init__(self, task_id: str, title: str):
        self.id = task_id
        self.title = title
        self.status = TaskStatus.PENDING
        self.created_at = datetime.now()
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.error: Optional[str] = None
        self._observers: List[weakref.ref] = []
    
    def add_observer(self, observer):
        """添加观察者"""
        self._observers.append(weakref.ref(observer))
    
    def notify_observers(self, event: str, **kwargs):
        """通知观察者"""
        for observer_ref in self._observers[:]:  # 复制列表以避免迭代时修改
            observer = observer_ref()
            if observer is None:
                self._observers.remove(observer_ref)
            else:
                if hasattr(observer, 'on_task_event'):
                    observer.on_task_event(self, event, **kwargs)
    
    @abstractmethod
    async def execute(self) -> Any:
        """执行任务"""
        pass
    
    async def run(self) -> Any:
        """运行任务"""
        try:
            self.status = TaskStatus.RUNNING
            self.started_at = datetime.now()
            self.notify_observers('started')
            
            result = await self.execute()
            
            self.status = TaskStatus.COMPLETED
            self.completed_at = datetime.now()
            self.notify_observers('completed', result=result)
            
            return result
            
        except Exception as e:
            self.status = TaskStatus.FAILED
            self.completed_at = datetime.now()
            self.error = str(e)
            self.notify_observers('failed', error=e)
            logger.error(f"任务执行失败: {self.title} - {e}")
            raise
    
    def cancel(self):
        """取消任务"""
        self.status = TaskStatus.CANCELLED
        self.completed_at = datetime.now()
        self.notify_observers('cancelled')
    
    @property
    def duration(self) -> Optional[timedelta]:
        """获取执行时长"""
        if self.started_at and self.completed_at:
            return self.completed_at - self.started_at
        return None

class FileProcessingTask(Task):
    """文件处理任务"""
    
    def __init__(self, task_id: str, file_info: FileInfo):
        super().__init__(task_id, f"处理文件: {file_info.name}")
        self.file_info = file_info
    
    @timing_decorator
    @retry(max_attempts=3)
    async def execute(self) -> Dict[str, Any]:
        """执行文件处理"""
        logger.info(f"开始处理文件: {self.file_info.path}")
        
        # 模拟文件处理过程
        await asyncio.sleep(0.1)  # 模拟I/O操作
        
        # 分析文件内容
        analysis_result = await self._analyze_file()
        
        logger.info(f"文件处理完成: {self.file_info.path}")
        return {
            'file_info': self.file_info.to_dict(),
            'analysis': analysis_result
        }
    
    async def _analyze_file(self) -> Dict[str, Any]:
        """分析文件"""
        try:
            with open(self.file_info.path, 'r', encoding=self.file_info.encoding) as f:
                content = f.read()
            
            # 简单的代码分析
            keywords = self.file_info.language.get_keywords()
            keyword_count = sum(content.count(keyword) for keyword in keywords)
            
            return {
                'char_count': len(content),
                'word_count': len(content.split()),
                'keyword_count': keyword_count,
                'has_main_function': 'def main(' in content or 'function main(' in content,
                'imports_count': content.count('import ') + content.count('from ') + content.count('#include'),
            }
        except Exception as e:
            logger.warning(f"文件分析失败: {e}")
            return {'error': str(e)}

class Project:
    """项目类"""
    
    def __init__(self, name: str, description: str, path: Path):
        self.id = self._generate_id()
        self.name = name
        self.description = description
        self.path = Path(path)
        self.files: Dict[str, FileInfo] = {}
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self._lock = threading.RLock()
    
    def _generate_id(self) -> str:
        """生成唯一ID"""
        import uuid
        return str(uuid.uuid4())
    
    @validate_file_size()
    def add_file(self, file_path: Path) -> FileInfo:
        """添加文件到项目"""
        with self._lock:
            try:
                file_info = FileInfo.from_path(file_path)
                self.files[file_info.path.name] = file_info
                self.updated_at = datetime.now()
                logger.info(f"添加文件到项目: {file_info.name}")
                return file_info
            except Exception as e:
                raise FileProcessingError(f"添加文件失败: {e}")
    
    def remove_file(self, filename: str) -> bool:
        """从项目中移除文件"""
        with self._lock:
            if filename in self.files:
                del self.files[filename]
                self.updated_at = datetime.now()
                logger.info(f"从项目中移除文件: {filename}")
                return True
            return False
    
    def get_file(self, filename: str) -> Optional[FileInfo]:
        """获取文件信息"""
        return self.files.get(filename)
    
    def get_all_files(self) -> List[FileInfo]:
        """获取所有文件"""
        return list(self.files.values())
    
    def scan_directory(self, directory: Optional[Path] = None) -> int:
        """扫描目录中的文件"""
        scan_path = directory or self.path
        if not scan_path.exists():
            raise FileNotFoundError(f"目录不存在: {scan_path}")
        
        count = 0
        for file_path in scan_path.rglob("*"):
            if file_path.is_file() and file_path.suffix in SUPPORTED_EXTENSIONS:
                try:
                    self.add_file(file_path)
                    count += 1
                except Exception as e:
                    logger.warning(f"跳过文件 {file_path}: {e}")
        
        logger.info(f"扫描完成，找到 {count} 个文件")
        return count
    
    def get_statistics(self) -> ProjectStats:
        """获取项目统计信息"""
        files = self.get_all_files()
        total_files = len(files)
        total_lines = sum(f.lines for f in files)
        total_size = sum(f.size for f in files)
        
        # 按语言分组
        languages = defaultdict(int)
        for file_info in files:
            languages[file_info.language.value] += 1
        
        return ProjectStats(total_files, total_lines, total_size, dict(languages))
    
    def search_files(self, query: str) -> List[FileInfo]:
        """搜索文件"""
        query = query.lower()
        results = []
        
        for file_info in self.files.values():
            if (query in file_info.name.lower() or 
                query in str(file_info.path).lower()):
                results.append(file_info)
        
        return results
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'path': str(self.path),
            'files_count': len(self.files),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'statistics': self.get_statistics()._asdict()
        }

class TaskManager:
    """任务管理器"""
    
    def __init__(self, max_workers: int = 4):
        self.tasks: Dict[str, Task] = {}
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self._running_tasks: set = set()
        self._lock = threading.Lock()
    
    def add_task(self, task: Task) -> str:
        """添加任务"""
        with self._lock:
            self.tasks[task.id] = task
            logger.info(f"添加任务: {task.title}")
            return task.id
    
    async def execute_task(self, task_id: str) -> Any:
        """执行单个任务"""
        task = self.tasks.get(task_id)
        if not task:
            raise ValueError(f"任务不存在: {task_id}")
        
        if task.status != TaskStatus.PENDING:
            raise ValueError(f"任务状态不正确: {task.status}")
        
        with self._lock:
            self._running_tasks.add(task_id)
        
        try:
            result = await task.run()
            return result
        finally:
            with self._lock:
                self._running_tasks.discard(task_id)
    
    async def execute_all(self) -> List[Any]:
        """执行所有待处理任务"""
        pending_tasks = [
            task for task in self.tasks.values() 
            if task.status == TaskStatus.PENDING
        ]
        
        if not pending_tasks:
            logger.info("没有待处理的任务")
            return []
        
        logger.info(f"开始执行 {len(pending_tasks)} 个任务")
        
        # 创建协程列表
        coroutines = [self.execute_task(task.id) for task in pending_tasks]
        
        # 并发执行
        results = await asyncio.gather(*coroutines, return_exceptions=True)
        
        # 处理结果
        successful_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"任务执行失败: {pending_tasks[i].title} - {result}")
            else:
                successful_results.append(result)
        
        logger.info(f"任务执行完成，成功: {len(successful_results)}, 失败: {len(results) - len(successful_results)}")
        return successful_results
    
    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """获取任务状态"""
        task = self.tasks.get(task_id)
        return task.status if task else None
    
    def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        task = self.tasks.get(task_id)
        if task and task.status in (TaskStatus.PENDING, TaskStatus.RUNNING):
            task.cancel()
            return True
        return False
    
    def get_statistics(self) -> Dict[str, int]:
        """获取任务统计"""
        stats = defaultdict(int)
        for task in self.tasks.values():
            stats[task.status.name.lower()] += 1
        
        stats['total'] = len(self.tasks)
        stats['running'] = len(self._running_tasks)
        return dict(stats)
    
    def cleanup_completed_tasks(self) -> int:
        """清理已完成的任务"""
        completed_statuses = {TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED}
        to_remove = [
            task_id for task_id, task in self.tasks.items()
            if task.status in completed_statuses
        ]
        
        for task_id in to_remove:
            del self.tasks[task_id]
        
        logger.info(f"清理了 {len(to_remove)} 个已完成的任务")
        return len(to_remove)

# 单例模式的配置管理器
class ConfigManager:
    """配置管理器（单例模式）"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized') or not self._initialized:
            self.config = {
                'app_name': APP_NAME,
                'app_version': APP_VERSION,
                'max_file_size': MAX_FILE_SIZE,
                'supported_extensions': SUPPORTED_EXTENSIONS,
                'log_level': 'INFO',
                'theme': 'dark',
                'auto_save': True,
                'auto_save_interval': 300,  # 5分钟
            }
            self._initialized = True
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """设置配置值"""
        self.config[key] = value
        logger.debug(f"配置更新: {key} = {value}")
    
    def load_from_file(self, config_path: Path) -> None:
        """从文件加载配置"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                file_config = json.load(f)
            self.config.update(file_config)
            logger.info(f"从文件加载配置: {config_path}")
        except Exception as e:
            logger.warning(f"加载配置文件失败: {e}")
    
    def save_to_file(self, config_path: Path) -> None:
        """保存配置到文件"""
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logger.info(f"配置已保存到: {config_path}")
        except Exception as e:
            logger.error(f"保存配置文件失败: {e}")

# 使用singledispatch的函数
@singledispatch
def process_data(data):
    """处理数据的通用函数"""
    raise NotImplementedError(f"不支持的数据类型: {type(data)}")

@process_data.register
def _(data: str):
    """处理字符串数据"""
    return data.strip().upper()

@process_data.register
def _(data: list):
    """处理列表数据"""
    return [process_data(item) for item in data]

@process_data.register
def _(data: dict):
    """处理字典数据"""
    return {k: process_data(v) for k, v in data.items()}

# 缓存函数
@lru_cache(maxsize=128)
def calculate_file_hash(file_path: str) -> str:
    """计算文件哈希值（带缓存）"""
    import hashlib
    try:
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception as e:
        logger.warning(f"计算文件哈希失败: {e}")
        return ""

# 工具函数
def format_file_size(size_bytes: int) -> str:
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

def format_duration(duration: timedelta) -> str:
    """格式化时间间隔"""
    total_seconds = int(duration.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    if hours > 0:
        return f"{hours}小时{minutes}分钟{seconds}秒"
    elif minutes > 0:
        return f"{minutes}分钟{seconds}秒"
    else:
        return f"{seconds}秒"

async def benchmark_performance():
    """性能基准测试"""
    logger.info("开始性能基准测试")
    
    # 创建测试项目
    with temp_directory() as temp_dir:
        project = Project("基准测试项目", "性能测试", temp_dir)
        
        # 生成测试文件
        test_files = []
        for i in range(10):
            for ext in ['.py', '.js', '.java']:
                test_file = temp_dir / f"test_{i}{ext}"
                test_file.write_text(f"# 测试文件 {i}\nprint('Hello, World!')\n" * 50)
                test_files.append(test_file)
        
        # 测试文件扫描性能
        start_time = time.time()
        file_count = project.scan_directory()
        scan_duration = time.time() - start_time
        
        logger.info(f"文件扫描性能: {file_count} 个文件，耗时 {scan_duration:.4f} 秒")
        
        # 测试任务处理性能
        task_manager = TaskManager(max_workers=4)
        
        # 创建处理任务
        for file_info in project.get_all_files():
            task = FileProcessingTask(f"task_{file_info.name}", file_info)
            task_manager.add_task(task)
        
        # 执行所有任务
        start_time = time.time()
        results = await task_manager.execute_all()
        execution_duration = time.time() - start_time
        
        logger.info(f"任务处理性能: {len(results)} 个任务，耗时 {execution_duration:.4f} 秒")
        
        # 显示统计信息
        stats = project.get_statistics()
        task_stats = task_manager.get_statistics()
        
        logger.info(f"项目统计: {stats}")
        logger.info(f"任务统计: {task_stats}")

def demonstrate_features():
    """展示Python特性"""
    print("=== Python 特性演示 ===")
    
    # 1. 数据类和枚举
    print("1. 数据类和枚举演示:")
    file_info = FileInfo.from_path(__file__)
    print(f"   当前文件: {file_info.name}")
    print(f"   语言: {file_info.language.value}")
    print(f"   大小: {format_file_size(file_info.size)}")
    
    # 2. 上下文管理器
    print("\n2. 上下文管理器演示:")
    try:
        with file_lock(Path(__file__)):
            print("   文件锁获取成功")
    except Exception as e:
        print(f"   文件锁错误: {e}")
    
    # 3. 装饰器
    print("\n3. 装饰器演示:")
    
    @timing_decorator
    def example_function():
        time.sleep(0.1)
        return "完成"
    
    result = example_function()
    print(f"   函数结果: {result}")
    
    # 4. singledispatch
    print("\n4. 单分派泛函数演示:")
    test_data = [
        "hello world",
        ["item1", "item2", "item3"],
        {"name": "test", "value": "data"}
    ]
    
    for data in test_data:
        processed = process_data(data)
        print(f"   原数据: {data}")
        print(f"   处理后: {processed}")
    
    # 5. 配置管理器（单例）
    print("\n5. 配置管理器演示:")
    config1 = ConfigManager()
    config2 = ConfigManager()
    print(f"   是否为同一实例: {config1 is config2}")
    print(f"   应用名称: {config1.get('app_name')}")
    
    # 6. 类型注解和泛型
    print("\n6. 类型注解演示:")
    
    def process_items(items: List[T]) -> List[T]:
        """处理项目列表"""
        return [item for item in items if item is not None]
    
    numbers = [1, 2, None, 3, 4]
    filtered_numbers = process_items(numbers)
    print(f"   过滤前: {numbers}")
    print(f"   过滤后: {filtered_numbers}")

async def main():
    """主函数"""
    print(f"=== {APP_NAME} v{APP_VERSION} ===")
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # 演示基本特性
        demonstrate_features()
        
        # 创建项目和任务管理器
        print("\n=== 项目管理演示 ===")
        project = Project("Python示例项目", "展示Python语言特性", Path("."))
        
        # 扫描当前目录
        print("扫描项目文件...")
        file_count = project.scan_directory()
        
        if file_count > 0:
            # 显示项目统计
            stats = project.get_statistics()
            print(f"\n项目统计:")
            print(f"  总文件数: {stats.total_files}")
            print(f"  总行数: {stats.total_lines}")
            print(f"  总大小: {format_file_size(stats.total_size)}")
            print(f"  语言分布: {stats.languages}")
            
            # 搜索文件
            search_results = project.search_files("test")
            print(f"\n搜索 'test' 找到 {len(search_results)} 个文件")
            
            # 异步任务处理演示
            print("\n=== 异步任务处理演示 ===")
            task_manager = TaskManager(max_workers=3)
            
            # 创建文件处理任务
            for file_info in project.get_all_files()[:5]:  # 只处理前5个文件
                task = FileProcessingTask(f"task_{file_info.name}", file_info)
                task_manager.add_task(task)
            
            # 执行任务
            print("开始执行任务...")
            start_time = time.time()
            results = await task_manager.execute_all()
            execution_time = time.time() - start_time
            
            print(f"任务执行完成:")
            print(f"  成功处理: {len(results)} 个文件")
            print(f"  执行时间: {execution_time:.4f} 秒")
            
            # 任务统计
            task_stats = task_manager.get_statistics()
            print(f"  任务统计: {task_stats}")
        
        # 性能基准测试
        print("\n=== 性能基准测试 ===")
        await benchmark_performance()
        
    except Exception as e:
        logger.error(f"程序执行出错: {e}")
        raise
    
    print("\n程序执行完成!")

if __name__ == "__main__":
    # 设置事件循环策略（Windows兼容性）
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    # 运行主程序
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        logger.error(f"程序异常退出: {e}")
        sys.exit(1)
