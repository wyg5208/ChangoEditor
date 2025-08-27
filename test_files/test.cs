/**
 * C#测试文件
 * 展示C# 12的现代特性和.NET生态系统
 * 
 * @author Chango Team
 * @version 1.0
 */

using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Text.Json;
using System.ComponentModel.DataAnnotations;
using System.Runtime.CompilerServices;

namespace ChangoEditor.Test
{
    // 记录类型 (C# 9+)
    public record Person(string Name, int Age, string Email)
    {
        // 属性验证
        public string Name { get; init; } = !string.IsNullOrEmpty(Name) ? Name : 
            throw new ArgumentException("姓名不能为空");
        
        public int Age { get; init; } = Age >= 0 ? Age : 
            throw new ArgumentException("年龄不能为负数");
        
        // 计算属性
        public bool IsAdult => Age >= 18;
        public string DisplayName => $"{Name} ({Age}岁)";
        
        // 解构方法
        public void Deconstruct(out string name, out bool isAdult)
        {
            name = Name;
            isAdult = IsAdult;
        }
    }
    
    // 值类型记录 (C# 10+)
    public readonly record struct Point(double X, double Y)
    {
        public double Distance => Math.Sqrt(X * X + Y * Y);
        public Point Translate(double dx, double dy) => new(X + dx, Y + dy);
        
        // 操作符重载
        public static Point operator +(Point a, Point b) => new(a.X + b.X, a.Y + b.Y);
        public static Point operator -(Point a, Point b) => new(a.X - b.X, a.Y - b.Y);
    }
    
    // 枚举
    public enum TaskStatus
    {
        Pending,
        InProgress,
        Completed,
        Cancelled
    }
    
    // 接口定义
    public interface ITaskProcessor<T> where T : class
    {
        Task<bool> ProcessAsync(T item);
        Task<IEnumerable<T>> ProcessBatchAsync(IEnumerable<T> items);
    }
    
    // 抽象基类
    public abstract class BaseTask
    {
        protected BaseTask(string id, string title)
        {
            Id = id ?? throw new ArgumentNullException(nameof(id));
            Title = title ?? throw new ArgumentNullException(nameof(title));
            CreatedAt = DateTime.UtcNow;
            Status = TaskStatus.Pending;
        }
        
        // 属性
        public string Id { get; }
        public string Title { get; }
        public DateTime CreatedAt { get; }
        public TaskStatus Status { get; protected set; }
        public DateTime? CompletedAt { get; protected set; }
        
        // 抽象方法
        public abstract Task ExecuteAsync();
        public abstract TimeSpan EstimatedDuration { get; }
        
        // 虚方法
        public virtual void OnCompleted()
        {
            Status = TaskStatus.Completed;
            CompletedAt = DateTime.UtcNow;
            Console.WriteLine($"任务完成: {Title}");
        }
        
        // 事件
        public event EventHandler<TaskEventArgs>? StatusChanged;
        
        protected virtual void OnStatusChanged(TaskStatus oldStatus, TaskStatus newStatus)
        {
            Status = newStatus;
            StatusChanged?.Invoke(this, new TaskEventArgs(Id, oldStatus, newStatus));
        }
    }
    
    // 事件参数类
    public class TaskEventArgs : EventArgs
    {
        public TaskEventArgs(string taskId, TaskStatus oldStatus, TaskStatus newStatus)
        {
            TaskId = taskId;
            OldStatus = oldStatus;
            NewStatus = newStatus;
        }
        
        public string TaskId { get; }
        public TaskStatus OldStatus { get; }
        public TaskStatus NewStatus { get; }
    }
    
    // 具体实现类
    public class CodeTask : BaseTask
    {
        public CodeTask(string id, string title, string language, int linesOfCode) 
            : base(id, title)
        {
            Language = language ?? throw new ArgumentNullException(nameof(language));
            LinesOfCode = linesOfCode > 0 ? linesOfCode : 
                throw new ArgumentException("代码行数必须大于0");
        }
        
        public string Language { get; }
        public int LinesOfCode { get; }
        
        public override TimeSpan EstimatedDuration => TimeSpan.FromMinutes(LinesOfCode * 0.5);
        
        public override async Task ExecuteAsync()
        {
            OnStatusChanged(Status, TaskStatus.InProgress);
            
            Console.WriteLine($"开始执行代码任务: {Title} ({Language}, {LinesOfCode}行)");
            
            // 模拟异步工作
            await Task.Delay(1000);
            
            // 模拟进度报告
            for (int i = 1; i <= 5; i++)
            {
                await Task.Delay(200);
                Console.WriteLine($"  进度: {i * 20}%");
            }
            
            OnCompleted();
        }
        
