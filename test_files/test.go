// Chango Editor Go测试文件
// 展示Go语言的现代特性和最佳实践
//
// 作者: Chango Team
// 创建时间: 2024-01-15

package main

import (
	"bufio"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"log"
	"math/rand"
	"net/http"
	"os"
	"path/filepath"
	"regexp"
	"sort"
	"strconv"
	"strings"
	"sync"
	"time"
)

// 常量定义
const (
	AppName    = "Chango Editor"
	AppVersion = "0.1.0"
	MaxWorkers = 10
	TimeoutSec = 30
)

// 自定义错误
var (
	ErrFileNotFound   = errors.New("文件未找到")
	ErrInvalidFormat  = errors.New("无效的文件格式")
	ErrPermissionDenied = errors.New("权限被拒绝")
	ErrTimeout        = errors.New("操作超时")
)

// 编程语言枚举
type Language int

const (
	Unknown Language = iota
	Python
	JavaScript
	TypeScript
	Go
	Rust
	Java
	Cpp
	CSharp
)

// String 方法实现Stringer接口
func (l Language) String() string {
	switch l {
	case Python:
		return "Python"
	case JavaScript:
		return "JavaScript"
	case TypeScript:
		return "TypeScript"
	case Go:
		return "Go"
	case Rust:
		return "Rust"
	case Java:
		return "Java"
	case Cpp:
		return "C++"
	case CSharp:
		return "C#"
	default:
		return "Unknown"
	}
}

// 文件信息结构体
type FileInfo struct {
	Path         string    `json:"path"`
	Name         string    `json:"name"`
	Size         int64     `json:"size"`
	Lines        int       `json:"lines"`
	Language     Language  `json:"language"`
	Encoding     string    `json:"encoding"`
	LastModified time.Time `json:"last_modified"`
	Checksum     string    `json:"checksum"`
}

// 项目结构体
type Project struct {
	ID          string     `json:"id"`
	Name        string     `json:"name"`
	Description string     `json:"description"`
	Path        string     `json:"path"`
	Language    Language   `json:"language"`
	Files       []FileInfo `json:"files"`
	CreatedAt   time.Time  `json:"created_at"`
	UpdatedAt   time.Time  `json:"updated_at"`
	mu          sync.RWMutex
}

// 添加文件到项目
func (p *Project) AddFile(file FileInfo) {
	p.mu.Lock()
	defer p.mu.Unlock()
	
	p.Files = append(p.Files, file)
	p.UpdatedAt = time.Now()
}

// 获取文件列表
func (p *Project) GetFiles() []FileInfo {
	p.mu.RLock()
	defer p.mu.RUnlock()
	
	// 返回副本以避免并发修改
	files := make([]FileInfo, len(p.Files))
	copy(files, p.Files)
	return files
}

// 统计信息
func (p *Project) GetStats() (totalFiles int, totalLines int, languages map[Language]int) {
	p.mu.RLock()
	defer p.mu.RUnlock()
	
	totalFiles = len(p.Files)
	languages = make(map[Language]int)
	
	for _, file := range p.Files {
		totalLines += file.Lines
		languages[file.Language]++
	}
	
	return
}

// 文件处理器接口
type FileProcessor interface {
	Process(ctx context.Context, file FileInfo) error
	GetName() string
}

// 语法高亮器
type SyntaxHighlighter struct {
	language Language
	keywords map[Language][]string
}

// 创建新的语法高亮器
func NewSyntaxHighlighter() *SyntaxHighlighter {
	keywords := map[Language][]string{
		Python: {"def", "class", "if", "else", "elif", "for", "while", "try", "except", "finally", 
			"import", "from", "as", "with", "lambda", "yield", "return", "pass", "break", "continue"},
		JavaScript: {"var", "let", "const", "function", "class", "if", "else", "for", "while", 
			"do", "switch", "case", "default", "try", "catch", "finally", "return", "break", "continue"},
		Go: {"var", "const", "func", "type", "struct", "interface", "map", "chan", "select", 
			"go", "defer", "if", "else", "for", "range", "switch", "case", "default", "break", "continue"},
	}
	
	return &SyntaxHighlighter{
		keywords: keywords,
	}
}

