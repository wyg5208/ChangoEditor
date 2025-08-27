<?php
/**
 * Chango Editor PHP测试文件
 * 展示PHP语言的现代特性和最佳实践
 * 
 * @author Chango Team
 * @version 1.0
 * @since 2024-01-15
 */

declare(strict_types=1);

namespace ChangoEditor\Test;

use DateTime;
use DateTimeInterface;
use InvalidArgumentException;
use JsonSerializable;
use PDO;
use PDOException;
use Throwable;

/**
 * 编程语言枚举
 */
enum Language: string
{
    case PHP = 'php';
    case Python = 'python';
    case JavaScript = 'javascript';
    case TypeScript = 'typescript';
    case Go = 'go';
    case Rust = 'rust';
    case Java = 'java';
    case CSharp = 'csharp';
    
    /**
     * 获取语言显示名称
     */
    public function getDisplayName(): string
    {
        return match($this) {
            self::PHP => 'PHP',
            self::Python => 'Python',
            self::JavaScript => 'JavaScript',
            self::TypeScript => 'TypeScript',
            self::Go => 'Go',
            self::Rust => 'Rust',
            self::Java => 'Java',
            self::CSharp => 'C#',
        };
    }
    
    /**
     * 获取文件扩展名
     */
    public function getExtensions(): array
    {
        return match($this) {
            self::PHP => ['php', 'php8', 'phtml'],
            self::Python => ['py', 'pyw', 'pyx'],
            self::JavaScript => ['js', 'jsx'],
            self::TypeScript => ['ts', 'tsx'],
            self::Go => ['go'],
            self::Rust => ['rs'],
            self::Java => ['java'],
            self::CSharp => ['cs'],
        };
    }
}

/**
 * 任务状态枚举
 */
enum TaskStatus: string
{
    case PENDING = 'pending';
    case IN_PROGRESS = 'in_progress';
    case COMPLETED = 'completed';
    case FAILED = 'failed';
    case CANCELLED = 'cancelled';
    
    public function getColor(): string
    {
        return match($this) {
            self::PENDING => '#ffc107',
            self::IN_PROGRESS => '#007bff',
            self::COMPLETED => '#28a745',
            self::FAILED => '#dc3545',
            self::CANCELLED => '#6c757d',
        };
    }
}

/**
 * 自定义异常基类
 */
abstract class ChangoEditorException extends \Exception
{
    protected array $context = [];
    
    public function __construct(
        string $message = '',
        int $code = 0,
        ?Throwable $previous = null,
        array $context = []
    ) {
        parent::__construct($message, $code, $previous);
        $this->context = $context;
    }
    
    public function getContext(): array
    {
        return $this->context;
    }
    
    public function setContext(array $context): self
    {
        $this->context = $context;
        return $this;
    }
}

/**
 * 文件相关异常
 */
class FileException extends ChangoEditorException {}

/**
 * 验证异常
 */
class ValidationException extends ChangoEditorException {}

/**
 * 数据库异常
 */
class DatabaseException extends ChangoEditorException {}

/**
 * 文件信息类
 */
