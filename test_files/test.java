/**
 * Java测试文件
 * 展示Java 11+的现代特性和面向对象编程
 * 
 * @author Chango Team
 * @version 1.0
 * @since 2024-01-01
 */

package com.changoeditor.test;

import java.util.*;
import java.util.stream.*;
import java.util.concurrent.*;
import java.util.function.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.nio.file.*;
import java.io.IOException;

// 注解定义
@FunctionalInterface
interface Calculator {
    double calculate(double a, double b);
}

// 记录类 (Java 14+)
record Person(String name, int age, String email) {
    // 紧凑构造器
    public Person {
        if (age < 0) {
            throw new IllegalArgumentException("年龄不能为负数");
        }
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("姓名不能为空");
        }
    }
    
    // 实例方法
    public boolean isAdult() {
        return age >= 18;
    }
    
    public String getDisplayName() {
        return String.format("%s (%d岁)", name, age);
    }
}

// 枚举类
enum Priority {
    LOW(1, "低优先级"),
    MEDIUM(2, "中优先级"),
    HIGH(3, "高优先级"),
    CRITICAL(4, "紧急");
    
    private final int level;
    private final String description;
    
    Priority(int level, String description) {
        this.level = level;
        this.description = description;
    }
    
    public int getLevel() { return level; }
    public String getDescription() { return description; }
    
    // 静态方法
    public static Priority fromLevel(int level) {
        return Arrays.stream(values())
                .filter(p -> p.level == level)
                .findFirst()
                .orElse(LOW);
    }
}

// 抽象基类
abstract class Task {
    protected final String id;
    protected final String title;
    protected final Priority priority;
    protected final LocalDateTime createdAt;
    protected boolean completed;
    
    public Task(String id, String title, Priority priority) {
        this.id = Objects.requireNonNull(id, "ID不能为null");
        this.title = Objects.requireNonNull(title, "标题不能为null");
        this.priority = Objects.requireNonNull(priority, "优先级不能为null");
        this.createdAt = LocalDateTime.now();
        this.completed = false;
    }
    
    // 抽象方法
    public abstract void execute();
    public abstract Duration getEstimatedDuration();
    
    // 具体方法
    public void markCompleted() {
        this.completed = true;
        onCompleted();
    }
    
    protected void onCompleted() {
        System.out.println("任务完成: " + title);
    }
    
    // Getter方法
    public String getId() { return id; }
    public String getTitle() { return title; }
    public Priority getPriority() { return priority; }
    public boolean isCompleted() { return completed; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    
    @Override
    public String toString() {
        return String.format("Task{id='%s', title='%s', priority=%s, completed=%s}", 
                id, title, priority, completed);
    }
    
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Task task)) return false;
        return Objects.equals(id, task.id);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}

// 具体实现类
class CodeTask extends Task {
    private final String language;
    private final int linesOfCode;
    
    public CodeTask(String id, String title, Priority priority, String language, int linesOfCode) {
        super(id, title, priority);
        this.language = language;
        this.linesOfCode = linesOfCode;
    }
    
    @Override
    public void execute() {
        System.out.printf("正在执行代码任务: %s (%s, %d行)%n", 
                title, language, linesOfCode);
        
        // 模拟执行过程
        try {
            Thread.sleep(1000); // 模拟工作时间
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        markCompleted();
    }
    
    @Override
    public Duration getEstimatedDuration() {
        // 按行数估算时间 (每行1分钟)
        return Duration.ofMinutes(linesOfCode);
    }
    
    public String getLanguage() { return language; }
    public int getLinesOfCode() { return linesOfCode; }
}

// 泛型类
class TaskManager<T extends Task> {
    private final List<T> tasks = new ArrayList<>();
    private final ExecutorService executor = Executors.newFixedThreadPool(4);
    
    // 添加任务
    public void addTask(T task) {
        tasks.add(task);
        System.out.println("添加任务: " + task.getTitle());
    }
    
    // 批量添加任务
    public void addTasks(Collection<T> tasks) {
        this.tasks.addAll(tasks);
        System.out.printf("批量添加 %d 个任务%n", tasks.size());
    }
    
    // 执行所有任务
    public CompletableFuture<Void> executeAllTasks() {
        List<CompletableFuture<Void>> futures = tasks.stream()
                .filter(task -> !task.isCompleted())
                .map(task -> CompletableFuture.runAsync(task::execute, executor))
                .toList();
        
        return CompletableFuture.allOf(futures.toArray(new CompletableFuture[0]));
    }
    
    // 获取已完成任务
    public List<T> getCompletedTasks() {
        return tasks.stream()
                .filter(Task::isCompleted)
                .collect(Collectors.toList());
    }
    
    // 按优先级分组
    public Map<Priority, List<T>> groupByPriority() {
        return tasks.stream()
                .collect(Collectors.groupingBy(Task::getPriority));
    }
    
    // 统计信息
    public TaskStatistics getStatistics() {
        long totalTasks = tasks.size();
        long completedTasks = tasks.stream().mapToLong(t -> t.isCompleted() ? 1 : 0).sum();
        
        return new TaskStatistics(totalTasks, completedTasks);
    }
    