// 实现FileProcessor接口
func (sh *SyntaxHighlighter) Process(ctx context.Context, file FileInfo) error {
	log.Printf("语法高亮处理文件: %s (%s)", file.Name, file.Language)
	
	// 模拟处理时间
	select {
	case <-time.After(100 * time.Millisecond):
		return nil
	case <-ctx.Done():
		return ctx.Err()
	}
}

func (sh *SyntaxHighlighter) GetName() string {
	return "SyntaxHighlighter"
}

// 文件分析器
type FileAnalyzer struct {
	patterns map[Language]*regexp.Regexp
}

// 创建新的文件分析器
func NewFileAnalyzer() *FileAnalyzer {
	patterns := map[Language]*regexp.Regexp{
		Python:     regexp.MustCompile(`\.py$`),
		JavaScript: regexp.MustCompile(`\.js$`),
		TypeScript: regexp.MustCompile(`\.ts$`),
		Go:         regexp.MustCompile(`\.go$`),
		Java:       regexp.MustCompile(`\.java$`),
		Cpp:        regexp.MustCompile(`\.(cpp|cxx|cc|c\+\+)$`),
		CSharp:     regexp.MustCompile(`\.cs$`),
	}
	
	return &FileAnalyzer{
		patterns: patterns,
	}
}

// 检测文件语言
func (fa *FileAnalyzer) DetectLanguage(filename string) Language {
	for lang, pattern := range fa.patterns {
		if pattern.MatchString(filename) {
			return lang
		}
	}
	return Unknown
}

// 实现FileProcessor接口
func (fa *FileAnalyzer) Process(ctx context.Context, file FileInfo) error {
	log.Printf("分析文件: %s", file.Name)
	
	// 模拟分析过程
	time.Sleep(50 * time.Millisecond)
	return nil
}

func (fa *FileAnalyzer) GetName() string {
	return "FileAnalyzer"
}

// 项目管理器
type ProjectManager struct {
	projects map[string]*Project
	mu       sync.RWMutex
	analyzer *FileAnalyzer
}

// 创建新的项目管理器
func NewProjectManager() *ProjectManager {
	return &ProjectManager{
		projects: make(map[string]*Project),
		analyzer: NewFileAnalyzer(),
	}
}

// 创建项目
func (pm *ProjectManager) CreateProject(name, description, path string) (*Project, error) {
	if name == "" {
		return nil, errors.New("项目名称不能为空")
	}
	
	pm.mu.Lock()
	defer pm.mu.Unlock()
	
	id := generateID()
	project := &Project{
		ID:          id,
		Name:        name,
		Description: description,
		Path:        path,
		Files:       make([]FileInfo, 0),
		CreatedAt:   time.Now(),
		UpdatedAt:   time.Now(),
	}
	
	pm.projects[id] = project
	log.Printf("创建项目: %s (ID: %s)", name, id)
	return project, nil
}

// 获取项目
func (pm *ProjectManager) GetProject(id string) (*Project, error) {
	pm.mu.RLock()
	defer pm.mu.RUnlock()
	
	project, exists := pm.projects[id]
	if !exists {
		return nil, fmt.Errorf("项目不存在: %s", id)
	}
	
	return project, nil
}

// 扫描项目文件
func (pm *ProjectManager) ScanProject(ctx context.Context, projectID string) error {
	project, err := pm.GetProject(projectID)
	if err != nil {
		return err
	}
	
	return filepath.Walk(project.Path, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		
		// 检查上下文取消
		select {
		case <-ctx.Done():
			return ctx.Err()
		default:
		}
		
		// 跳过目录和隐藏文件
		if info.IsDir() || strings.HasPrefix(info.Name(), ".") {
			return nil
		}
		
		// 检测语言
		language := pm.analyzer.DetectLanguage(info.Name())
		if language == Unknown {
			return nil // 跳过不支持的文件类型
		}
		
		// 创建文件信息
		fileInfo := FileInfo{
			Path:         path,
			Name:         info.Name(),
			Size:         info.Size(),
			Language:     language,
			Encoding:     "utf-8",
			LastModified: info.ModTime(),
			Checksum:     generateChecksum(path),
		}
		
		// 计算行数
		if lines, err := countLines(path); err == nil {
			fileInfo.Lines = lines
		}
		
		// 添加到项目
		project.AddFile(fileInfo)
		
		return nil
	})
}

// 工作池
type WorkerPool struct {
	workers   int
	jobQueue  chan FileInfo
	processor FileProcessor
	wg        sync.WaitGroup
}