readonly class FileInfo implements JsonSerializable
{
    public function __construct(
        public string $id,
        public string $path,
        public string $name,
        public int $size,
        public int $lines,
        public Language $language,
        public string $encoding,
        public string $checksum,
        public DateTimeInterface $createdAt,
        public DateTimeInterface $modifiedAt,
    ) {}
    
    /**
     * 从文件路径创建FileInfo实例
     */
    public static function fromPath(string $path): self
    {
        if (!file_exists($path)) {
            throw new FileException("文件不存在: {$path}");
        }
        
        if (!is_readable($path)) {
            throw new FileException("文件不可读: {$path}");
        }
        
        $pathInfo = pathinfo($path);
        $stat = stat($path);
        $size = filesize($path);
        
        // 检测语言
        $extension = strtolower($pathInfo['extension'] ?? '');
        $language = self::detectLanguage($extension);
        
        // 计算行数
        $lines = self::countLines($path);
        
        // 生成校验和
        $checksum = hash_file('sha256', $path);
        
        return new self(
            id: uniqid('file_', true),
            path: realpath($path),
            name: $pathInfo['basename'],
            size: $size,
            lines: $lines,
            language: $language,
            encoding: 'utf-8',
            checksum: $checksum,
            createdAt: new DateTime('@' . $stat['ctime']),
            modifiedAt: new DateTime('@' . $stat['mtime']),
        );
    }
    
    /**
     * 检测文件语言
     */
    private static function detectLanguage(string $extension): Language
    {
        foreach (Language::cases() as $language) {
            if (in_array($extension, $language->getExtensions(), true)) {
                return $language;
            }
        }
        
        return Language::PHP; // 默认
    }
    
    /**
     * 计算文件行数
     */
    private static function countLines(string $path): int
    {
        $file = new \SplFileObject($path);
        $file->seek(PHP_INT_MAX);
        return $file->key() + 1;
    }
    
    /**
     * 检查是否支持语法高亮
     */
    public function supportsHighlighting(): bool
    {
        return true; // 所有语言都支持
    }
    
    /**
     * 获取相对路径
     */
    public function getRelativePath(string $basePath): string
    {
        $basePath = rtrim($basePath, DIRECTORY_SEPARATOR) . DIRECTORY_SEPARATOR;
        
        if (str_starts_with($this->path, $basePath)) {
            return substr($this->path, strlen($basePath));
        }
        
        return $this->path;
    }
    
    /**
     * JSON序列化
     */
    public function jsonSerialize(): array
    {
        return [
            'id' => $this->id,
            'path' => $this->path,
            'name' => $this->name,
            'size' => $this->size,
            'lines' => $this->lines,
            'language' => $this->language->value,
            'language_display' => $this->language->getDisplayName(),
            'encoding' => $this->encoding,
            'checksum' => $this->checksum,
            'created_at' => $this->createdAt->format(DateTimeInterface::ISO8601),
            'modified_at' => $this->modifiedAt->format(DateTimeInterface::ISO8601),
        ];
    }
}

/**
 * 任务接口
 */
interface TaskInterface
{
    public function getId(): string;
    public function getTitle(): string;
    public function getStatus(): TaskStatus;
    public function execute(): void;
    public function cancel(): void;
}

/**
 * 任务特征
 */
trait TaskTrait
{
    protected string $id;
    protected string $title;
    protected TaskStatus $status;
    protected DateTimeInterface $createdAt;
    protected ?DateTimeInterface $startedAt = null;
    protected ?DateTimeInterface $completedAt = null;
    protected array $metadata = [];
    
    public function getId(): string
    {
        return $this->id;
    }
    
    public function getTitle(): string
    {
        return $this->title;
    }
    
    public function getStatus(): TaskStatus
    {
        return $this->status;
    }
    
    public function getCreatedAt(): DateTimeInterface
    {
        return $this->createdAt;
    }
    
    public function getStartedAt(): ?DateTimeInterface
    {
        return $this->startedAt;
    }
    
    public function getCompletedAt(): ?DateTimeInterface
    {
        return $this->completedAt;
    }
    
    public function getDuration(): ?int
    {
        if ($this->startedAt && $this->completedAt) {
            return $this->completedAt->getTimestamp() - $this->startedAt->getTimestamp();
        }
        
        return null;
    }
    
    public function setMetadata(string $key, mixed $value): void
    {
        $this->metadata[$key] = $value;
    }
    
    public function getMetadata(string $key = null): mixed
    {
        if ($key === null) {
            return $this->metadata;
        }
        
        return $this->metadata[$key] ?? null;
    }
    