        // ToString override
        public override string ToString() => 
            $"CodeTask {{ Id: {Id}, Title: {Title}, Language: {Language}, Lines: {LinesOfCode} }}";
    }
    
    // 泛型类与约束
    public class TaskManager<T> : ITaskProcessor<T>, IDisposable 
        where T : BaseTask
    {
        private readonly List<T> _tasks = new();
        private readonly SemaphoreSlim _semaphore = new(Environment.ProcessorCount);
        private bool _disposed;
        
        // 事件
        public event EventHandler<T>? TaskAdded;
        public event EventHandler<T>? TaskCompleted;
        
        // 属性
        public int TaskCount => _tasks.Count;
        public IReadOnlyList<T> Tasks => _tasks.AsReadOnly();
        
        // 索引器
        public T? this[string id] => _tasks.FirstOrDefault(t => t.Id == id);
        
        // 添加任务
        public void AddTask(T task)
        {
            ArgumentNullException.ThrowIfNull(task);
            
            _tasks.Add(task);
            task.StatusChanged += OnTaskStatusChanged;
            
            TaskAdded?.Invoke(this, task);
            Console.WriteLine($"添加任务: {task.Title}");
        }
        
        // 批量添加任务
        public void AddTasks(params T[] tasks) => AddTasks(tasks.AsEnumerable());
        
        public void AddTasks(IEnumerable<T> tasks)
        {
            foreach (var task in tasks)
            {
                AddTask(task);
            }
        }
        
        // 实现接口方法
        public async Task<bool> ProcessAsync(T item)
        {
            await _semaphore.WaitAsync();
            try
            {
                await item.ExecuteAsync();
                return item.Status == TaskStatus.Completed;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"任务执行失败: {item.Title}, 错误: {ex.Message}");
                return false;
            }
            finally
            {
                _semaphore.Release();
            }
        }
        
        public async Task<IEnumerable<T>> ProcessBatchAsync(IEnumerable<T> items)
        {
            var tasks = items.Select(ProcessAsync);
            var results = await Task.WhenAll(tasks);
            
            return items.Where((item, index) => results[index]);
        }
        
        // LINQ查询方法
        public IEnumerable<T> GetTasksByStatus(TaskStatus status) =>
            _tasks.Where(t => t.Status == status);
        
        public IEnumerable<TResult> SelectTasks<TResult>(Func<T, TResult> selector) =>
            _tasks.Select(selector);
        
        // 分组统计
        public Dictionary<TaskStatus, int> GetTaskStatistics() =>
            _tasks.GroupBy(t => t.Status)
                  .ToDictionary(g => g.Key, g => g.Count());
        
        // 异步枚举 (C# 8+)
        public async IAsyncEnumerable<T> GetTasksAsync([EnumeratorCancellation] CancellationToken cancellationToken = default)
        {
            foreach (var task in _tasks)
            {
                if (cancellationToken.IsCancellationRequested)
                    yield break;
                
                await Task.Delay(10, cancellationToken); // 模拟异步操作
                yield return task;
            }
        }
        
        // 事件处理
        private void OnTaskStatusChanged(object? sender, TaskEventArgs e)
        {
            if (e.NewStatus == TaskStatus.Completed && sender is T task)
            {
                TaskCompleted?.Invoke(this, task);
            }
        }
        
        // 析构和释放资源
        public void Dispose()
        {
            Dispose(true);
            GC.SuppressFinalize(this);
        }
        
        protected virtual void Dispose(bool disposing)
        {
            if (!_disposed && disposing)
            {
                _semaphore.Dispose();
                _disposed = true;
            }
        }
        
