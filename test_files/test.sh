#!/bin/bash
#
# Chango Editor - Shell脚本测试文件
# 展示Bash脚本语法和各种Shell编程特性
# 
# 作者: Chango Team
# 创建时间: 2024-01-15
# 版本: 1.0
#

# 设置错误处理
set -euo pipefail  # 遇到错误立即退出，使用未定义变量时报错，管道命令失败时退出
IFS=$'\n\t'        # 设置字段分隔符

# 全局变量
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_NAME="$(basename "$0")"
readonly TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S')"
readonly LOG_FILE="${SCRIPT_DIR}/chango_editor_test.log"
readonly TEMP_DIR="/tmp/chango_editor_$$"

# 颜色代码
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly PURPLE='\033[0;35m'
readonly CYAN='\033[0;36m'
readonly WHITE='\033[1;37m'
readonly NC='\033[0m' # No Color

# 日志级别
readonly LOG_DEBUG=0
readonly LOG_INFO=1
readonly LOG_WARN=2
readonly LOG_ERROR=3

# 配置变量
DEBUG_MODE=${DEBUG_MODE:-false}
VERBOSE=${VERBOSE:-false}
DRY_RUN=${DRY_RUN:-false}
LOG_LEVEL=${LOG_LEVEL:-$LOG_INFO}

# 帮助信息
usage() {
    cat << EOF
使用方法: $SCRIPT_NAME [选项] [命令]

Chango Editor Shell脚本测试工具

选项:
    -h, --help          显示帮助信息
    -v, --verbose       详细输出
    -d, --debug         调试模式
    -n, --dry-run       仅显示将要执行的命令
    -l, --log-level     设置日志级别 (0-3)
    -o, --output DIR    输出目录

命令:
    install             安装 Chango Editor
    test                运行测试
    build               构建项目
    clean               清理临时文件
    setup               初始化开发环境
    benchmark           性能基准测试

示例:
    $SCRIPT_NAME install
    $SCRIPT_NAME --verbose test
    $SCRIPT_NAME --debug --dry-run build

环境变量:
    CHANGO_EDITOR_HOME  Chango Editor安装目录
    PYTHON_VERSION      指定Python版本
    BUILD_TYPE          构建类型 (debug|release)

EOF
}

# 日志函数
log() {
    local level=$1
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    case $level in
        $LOG_DEBUG)
            [[ $LOG_LEVEL -le $LOG_DEBUG ]] && echo -e "${CYAN}[DEBUG]${NC} $message" | tee -a "$LOG_FILE"
            ;;
        $LOG_INFO)
            [[ $LOG_LEVEL -le $LOG_INFO ]] && echo -e "${GREEN}[INFO]${NC} $message" | tee -a "$LOG_FILE"
            ;;
        $LOG_WARN)
            [[ $LOG_LEVEL -le $LOG_WARN ]] && echo -e "${YELLOW}[WARN]${NC} $message" | tee -a "$LOG_FILE" >&2
            ;;
        $LOG_ERROR)
            [[ $LOG_LEVEL -le $LOG_ERROR ]] && echo -e "${RED}[ERROR]${NC} $message" | tee -a "$LOG_FILE" >&2
            ;;
    esac
}

# 便捷日志函数
debug() { log $LOG_DEBUG "$@"; }
info() { log $LOG_INFO "$@"; }
warn() { log $LOG_WARN "$@"; }
error() { log $LOG_ERROR "$@"; }

# 检查依赖
check_dependencies() {
    local deps=("python3" "pip" "git" "wget" "curl")
    local missing=()
    
    info "检查系统依赖..."
    
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            missing+=("$dep")
        else
            debug "✓ $dep 已安装: $(command -v "$dep")"
        fi
    done
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        error "缺少依赖: ${missing[*]}"
        error "请安装缺少的依赖后重试"
        return 1
    fi
    
    info "所有依赖检查通过"
    return 0
}

# 检测操作系统
detect_os() {
    local os_name=""
    local os_version=""
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        os_name="Linux"
        if [[ -f /etc/os-release ]]; then
            # shellcheck source=/dev/null
            source /etc/os-release
            os_version="$NAME $VERSION"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        os_name="macOS"
        os_version=$(sw_vers -productVersion)
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]]; then
        os_name="Windows"
        os_version=$(cmd.exe /c ver 2>/dev/null | grep -o '[0-9]*\.[0-9]*\.[0-9]*')
    else
        os_name="Unknown"
        os_version="Unknown"
    fi
    
    info "操作系统: $os_name $os_version"
    echo "$os_name"
}

