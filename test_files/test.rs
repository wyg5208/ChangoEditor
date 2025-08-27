//! Chango Editor Rust测试文件
//! 展示Rust语言的现代特性和最佳实践
//! 
//! 作者: Chango Team
//! 创建时间: 2024-01-15

use std::collections::{HashMap, HashSet};
use std::error::Error;
use std::fmt;
use std::fs;
use std::io::{self, BufRead, BufReader};
use std::path::{Path, PathBuf};
use std::sync::{Arc, Mutex, RwLock};
use std::thread;
use std::time::{Duration, Instant, SystemTime, UNIX_EPOCH};

// 使用外部 crate (需要在 Cargo.toml 中添加)
use serde::{Deserialize, Serialize};
use tokio;
use uuid::Uuid;

/// 应用程序常量
const APP_NAME: &str = "Chango Editor";
const APP_VERSION: &str = "0.1.0";
const MAX_FILE_SIZE: usize = 100 * 1024 * 1024; // 100MB
const SUPPORTED_EXTENSIONS: &[&str] = &[".rs", ".py", ".js", ".ts", ".go", ".java", ".cpp", ".cs"];

/// 编程语言枚举
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum Language {
    Rust,
    Python,
    JavaScript,
    TypeScript,
    Go,
    Java,
    Cpp,
    CSharp,
    Unknown,
}

impl Language {
    /// 从文件扩展名获取语言类型
    pub fn from_extension(ext: &str) -> Self {
        match ext.to_lowercase().as_str() {
            "rs" => Language::Rust,
            "py" | "pyw" | "pyx" => Language::Python,
            "js" | "jsx" => Language::JavaScript,
            "ts" | "tsx" => Language::TypeScript,
            "go" => Language::Go,
            "java" => Language::Java,
            "cpp" | "cxx" | "cc" | "c++" => Language::Cpp,
            "cs" => Language::CSharp,
            _ => Language::Unknown,
        }
    }
    
    /// 获取语言的关键字
    pub fn keywords(&self) -> &'static [&'static str] {
        match self {
            Language::Rust => &[
                "fn", "let", "mut", "const", "static", "struct", "enum", "impl", "trait",
                "mod", "pub", "use", "crate", "super", "self", "if", "else", "match",
                "for", "while", "loop", "break", "continue", "return", "async", "await",
                "unsafe", "extern", "type", "where", "dyn", "move", "ref", "in",
            ],
            Language::Python => &[
                "def", "class", "if", "else", "elif", "for", "while", "try", "except",
                "finally", "import", "from", "as", "with", "lambda", "yield", "return",
                "pass", "break", "continue", "async", "await", "global", "nonlocal",
            ],
            Language::JavaScript => &[
                "var", "let", "const", "function", "class", "if", "else", "for", "while",
                "do", "switch", "case", "default", "try", "catch", "finally", "return",
                "break", "continue", "throw", "new", "this", "super", "extends", "import",
                "export", "async", "await", "typeof", "instanceof",
            ],
            _ => &[],
        }
    }
}

impl fmt::Display for Language {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let name = match self {
            Language::Rust => "Rust",
            Language::Python => "Python",
            Language::JavaScript => "JavaScript",
            Language::TypeScript => "TypeScript",
            Language::Go => "Go",
            Language::Java => "Java",
            Language::Cpp => "C++",
            Language::CSharp => "C#",
            Language::Unknown => "Unknown",
        };
        write!(f, "{}", name)
    }
}

/// 自定义错误类型
#[derive(Debug)]
pub enum ChangoEditorError {
    IoError(io::Error),
    ParseError(String),
    ValidationError(String),
    NotFound(String),
    PermissionDenied(String),
    FileTooLarge(usize),
}

impl fmt::Display for ChangoEditorError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ChangoEditorError::IoError(err) => write!(f, "IO错误: {}", err),
            ChangoEditorError::ParseError(msg) => write!(f, "解析错误: {}", msg),
            ChangoEditorError::ValidationError(msg) => write!(f, "验证错误: {}", msg),
            ChangoEditorError::NotFound(item) => write!(f, "未找到: {}", item),
            ChangoEditorError::PermissionDenied(msg) => write!(f, "权限被拒绝: {}", msg),
            ChangoEditorError::FileTooLarge(size) => write!(f, "文件过大: {} 字节", size),
        }
    }
}