        ~TaskManager()
        {
            Dispose(false);
        }
    }
    
    // 扩展方法
    public static class TaskExtensions
    {
        public static async Task<T[]> WhenAll<T>(this IEnumerable<Task<T>> tasks)
        {
            return await Task.WhenAll(tasks);
        }
        
        public static T[] WhereNotNull<T>(this IEnumerable<T?> source) where T : class
        {
            return source.Where(x => x is not null).Cast<T>().ToArray();
        }
    }
    
    // 工具类
    public static class TaskUtils
    {
        // 静态工厂方法
        public static CodeTask CreatePythonTask(string id, string title, int lines) =>
            new(id, title, "Python", lines);
        
        public static CodeTask CreateCSharpTask(string id, string title, int lines) =>
            new(id, title, "C#", lines);
        
        // JSON序列化
        public static string SerializeTask<T>(T task) where T : BaseTask
        {
            var options = new JsonSerializerOptions
            {
                WriteIndented = true,
                PropertyNamingPolicy = JsonNamingPolicy.CamelCase
            };
            
            return JsonSerializer.Serialize(task, options);
        }
        
        // 文件操作
        public static async Task SaveTasksAsync<T>(IEnumerable<T> tasks, string filePath) 
            where T : BaseTask
        {
            var json = JsonSerializer.Serialize(tasks, new JsonSerializerOptions 
            { 
                WriteIndented = true 
            });
            
            await File.WriteAllTextAsync(filePath, json);
            Console.WriteLine($"任务已保存到: {filePath}");
        }
    }
    
    // 主程序类
    public class Program
    {
        public static async Task Main(string[] args)
        {
            Console.WriteLine("=== C# 编程语言特性演示 ===");
            Console.WriteLine($"启动时间: {DateTime.Now:yyyy-MM-dd HH:mm:ss}");
            
            try
            {
                // 创建任务管理器
                using var taskManager = new TaskManager<CodeTask>();
                
                // 事件订阅
                taskManager.TaskAdded += (sender, task) => 
                    Console.WriteLine($"事件: 任务已添加 - {task.Title}");
                
                taskManager.TaskCompleted += (sender, task) => 
                    Console.WriteLine($"事件: 任务已完成 - {task.Title}");
                
                // 创建测试数据
                var tasks = new[]
                {
                    TaskUtils.CreatePythonTask("task-1", "数据分析脚本", 150),
                    TaskUtils.CreateCSharpTask("task-2", "Web API开发", 300),
                    new CodeTask("task-3", "前端组件", "TypeScript", 200),
                    new CodeTask("task-4", "数据库迁移", "SQL", 50)
                };
                
                // 添加任务
                taskManager.AddTasks(tasks);
                
                // 显示任务统计
                Console.WriteLine("\n=== 任务统计 ===");
                var stats = taskManager.GetTaskStatistics();
                foreach (var (status, count) in stats)
                {
                    Console.WriteLine($"{status}: {count}个任务");
                }
                
                // 使用异步枚举
                Console.WriteLine("\n=== 异步枚举演示 ===");
                await foreach (var task in taskManager.GetTasksAsync())
                {
                    Console.WriteLine($"枚举任务: {task.Title}");
                }
                
                // 执行所有任务
                Console.WriteLine("\n=== 执行任务 ===");
                var completedTasks = await taskManager.ProcessBatchAsync(tasks);
                Console.WriteLine($"完成了 {completedTasks.Count()} 个任务");
                
                // 记录类型演示
                Console.WriteLine("\n=== 记录类型演示 ===");
                var person = new Person("张三", 25, "zhangsan@example.com");
                Console.WriteLine($"人员信息: {person.DisplayName}");
                Console.WriteLine($"是否成年: {person.IsAdult}");
                
                // 解构
                var (name, isAdult) = person;
                Console.WriteLine($"解构结果: {name}, 成年: {isAdult}");
                
                // 值类型记录
                var point1 = new Point(3, 4);
                var point2 = new Point(1, 2);
                var sum = point1 + point2;
                Console.WriteLine($"点运算: {point1} + {point2} = {sum}");
                Console.WriteLine($"距离: {point1.Distance:F2}");
                
                // LINQ和扩展方法
                Console.WriteLine("\n=== LINQ 查询演示 ===");
                var completedCodeTasks = taskManager
                    .GetTasksByStatus(TaskStatus.Completed)
                    .Where(t => t.LinesOfCode > 100)
                    .OrderBy(t => t.LinesOfCode)
                    .ToArray();
                
                Console.WriteLine($"大型已完成任务: {completedCodeTasks.Length}个");
                
                // 保存任务到文件
                await TaskUtils.SaveTasksAsync(tasks, "tasks.json");
                
                // 模式匹配 (C# 8+)
                Console.WriteLine("\n=== 模式匹配演示 ===");
                foreach (var task in tasks)
                {
                    var description = task switch
                    {
                        { Language: "Python", LinesOfCode: > 100 } => "大型Python项目",
                        { Language: "C#", LinesOfCode: > 200 } => "大型C#项目",
                        { LinesOfCode: < 100 } => "小型项目",
                        _ => "标准项目"
                    };
                    
                    Console.WriteLine($"{task.Title}: {description}");
                }
                
            }
            catch (Exception ex)
            {
                Console.WriteLine($"程序执行出错: {ex.Message}");
                Console.WriteLine(ex.StackTrace);
            }
            
            Console.WriteLine("\n程序执行完成!");
        }
    }
}