// 创建工作池
func NewWorkerPool(workers int, processor FileProcessor) *WorkerPool {
	return &WorkerPool{
		workers:   workers,
		jobQueue:  make(chan FileInfo, workers*2),
		processor: processor,
	}
}

// 启动工作池
func (wp *WorkerPool) Start(ctx context.Context) {
	for i := 0; i < wp.workers; i++ {
		wp.wg.Add(1)
		go wp.worker(ctx, i)
	}
}

// 工作协程
func (wp *WorkerPool) worker(ctx context.Context, id int) {
	defer wp.wg.Done()
	
	for {
		select {
		case file, ok := <-wp.jobQueue:
			if !ok {
				log.Printf("工作协程 %d 退出", id)
				return
			}
			
			log.Printf("工作协程 %d 处理文件: %s", id, file.Name)
			if err := wp.processor.Process(ctx, file); err != nil {
				log.Printf("处理文件失败: %s, 错误: %v", file.Name, err)
			}
			
		case <-ctx.Done():
			log.Printf("工作协程 %d 被取消", id)
			return
		}
	}
}

// 提交任务
func (wp *WorkerPool) Submit(file FileInfo) {
	wp.jobQueue <- file
}

// 关闭工作池
func (wp *WorkerPool) Close() {
	close(wp.jobQueue)
	wp.wg.Wait()
}

// HTTP服务器
type Server struct {
	pm     *ProjectManager
	mux    *http.ServeMux
	server *http.Server
}

// 创建新服务器
func NewServer(pm *ProjectManager) *Server {
	s := &Server{
		pm:  pm,
		mux: http.NewServeMux(),
	}
	
	s.setupRoutes()
	s.server = &http.Server{
		Addr:    ":8080",
		Handler: s.mux,
		ReadTimeout:  30 * time.Second,
		WriteTimeout: 30 * time.Second,
	}
	
	return s
}

// 设置路由
func (s *Server) setupRoutes() {
	s.mux.HandleFunc("/api/projects", s.handleProjects)
	s.mux.HandleFunc("/api/projects/", s.handleProjectDetail)
	s.mux.HandleFunc("/api/health", s.handleHealth)
	s.mux.HandleFunc("/", s.handleIndex)
}

// 处理项目列表
func (s *Server) handleProjects(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodGet:
		s.getProjects(w, r)
	case http.MethodPost:
		s.createProject(w, r)
	default:
		http.Error(w, "方法不允许", http.StatusMethodNotAllowed)
	}
}

// 获取项目列表
func (s *Server) getProjects(w http.ResponseWriter, r *http.Request) {
	s.pm.mu.RLock()
	projects := make([]*Project, 0, len(s.pm.projects))
	for _, project := range s.pm.projects {
		projects = append(projects, project)
	}
	s.pm.mu.RUnlock()
	
	// 按创建时间排序
	sort.Slice(projects, func(i, j int) bool {
		return projects[i].CreatedAt.After(projects[j].CreatedAt)
	})
	
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(projects)
}

// 创建项目
func (s *Server) createProject(w http.ResponseWriter, r *http.Request) {
	var req struct {
		Name        string `json:"name"`
		Description string `json:"description"`
		Path        string `json:"path"`
	}
	
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "无效的JSON格式", http.StatusBadRequest)
		return
	}
	
	project, err := s.pm.CreateProject(req.Name, req.Description, req.Path)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(project)
}

// 处理项目详情
func (s *Server) handleProjectDetail(w http.ResponseWriter, r *http.Request) {
	// 提取项目ID
	path := strings.TrimPrefix(r.URL.Path, "/api/projects/")
	projectID := strings.Split(path, "/")[0]
	
	project, err := s.pm.GetProject(projectID)
	if err != nil {
		http.Error(w, "项目不存在", http.StatusNotFound)
		return
	}
	
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(project)
}

// 健康检查
func (s *Server) handleHealth(w http.ResponseWriter, r *http.Request) {
	health := map[string]interface{}{
		"status":    "healthy",
		"timestamp": time.Now(),
		"version":   AppVersion,
		"uptime":    time.Since(startTime),
	}
	
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(health)
}