impl Error for ChangoEditorError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match self {
            ChangoEditorError::IoError(err) => Some(err),
            _ => None,
        }
    }
}

impl From<io::Error> for ChangoEditorError {
    fn from(err: io::Error) -> Self {
        ChangoEditorError::IoError(err)
    }
}

/// 类型别名
type Result<T> = std::result::Result<T, ChangoEditorError>;

/// 文件信息结构体
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FileInfo {
    pub id: Uuid,
    pub path: PathBuf,
    pub name: String,
    pub size: u64,
    pub lines: usize,
    pub language: Language,
    pub encoding: String,
    pub checksum: String,
    pub created_at: SystemTime,
    pub modified_at: SystemTime,
}

impl FileInfo {
    /// 从文件路径创建FileInfo
    pub fn from_path<P: AsRef<Path>>(path: P) -> Result<Self> {
        let path = path.as_ref();
        let metadata = fs::metadata(path)?;
        
        // 检查文件大小
        if metadata.len() > MAX_FILE_SIZE as u64 {
            return Err(ChangoEditorError::FileTooLarge(metadata.len() as usize));
        }
        
        let name = path.file_name()
            .and_then(|n| n.to_str())
            .unwrap_or("unknown")
            .to_string();
        
        let extension = path.extension()
            .and_then(|ext| ext.to_str())
            .unwrap_or("");
        
        let language = Language::from_extension(extension);
        let lines = count_lines(path)?;
        let checksum = calculate_checksum(path)?;
        
        Ok(FileInfo {
            id: Uuid::new_v4(),
            path: path.to_path_buf(),
            name,
            size: metadata.len(),
            lines,
            language,
            encoding: "utf-8".to_string(),
            checksum,
            created_at: metadata.created().unwrap_or(UNIX_EPOCH),
            modified_at: metadata.modified().unwrap_or(UNIX_EPOCH),
        })
    }
    
    /// 检查文件是否支持语法高亮
    pub fn supports_highlighting(&self) -> bool {
        self.language != Language::Unknown
    }
    
    /// 获取相对路径
    pub fn relative_path(&self, base: &Path) -> Option<PathBuf> {
        self.path.strip_prefix(base).ok().map(|p| p.to_path_buf())
    }
}

/// 项目配置
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProjectConfig {
    pub auto_save: bool,
    pub auto_save_interval: Duration,
    pub max_backups: usize,
    pub enable_git: bool,
    pub exclude_patterns: Vec<String>,
    pub syntax_themes: HashMap<Language, String>,
}

impl Default for ProjectConfig {
    fn default() -> Self {
        let mut syntax_themes = HashMap::new();
        syntax_themes.insert(Language::Rust, "rust-dark".to_string());
        syntax_themes.insert(Language::Python, "python-dark".to_string());
        syntax_themes.insert(Language::JavaScript, "js-dark".to_string());
        
        Self {
            auto_save: false,
            auto_save_interval: Duration::from_secs(300),
            max_backups: 5,
            enable_git: true,
            exclude_patterns: vec![
                "*.tmp".to_string(),
                "*.bak".to_string(),
                ".git/*".to_string(),
                "target/*".to_string(),
                "node_modules/*".to_string(),
            ],
            syntax_themes,
        }
    }
}

/// 项目结构体
#[derive(Debug)]
pub struct Project {
    pub id: Uuid,
    pub name: String,
    pub description: String,
    pub path: PathBuf,
    pub config: ProjectConfig,
    files: RwLock<HashMap<Uuid, FileInfo>>,
    file_index: RwLock<HashMap<PathBuf, Uuid>>,
    created_at: SystemTime,
    updated_at: RwLock<SystemTime>,
}

impl Project {
    /// 创建新项目
    pub fn new<S: Into<String>, P: AsRef<Path>>(
        name: S,
        description: S,
        path: P,
    ) -> Result<Self> {
        let path = path.as_ref().to_path_buf();
        
        if !path.exists() {
            return Err(ChangoEditorError::NotFound(format!("路径不存在: {:?}", path)));
        }
        
        if !path.is_dir() {
            return Err(ChangoEditorError::ValidationError("路径必须是目录".to_string()));
        }
        
        Ok(Project {
            id: Uuid::new_v4(),
            name: name.into(),
            description: description.into(),
            path,
            config: ProjectConfig::default(),
            files: RwLock::new(HashMap::new()),
            file_index: RwLock::new(HashMap::new()),
            created_at: SystemTime::now(),
            updated_at: RwLock::new(SystemTime::now()),
        })
    }
    