    protected function setStatus(TaskStatus $status): void
    {
        $this->status = $status;
        
        match($status) {
            TaskStatus::IN_PROGRESS => $this->startedAt = new DateTime(),
            TaskStatus::COMPLETED, TaskStatus::FAILED, TaskStatus::CANCELLED => $this->completedAt = new DateTime(),
            default => null,
        };
    }
}

/**
 * 代码任务类
 */
class CodeTask implements TaskInterface
{
    use TaskTrait;
    
    public function __construct(
        string $title,
        private readonly Language $language,
        private readonly int $linesOfCode,
        private readonly string $description = ''
    ) {
        $this->id = uniqid('task_', true);
        $this->title = $title;
        $this->status = TaskStatus::PENDING;
        $this->createdAt = new DateTime();
        
        $this->setMetadata('language', $language->value);
        $this->setMetadata('lines_of_code', $linesOfCode);
        $this->setMetadata('description', $description);
    }
    
    public function execute(): void
    {
        $this->setStatus(TaskStatus::IN_PROGRESS);
        
        try {
            echo "开始执行代码任务: {$this->title}\n";
            echo "语言: {$this->language->getDisplayName()}\n";
            echo "代码行数: {$this->linesOfCode}\n";
            
            // 模拟执行过程
            $steps = [
                '读取源代码文件',
                '语法分析',
                '语义分析',
                '代码优化',
                '生成目标代码',
            ];
            
            foreach ($steps as $step) {
                echo "  执行步骤: {$step}\n";
                usleep(200000); // 200ms
            }
            
            $this->setStatus(TaskStatus::COMPLETED);
            echo "任务完成: {$this->title}\n";
            
        } catch (Throwable $e) {
            $this->setStatus(TaskStatus::FAILED);
            $this->setMetadata('error', $e->getMessage());
            throw new ChangoEditorException("任务执行失败: {$e->getMessage()}", 0, $e);
        }
    }
    
    public function cancel(): void
    {
        $this->setStatus(TaskStatus::CANCELLED);
        echo "任务已取消: {$this->title}\n";
    }
    
    public function getLanguage(): Language
    {
        return $this->language;
    }
    
    public function getLinesOfCode(): int
    {
        return $this->linesOfCode;
    }
    
    public function getEstimatedDuration(): int
    {
        // 每行代码估算1秒
        return $this->linesOfCode;
    }
}

/**
 * 任务管理器
 */
class TaskManager
{
    private array $tasks = [];
    private array $running = [];
    private int $maxConcurrent;
    
    public function __construct(int $maxConcurrent = 5)
    {
        $this->maxConcurrent = $maxConcurrent;
    }
    
    /**
     * 添加任务
     */
    public function addTask(TaskInterface $task): void
    {
        $this->tasks[$task->getId()] = $task;
        echo "添加任务: {$task->getTitle()}\n";
    }
    
    /**
     * 执行所有任务
     */
    public function executeAll(): void
    {
        foreach ($this->tasks as $task) {
            if ($task->getStatus() === TaskStatus::PENDING) {
                $this->executeTask($task);
            }
        }
    }
    
    /**
     * 执行单个任务
     */
    public function executeTask(TaskInterface $task): void
    {
        try {
            $task->execute();
        } catch (Throwable $e) {
            echo "任务执行失败: {$task->getTitle()}, 错误: {$e->getMessage()}\n";
        }
    }
    
    /**
     * 获取任务统计
     */
    public function getStatistics(): array
    {
        $stats = [
            'total' => count($this->tasks),
            'pending' => 0,
            'in_progress' => 0,
            'completed' => 0,
            'failed' => 0,
            'cancelled' => 0,
        ];
        
        foreach ($this->tasks as $task) {
            $status = $task->getStatus()->value;
            $stats[$status]++;
        }
        
        return $stats;
    }
    
    /**
     * 按状态获取任务
     */
    public function getTasksByStatus(TaskStatus $status): array
    {
        return array_filter(
            $this->tasks,
            fn(TaskInterface $task) => $task->getStatus() === $status
        );
    }
    
