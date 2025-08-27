# Chango Editor Ruby测试文件
# 展示Ruby语言的优雅特性和最佳实践
# 
# 作者: Chango Team
# 创建时间: 2024-01-15

require 'json'
require 'time'
require 'digest'
require 'fileutils'
require 'pathname'
require 'ostruct'
require 'forwardable'

# 全局常量
APP_NAME = 'Chango Editor'
APP_VERSION = '0.1.0'
SUPPORTED_EXTENSIONS = %w[.rb .py .js .ts .go .rs .java .cpp .cs .php].freeze

# 编程语言模块
module Language
  RUBY = 'ruby'
  PYTHON = 'python'
  JAVASCRIPT = 'javascript'
  TYPESCRIPT = 'typescript'
  GO = 'go'
  RUST = 'rust'
  JAVA = 'java'
  CPP = 'cpp'
  CSHARP = 'csharp'
  PHP = 'php'
  UNKNOWN = 'unknown'
  
  # 语言映射表
  LANGUAGE_MAP = {
    '.rb' => RUBY,
    '.py' => PYTHON,
    '.pyw' => PYTHON,
    '.js' => JAVASCRIPT,
    '.jsx' => JAVASCRIPT,
    '.ts' => TYPESCRIPT,
    '.tsx' => TYPESCRIPT,
    '.go' => GO,
    '.rs' => RUST,
    '.java' => JAVA,
    '.cpp' => CPP,
    '.cxx' => CPP,
    '.cc' => CPP,
    '.cs' => CSHARP,
    '.php' => PHP
  }.freeze
  
  # 语言显示名称
  DISPLAY_NAMES = {
    RUBY => 'Ruby',
    PYTHON => 'Python',
    JAVASCRIPT => 'JavaScript',
    TYPESCRIPT => 'TypeScript',
    GO => 'Go',
    RUST => 'Rust',
    JAVA => 'Java',
    CPP => 'C++',
    CSHARP => 'C#',
    PHP => 'PHP',
    UNKNOWN => 'Unknown'
  }.freeze
  
  # 关键字映射
  KEYWORDS = {
    RUBY => %w[
      def class module if else elsif unless case when then end begin rescue ensure
      while until for in do break next return yield super self nil true false
      and or not alias undef defined? private protected public require load
      attr_reader attr_writer attr_accessor include extend proc lambda block_given?
    ],
    PYTHON => %w[
      def class if else elif for while try except finally import from as with
      lambda yield return pass break continue global nonlocal async await
      and or not in is del assert raise True False None
    ],
    JAVASCRIPT => %w[
      var let const function class if else for while do switch case default
      try catch finally return break continue throw new this super extends
      import export async await typeof instanceof in of
    ]
  }.freeze
  
  module_function
  
  # 从文件扩展名检测语言
  def detect_from_extension(extension)
    LANGUAGE_MAP[extension.downcase] || UNKNOWN
  end
  
  # 获取语言显示名称
  def display_name(language)
    DISPLAY_NAMES[language] || 'Unknown'
  end
  
  # 获取语言关键字
  def keywords(language)
    KEYWORDS[language] || []
  end
  
  # 检查是否支持语法高亮
  def supports_highlighting?(language)
    KEYWORDS.key?(language)
  end
end

# 自定义异常类
class ChangoEditorError < StandardError
  attr_reader :context
  
  def initialize(message, context = {})
    super(message)
    @context = context
  end
end

class FileNotFoundError < ChangoEditorError; end
class ValidationError < ChangoEditorError; end
class ProcessingError < ChangoEditorError; end