    /// 扫描项目文件
    pub fn scan_files(&self) -> Result<usize> {
        let mut file_count = 0;
        
        for entry in walkdir::WalkDir::new(&self.path)
            .follow_links(false)
            .into_iter()
            .filter_map(|e| e.ok())
        {
            if entry.file_type().is_file() {
                if let Some(extension) = entry.path().extension() {
                    if SUPPORTED_EXTENSIONS.iter().any(|&ext| {
                        extension.to_str().unwrap_or("").ends_with(&ext[1..])
                    }) {
                        match FileInfo::from_path(entry.path()) {
                            Ok(file_info) => {
                                self.add_file(file_info)?;
                                file_count += 1;
                            }
                            Err(e) => {
                                eprintln!("跳过文件 {:?}: {}", entry.path(), e);
                            }
                        }
                    }
                }
            }
        }
        
        self.update_timestamp();
        Ok(file_count)
    }
    
    /// 添加文件
    pub fn add_file(&self, file_info: FileInfo) -> Result<()> {
        let file_id = file_info.id;
        let file_path = file_info.path.clone();
        
        {
            let mut files = self.files.write().unwrap();
            let mut index = self.file_index.write().unwrap();
            
            files.insert(file_id, file_info);
            index.insert(file_path, file_id);
        }
        
        self.update_timestamp();
        Ok(())
    }
    
    /// 获取文件
    pub fn get_file(&self, id: &Uuid) -> Option<FileInfo> {
        self.files.read().unwrap().get(id).cloned()
    }
    
    /// 通过路径查找文件
    pub fn find_file_by_path<P: AsRef<Path>>(&self, path: P) -> Option<FileInfo> {
        let path = path.as_ref();
        let index = self.file_index.read().unwrap();
        let files = self.files.read().unwrap();
        
        index.get(path)
            .and_then(|id| files.get(id))
            .cloned()
    }
    
    /// 获取所有文件
    pub fn get_all_files(&self) -> Vec<FileInfo> {
        self.files.read().unwrap().values().cloned().collect()
    }
    
    /// 按语言分组文件
    pub fn group_by_language(&self) -> HashMap<Language, Vec<FileInfo>> {
        let mut groups: HashMap<Language, Vec<FileInfo>> = HashMap::new();
        
        for file in self.get_all_files() {
            groups.entry(file.language).or_default().push(file);
        }
        
        groups
    }
    
    /// 获取项目统计
    pub fn get_statistics(&self) -> ProjectStatistics {
        let files = self.get_all_files();
        let mut language_stats = HashMap::new();
        let mut total_lines = 0;
        let mut total_size = 0;
        
        for file in &files {
            total_lines += file.lines;
            total_size += file.size;
            
            let stats = language_stats.entry(file.language).or_insert(LanguageStats {
                file_count: 0,
                line_count: 0,
                byte_count: 0,
            });
            
            stats.file_count += 1;
            stats.line_count += file.lines;
            stats.byte_count += file.size;
        }
        
        ProjectStatistics {
            total_files: files.len(),
            total_lines,
            total_size,
            language_stats,
            created_at: self.created_at,
            updated_at: *self.updated_at.read().unwrap(),
        }
    }
    
    /// 搜索文件
    pub fn search_files(&self, query: &str) -> Vec<FileInfo> {
        let query = query.to_lowercase();
        
        self.get_all_files()
            .into_iter()
            .filter(|file| {
                file.name.to_lowercase().contains(&query) ||
                file.path.to_string_lossy().to_lowercase().contains(&query)
            })
            .collect()
    }
    
    /// 更新时间戳
    fn update_timestamp(&self) {
        *self.updated_at.write().unwrap() = SystemTime::now();
    }
}

/// 语言统计信息
#[derive(Debug, Clone)]
pub struct LanguageStats {
    pub file_count: usize,
    pub line_count: usize,
    pub byte_count: u64,
}

/// 项目统计信息
#[derive(Debug, Clone)]
pub struct ProjectStatistics {
    pub total_files: usize,
    pub total_lines: usize,
    pub total_size: u64,
    pub language_stats: HashMap<Language, LanguageStats>,
    pub created_at: SystemTime,
    pub updated_at: SystemTime,
}