// 首页
func (s *Server) handleIndex(w http.ResponseWriter, r *http.Request) {
	html := `
<!DOCTYPE html>
<html>
<head>
    <title>Chango Editor API</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .endpoint { margin: 20px 0; padding: 10px; border-left: 4px solid #007acc; }
        .method { color: #007acc; font-weight: bold; }
        code { background: #f4f4f4; padding: 2px 4px; }
    </style>
</head>
<body>
    <h1>Chango Editor API</h1>
    <p>版本: %s</p>
    
    <h2>API端点</h2>
    
    <div class="endpoint">
        <div><span class="method">GET</span> <code>/api/health</code></div>
        <div>健康检查</div>
    </div>
    
    <div class="endpoint">
        <div><span class="method">GET</span> <code>/api/projects</code></div>
        <div>获取项目列表</div>
    </div>
    
    <div class="endpoint">
        <div><span class="method">POST</span> <code>/api/projects</code></div>
        <div>创建新项目</div>
    </div>
    
    <div class="endpoint">
        <div><span class="method">GET</span> <code>/api/projects/{id}</code></div>
        <div>获取项目详情</div>
    </div>
</body>
</html>
`
	
	fmt.Fprintf(w, html, AppVersion)
}

// 启动服务器
func (s *Server) Start() error {
	log.Printf("服务器启动在 %s", s.server.Addr)
	return s.server.ListenAndServe()
}

// 优雅关闭
func (s *Server) Shutdown(ctx context.Context) error {
	log.Println("关闭服务器...")
	return s.server.Shutdown(ctx)
}

// 工具函数

var startTime = time.Now()

// 生成ID
func generateID() string {
	return fmt.Sprintf("%d_%d", time.Now().UnixNano(), rand.Intn(1000))
}

// 生成校验和
func generateChecksum(filename string) string {
	// 简化版校验和生成
	return fmt.Sprintf("sha256_%x", time.Now().UnixNano())
}

// 计算文件行数
func countLines(filename string) (int, error) {
	file, err := os.Open(filename)
	if err != nil {
		return 0, err
	}
	defer file.Close()
	
	scanner := bufio.NewScanner(file)
	lines := 0
	for scanner.Scan() {
		lines++
	}
	
	return lines, scanner.Err()
}

// 命令行解析
func parseArgs() (string, string, string) {
	if len(os.Args) < 4 {
		fmt.Printf("使用方法: %s <命令> <项目名> <项目路径>\n", os.Args[0])
		fmt.Println("命令:")
		fmt.Println("  create   - 创建新项目")
		fmt.Println("  scan     - 扫描项目文件")
		fmt.Println("  serve    - 启动HTTP服务器")
		os.Exit(1)
	}
	
	return os.Args[1], os.Args[2], os.Args[3]
}

// 演示并发处理
func demonstrateConcurrency(pm *ProjectManager, projectID string) {
	project, err := pm.GetProject(projectID)
	if err != nil {
		log.Printf("获取项目失败: %v", err)
		return
	}
	
	files := project.GetFiles()
	if len(files) == 0 {
		log.Println("项目中没有文件")
		return
	}
	
	// 创建上下文
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()
	
	// 创建语法高亮器
	highlighter := NewSyntaxHighlighter()
	
	// 创建工作池
	pool := NewWorkerPool(5, highlighter)
	pool.Start(ctx)
	
	// 提交任务
	for _, file := range files {
		pool.Submit(file)
	}
	
	// 关闭工作池
	pool.Close()
	
	log.Println("并发处理完成")
}

// 错误处理示例
func handleError(err error) {
	switch {
	case errors.Is(err, ErrFileNotFound):
		log.Println("处理文件未找到错误")
	case errors.Is(err, ErrPermissionDenied):
		log.Println("处理权限被拒绝错误")
	case errors.Is(err, context.DeadlineExceeded):
		log.Println("处理超时错误")
	default:
		log.Printf("未知错误: %v", err)
	}
}

// 接口示例
type Formatter interface {
	Format(code string) (string, error)
}

type PythonFormatter struct{}

func (pf *PythonFormatter) Format(code string) (string, error) {
	// 模拟Python代码格式化
	lines := strings.Split(code, "\n")
	formatted := make([]string, len(lines))
	
	for i, line := range lines {
		formatted[i] = strings.TrimSpace(line)
	}
	
	return strings.Join(formatted, "\n"), nil
}

// 泛型示例 (Go 1.18+)
type Stack[T any] struct {
	items []T
	mu    sync.Mutex
}