# 文件信息类
class FileInfo
  attr_reader :id, :path, :name, :size, :lines, :language, :encoding, 
              :checksum, :created_at, :modified_at
  
  def initialize(path)
    @path = Pathname.new(path).expand_path
    
    raise FileNotFoundError, "文件不存在: #{@path}" unless @path.exist?
    raise ValidationError, "路径不是文件: #{@path}" unless @path.file?
    
    @id = generate_id
    @name = @path.basename.to_s
    @size = @path.size
    @lines = count_lines
    @language = Language.detect_from_extension(@path.extname)
    @encoding = detect_encoding
    @checksum = calculate_checksum
    @created_at = @path.ctime
    @modified_at = @path.mtime
  end
  
  # 类方法：从路径创建FileInfo
  def self.from_path(path)
    new(path)
  rescue => e
    raise ProcessingError, "无法处理文件 #{path}: #{e.message}"
  end
  
  # 检查是否支持语法高亮
  def supports_highlighting?
    Language.supports_highlighting?(@language)
  end
  
  # 获取相对路径
  def relative_path(base_path)
    @path.relative_path_from(Pathname.new(base_path))
  rescue ArgumentError
    @path
  end
  
  # 获取语言显示名称
  def language_display_name
    Language.display_name(@language)
  end
  
  # 获取文件大小（人类可读）
  def human_size
    bytes = @size.to_f
    units = %w[B KB MB GB TB]
    
    units.each_with_index do |unit, index|
      return "#{bytes.round(2)} #{unit}" if bytes < 1024 || index == units.length - 1
      bytes /= 1024
    end
  end
  
  # 转换为Hash
  def to_h
    {
      id: @id,
      path: @path.to_s,
      name: @name,
      size: @size,
      human_size: human_size,
      lines: @lines,
      language: @language,
      language_display: language_display_name,
      encoding: @encoding,
      checksum: @checksum,
      created_at: @created_at.iso8601,
      modified_at: @modified_at.iso8601,
      supports_highlighting: supports_highlighting?
    }
  end
  
  # JSON序列化
  def to_json(*args)
    to_h.to_json(*args)
  end
  
  private
  
  # 生成唯一ID
  def generate_id
    "file_#{Time.now.to_f}_#{rand(1000)}"
  end
  
  # 计算文件行数
  def count_lines
    return 0 if @size.zero?
    
    File.open(@path, 'r') { |f| f.readlines.count }
  rescue => e
    puts "警告: 无法计算文件行数 #{@path}: #{e.message}"
    0
  end
  
  # 检测文件编码
  def detect_encoding
    # 简化版编码检测
    'utf-8'
  end
  
  # 计算文件校验和
  def calculate_checksum
    Digest::SHA256.file(@path).hexdigest
  rescue => e
    puts "警告: 无法计算校验和 #{@path}: #{e.message}"
    'unknown'
  end
end

# 任务状态枚举
module TaskStatus
  PENDING = 'pending'
  RUNNING = 'running'
  COMPLETED = 'completed'
  FAILED = 'failed'
  CANCELLED = 'cancelled'
  
  ALL = [PENDING, RUNNING, COMPLETED, FAILED, CANCELLED].freeze
  
  module_function
  
  def valid?(status)
    ALL.include?(status)
  end
  
  def color(status)
    case status
    when PENDING then :yellow
    when RUNNING then :blue
    when COMPLETED then :green
    when FAILED then :red
    when CANCELLED then :gray
    else :white
    end
  end
end