/// 项目管理器
pub struct ProjectManager {
    projects: Arc<RwLock<HashMap<Uuid, Arc<Project>>>>,
    recent_projects: Arc<Mutex<Vec<Uuid>>>,
}

impl ProjectManager {
    /// 创建新的项目管理器
    pub fn new() -> Self {
        Self {
            projects: Arc::new(RwLock::new(HashMap::new())),
            recent_projects: Arc::new(Mutex::new(Vec::new())),
        }
    }
    
    /// 创建项目
    pub fn create_project<S: Into<String>, P: AsRef<Path>>(
        &self,
        name: S,
        description: S,
        path: P,
    ) -> Result<Arc<Project>> {
        let project = Arc::new(Project::new(name, description, path)?);
        let project_id = project.id;
        
        {
            let mut projects = self.projects.write().unwrap();
            projects.insert(project_id, project.clone());
        }
        
        self.add_to_recent(project_id);
        
        println!("创建项目: {} (ID: {})", project.name, project.id);
        Ok(project)
    }
    
    /// 获取项目
    pub fn get_project(&self, id: &Uuid) -> Option<Arc<Project>> {
        self.projects.read().unwrap().get(id).cloned()
    }
    
    /// 获取所有项目
    pub fn get_all_projects(&self) -> Vec<Arc<Project>> {
        self.projects.read().unwrap().values().cloned().collect()
    }
    
    /// 删除项目
    pub fn remove_project(&self, id: &Uuid) -> Result<()> {
        let mut projects = self.projects.write().unwrap();
        
        if projects.remove(id).is_some() {
            self.remove_from_recent(id);
            println!("删除项目: {}", id);
            Ok(())
        } else {
            Err(ChangoEditorError::NotFound(format!("项目不存在: {}", id)))
        }
    }
    
    /// 获取最近项目
    pub fn get_recent_projects(&self, limit: usize) -> Vec<Arc<Project>> {
        let recent = self.recent_projects.lock().unwrap();
        let projects = self.projects.read().unwrap();
        
        recent
            .iter()
            .take(limit)
            .filter_map(|id| projects.get(id).cloned())
            .collect()
    }
    
    /// 添加到最近项目
    fn add_to_recent(&self, project_id: Uuid) {
        let mut recent = self.recent_projects.lock().unwrap();
        
        // 移除已存在的条目
        recent.retain(|&id| id != project_id);
        
        // 添加到开头
        recent.insert(0, project_id);
        
        // 限制最大数量
        recent.truncate(10);
    }
    
    /// 从最近项目中移除
    fn remove_from_recent(&self, project_id: &Uuid) {
        let mut recent = self.recent_projects.lock().unwrap();
        recent.retain(|id| id != project_id);
    }
}

impl Default for ProjectManager {
    fn default() -> Self {
        Self::new()
    }
}

/// 语法高亮器特征
pub trait SyntaxHighlighter {
    fn highlight(&self, code: &str, language: Language) -> Result<String>;
    fn get_keywords(&self, language: Language) -> &[&str];
}

/// 简单语法高亮器实现
pub struct SimpleSyntaxHighlighter {
    keyword_patterns: HashMap<Language, regex::Regex>,
}

impl SimpleSyntaxHighlighter {
    pub fn new() -> Result<Self> {
        let mut keyword_patterns = HashMap::new();
        
        for &language in &[Language::Rust, Language::Python, Language::JavaScript] {
            let keywords = language.keywords();
            let pattern = format!(r"\b({})\b", keywords.join("|"));
            let regex = regex::Regex::new(&pattern)
                .map_err(|e| ChangoEditorError::ParseError(e.to_string()))?;
            keyword_patterns.insert(language, regex);
        }
        
        Ok(Self {
            keyword_patterns,
        })
    }
}

impl SyntaxHighlighter for SimpleSyntaxHighlighter {
    fn highlight(&self, code: &str, language: Language) -> Result<String> {
        if let Some(regex) = self.keyword_patterns.get(&language) {
            let highlighted = regex.replace_all(code, "<keyword>$1</keyword>");
            Ok(highlighted.to_string())
        } else {
            Ok(code.to_string())
        }
    }
    
    fn get_keywords(&self, language: Language) -> &[&str] {
        language.keywords()
    }
}

/// 文件处理器特征
pub trait FileProcessor: Send + Sync {
    fn process(&self, file: &FileInfo) -> Result<()>;
    fn get_name(&self) -> &str;
}