# 创建临时目录
create_temp_dir() {
    if [[ ! -d "$TEMP_DIR" ]]; then
        mkdir -p "$TEMP_DIR"
        debug "创建临时目录: $TEMP_DIR"
    fi
}

# 清理函数
cleanup() {
    local exit_code=$?
    
    debug "清理临时文件..."
    
    if [[ -d "$TEMP_DIR" ]]; then
        rm -rf "$TEMP_DIR"
        debug "删除临时目录: $TEMP_DIR"
    fi
    
    if [[ $exit_code -ne 0 ]]; then
        error "脚本异常退出 (退出码: $exit_code)"
    else
        info "脚本正常退出"
    fi
    
    exit $exit_code
}

# 信号处理
handle_signal() {
    local signal=$1
    warn "收到信号: $signal"
    cleanup
}

# 执行命令
execute_command() {
    local cmd="$1"
    local description="${2:-执行命令}"
    
    info "$description: $cmd"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        info "[DRY RUN] 将要执行: $cmd"
        return 0
    fi
    
    if [[ "$VERBOSE" == "true" ]]; then
        eval "$cmd"
    else
        eval "$cmd" &> /dev/null
    fi
    
    local exit_code=$?
    if [[ $exit_code -eq 0 ]]; then
        debug "命令执行成功"
    else
        error "命令执行失败 (退出码: $exit_code)"
        return $exit_code
    fi
}

# 下载文件
download_file() {
    local url="$1"
    local output_file="$2"
    local description="${3:-下载文件}"
    
    info "$description..."
    
    if command -v curl &> /dev/null; then
        execute_command "curl -L -o '$output_file' '$url'" "使用curl下载"
    elif command -v wget &> /dev/null; then
        execute_command "wget -O '$output_file' '$url'" "使用wget下载"
    else
        error "未找到下载工具 (curl 或 wget)"
        return 1
    fi
}

# Python环境检查
check_python_environment() {
    local python_cmd="python3"
    local min_version="3.8"
    
    info "检查Python环境..."
    
    if ! command -v "$python_cmd" &> /dev/null; then
        error "未找到 $python_cmd"
        return 1
    fi
    
    local python_version
    python_version=$($python_cmd --version 2>&1 | cut -d' ' -f2)
    info "Python版本: $python_version"
    
    # 版本比较 (简化版)
    if [[ "$(printf '%s\n' "$min_version" "$python_version" | sort -V | head -n1)" != "$min_version" ]]; then
        error "Python版本过低，最低要求: $min_version"
        return 1
    fi
    
    # 检查虚拟环境
    if [[ -n "${VIRTUAL_ENV:-}" ]]; then
        info "当前在虚拟环境中: $VIRTUAL_ENV"
    else
        warn "未在虚拟环境中，建议创建虚拟环境"
    fi
    
    return 0
}

# 安装Chango Editor
install_chango_editor() {
    info "开始安装 Chango Editor..."
    
    create_temp_dir
    
    # 检查依赖
    check_dependencies || return 1
    check_python_environment || return 1
    
    # 克隆仓库
    local repo_url="https://github.com/chango_editor/chango_editor-lite.git"
    local install_dir="${CHANGO_EDITOR_HOME:-$HOME/.chango_editor}"
    
    if [[ -d "$install_dir" ]]; then
        warn "安装目录已存在: $install_dir"
        read -p "是否覆盖安装? (y/N): " -r
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            info "安装取消"
            return 0
        fi
        execute_command "rm -rf '$install_dir'" "删除现有安装"
    fi
    
    execute_command "git clone '$repo_url' '$install_dir'" "克隆代码仓库"
    
    # 进入安装目录
    cd "$install_dir"
    
    # 创建虚拟环境
    execute_command "python3 -m venv venv" "创建虚拟环境"
    
    # 激活虚拟环境
    # shellcheck source=/dev/null
    source venv/bin/activate
    
    # 升级pip
    execute_command "pip install --upgrade pip" "升级pip"
    
    # 安装依赖
    if [[ -f "requirements.txt" ]]; then
        execute_command "pip install -r requirements.txt" "安装依赖包"
    else
        warn "未找到 requirements.txt 文件"
    fi
    
    # 创建启动脚本
    local start_script="$install_dir/chango_editor"
    cat > "$start_script" << 'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/venv/bin/activate"
python "$SCRIPT_DIR/src/main.py" "$@"
EOF
    
    chmod +x "$start_script"
    
    # 创建桌面快捷方式 (Linux)
    if [[ "$(detect_os)" == "Linux" ]] && command -v desktop-file-install &> /dev/null; then
        local desktop_file="$HOME/.local/share/applications/chango_editor-lite.desktop"
        cat > "$desktop_file" << EOF
[Desktop Entry]
Name=Chango Editor
Comment=轻量级代码编辑器
Exec=$start_script
Icon=$install_dir/resources/icons/chango_editor.png
Terminal=false
Type=Application
Categories=Development;TextEditor;
EOF
        info "创建桌面快捷方式: $desktop_file"
    fi
    
    info "Chango Editor 安装完成!"
    info "安装目录: $install_dir"
    info "启动命令: $start_script"
    
    return 0
}