# 任务基类
class Task
  attr_reader :id, :title, :status, :created_at, :started_at, :completed_at, :error
  
  def initialize(title)
    @id = generate_id
    @title = title
    @status = TaskStatus::PENDING
    @created_at = Time.now
    @started_at = nil
    @completed_at = nil
    @error = nil
  end
  
  # 执行任务
  def execute
    @status = TaskStatus::RUNNING
    @started_at = Time.now
    
    begin
      perform
      @status = TaskStatus::COMPLETED
    rescue => e
      @status = TaskStatus::FAILED
      @error = e.message
      raise
    ensure
      @completed_at = Time.now
    end
  end
  
  # 取消任务
  def cancel
    @status = TaskStatus::CANCELLED
    @completed_at = Time.now
  end
  
  # 获取执行时长
  def duration
    return nil unless @started_at
    
    end_time = @completed_at || Time.now
    end_time - @started_at
  end
  
  # 检查任务状态
  def pending?
    @status == TaskStatus::PENDING
  end
  
  def running?
    @status == TaskStatus::RUNNING
  end
  
  def completed?
    @status == TaskStatus::COMPLETED
  end
  
  def failed?
    @status == TaskStatus::FAILED
  end
  
  def cancelled?
    @status == TaskStatus::CANCELLED
  end
  
  def finished?
    completed? || failed? || cancelled?
  end
  
  # 转换为Hash
  def to_h
    {
      id: @id,
      title: @title,
      status: @status,
      created_at: @created_at.iso8601,
      started_at: @started_at&.iso8601,
      completed_at: @completed_at&.iso8601,
      duration: duration,
      error: @error
    }
  end
  
  protected
  
  # 子类需要实现的方法
  def perform
    raise NotImplementedError, '子类必须实现perform方法'
  end
  
  private
  
  def generate_id
    "task_#{Time.now.to_f}_#{rand(1000)}"
  end
end

# 代码处理任务
class CodeTask < Task
  attr_reader :language, :lines_of_code, :file_path
  
  def initialize(title, language, lines_of_code, file_path = nil)
    super(title)
    @language = language
    @lines_of_code = lines_of_code
    @file_path = file_path
  end
  
  # 获取预估执行时间
  def estimated_duration
    # 每1000行代码预估1秒
    (@lines_of_code / 1000.0).ceil
  end
  
  def to_h
    super.merge(
      language: @language,
      language_display: Language.display_name(@language),
      lines_of_code: @lines_of_code,
      file_path: @file_path,
      estimated_duration: estimated_duration
    )
  end
  
  protected
  
  def perform
    puts "开始执行代码任务: #{@title}"
    puts "  语言: #{Language.display_name(@language)}"
    puts "  代码行数: #{@lines_of_code}"
    puts "  文件路径: #{@file_path}" if @file_path
    
    # 模拟处理步骤
    steps = [
      '加载源代码',
      '词法分析',
      '语法分析',
      '语义分析',
      '代码优化',
      '生成结果'
    ]
    
    steps.each_with_index do |step, index|
      puts "  [#{index + 1}/#{steps.length}] #{step}..."
      sleep(0.1 + rand(0.3)) # 随机延迟模拟真实处理
    end
    
    puts "任务完成: #{@title}"
  end
end