/// 并发文件处理器
pub struct ConcurrentFileProcessor<T: FileProcessor> {
    processor: Arc<T>,
    worker_count: usize,
}

impl<T: FileProcessor + 'static> ConcurrentFileProcessor<T> {
    pub fn new(processor: T, worker_count: usize) -> Self {
        Self {
            processor: Arc::new(processor),
            worker_count,
        }
    }
    
    /// 并发处理文件列表
    pub fn process_files(&self, files: Vec<FileInfo>) -> Result<Vec<Result<()>>> {
        let (tx, rx) = crossbeam_channel::bounded(files.len());
        let results = Arc::new(Mutex::new(Vec::new()));
        
        // 启动工作线程
        let mut handles = vec![];
        for worker_id in 0..self.worker_count {
            let rx = rx.clone();
            let processor = self.processor.clone();
            let results = results.clone();
            
            let handle = thread::spawn(move || {
                while let Ok((index, file)) = rx.recv() {
                    println!("工作线程 {} 处理文件: {}", worker_id, file.name);
                    let result = processor.process(&file);
                    
                    {
                        let mut results = results.lock().unwrap();
                        results.push((index, result));
                    }
                }
            });
            
            handles.push(handle);
        }
        
        // 发送任务
        for (index, file) in files.into_iter().enumerate() {
            tx.send((index, file)).unwrap();
        }
        drop(tx);
        
        // 等待完成
        for handle in handles {
            handle.join().unwrap();
        }
        
        // 收集结果
        let mut results = results.lock().unwrap();
        results.sort_by_key(|(index, _)| *index);
        
        Ok(results.into_iter().map(|(_, result)| result).collect())
    }
}

/// 代码格式化器
pub struct CodeFormatter;

impl FileProcessor for CodeFormatter {
    fn process(&self, file: &FileInfo) -> Result<()> {
        match file.language {
            Language::Rust => {
                println!("格式化Rust代码: {}", file.name);
                // 模拟rustfmt处理
                thread::sleep(Duration::from_millis(100));
            }
            Language::Python => {
                println!("格式化Python代码: {}", file.name);
                // 模拟black处理
                thread::sleep(Duration::from_millis(80));
            }
            Language::JavaScript => {
                println!("格式化JavaScript代码: {}", file.name);
                // 模拟prettier处理
                thread::sleep(Duration::from_millis(60));
            }
            _ => {
                println!("跳过不支持的语言: {} ({})", file.name, file.language);
            }
        }
        Ok(())
    }
    
    fn get_name(&self) -> &str {
        "CodeFormatter"
    }
}

/// 异步文件服务
pub struct AsyncFileService {
    project_manager: Arc<ProjectManager>,
}

impl AsyncFileService {
    pub fn new(project_manager: Arc<ProjectManager>) -> Self {
        Self { project_manager }
    }
    
    /// 异步扫描项目
    pub async fn scan_project_async(&self, project_id: Uuid) -> Result<usize> {
        let project = self.project_manager
            .get_project(&project_id)
            .ok_or_else(|| ChangoEditorError::NotFound(format!("项目不存在: {}", project_id)))?;
        
        // 在异步上下文中执行CPU密集型任务
        let project_clone = project.clone();
        let result = tokio::task::spawn_blocking(move || {
            project_clone.scan_files()
        }).await;
        
        match result {
            Ok(count) => count,
            Err(e) => Err(ChangoEditorError::ParseError(format!("异步任务失败: {}", e))),
        }
    }
    
    /// 异步搜索文件
    pub async fn search_files_async(&self, project_id: Uuid, query: String) -> Result<Vec<FileInfo>> {
        let project = self.project_manager
            .get_project(&project_id)
            .ok_or_else(|| ChangoEditorError::NotFound(format!("项目不存在: {}", project_id)))?;
        
        let project_clone = project.clone();
        let result = tokio::task::spawn_blocking(move || {
            project_clone.search_files(&query)
        }).await;
        
        match result {
            Ok(files) => Ok(files),
            Err(e) => Err(ChangoEditorError::ParseError(format!("搜索失败: {}", e))),
        }
    }
}

// 工具函数

/// 计算文件行数
fn count_lines<P: AsRef<Path>>(path: P) -> Result<usize> {
    let file = fs::File::open(path)?;
    let reader = BufReader::new(file);
    Ok(reader.lines().count())
}