    /**
     * 清理已完成的任务
     */
    public function cleanup(): void
    {
        $this->tasks = array_filter(
            $this->tasks,
            fn(TaskInterface $task) => !in_array(
                $task->getStatus(),
                [TaskStatus::COMPLETED, TaskStatus::FAILED, TaskStatus::CANCELLED],
                true
            )
        );
        
        echo "清理完成，剩余任务: " . count($this->tasks) . "\n";
    }
}

/**
 * 项目类
 */
class Project implements JsonSerializable
{
    private array $files = [];
    private DateTimeInterface $updatedAt;
    
    public function __construct(
        private readonly string $id,
        private string $name,
        private string $description,
        private readonly string $path,
        private readonly DateTimeInterface $createdAt = new DateTime(),
    ) {
        $this->updatedAt = new DateTime();
    }
    
    /**
     * 扫描项目文件
     */
    public function scanFiles(): int
    {
        $this->files = [];
        $count = 0;
        
        $iterator = new \RecursiveIteratorIterator(
            new \RecursiveDirectoryIterator($this->path, \RecursiveDirectoryIterator::SKIP_DOTS)
        );
        
        foreach ($iterator as $file) {
            if ($file->isFile()) {
                try {
                    $fileInfo = FileInfo::fromPath($file->getPathname());
                    $this->files[$fileInfo->id] = $fileInfo;
                    $count++;
                } catch (FileException $e) {
                    echo "跳过文件: {$file->getPathname()}, 原因: {$e->getMessage()}\n";
                }
            }
        }
        
        $this->updatedAt = new DateTime();
        return $count;
    }
    
    /**
     * 添加文件
     */
    public function addFile(FileInfo $file): void
    {
        $this->files[$file->id] = $file;
        $this->updatedAt = new DateTime();
    }
    
    /**
     * 获取所有文件
     */
    public function getFiles(): array
    {
        return array_values($this->files);
    }
    
    /**
     * 按语言分组文件
     */
    public function groupByLanguage(): array
    {
        $groups = [];
        
        foreach ($this->files as $file) {
            $language = $file->language->value;
            $groups[$language][] = $file;
        }
        
        return $groups;
    }
    
    /**
     * 搜索文件
     */
    public function searchFiles(string $query): array
    {
        $query = strtolower($query);
        
        return array_filter($this->files, function(FileInfo $file) use ($query) {
            return str_contains(strtolower($file->name), $query) ||
                   str_contains(strtolower($file->path), $query);
        });
    }
    
    /**
     * 获取项目统计
     */
    public function getStatistics(): array
    {
        $stats = [
            'total_files' => count($this->files),
            'total_lines' => 0,
            'total_size' => 0,
            'languages' => [],
        ];
        
        foreach ($this->files as $file) {
            $stats['total_lines'] += $file->lines;
            $stats['total_size'] += $file->size;
            
            $language = $file->language->value;
            if (!isset($stats['languages'][$language])) {
                $stats['languages'][$language] = [
                    'files' => 0,
                    'lines' => 0,
                    'size' => 0,
                ];
            }
            
            $stats['languages'][$language]['files']++;
            $stats['languages'][$language]['lines'] += $file->lines;
            $stats['languages'][$language]['size'] += $file->size;
        }
        
        return $stats;
    }
    
    // Getters
    public function getId(): string { return $this->id; }
    public function getName(): string { return $this->name; }
    public function getDescription(): string { return $this->description; }
    public function getPath(): string { return $this->path; }
    public function getCreatedAt(): DateTimeInterface { return $this->createdAt; }
    public function getUpdatedAt(): DateTimeInterface { return $this->updatedAt; }
    
    public function jsonSerialize(): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'description' => $this->description,
            'path' => $this->path,
            'files_count' => count($this->files),
            'created_at' => $this->createdAt->format(DateTimeInterface::ISO8601),
            'updated_at' => $this->updatedAt->format(DateTimeInterface::ISO8601),
        ];
    }
}