func NewStack[T any]() *Stack[T] {
	return &Stack[T]{
		items: make([]T, 0),
	}
}

func (s *Stack[T]) Push(item T) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.items = append(s.items, item)
}

func (s *Stack[T]) Pop() (T, bool) {
	s.mu.Lock()
	defer s.mu.Unlock()
	
	var zero T
	if len(s.items) == 0 {
		return zero, false
	}
	
	item := s.items[len(s.items)-1]
	s.items = s.items[:len(s.items)-1]
	return item, true
}

func (s *Stack[T]) Size() int {
	s.mu.Lock()
	defer s.mu.Unlock()
	return len(s.items)
}

// 主函数
func main() {
	// 设置随机种子
	rand.Seed(time.Now().UnixNano())
	
	fmt.Printf("=== %s v%s ===\n", AppName, AppVersion)
	fmt.Printf("启动时间: %s\n", time.Now().Format("2006-01-02 15:04:05"))
	
	// 创建项目管理器
	pm := NewProjectManager()
	
	// 解析命令行参数
	if len(os.Args) < 2 {
		fmt.Println("使用方法:")
		fmt.Printf("  %s serve                    - 启动HTTP服务器\n", os.Args[0])
		fmt.Printf("  %s demo                     - 运行演示\n", os.Args[0])
		fmt.Printf("  %s create <name> <path>     - 创建项目\n", os.Args[0])
		return
	}
	
	command := os.Args[1]
	
	switch command {
	case "serve":
		// 启动HTTP服务器
		server := NewServer(pm)
		
		// 优雅关闭
		go func() {
			if err := server.Start(); err != nil && err != http.ErrServerClosed {
				log.Fatalf("服务器启动失败: %v", err)
			}
		}()
		
		// 等待中断信号
		fmt.Println("按 Ctrl+C 停止服务器")
		select {}
		
	case "demo":
		// 运行演示
		fmt.Println("\n=== 功能演示 ===")
		
		// 创建示例项目
		project, err := pm.CreateProject("示例项目", "Go语言项目演示", ".")
		if err != nil {
			log.Fatalf("创建项目失败: %v", err)
		}
		
		// 扫描文件
		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		defer cancel()
		
		fmt.Println("扫描项目文件...")
		if err := pm.ScanProject(ctx, project.ID); err != nil {
			log.Printf("扫描失败: %v", err)
		}
		
		// 显示统计信息
		totalFiles, totalLines, languages := project.GetStats()
		fmt.Printf("\n项目统计:\n")
		fmt.Printf("  总文件数: %d\n", totalFiles)
		fmt.Printf("  总行数: %d\n", totalLines)
		fmt.Printf("  语言分布:\n")
		for lang, count := range languages {
			fmt.Printf("    %s: %d 个文件\n", lang, count)
		}
		
		// 演示并发处理
		fmt.Println("\n演示并发处理...")
		demonstrateConcurrency(pm, project.ID)
		
		// 演示泛型
		fmt.Println("\n演示泛型Stack...")
		stack := NewStack[string]()
		stack.Push("item1")
		stack.Push("item2")
		stack.Push("item3")
		
		fmt.Printf("Stack大小: %d\n", stack.Size())
		
		for stack.Size() > 0 {
			if item, ok := stack.Pop(); ok {
				fmt.Printf("弹出: %s\n", item)
			}
		}
		
		// 演示接口
		fmt.Println("\n演示接口...")
		var formatter Formatter = &PythonFormatter{}
		code := "def hello():\n    print('Hello, World!')\n"
		formatted, err := formatter.Format(code)
		if err != nil {
			log.Printf("格式化失败: %v", err)
		} else {
			fmt.Printf("格式化后的代码:\n%s\n", formatted)
		}
		
	case "create":
		if len(os.Args) < 4 {
			fmt.Printf("使用方法: %s create <项目名> <项目路径>\n", os.Args[0])
			return
		}
		
		name := os.Args[2]
		path := os.Args[3]
		
		project, err := pm.CreateProject(name, "通过命令行创建", path)
		if err != nil {
			log.Fatalf("创建项目失败: %v", err)
		}
		
		fmt.Printf("项目创建成功: %s (ID: %s)\n", project.Name, project.ID)
		
	default:
		fmt.Printf("未知命令: %s\n", command)
	}
	
	fmt.Println("\n程序执行完成!")
}