# 运行测试
run_tests() {
    info "运行 Chango Editor 测试套件..."
    
    # 检查测试环境
    if [[ ! -d "tests" ]]; then
        error "未找到测试目录"
        return 1
    fi
    
    # 安装测试依赖
    if [[ -f "requirements-test.txt" ]]; then
        execute_command "pip install -r requirements-test.txt" "安装测试依赖"
    fi
    
    # 运行单元测试
    execute_command "python -m pytest tests/ -v --tb=short" "运行单元测试"
    
    # 运行语法检查
    if command -v flake8 &> /dev/null; then
        execute_command "flake8 src/ tests/" "运行代码风格检查"
    fi
    
    # 运行类型检查
    if command -v mypy &> /dev/null; then
        execute_command "mypy src/" "运行类型检查"
    fi
    
    info "测试完成"
    return 0
}

# 构建项目
build_project() {
    local build_type="${BUILD_TYPE:-release}"
    
    info "构建 Chango Editor (类型: $build_type)..."
    
    create_temp_dir
    
    # 清理之前的构建
    execute_command "rm -rf build/ dist/ *.egg-info/" "清理构建目录"
    
    # 构建Python包
    execute_command "python setup.py sdist bdist_wheel" "构建Python包"
    
    # 创建可执行文件 (使用PyInstaller)
    if command -v pyinstaller &> /dev/null; then
        local pyinstaller_args="--onefile --windowed"
        
        if [[ "$build_type" == "debug" ]]; then
            pyinstaller_args+=" --debug"
        fi
        
        execute_command "pyinstaller $pyinstaller_args src/main.py -n chango_editor-lite" "创建可执行文件"
    else
        warn "未找到 PyInstaller，跳过可执行文件创建"
    fi
    
    info "构建完成"
    info "构建产物:"
    find dist/ -type f -exec ls -lh {} \; 2>/dev/null | while read -r line; do
        info "  $line"
    done
    
    return 0
}

# 性能基准测试
run_benchmark() {
    info "运行性能基准测试..."
    
    create_temp_dir
    
    # 创建测试文件
    local test_files=(
        "$TEMP_DIR/small.py"
        "$TEMP_DIR/medium.py"
        "$TEMP_DIR/large.py"
    )
    
    # 生成不同大小的Python测试文件
    for ((i=0; i<100; i++)); do
        echo "def function_$i(): pass" >> "${test_files[0]}"
    done
    
    for ((i=0; i<1000; i++)); do
        echo "def function_$i(): pass" >> "${test_files[1]}"
    done
    
    for ((i=0; i<10000; i++)); do
        echo "def function_$i(): pass" >> "${test_files[2]}"
    done
    
    # 测试启动时间
    info "测试启动时间..."
    local start_time
    local end_time
    local duration
    
    for i in {1..3}; do
        start_time=$(date +%s.%N)
        execute_command "timeout 10s python src/main.py --help > /dev/null" "启动测试 $i"
        end_time=$(date +%s.%N)
        duration=$(echo "$end_time - $start_time" | bc)
        info "启动时间 $i: ${duration}s"
    done
    
    # 测试文件加载时间
    info "测试文件加载时间..."
    for test_file in "${test_files[@]}"; do
        local file_size
        file_size=$(stat -f%z "$test_file" 2>/dev/null || stat -c%s "$test_file" 2>/dev/null)
        info "测试文件: $(basename "$test_file") (${file_size} 字节)"
        
        start_time=$(date +%s.%N)
        execute_command "timeout 30s python src/main.py '$test_file' &" "加载测试文件"
        sleep 2
        killall python 2>/dev/null || true
        end_time=$(date +%s.%N)
        duration=$(echo "$end_time - $start_time" | bc)
        info "加载时间: ${duration}s"
    done
    
    info "性能基准测试完成"
    return 0
}