/**
 * 数据库管理器
 */
class DatabaseManager
{
    private PDO $pdo;
    
    public function __construct(string $dsn, string $username = '', string $password = '')
    {
        try {
            $this->pdo = new PDO($dsn, $username, $password, [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                PDO::ATTR_EMULATE_PREPARES => false,
            ]);
        } catch (PDOException $e) {
            throw new DatabaseException("数据库连接失败: {$e->getMessage()}", 0, $e);
        }
    }
    
    /**
     * 创建表
     */
    public function createTables(): void
    {
        $sql = "
            CREATE TABLE IF NOT EXISTS projects (
                id VARCHAR(255) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                path VARCHAR(500) NOT NULL,
                created_at DATETIME NOT NULL,
                updated_at DATETIME NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS files (
                id VARCHAR(255) PRIMARY KEY,
                project_id VARCHAR(255),
                path VARCHAR(500) NOT NULL,
                name VARCHAR(255) NOT NULL,
                size BIGINT NOT NULL,
                lines INT NOT NULL,
                language VARCHAR(50) NOT NULL,
                encoding VARCHAR(20) NOT NULL,
                checksum VARCHAR(64) NOT NULL,
                created_at DATETIME NOT NULL,
                modified_at DATETIME NOT NULL,
                FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
            );
        ";
        
        $this->pdo->exec($sql);
    }
    
    /**
     * 保存项目
     */
    public function saveProject(Project $project): void
    {
        $sql = "INSERT OR REPLACE INTO projects (id, name, description, path, created_at, updated_at) 
                VALUES (?, ?, ?, ?, ?, ?)";
        
        $stmt = $this->pdo->prepare($sql);
        $stmt->execute([
            $project->getId(),
            $project->getName(),
            $project->getDescription(),
            $project->getPath(),
            $project->getCreatedAt()->format('Y-m-d H:i:s'),
            $project->getUpdatedAt()->format('Y-m-d H:i:s'),
        ]);
    }
    
    /**
     * 保存文件信息
     */
    public function saveFile(FileInfo $file, string $projectId): void
    {
        $sql = "INSERT OR REPLACE INTO files 
                (id, project_id, path, name, size, lines, language, encoding, checksum, created_at, modified_at) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
        
        $stmt = $this->pdo->prepare($sql);
        $stmt->execute([
            $file->id,
            $projectId,
            $file->path,
            $file->name,
            $file->size,
            $file->lines,
            $file->language->value,
            $file->encoding,
            $file->checksum,
            $file->createdAt->format('Y-m-d H:i:s'),
            $file->modifiedAt->format('Y-m-d H:i:s'),
        ]);
    }
}

/**
 * 工具类
 */
class Utils
{
    /**
     * 格式化文件大小
     */
    public static function formatBytes(int $bytes, int $precision = 2): string
    {
        $units = ['B', 'KB', 'MB', 'GB', 'TB'];
        
        for ($i = 0; $bytes > 1024 && $i < count($units) - 1; $i++) {
            $bytes /= 1024;
        }
        
        return round($bytes, $precision) . ' ' . $units[$i];
    }
    
    /**
     * 格式化持续时间
     */
    public static function formatDuration(int $seconds): string
    {
        if ($seconds < 60) {
            return "{$seconds}秒";
        }
        
        $minutes = intval($seconds / 60);
        $remainingSeconds = $seconds % 60;
        
        if ($minutes < 60) {
            return "{$minutes}分{$remainingSeconds}秒";
        }
        
        $hours = intval($minutes / 60);
        $remainingMinutes = $minutes % 60;
        
        return "{$hours}时{$remainingMinutes}分{$remainingSeconds}秒";
    }
    