    // 查找任务
    public Optional<T> findTaskById(String id) {
        return tasks.stream()
                .filter(task -> task.getId().equals(id))
                .findFirst();
    }
    
    // 使用流式API进行复杂查询
    public List<T> findTasksByCondition(Predicate<T> condition) {
        return tasks.stream()
                .filter(condition)
                .sorted(Comparator.comparing(Task::getPriority))
                .collect(Collectors.toList());
    }
    
    // 关闭资源
    public void shutdown() {
        executor.shutdown();
        try {
            if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
                executor.shutdownNow();
            }
        } catch (InterruptedException e) {
            executor.shutdownNow();
            Thread.currentThread().interrupt();
        }
    }
}

// 内部记录类
record TaskStatistics(long total, long completed) {
    public double getCompletionRate() {
        return total > 0 ? (double) completed / total * 100 : 0.0;
    }
    
    public String getFormattedSummary() {
        return String.format("任务统计: %d/%d 已完成 (%.1f%%)", 
                completed, total, getCompletionRate());
    }
}

// 工具类
final class TaskUtils {
    private TaskUtils() {} // 防止实例化
    
    // 静态工厂方法
    public static CodeTask createPythonTask(String id, String title, int lines) {
        return new CodeTask(id, title, Priority.MEDIUM, "Python", lines);
    }
    
    public static CodeTask createJavaTask(String id, String title, int lines) {
        return new CodeTask(id, title, Priority.HIGH, "Java", lines);
    }
    
    // 文件操作
    public static void saveTasksToFile(List<Task> tasks, String filename) {
        try {
            List<String> lines = tasks.stream()
                    .map(Task::toString)
                    .collect(Collectors.toList());
            
            Files.write(Paths.get(filename), lines, StandardOpenOption.CREATE);
            System.out.println("任务已保存到: " + filename);
        } catch (IOException e) {
            System.err.println("保存失败: " + e.getMessage());
        }
    }
    
    // Lambda表达式和方法引用示例
    public static void demonstrateFunctionalProgramming() {
        List<Integer> numbers = List.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
        
        // 函数式接口
        Calculator add = (a, b) -> a + b;
        Calculator multiply = (a, b) -> a * b;
        
        // 流式操作
        List<Integer> evenSquares = numbers.stream()
                .filter(n -> n % 2 == 0)         // 过滤偶数
                .map(n -> n * n)                 // 平方
                .collect(Collectors.toList());   // 收集结果
        
        System.out.println("偶数的平方: " + evenSquares);
        
        // 方法引用
        numbers.forEach(System.out::println);
        
        // 计算器使用
        System.out.println("3 + 4 = " + add.calculate(3, 4));
        System.out.println("3 * 4 = " + multiply.calculate(3, 4));
    }
}

// 主类
public class JavaTestMain {
    private static final DateTimeFormatter FORMATTER = 
            DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
    
    public static void main(String[] args) {
        System.out.println("=== Java编程语言特性演示 ===");
        System.out.println("启动时间: " + LocalDateTime.now().format(FORMATTER));
        
        try {
            // 创建任务管理器
            TaskManager<CodeTask> taskManager = new TaskManager<>();
            
            // 创建测试数据
            List<CodeTask> tasks = List.of(
                    TaskUtils.createPythonTask("task-1", "数据分析脚本", 150),
                    TaskUtils.createJavaTask("task-2", "Web服务开发", 300),
                    new CodeTask("task-3", "前端界面", Priority.LOW, "JavaScript", 200),
                    new CodeTask("task-4", "数据库优化", Priority.CRITICAL, "SQL", 50)
            );
            
            // 添加任务
            taskManager.addTasks(tasks);
            
            // 显示任务信息
            System.out.println("\n=== 任务列表 ===");
            tasks.forEach(System.out::println);
            
            // 按优先级分组
            System.out.println("\n=== 按优先级分组 ===");
            taskManager.groupByPriority().forEach((priority, taskList) -> {
                System.out.printf("%s: %d个任务%n", priority.getDescription(), taskList.size());
            });
            
            // 执行所有任务
            System.out.println("\n=== 执行任务 ===");
            CompletableFuture<Void> allTasks = taskManager.executeAllTasks();
            allTasks.get(30, TimeUnit.SECONDS); // 等待完成
            
            // 显示统计信息
            System.out.println("\n=== 统计信息 ===");
            TaskStatistics stats = taskManager.getStatistics();
            System.out.println(stats.getFormattedSummary());
            
            // 函数式编程演示
            System.out.println("\n=== 函数式编程演示 ===");
            TaskUtils.demonstrateFunctionalProgramming();
            
            // 记录类演示
            System.out.println("\n=== 记录类演示 ===");
            Person person = new Person("张三", 25, "zhangsan@example.com");
            System.out.println("人员信息: " + person.getDisplayName());
            System.out.println("是否成年: " + person.isAdult());
            
            // 保存任务到文件
            TaskUtils.saveTasksToFile(new ArrayList<>(tasks), "tasks.txt");
            
            // 清理资源
            taskManager.shutdown();
            
        } catch (Exception e) {
            System.err.println("程序执行出错: " + e.getMessage());
            e.printStackTrace();
        }
        
        System.out.println("\n程序执行完成!");
    }
}