# 任务管理器
class TaskManager
  extend Forwardable
  
  def_delegators :@tasks, :size, :length, :count, :empty?
  
  attr_reader :tasks, :max_concurrent
  
  def initialize(max_concurrent = 3)
    @tasks = {}
    @max_concurrent = max_concurrent
    @running_count = 0
  end
  
  # 添加任务
  def add_task(task)
    @tasks[task.id] = task
    puts "添加任务: #{task.title}"
  end
  
  # 创建代码任务的便捷方法
  def add_code_task(title, language, lines_of_code, file_path = nil)
    task = CodeTask.new(title, language, lines_of_code, file_path)
    add_task(task)
    task
  end
  
  # 执行所有待处理任务
  def execute_all
    pending_tasks = @tasks.values.select(&:pending?)
    
    puts "开始执行 #{pending_tasks.length} 个任务..."
    
    pending_tasks.each do |task|
      execute_task(task)
    end
    
    puts "所有任务执行完成"
  end
  
  # 执行单个任务
  def execute_task(task)
    return unless task.pending?
    
    begin
      task.execute
    rescue => e
      puts "任务执行失败: #{task.title} - #{e.message}"
    end
  end
  
  # 并发执行任务
  def execute_concurrent
    pending_tasks = @tasks.values.select(&:pending?)
    threads = []
    
    puts "开始并发执行 #{pending_tasks.length} 个任务 (最大并发数: #{@max_concurrent})..."
    
    pending_tasks.each_slice(@max_concurrent) do |task_batch|
      task_batch.each do |task|
        threads << Thread.new do
          Thread.current[:task] = task
          execute_task(task)
        end
      end
      
      # 等待当前批次完成
      threads.each(&:join)
      threads.clear
    end
    
    puts "并发执行完成"
  end
  
  # 取消所有任务
  def cancel_all
    @tasks.values.each do |task|
      task.cancel unless task.finished?
    end
    
    puts "已取消所有未完成的任务"
  end
  
  # 清理已完成的任务
  def cleanup
    before_count = @tasks.size
    @tasks.reject! { |_, task| task.finished? }
    after_count = @tasks.size
    
    puts "清理完成，删除了 #{before_count - after_count} 个已完成的任务"
  end
  
  # 按状态获取任务
  def tasks_by_status(status)
    @tasks.values.select { |task| task.status == status }
  end
  
  # 获取任务统计
  def statistics
    stats = Hash.new(0)
    
    @tasks.values.each do |task|
      stats[task.status] += 1
    end
    
    stats.merge(
      total: @tasks.size,
      pending: tasks_by_status(TaskStatus::PENDING).size,
      running: tasks_by_status(TaskStatus::RUNNING).size,
      completed: tasks_by_status(TaskStatus::COMPLETED).size,
      failed: tasks_by_status(TaskStatus::FAILED).size,
      cancelled: tasks_by_status(TaskStatus::CANCELLED).size
    )
  end
  
  # 查找任务
  def find_task(id)
    @tasks[id]
  end
  
  # 搜索任务
  def search_tasks(query)
    @tasks.values.select do |task|
      task.title.downcase.include?(query.downcase)
    end
  end
  
  # 转换为数组
  def to_a
    @tasks.values
  end
  
  # 转换为Hash
  def to_h
    {
      total_tasks: @tasks.size,
      max_concurrent: @max_concurrent,
      statistics: statistics,
      tasks: @tasks.transform_values(&:to_h)
    }
  end
end

# 项目类
class Project
  attr_reader :id, :name, :description, :path, :files, :created_at, :updated_at
  
  def initialize(name, description, path)
    @id = generate_id
    @name = name
    @description = description
    @path = Pathname.new(path).expand_path
    @files = {}
    @created_at = Time.now
    @updated_at = Time.now
    
    validate_path!
  end
  
  # 扫描项目文件
  def scan_files
    puts "扫描项目文件: #{@path}"
    
    @files.clear
    file_count = 0
    
    Find.find(@path) do |path|
      next unless File.file?(path)
      next if should_ignore?(path)
      
      begin
        file_info = FileInfo.from_path(path)
        @files[file_info.id] = file_info
        file_count += 1
      rescue ProcessingError => e
        puts "跳过文件: #{e.message}"
      end
    end
    
    @updated_at = Time.now
    puts "扫描完成，找到 #{file_count} 个文件"
    
    file_count
  end
  
  # 添加文件
  def add_file(file_info)
    @files[file_info.id] = file_info
    @updated_at = Time.now
  end
  
  # 获取所有文件
  def all_files
    @files.values
  end
  
  # 按语言分组文件
  def files_by_language
    all_files.group_by(&:language)
  end
  
  # 搜索文件
  def search_files(query)
    query = query.downcase
    
    all_files.select do |file|
      file.name.downcase.include?(query) ||
        file.path.to_s.downcase.include?(query)
    end
  end
  
  # 获取项目统计
  def statistics
    files = all_files
    
    stats = {
      total_files: files.size,
      total_lines: files.sum(&:lines),
      total_size: files.sum(&:size),
      languages: {}
    }
    
    files_by_language.each do |language, lang_files|
      stats[:languages][language] = {
        display_name: Language.display_name(language),
        files: lang_files.size,
        lines: lang_files.sum(&:lines),
        size: lang_files.sum(&:size)
      }
    end
    
    stats
  end
  
  # 转换为Hash
  def to_h
    {
      id: @id,
      name: @name,
      description: @description,
      path: @path.to_s,
      files_count: @files.size,
      created_at: @created_at.iso8601,
      updated_at: @updated_at.iso8601,
      statistics: statistics
    }
  end
  
  # JSON序列化
  def to_json(*args)
    to_h.to_json(*args)
  end
  
  private
  
  def generate_id
    "project_#{Time.now.to_f}_#{rand(1000)}"
  end
  
  def validate_path!
    raise FileNotFoundError, "项目路径不存在: #{@path}" unless @path.exist?
    raise ValidationError, "项目路径必须是目录: #{@path}" unless @path.directory?
  end
  
  # 检查是否应该忽略文件
  def should_ignore?(path)
    pathname = Pathname.new(path)
    
    # 忽略隐藏文件
    return true if pathname.basename.to_s.start_with?('.')
    
    # 忽略特定目录
    ignore_dirs = %w[.git node_modules target build dist .vscode .idea]
    return true if ignore_dirs.any? { |dir| pathname.to_s.include?("/#{dir}/") }
    
    # 只处理支持的文件扩展名
    return true unless SUPPORTED_EXTENSIONS.include?(pathname.extname.downcase)
    
    false
  end