    /**
     * 生成随机ID
     */
    public static function generateId(string $prefix = ''): string
    {
        return $prefix . uniqid('', true) . '_' . random_int(1000, 9999);
    }
}

// 主程序
function main(): void
{
    echo "=== Chango Editor PHP 功能演示 ===\n";
    echo "启动时间: " . (new DateTime())->format('Y-m-d H:i:s') . "\n\n";
    
    try {
        // 创建项目
        $project = new Project(
            id: Utils::generateId('proj_'),
            name: 'PHP示例项目',
            description: '展示PHP现代特性的示例项目',
            path: __DIR__
        );
        
        echo "创建项目: {$project->getName()}\n";
        
        // 扫描文件
        $fileCount = $project->scanFiles();
        echo "扫描到 {$fileCount} 个文件\n\n";
        
        // 显示统计信息
        $stats = $project->getStatistics();
        echo "=== 项目统计 ===\n";
        echo "总文件数: {$stats['total_files']}\n";
        echo "总行数: {$stats['total_lines']}\n";
        echo "总大小: " . Utils::formatBytes($stats['total_size']) . "\n";
        
        echo "\n语言分布:\n";
        foreach ($stats['languages'] as $language => $langStats) {
            $languageEnum = Language::from($language);
            echo "  {$languageEnum->getDisplayName()}: {$langStats['files']} 个文件, {$langStats['lines']} 行代码\n";
        }
        
        // 任务管理演示
        echo "\n=== 任务管理演示 ===\n";
        $taskManager = new TaskManager(3);
        
        // 创建任务
        $tasks = [
            new CodeTask('Python数据分析', Language::Python, 150, '数据清洗和可视化'),
            new CodeTask('JavaScript前端', Language::JavaScript, 300, 'React组件开发'),
            new CodeTask('PHP后端API', Language::PHP, 200, 'RESTful API开发'),
            new CodeTask('Go微服务', Language::Go, 400, '高并发微服务'),
        ];
        
        foreach ($tasks as $task) {
            $taskManager->addTask($task);
        }
        
        // 执行所有任务
        echo "\n开始执行任务...\n";
        $start = microtime(true);
        $taskManager->executeAll();
        $duration = microtime(true) - $start;
        
        echo "\n任务执行完成，耗时: " . Utils::formatDuration((int)$duration) . "\n";
        
        // 显示任务统计
        $taskStats = $taskManager->getStatistics();
        echo "\n任务统计:\n";
        foreach ($taskStats as $status => $count) {
            $statusEnum = TaskStatus::from($status);
            echo "  {$status}: {$count} 个任务\n";
        }
        
        // 文件搜索演示
        echo "\n=== 文件搜索演示 ===\n";
        $searchResults = $project->searchFiles('test');
        echo "搜索 'test' 找到 " . count($searchResults) . " 个文件\n";
        
        foreach (array_slice($searchResults, 0, 3) as $file) {
            echo "  - {$file->name} ({$file->language->getDisplayName()})\n";
        }
        
        // 语言分组演示
        echo "\n=== 语言分组演示 ===\n";
        $groups = $project->groupByLanguage();
        foreach ($groups as $language => $files) {
            $languageEnum = Language::from($language);
            echo "{$languageEnum->getDisplayName()}: " . count($files) . " 个文件\n";
        }
        
        // JSON序列化演示
        echo "\n=== JSON序列化演示 ===\n";
        $projectJson = json_encode($project, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
        echo "项目JSON:\n{$projectJson}\n";
        
        if (!empty($project->getFiles())) {
            $firstFile = $project->getFiles()[0];
            $fileJson = json_encode($firstFile, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
            echo "\n文件JSON:\n{$fileJson}\n";
        }
        
    } catch (Throwable $e) {
        echo "错误: {$e->getMessage()}\n";
        echo "堆栈跟踪:\n{$e->getTraceAsString()}\n";
    }
    
    echo "\n程序执行完成!\n";
}

// 如果直接运行此文件，则执行主程序
if (basename(__FILE__) === basename($_SERVER['SCRIPT_NAME'])) {
    main();
}