# 清理临时文件
clean_project() {
    info "清理项目临时文件..."
    
    local clean_patterns=(
        "__pycache__"
        "*.pyc"
        "*.pyo"
        "*.pyd"
        ".pytest_cache"
        ".coverage"
        "htmlcov"
        "build"
        "dist"
        "*.egg-info"
        ".mypy_cache"
        ".tox"
        "venv"
        ".venv"
        "node_modules"
        ".DS_Store"
        "Thumbs.db"
    )
    
    for pattern in "${clean_patterns[@]}"; do
        # 使用find命令安全删除
        find . -name "$pattern" -type d -exec rm -rf {} + 2>/dev/null || true
        find . -name "$pattern" -type f -delete 2>/dev/null || true
    done
    
    # 清理日志文件
    if [[ -f "$LOG_FILE" ]]; then
        > "$LOG_FILE"  # 清空日志文件
        debug "清空日志文件: $LOG_FILE"
    fi
    
    info "清理完成"
    return 0
}

# 初始化开发环境
setup_dev_environment() {
    info "初始化开发环境..."
    
    # 检查Git配置
    if ! git config --get user.name &> /dev/null; then
        warn "Git用户名未配置"
        read -p "请输入Git用户名: " -r git_name
        git config --global user.name "$git_name"
    fi
    
    if ! git config --get user.email &> /dev/null; then
        warn "Git邮箱未配置"
        read -p "请输入Git邮箱: " -r git_email
        git config --global user.email "$git_email"
    fi
    
    # 安装开发工具
    if [[ -f "requirements-dev.txt" ]]; then
        execute_command "pip install -r requirements-dev.txt" "安装开发依赖"
    fi
    
    # 安装pre-commit钩子
    if command -v pre-commit &> /dev/null; then
        execute_command "pre-commit install" "安装pre-commit钩子"
    fi
    
    # 创建配置文件
    local config_dir="$HOME/.chango_editor"
    if [[ ! -d "$config_dir" ]]; then
        mkdir -p "$config_dir"
        info "创建配置目录: $config_dir"
    fi
    
    info "开发环境初始化完成"
    return 0
}

# 主函数
main() {
    local command=""
    
    # 设置信号处理
    trap 'handle_signal SIGINT' INT
    trap 'handle_signal SIGTERM' TERM
    trap 'cleanup' EXIT
    
    # 解析命令行参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                usage
                exit 0
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -d|--debug)
                DEBUG_MODE=true
                LOG_LEVEL=$LOG_DEBUG
                shift
                ;;
            -n|--dry-run)
                DRY_RUN=true
                shift
                ;;
            -l|--log-level)
                LOG_LEVEL="$2"
                shift 2
                ;;
            -o|--output)
                OUTPUT_DIR="$2"
                shift 2
                ;;
            install|test|build|clean|setup|benchmark)
                command="$1"
                shift
                ;;
            *)
                error "未知选项: $1"
                usage
                exit 1
                ;;
        esac
    done
    
    # 检查命令
    if [[ -z "$command" ]]; then
        error "请指定命令"
        usage
        exit 1
    fi
    
    # 创建日志文件目录
    mkdir -p "$(dirname "$LOG_FILE")"
    
    # 记录开始时间
    info "=================================================="
    info "Chango Editor Shell脚本启动"
    info "时间: $TIMESTAMP"
    info "命令: $command"
    info "参数: DEBUG=$DEBUG_MODE, VERBOSE=$VERBOSE, DRY_RUN=$DRY_RUN"
    info "=================================================="
    
    # 执行命令
    case $command in
        install)
            install_chango_editor
            ;;
        test)
            run_tests
            ;;
        build)
            build_project
            ;;
        clean)
            clean_project
            ;;
        setup)
            setup_dev_environment
            ;;
        benchmark)
            run_benchmark
            ;;
        *)
            error "未实现的命令: $command"
            exit 1
            ;;
    esac
    
    local exit_code=$?
    if [[ $exit_code -eq 0 ]]; then
        info "命令 '$command' 执行成功"
    else
        error "命令 '$command' 执行失败 (退出码: $exit_code)"
    fi
    
    return $exit_code
}

# 脚本入口
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
