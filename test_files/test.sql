-- Chango Editor SQL测试文件
-- 展示SQL语法和数据库操作
-- 作者: Chango Team
-- 创建时间: 2024-01-15

-- 数据库创建和使用
CREATE DATABASE IF NOT EXISTS chango_editor_db 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

USE chango_editor_db;

-- 删除已存在的表（用于重新创建）
DROP TABLE IF EXISTS user_sessions;
DROP TABLE IF EXISTS project_files;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS languages;

-- 创建编程语言表
CREATE TABLE languages (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE,
    display_name VARCHAR(100) NOT NULL,
    file_extensions JSON,
    keywords JSON,
    color_scheme VARCHAR(20) DEFAULT 'default',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- 索引
    INDEX idx_name (name),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建用户表
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(100),
    avatar_url VARCHAR(255),
    preferences JSON,
    last_login_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    
    -- 约束
    CONSTRAINT chk_email_format CHECK (email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT chk_username_length CHECK (CHAR_LENGTH(username) >= 3),
    
    -- 索引
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_last_login (last_login_at),
    INDEX idx_active (is_active),
    FULLTEXT idx_display_name (display_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建项目表
CREATE TABLE projects (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    owner_id BIGINT NOT NULL,
    language_id INT,
    repository_url VARCHAR(255),
    local_path VARCHAR(500),
    settings JSON,
    file_count INT DEFAULT 0,
    total_lines INT DEFAULT 0,
    last_opened_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    
    -- 外键约束
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (language_id) REFERENCES languages(id) ON DELETE SET NULL,
    
    -- 索引
    INDEX idx_owner (owner_id),
    INDEX idx_language (language_id),
    INDEX idx_name (name),
    INDEX idx_last_opened (last_opened_at),
    INDEX idx_active (is_active),
    FULLTEXT idx_description (description)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建项目文件表
CREATE TABLE project_files (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    project_id BIGINT NOT NULL,
    file_path VARCHAR(1000) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_size BIGINT DEFAULT 0,
    line_count INT DEFAULT 0,
    language_id INT,
    encoding VARCHAR(20) DEFAULT 'utf-8',
    last_modified TIMESTAMP NULL,
    checksum VARCHAR(64),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- 外键约束
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (language_id) REFERENCES languages(id) ON DELETE SET NULL,
    
    -- 唯一约束
    UNIQUE KEY uk_project_file (project_id, file_path),
    
    -- 索引
    INDEX idx_project (project_id),
    INDEX idx_language (language_id),
    INDEX idx_filename (file_name),
    INDEX idx_size (file_size),
    INDEX idx_modified (last_modified),
    FULLTEXT idx_file_path (file_path)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建用户会话表
CREATE TABLE user_sessions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    session_token VARCHAR(255) NOT NULL UNIQUE,
    opened_files JSON,
    active_file_id BIGINT,
    cursor_position JSON,
    window_state JSON,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    ended_at TIMESTAMP NULL,
    duration_minutes INT GENERATED ALWAYS AS (
        CASE 
            WHEN ended_at IS NOT NULL THEN 
                TIMESTAMPDIFF(MINUTE, started_at, ended_at)
            ELSE 
                TIMESTAMPDIFF(MINUTE, started_at, NOW())
        END
    ) STORED,
    
    -- 外键约束
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (active_file_id) REFERENCES project_files(id) ON DELETE SET NULL,
    
    -- 索引
    INDEX idx_user (user_id),
    INDEX idx_token (session_token),
    INDEX idx_activity (last_activity_at),
    INDEX idx_duration (duration_minutes)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 插入测试数据

-- 插入编程语言数据
INSERT INTO languages (name, display_name, file_extensions, keywords, color_scheme) VALUES
('python', 'Python', '["py", "pyw", "pyx"]', '["def", "class", "if", "else", "elif", "for", "while", "try", "except", "finally", "import", "from", "as", "with", "lambda", "yield", "return", "pass", "break", "continue"]', 'python'),
('javascript', 'JavaScript', '["js", "jsx"]', '["var", "let", "const", "function", "class", "if", "else", "for", "while", "do", "switch", "case", "default", "try", "catch", "finally", "return", "break", "continue", "throw", "new", "this", "super", "extends", "import", "export", "async", "await"]', 'javascript'),
('typescript', 'TypeScript', '["ts", "tsx"]', '["var", "let", "const", "function", "class", "interface", "type", "enum", "namespace", "module", "public", "private", "protected", "readonly", "static", "abstract"]', 'typescript'),
('html', 'HTML', '["html", "htm", "xhtml"]', '["html", "head", "title", "meta", "link", "style", "script", "body", "div", "span", "p", "h1", "h2", "h3", "h4", "h5", "h6", "a", "img", "ul", "ol", "li", "table", "tr", "td", "th", "form", "input", "button", "textarea", "select", "option"]', 'web'),
('css', 'CSS', '["css", "scss", "sass", "less"]', '["color", "background", "font", "margin", "padding", "border", "width", "height", "display", "position", "top", "left", "right", "bottom", "float", "clear", "overflow"]', 'web'),
('java', 'Java', '["java"]', '["abstract", "assert", "boolean", "break", "byte", "case", "catch", "char", "class", "const", "continue", "default", "do", "double", "else", "enum", "extends", "final", "finally", "float", "for", "goto", "if", "implements", "import", "instanceof", "int", "interface", "long", "native", "new", "package", "private", "protected", "public", "return", "short", "static", "strictfp", "super", "switch", "synchronized", "this", "throw", "throws", "transient", "try", "void", "volatile", "while"]', 'java'),
('csharp', 'C#', '["cs"]', '["abstract", "as", "base", "bool", "break", "byte", "case", "catch", "char", "checked", "class", "const", "continue", "decimal", "default", "delegate", "do", "double", "else", "enum", "event", "explicit", "extern", "false", "finally", "fixed", "float", "for", "foreach", "goto", "if", "implicit", "in", "int", "interface", "internal", "is", "lock", "long", "namespace", "new", "null", "object", "operator", "out", "override", "params", "private", "protected", "public", "readonly", "ref", "return", "sbyte", "sealed", "short", "sizeof", "stackalloc", "static", "string", "struct", "switch", "this", "throw", "true", "try", "typeof", "uint", "ulong", "unchecked", "unsafe", "ushort", "using", "virtual", "void", "volatile", "while"]', 'csharp'),
('cpp', 'C++', '["cpp", "cxx", "cc", "c", "h", "hpp", "hxx"]', '["alignas", "alignof", "and", "and_eq", "asm", "auto", "bitand", "bitor", "bool", "break", "case", "catch", "char", "char16_t", "char32_t", "class", "compl", "const", "constexpr", "const_cast", "continue", "decltype", "default", "delete", "do", "double", "dynamic_cast", "else", "enum", "explicit", "export", "extern", "false", "float", "for", "friend", "goto", "if", "inline", "int", "long", "mutable", "namespace", "new", "noexcept", "not", "not_eq", "nullptr", "operator", "or", "or_eq", "private", "protected", "public", "register", "reinterpret_cast", "return", "short", "signed", "sizeof", "static", "static_assert", "static_cast", "struct", "switch", "template", "this", "thread_local", "throw", "true", "try", "typedef", "typeid", "typename", "union", "unsigned", "using", "virtual", "void", "volatile", "wchar_t", "while", "xor", "xor_eq"]', 'cpp');

-- 插入用户数据
INSERT INTO users (username, email, password_hash, display_name, preferences) VALUES
('admin', 'admin@chango_editor.com', SHA2('admin123', 256), '管理员', '{"theme": "dark", "font_size": 14, "tab_size": 4, "word_wrap": false}'),
('developer1', 'dev1@example.com', SHA2('dev123', 256), '开发者一号', '{"theme": "light", "font_size": 12, "tab_size": 2, "word_wrap": true}'),
('developer2', 'dev2@example.com', SHA2('dev456', 256), '开发者二号', '{"theme": "dark", "font_size": 13, "tab_size": 4, "word_wrap": false}'),
('testuser', 'test@example.com', SHA2('test789', 256), '测试用户', '{"theme": "auto", "font_size": 11, "tab_size": 4, "word_wrap": true}');

-- 插入项目数据
INSERT INTO projects (name, description, owner_id, language_id, repository_url, settings) VALUES
('Chango Lite', '轻量级代码编辑器项目', 1, 1, 'https://github.com/chango_editor/chango_editor-lite', '{"auto_save": true, "backup_enabled": true, "max_backups": 5}'),
('Web前端项目', 'React + TypeScript 前端应用', 2, 3, 'https://github.com/example/frontend-app', '{"auto_save": false, "backup_enabled": true, "max_backups": 3}'),
('Java后端服务', 'Spring Boot 微服务项目', 2, 6, 'https://github.com/example/backend-service', '{"auto_save": true, "backup_enabled": true, "max_backups": 10}'),
('移动应用', 'React Native 跨平台应用', 3, 2, 'https://github.com/example/mobile-app', '{"auto_save": true, "backup_enabled": false}'),
('数据分析脚本', 'Python 数据科学项目', 4, 1, NULL, '{"auto_save": false, "backup_enabled": true, "max_backups": 7}');

-- 插入项目文件数据
INSERT INTO project_files (project_id, file_path, file_name, file_size, line_count, language_id, encoding, checksum) VALUES
(1, '/src/main.py', 'main.py', 1024, 45, 1, 'utf-8', 'a1b2c3d4e5f6'),
(1, '/src/ui/main_window.py', 'main_window.py', 15360, 642, 1, 'utf-8', 'f6e5d4c3b2a1'),
(1, '/src/core/editor.py', 'editor.py', 8192, 383, 1, 'utf-8', 'b2c3d4e5f6a1'),
(1, '/requirements.txt', 'requirements.txt', 256, 12, NULL, 'utf-8', 'c3d4e5f6a1b2'),
(2, '/src/components/App.tsx', 'App.tsx', 2048, 98, 3, 'utf-8', 'd4e5f6a1b2c3'),
(2, '/src/index.html', 'index.html', 1536, 67, 4, 'utf-8', 'e5f6a1b2c3d4'),
(2, '/src/styles/main.css', 'main.css', 3072, 145, 5, 'utf-8', 'f6a1b2c3d4e5'),
(3, '/src/main/java/Application.java', 'Application.java', 4096, 128, 6, 'utf-8', 'a1b2c3d4e5f6'),
(3, '/src/main/resources/application.yml', 'application.yml', 512, 32, NULL, 'utf-8', 'b2c3d4e5f6a1'),
(4, '/App.js', 'App.js', 2560, 112, 2, 'utf-8', 'c3d4e5f6a1b2'),
(5, '/analysis.py', 'analysis.py', 6144, 267, 1, 'utf-8', 'd4e5f6a1b2c3'),
(5, '/data_processing.py', 'data_processing.py', 4608, 189, 1, 'utf-8', 'e5f6a1b2c3d4');

-- 更新项目的文件统计信息
UPDATE projects p SET 
    file_count = (SELECT COUNT(*) FROM project_files pf WHERE pf.project_id = p.id),
    total_lines = (SELECT COALESCE(SUM(line_count), 0) FROM project_files pf WHERE pf.project_id = p.id);

-- 插入用户会话数据
INSERT INTO user_sessions (user_id, session_token, opened_files, active_file_id, cursor_position, window_state) VALUES
(1, 'session_admin_001', '[1, 2, 3]', 2, '{"line": 42, "column": 16}', '{"width": 1200, "height": 800, "maximized": false}'),
(2, 'session_dev1_001', '[5, 6]', 5, '{"line": 1, "column": 1}', '{"width": 1440, "height": 900, "maximized": true}'),
(3, 'session_dev2_001', '[10]', 10, '{"line": 67, "column": 23}', '{"width": 1920, "height": 1080, "maximized": false}'),
(4, 'session_test_001', '[11, 12]', 11, '{"line": 15, "column": 8}', '{"width": 1024, "height": 768, "maximized": false}');

-- 复杂查询示例

-- 1. 用户项目统计
SELECT 
    u.username,
    u.display_name,
    COUNT(p.id) as project_count,
    SUM(p.file_count) as total_files,
    SUM(p.total_lines) as total_lines,
    AVG(p.total_lines) as avg_lines_per_project
FROM users u
LEFT JOIN projects p ON u.id = p.owner_id AND p.is_active = TRUE
WHERE u.is_active = TRUE
GROUP BY u.id, u.username, u.display_name
ORDER BY total_lines DESC;

-- 2. 编程语言使用统计
SELECT 
    l.display_name,
    COUNT(DISTINCT p.id) as project_count,
    COUNT(pf.id) as file_count,
    SUM(pf.line_count) as total_lines,
    AVG(pf.line_count) as avg_lines_per_file,
    AVG(pf.file_size) as avg_file_size
FROM languages l
LEFT JOIN projects p ON l.id = p.language_id
LEFT JOIN project_files pf ON l.id = pf.language_id
GROUP BY l.id, l.display_name
HAVING project_count > 0 OR file_count > 0
ORDER BY total_lines DESC;

-- 3. 项目详细信息（包含最近活动）
SELECT 
    p.name as project_name,
    p.description,
    u.display_name as owner_name,
    l.display_name as primary_language,
    p.file_count,
    p.total_lines,
    p.last_opened_at,
    COUNT(DISTINCT us.id) as session_count,
    MAX(us.last_activity_at) as last_activity,
    SUM(us.duration_minutes) as total_usage_minutes
FROM projects p
JOIN users u ON p.owner_id = u.id
LEFT JOIN languages l ON p.language_id = l.id
LEFT JOIN project_files pf ON p.id = pf.project_id
LEFT JOIN user_sessions us ON u.id = us.user_id
WHERE p.is_active = TRUE
GROUP BY p.id, p.name, p.description, u.display_name, l.display_name, p.file_count, p.total_lines, p.last_opened_at
ORDER BY last_activity DESC NULLS LAST;

-- 4. 文件类型分布
SELECT 
    SUBSTRING_INDEX(pf.file_name, '.', -1) as file_extension,
    COUNT(*) as file_count,
    SUM(pf.file_size) as total_size,
    AVG(pf.file_size) as avg_size,
    SUM(pf.line_count) as total_lines,
    AVG(pf.line_count) as avg_lines
FROM project_files pf
JOIN projects p ON pf.project_id = p.id
WHERE p.is_active = TRUE 
    AND pf.file_name LIKE '%.%'
GROUP BY file_extension
HAVING file_count >= 1
ORDER BY total_lines DESC;

-- 5. 用户活动分析
SELECT 
    u.username,
    COUNT(us.id) as session_count,
    SUM(us.duration_minutes) as total_minutes,
    AVG(us.duration_minutes) as avg_session_minutes,
    MAX(us.last_activity_at) as last_seen,
    JSON_LENGTH(us.opened_files) as avg_open_files
FROM users u
LEFT JOIN user_sessions us ON u.id = us.user_id
WHERE u.is_active = TRUE
GROUP BY u.id, u.username
ORDER BY total_minutes DESC;

-- 6. 最近修改的文件
SELECT 
    pf.file_name,
    pf.file_path,
    p.name as project_name,
    u.display_name as owner_name,
    l.display_name as language,
    pf.file_size,
    pf.line_count,
    pf.last_modified,
    pf.updated_at
FROM project_files pf
JOIN projects p ON pf.project_id = p.id
JOIN users u ON p.owner_id = u.id
LEFT JOIN languages l ON pf.language_id = l.id
WHERE p.is_active = TRUE
    AND pf.last_modified IS NOT NULL
ORDER BY pf.last_modified DESC
LIMIT 20;

-- 视图定义

-- 创建项目摘要视图
CREATE VIEW project_summary AS
SELECT 
    p.id,
    p.name,
    p.description,
    u.username as owner,
    l.display_name as language,
    p.file_count,
    p.total_lines,
    p.created_at,
    p.last_opened_at,
    CASE 
        WHEN p.last_opened_at >= DATE_SUB(NOW(), INTERVAL 7 DAY) THEN 'active'
        WHEN p.last_opened_at >= DATE_SUB(NOW(), INTERVAL 30 DAY) THEN 'recent'
        WHEN p.last_opened_at IS NOT NULL THEN 'old'
        ELSE 'never_opened'
    END as activity_status
FROM projects p
JOIN users u ON p.owner_id = u.id
LEFT JOIN languages l ON p.language_id = l.id
WHERE p.is_active = TRUE;

-- 创建用户统计视图
CREATE VIEW user_statistics AS
SELECT 
    u.id,
    u.username,
    u.display_name,
    COUNT(DISTINCT p.id) as project_count,
    COALESCE(SUM(p.file_count), 0) as total_files,
    COALESCE(SUM(p.total_lines), 0) as total_lines,
    COUNT(DISTINCT us.id) as session_count,
    COALESCE(SUM(us.duration_minutes), 0) as total_usage_minutes,
    MAX(us.last_activity_at) as last_activity,
    u.created_at as joined_at
FROM users u
LEFT JOIN projects p ON u.id = p.owner_id AND p.is_active = TRUE
LEFT JOIN user_sessions us ON u.id = us.user_id
WHERE u.is_active = TRUE
GROUP BY u.id, u.username, u.display_name, u.created_at;

-- 存储过程示例

DELIMITER //

-- 创建用户项目的存储过程
CREATE PROCEDURE CreateUserProject(
    IN p_user_id BIGINT,
    IN p_name VARCHAR(100),
    IN p_description TEXT,
    IN p_language_name VARCHAR(50),
    IN p_repository_url VARCHAR(255)
)
BEGIN
    DECLARE v_language_id INT DEFAULT NULL;
    DECLARE v_project_id BIGINT;
    
    -- 声明异常处理
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    -- 开始事务
    START TRANSACTION;
    
    -- 获取语言ID
    IF p_language_name IS NOT NULL THEN
        SELECT id INTO v_language_id 
        FROM languages 
        WHERE name = p_language_name;
    END IF;
    
    -- 插入项目
    INSERT INTO projects (name, description, owner_id, language_id, repository_url)
    VALUES (p_name, p_description, p_user_id, v_language_id, p_repository_url);
    
    -- 获取新创建的项目ID
    SET v_project_id = LAST_INSERT_ID();
    
    -- 提交事务
    COMMIT;
    
    -- 返回项目ID
    SELECT v_project_id as project_id;
END //

-- 清理用户会话的存储过程
CREATE PROCEDURE CleanupExpiredSessions(IN p_days_old INT)
BEGIN
    DECLARE v_deleted_count INT DEFAULT 0;
    
    -- 更新已结束的会话
    UPDATE user_sessions 
    SET ended_at = last_activity_at
    WHERE ended_at IS NULL 
        AND last_activity_at < DATE_SUB(NOW(), INTERVAL p_days_old DAY);
    
    -- 删除过期会话
    DELETE FROM user_sessions 
    WHERE ended_at IS NOT NULL 
        AND ended_at < DATE_SUB(NOW(), INTERVAL p_days_old DAY);
    
    -- 获取删除的记录数
    SET v_deleted_count = ROW_COUNT();
    
    -- 返回结果
    SELECT v_deleted_count as deleted_sessions;
END //

DELIMITER ;

-- 触发器示例

-- 项目文件更新触发器
DELIMITER //

CREATE TRIGGER update_project_stats_after_file_insert
    AFTER INSERT ON project_files
    FOR EACH ROW
BEGIN
    UPDATE projects 
    SET 
        file_count = (SELECT COUNT(*) FROM project_files WHERE project_id = NEW.project_id),
        total_lines = (SELECT COALESCE(SUM(line_count), 0) FROM project_files WHERE project_id = NEW.project_id),
        updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.project_id;
END //

CREATE TRIGGER update_project_stats_after_file_delete
    AFTER DELETE ON project_files
    FOR EACH ROW
BEGIN
    UPDATE projects 
    SET 
        file_count = (SELECT COUNT(*) FROM project_files WHERE project_id = OLD.project_id),
        total_lines = (SELECT COALESCE(SUM(line_count), 0) FROM project_files WHERE project_id = OLD.project_id),
        updated_at = CURRENT_TIMESTAMP
    WHERE id = OLD.project_id;
END //

CREATE TRIGGER update_project_stats_after_file_update
    AFTER UPDATE ON project_files
    FOR EACH ROW
BEGIN
    IF OLD.line_count != NEW.line_count OR OLD.project_id != NEW.project_id THEN
        -- 更新旧项目统计
        IF OLD.project_id != NEW.project_id THEN
            UPDATE projects 
            SET 
                file_count = (SELECT COUNT(*) FROM project_files WHERE project_id = OLD.project_id),
                total_lines = (SELECT COALESCE(SUM(line_count), 0) FROM project_files WHERE project_id = OLD.project_id),
                updated_at = CURRENT_TIMESTAMP
            WHERE id = OLD.project_id;
        END IF;
        
        -- 更新新项目统计
        UPDATE projects 
        SET 
            file_count = (SELECT COUNT(*) FROM project_files WHERE project_id = NEW.project_id),
            total_lines = (SELECT COALESCE(SUM(line_count), 0) FROM project_files WHERE project_id = NEW.project_id),
            updated_at = CURRENT_TIMESTAMP
        WHERE id = NEW.project_id;
    END IF;
END //

DELIMITER ;

-- 索引优化建议
ANALYZE TABLE users, projects, project_files, user_sessions, languages;

-- 显示表信息
SHOW TABLE STATUS LIKE 'users';
SHOW TABLE STATUS LIKE 'projects';
SHOW TABLE STATUS LIKE 'project_files';

-- 性能查询示例
EXPLAIN SELECT * FROM project_summary WHERE activity_status = 'active';
EXPLAIN SELECT * FROM user_statistics ORDER BY total_lines DESC;

-- 数据完整性检查
SELECT 'projects without owner' as check_type, COUNT(*) as count
FROM projects p LEFT JOIN users u ON p.owner_id = u.id WHERE u.id IS NULL
UNION ALL
SELECT 'files without project', COUNT(*)
FROM project_files pf LEFT JOIN projects p ON pf.project_id = p.id WHERE p.id IS NULL
UNION ALL
SELECT 'sessions without user', COUNT(*)
FROM user_sessions us LEFT JOIN users u ON us.user_id = u.id WHERE u.id IS NULL;

-- 备份和恢复命令提示
-- mysqldump -u root -p chango_editor_db > chango_editor_backup.sql
-- mysql -u root -p chango_editor_db < chango_editor_backup.sql

-- 查询结束
SELECT 'Chango Lite 数据库初始化完成!' as message,
       NOW() as completion_time;