end

# 语法高亮器类
class SyntaxHighlighter
  def initialize
    @keyword_patterns = {}
    build_patterns
  end
  
  # 高亮代码
  def highlight(code, language)
    return code unless Language.supports_highlighting?(language)
    
    pattern = @keyword_patterns[language]
    return code unless pattern
    
    # 简单的关键字高亮（实际应用中会更复杂）
    highlighted = code.gsub(pattern) { |match| "<keyword>#{match}</keyword>" }
    highlighted
  end
  
  # 获取语言关键字
  def keywords(language)
    Language.keywords(language)
  end
  
  private
  
  def build_patterns
    Language::KEYWORDS.each do |language, keywords|
      # 构建正则表达式模式
      pattern = /\b(#{keywords.join('|')})\b/
      @keyword_patterns[language] = pattern
    end
  end
end

# 工具方法模块
module Utils
  module_function
  
  # 格式化文件大小
  def format_bytes(bytes)
    units = %w[B KB MB GB TB]
    size = bytes.to_f
    
    units.each_with_index do |unit, index|
      return "#{size.round(2)} #{unit}" if size < 1024 || index == units.length - 1
      size /= 1024
    end
  end
  
  # 格式化时间段
  def format_duration(seconds)
    return '0秒' if seconds.nil? || seconds < 1
    
    hours = seconds / 3600
    minutes = (seconds % 3600) / 60
    secs = seconds % 60
    
    parts = []
    parts << "#{hours}小时" if hours > 0
    parts << "#{minutes}分钟" if minutes > 0
    parts << "#{secs.round(1)}秒" if secs > 0 || parts.empty?
    
    parts.join
  end
  
  # 生成随机颜色
  def random_color
    "##{rand(16777215).to_s(16).rjust(6, '0')}"
  end
  
  # 计算百分比
  def percentage(part, total)
    return 0 if total.zero?
    ((part.to_f / total) * 100).round(2)
  end
end

# 性能基准测试
class Benchmark
  def self.run
    puts "=== 性能基准测试 ==="
    
    # 创建临时测试目录
    test_dir = "/tmp/chango_editor_benchmark_#{Time.now.to_i}"
    FileUtils.mkdir_p(test_dir)
    
    begin
      # 生成测试文件
      puts "生成测试文件..."
      file_count = generate_test_files(test_dir, 50)
      puts "生成了 #{file_count} 个测试文件"
      
      # 基准测试：项目扫描
      puts "\n测试项目扫描性能..."
      project = Project.new('基准测试项目', '性能测试', test_dir)
      
      scan_time = time_block do
        project.scan_files
      end
      
      puts "扫描 #{project.all_files.size} 个文件耗时: #{Utils.format_duration(scan_time)}"
      
      # 基准测试：文件搜索
      puts "\n测试文件搜索性能..."
      search_time = time_block do
        results = project.search_files('test')
        puts "搜索找到 #{results.size} 个文件"
      end
      
      puts "搜索耗时: #{Utils.format_duration(search_time)}"
      
      # 基准测试：任务处理
      puts "\n测试任务处理性能..."
      task_manager = TaskManager.new(3)
      
      # 创建测试任务
      10.times do |i|
        language = [Language::RUBY, Language::PYTHON, Language::JAVASCRIPT].sample
        task_manager.add_code_task("测试任务 #{i + 1}", language, rand(100..500))
      end
      
      concurrent_time = time_block do
        task_manager.execute_concurrent
      end
      
      puts "并发执行 #{task_manager.count} 个任务耗时: #{Utils.format_duration(concurrent_time)}"
      
      # 显示统计信息
      puts "\n=== 项目统计 ==="
      stats = project.statistics
      puts "总文件数: #{stats[:total_files]}"
      puts "总行数: #{stats[:total_lines]}"
      puts "总大小: #{Utils.format_bytes(stats[:total_size])}"
      
      puts "\n语言分布:"
      stats[:languages].each do |language, lang_stats|
        puts "  #{lang_stats[:display_name]}: #{lang_stats[:files]} 个文件, #{lang_stats[:lines]} 行代码"
      end
      
    ensure
      # 清理测试文件
      FileUtils.rm_rf(test_dir) if Dir.exist?(test_dir)
    end
  end
  
  private_class_method def self.time_block
    start_time = Time.now
    yield
    Time.now - start_time
  end
  
  private_class_method def self.generate_test_files(dir, count)
    languages = [Language::RUBY, Language::PYTHON, Language::JAVASCRIPT]
    extensions = { Language::RUBY => '.rb', Language::PYTHON => '.py', Language::JAVASCRIPT => '.js' }
    
    count.times do |i|
      language = languages[i % languages.length]
      ext = extensions[language]
      filename = "test_file_#{i}#{ext}"
      filepath = File.join(dir, filename)
      
      content = generate_sample_code(language, i)
      File.write(filepath, content)
    end
    
    count
  end
  
  private_class_method def self.generate_sample_code(language, index)
    case language
    when Language::RUBY
      <<~RUBY
        # 测试文件 #{index}
        class TestClass#{index}
          def initialize(value)
            @value = value
          end
          
          def process
            puts "Processing value: #{\@value}"
            result = @value * 2
            puts "Result: #{result}"
            result
          end
        end
        
        test = TestClass#{index}.new(#{index})
        test.process
      RUBY
    when Language::PYTHON
      <<~PYTHON
        # 测试文件 #{index}
        class TestClass#{index}:
            def __init__(self, value):
                self.value = value
            
            def process(self):
                print(f"Processing value: {self.value}")
                result = self.value * 2
                print(f"Result: {result}")
                return result
        
        test = TestClass#{index}(#{index})
        test.process()
      PYTHON
    when Language::JAVASCRIPT
      <<~JAVASCRIPT
        // 测试文件 #{index}
        class TestClass#{index} {
            constructor(value) {
                this.value = value;
            }
            
            process() {
                console.log(`Processing value: ${this.value}`);
                const result = this.value * 2;
                console.log(`Result: ${result}`);
                return result;
            }
        }
        
        const test = new TestClass#{index}(#{index});
        test.process();
      JAVASCRIPT
    else
      "# 未知语言测试文件 #{index}\n"
    end
  end