/// 计算文件校验和
fn calculate_checksum<P: AsRef<Path>>(path: P) -> Result<String> {
    let content = fs::read(path)?;
    let hash = sha2::Sha256::digest(&content);
    Ok(format!("{:x}", hash))
}

/// 性能基准测试
pub fn benchmark_file_processing() -> Result<()> {
    println!("=== 性能基准测试 ===");
    
    // 创建测试项目
    let temp_dir = std::env::temp_dir().join("chango_editor_benchmark");
    fs::create_dir_all(&temp_dir)?;
    
    let pm = ProjectManager::new();
    let project = pm.create_project(
        "基准测试项目",
        "性能测试项目",
        &temp_dir,
    )?;
    
    // 生成测试文件
    let test_files = generate_test_files(&temp_dir, 100)?;
    
    // 添加文件到项目
    for file_path in test_files {
        if let Ok(file_info) = FileInfo::from_path(&file_path) {
            project.add_file(file_info)?;
        }
    }
    
    // 基准测试：文件扫描
    let start = Instant::now();
    let file_count = project.scan_files()?;
    let scan_duration = start.elapsed();
    
    println!("扫描 {} 个文件耗时: {:?}", file_count, scan_duration);
    
    // 基准测试：文件搜索
    let start = Instant::now();
    let results = project.search_files("test");
    let search_duration = start.elapsed();
    
    println!("搜索找到 {} 个文件，耗时: {:?}", results.len(), search_duration);
    
    // 基准测试：并发处理
    let files = project.get_all_files();
    let formatter = CodeFormatter;
    let processor = ConcurrentFileProcessor::new(formatter, 4);
    
    let start = Instant::now();
    let results = processor.process_files(files)?;
    let process_duration = start.elapsed();
    
    let success_count = results.iter().filter(|r| r.is_ok()).count();
    println!("并发处理 {} 个文件成功，耗时: {:?}", success_count, process_duration);
    
    // 清理测试文件
    fs::remove_dir_all(&temp_dir)?;
    
    Ok(())
}

/// 生成测试文件
fn generate_test_files(dir: &Path, count: usize) -> Result<Vec<PathBuf>> {
    let mut files = Vec::new();
    let languages = &[Language::Rust, Language::Python, Language::JavaScript];
    
    for i in 0..count {
        let lang = languages[i % languages.len()];
        let extension = match lang {
            Language::Rust => "rs",
            Language::Python => "py", 
            Language::JavaScript => "js",
            _ => "txt",
        };
        
        let filename = format!("test_file_{}.{}", i, extension);
        let file_path = dir.join(&filename);
        
        let content = generate_sample_code(lang, i);
        fs::write(&file_path, content)?;
        
        files.push(file_path);
    }
    
    Ok(files)
}

/// 生成示例代码
fn generate_sample_code(language: Language, index: usize) -> String {
    match language {
        Language::Rust => format!(
            "// 测试文件 {}\n\
            fn main() {{\n\
                println!(\"Hello from Rust file {}!\");\n\
                let x = {};\n\
                let y = x * 2;\n\
                println!(\"Result: {{}}\", y);\n\
            }}\n",
            index, index, index
        ),
        Language::Python => format!(
            "# 测试文件 {}\n\
            def main():\n\
                print(\"Hello from Python file {}!\")\n\
                x = {}\n\
                y = x * 2\n\
                print(f\"Result: {{y}}\")\n\
            \n\
            if __name__ == \"__main__\":\n\
                main()\n",
            index, index, index
        ),
        Language::JavaScript => format!(
            "// 测试文件 {}\n\
            function main() {{\n\
                console.log(\"Hello from JavaScript file {}!\");\n\
                const x = {};\n\
                const y = x * 2;\n\
                console.log(`Result: ${{y}}`);\n\
            }}\n\
            \n\
            main();\n",
            index, index, index
        ),
        _ => format!("# 未知语言测试文件 {}\n", index),
    }
}