end

# 主程序
def main
  puts "=== #{APP_NAME} v#{APP_VERSION} ==="
  puts "启动时间: #{Time.now.strftime('%Y-%m-%d %H:%M:%S')}"
  puts
  
  # 解析命令行参数
  command = ARGV[0] || 'demo'
  
  case command
  when 'demo'
    run_demo
  when 'benchmark'
    Benchmark.run
  when 'create'
    create_project_from_args
  else
    puts "未知命令: #{command}"
    puts "可用命令: demo, benchmark, create <name> <path>"
  end
  
  puts "\n程序执行完成!"
end

# 运行功能演示
def run_demo
  puts "=== 功能演示 ==="
  
  begin
    # 创建项目
    project = Project.new('Ruby示例项目', '展示Ruby语言特性', '.')
    puts "创建项目: #{project.name}"
    
    # 扫描文件
    file_count = project.scan_files
    
    # 显示项目统计
    puts "\n=== 项目统计 ==="
    stats = project.statistics
    puts "总文件数: #{stats[:total_files]}"
    puts "总行数: #{stats[:total_lines]}"
    puts "总大小: #{Utils.format_bytes(stats[:total_size])}"
    
    if stats[:languages].any?
      puts "\n语言分布:"
      stats[:languages].each do |language, lang_stats|
        percentage = Utils.percentage(lang_stats[:files], stats[:total_files])
        puts "  #{lang_stats[:display_name]}: #{lang_stats[:files]} 个文件 (#{percentage}%), #{lang_stats[:lines]} 行代码"
      end
    end
    
    # 文件搜索演示
    puts "\n=== 文件搜索演示 ==="
    search_results = project.search_files('test')
    puts "搜索 'test' 找到 #{search_results.size} 个文件"
    
    search_results.first(3).each do |file|
      puts "  - #{file.name} (#{file.language_display_name}, #{file.lines} 行)"
    end
    
    # 任务管理演示
    puts "\n=== 任务管理演示 ==="
    task_manager = TaskManager.new(3)
    
    # 创建各种任务
    tasks_data = [
      ['Ruby Web应用', Language::RUBY, 300],
      ['Python数据分析', Language::PYTHON, 150],
      ['JavaScript前端', Language::JAVASCRIPT, 250],
      ['Go微服务', Language::GO, 400],
      ['Rust系统工具', Language::RUST, 200]
    ]
    
    tasks_data.each do |title, language, lines|
      task_manager.add_code_task(title, language, lines)
    end
    
    puts "创建了 #{task_manager.count} 个任务"
    
    # 执行任务
    puts "\n开始执行任务..."
    start_time = Time.now
    task_manager.execute_concurrent
    execution_time = Time.now - start_time
    
    puts "任务执行完成，耗时: #{Utils.format_duration(execution_time)}"
    
    # 显示任务统计
    puts "\n任务统计:"
    stats = task_manager.statistics
    %w[completed failed cancelled].each do |status|
      count = stats[status.to_sym]
      puts "  #{status.capitalize}: #{count} 个任务" if count > 0
    end
    
    # 语法高亮演示
    puts "\n=== 语法高亮演示 ==="
    highlighter = SyntaxHighlighter.new
    
    sample_code = "def hello_world\n  puts 'Hello, Ruby!'\nend"
    highlighted = highlighter.highlight(sample_code, Language::RUBY)
    
    puts "原代码:"
    puts sample_code
    puts "\n高亮后:"
    puts highlighted
    
    # JSON序列化演示
    puts "\n=== JSON序列化演示 ==="
    project_json = JSON.pretty_generate(project.to_h)
    puts "项目JSON (前200字符):"
    puts project_json[0..200] + "..."
    
  rescue => e
    puts "错误: #{e.message}"
    puts "堆栈跟踪:"
    puts e.backtrace.first(5).join("\n")
  end
end

# 从命令行参数创建项目
def create_project_from_args
  if ARGV.length < 3
    puts "使用方法: #{$0} create <项目名> <项目路径>"
    return
  end
  
  name = ARGV[1]
  path = ARGV[2]
  
  begin
    project = Project.new(name, '通过命令行创建', path)
    puts "项目创建成功: #{project.name} (ID: #{project.id})"
    
    file_count = project.scan_files
    stats = project.statistics
    
    puts "扫描结果:"
    puts "  文件数: #{stats[:total_files]}"
    puts "  总行数: #{stats[:total_lines]}"
    puts "  总大小: #{Utils.format_bytes(stats[:total_size])}"
    
  rescue => e
    puts "创建项目失败: #{e.message}"
  end
end

# 如果直接运行此文件，则执行主程序
if __FILE__ == $0
  main
end