/// 异步主函数演示
#[tokio::main]
async fn async_demo() -> Result<()> {
    println!("=== 异步功能演示 ===");
    
    let pm = Arc::new(ProjectManager::new());
    let service = AsyncFileService::new(pm.clone());
    
    // 创建测试项目
    let temp_dir = std::env::temp_dir().join("chango_editor_async_demo");
    fs::create_dir_all(&temp_dir)?;
    
    let project = pm.create_project(
        "异步演示项目", 
        "异步功能测试项目",
        &temp_dir,
    )?;
    
    // 生成测试文件
    generate_test_files(&temp_dir, 50)?;
    
    // 异步扫描
    println!("开始异步扫描...");
    let start = Instant::now();
    let file_count = service.scan_project_async(project.id).await?;
    let duration = start.elapsed();
    
    println!("异步扫描完成: {} 个文件，耗时: {:?}", file_count, duration);
    
    // 异步搜索
    println!("开始异步搜索...");
    let start = Instant::now();
    let results = service.search_files_async(project.id, "test".to_string()).await?;
    let duration = start.elapsed();
    
    println!("异步搜索完成: {} 个结果，耗时: {:?}", results.len(), duration);
    
    // 清理
    fs::remove_dir_all(&temp_dir)?;
    
    Ok(())
}

/// 主函数
fn main() -> Result<()> {
    println!("=== {} v{} ===", APP_NAME, APP_VERSION);
    println!("启动时间: {}", chrono::Local::now().format("%Y-%m-%d %H:%M:%S"));
    
    // 解析命令行参数
    let args: Vec<String> = std::env::args().collect();
    
    if args.len() < 2 {
        println!("使用方法:");
        println!("  {} demo          - 运行功能演示", args[0]);
        println!("  {} benchmark     - 运行性能基准测试", args[0]);
        println!("  {} async         - 运行异步功能演示", args[0]);
        println!("  {} create <name> <path> - 创建项目", args[0]);
        return Ok(());
    }
    
    match args[1].as_str() {
        "demo" => {
            // 功能演示
            println!("\n=== 功能演示 ===");
            
            let pm = ProjectManager::new();
            
            // 创建示例项目
            let project = pm.create_project(
                "Rust示例项目",
                "展示Rust语言特性",
                ".",
            )?;
            
            // 扫描文件
            let file_count = project.scan_files()?;
            println!("扫描到 {} 个文件", file_count);
            
            // 显示统计信息
            let stats = project.get_statistics();
            println!("\n项目统计:");
            println!("  总文件数: {}", stats.total_files);
            println!("  总行数: {}", stats.total_lines);
            println!("  总大小: {} 字节", stats.total_size);
            
            println!("\n语言分布:");
            for (language, lang_stats) in stats.language_stats {
                println!("  {}: {} 个文件, {} 行代码", 
                    language, lang_stats.file_count, lang_stats.line_count);
            }
            
            // 演示搜索
            let search_results = project.search_files("test");
            println!("\n搜索 'test' 找到 {} 个文件", search_results.len());
            
            // 演示并发处理
            let files = project.get_all_files();
            if !files.is_empty() {
                println!("\n演示并发处理...");
                let formatter = CodeFormatter;
                let processor = ConcurrentFileProcessor::new(formatter, 3);
                
                let start = Instant::now();
                let results = processor.process_files(files.clone())?;
                let duration = start.elapsed();
                
                let success_count = results.iter().filter(|r| r.is_ok()).count();
                println!("并发处理完成: {}/{} 成功，耗时: {:?}", 
                    success_count, files.len(), duration);
            }
            
            // 演示语法高亮
            if let Ok(highlighter) = SimpleSyntaxHighlighter::new() {
                let sample_code = "fn main() { let x = 42; println!(\"Hello, Rust!\"); }";
                let highlighted = highlighter.highlight(sample_code, Language::Rust)?;
                println!("\n语法高亮演示:");
                println!("原代码: {}", sample_code);
                println!("高亮后: {}", highlighted);
            }
        }
        
        "benchmark" => {
            benchmark_file_processing()?;
        }
        
        "async" => {
            // 运行异步演示
            tokio::runtime::Runtime::new()
                .unwrap()
                .block_on(async_demo())?;
        }
        
        "create" => {
            if args.len() < 4 {
                println!("使用方法: {} create <项目名> <项目路径>", args[0]);
                return Ok(());
            }
            
            let name = &args[2];
            let path = &args[3];
            
            let pm = ProjectManager::new();
            let project = pm.create_project(name, "通过命令行创建", path)?;
            
            println!("项目创建成功: {} (ID: {})", project.name, project.id);
            
            let file_count = project.scan_files()?;
            println!("扫描到 {} 个文件", file_count);
        }
        
        _ => {
            println!("未知命令: {}", args[1]);
            return Ok(());
        }
    }
    
    println!("\n程序执行完成!");
    Ok(())
}
