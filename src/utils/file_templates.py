"""
文件模板 - Chango Editor

提供各种编程语言的文件模板
"""

import os
from datetime import datetime

class FileTemplates:
    """文件模板管理器"""
    
    @staticmethod
    def get_template(file_extension):
        """根据文件扩展名获取模板"""
        templates = {
            '.py': FileTemplates.python_template,
            '.js': FileTemplates.javascript_template,
            '.ts': FileTemplates.typescript_template,
            '.html': FileTemplates.html_template,
            '.css': FileTemplates.css_template,
            '.java': FileTemplates.java_template,
            '.cpp': FileTemplates.cpp_template,
            '.c': FileTemplates.c_template,
            '.cs': FileTemplates.csharp_template,
            '.php': FileTemplates.php_template,
            '.rb': FileTemplates.ruby_template,
            '.go': FileTemplates.go_template,
            '.rs': FileTemplates.rust_template,
            '.sql': FileTemplates.sql_template,
            '.md': FileTemplates.markdown_template,
            '.sh': FileTemplates.bash_template,
        }
        
        template_func = templates.get(file_extension.lower())
        if template_func:
            return template_func()
        return ""
    
    @staticmethod
    def python_template():
        """Python文件模板"""
        return f'''#!/usr/bin/env python3
"""
文件描述

作者: Your Name
创建时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""


def main():
    """主函数"""
    print("Hello, Python!")


if __name__ == "__main__":
    main()
'''

    @staticmethod
    def javascript_template():
        """JavaScript文件模板"""
        return f'''/**
 * 文件描述
 * 
 * @author Your Name
 * @date {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
 */

'use strict';

// 主函数
function main() {{
    console.log('Hello, JavaScript!');
}}

// 执行主函数
main();
'''

    @staticmethod
    def typescript_template():
        """TypeScript文件模板"""
        return f'''/**
 * 文件描述
 * 
 * @author Your Name
 * @date {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
 */

// 主函数
function main(): void {{
    console.log('Hello, TypeScript!');
}}

// 执行主函数
main();
'''

    @staticmethod
    def html_template():
        """HTML文件模板"""
        return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文档标题</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>欢迎使用 PyEditor Lite</h1>
        <p>这是一个HTML模板文件。</p>
        <!-- 创建时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} -->
    </div>
    
    <script>
        console.log('HTML模板加载完成');
    </script>
</body>
</html>
'''

    @staticmethod
    def css_template():
        """CSS文件模板"""
        return f'''/*
 * CSS样式文件
 * 
 * 作者: Your Name
 * 创建时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
 */

/* 重置样式 */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

/* 基础样式 */
body {{
    font-family: 'Arial', sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f4f4f4;
}}

/* 容器样式 */
.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}}

/* 标题样式 */
h1, h2, h3, h4, h5, h6 {{
    margin-bottom: 1rem;
    font-weight: bold;
}}

/* 段落样式 */
p {{
    margin-bottom: 1rem;
}}
'''

    @staticmethod
    def java_template():
        """Java文件模板"""
        return f'''/**
 * 文件描述
 * 
 * @author Your Name
 * @date {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
 */

public class Main {{
    
    /**
     * 主方法
     * @param args 命令行参数
     */
    public static void main(String[] args) {{
        System.out.println("Hello, Java!");
    }}
}}
'''

    @staticmethod
    def cpp_template():
        """C++文件模板"""
        return f'''/**
 * 文件描述
 * 
 * @author Your Name
 * @date {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
 */

#include <iostream>
#include <string>

int main() {{
    std::cout << "Hello, C++!" << std::endl;
    return 0;
}}
'''

    @staticmethod
    def c_template():
        """C文件模板"""
        return f'''/**
 * 文件描述
 * 
 * @author Your Name
 * @date {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
 */

#include <stdio.h>
#include <stdlib.h>

int main() {{
    printf("Hello, C!\\n");
    return 0;
}}
'''

    @staticmethod
    def csharp_template():
        """C#文件模板"""
        return f'''/**
 * 文件描述
 * 
 * @author Your Name
 * @date {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
 */

using System;

namespace MyApplication
{{
    class Program
    {{
        static void Main(string[] args)
        {{
            Console.WriteLine("Hello, C#!");
        }}
    }}
}}
'''

    @staticmethod
    def php_template():
        """PHP文件模板"""
        return f'''<?php
/**
 * 文件描述
 * 
 * @author Your Name
 * @date {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
 */

// 主函数
function main() {{
    echo "Hello, PHP!\\n";
}}

// 执行主函数
main();
?>
'''

    @staticmethod
    def ruby_template():
        """Ruby文件模板"""
        return f'''#!/usr/bin/env ruby
# -*- coding: utf-8 -*-

##
# 文件描述
# 
# @author Your Name
# @date {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
##

def main
  puts "Hello, Ruby!"
end

# 执行主函数
main if __FILE__ == $0
'''

    @staticmethod
    def go_template():
        """Go文件模板"""
        return f'''/**
 * 文件描述
 * 
 * @author Your Name
 * @date {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
 */

package main

import "fmt"

func main() {{
    fmt.Println("Hello, Go!")
}}
'''

    @staticmethod
    def rust_template():
        """Rust文件模板"""
        return f'''/**
 * 文件描述
 * 
 * @author Your Name
 * @date {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
 */

fn main() {{
    println!("Hello, Rust!");
}}
'''

    @staticmethod
    def sql_template():
        """SQL文件模板"""
        return f'''-- 文件描述
-- 
-- 作者: Your Name
-- 创建时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

-- 示例查询
SELECT 
    'Hello, SQL!' AS message,
    NOW() AS current_time;

-- 创建表示例
-- CREATE TABLE example_table (
--     id INT PRIMARY KEY AUTO_INCREMENT,
--     name VARCHAR(100) NOT NULL,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );
'''

    @staticmethod
    def markdown_template():
        """Markdown文件模板"""
        return f'''# 文档标题

> 文档描述
> 
> 作者: Your Name  
> 创建时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 目录

- [简介](#简介)
- [安装](#安装)
- [使用方法](#使用方法)
- [示例](#示例)

## 简介

这是一个Markdown文档模板。

## 安装

```bash
# 安装命令示例
npm install package-name
```

## 使用方法

1. 第一步
2. 第二步
3. 第三步

## 示例

```python
def hello():
    print("Hello, World!")
```

---

*文档由 PyEditor Lite 创建*
'''

    @staticmethod
    def bash_template():
        """Bash脚本模板"""
        return f'''#!/bin/bash
# 
# 脚本描述
# 
# 作者: Your Name
# 创建时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
#

set -e  # 遇到错误立即退出
set -u  # 使用未定义变量时报错

# 主函数
main() {{
    echo "Hello, Bash!"
}}

# 检查是否作为脚本运行
if [[ "${{BASH_SOURCE[0]}}" == "${{0}}" ]]; then
    main "$@"
fi
'''

    @staticmethod
    def get_available_templates():
        """获取所有可用模板的列表"""
        return {
            'Python (.py)': '.py',
            'JavaScript (.js)': '.js',
            'TypeScript (.ts)': '.ts',
            'HTML (.html)': '.html',
            'CSS (.css)': '.css',
            'Java (.java)': '.java',
            'C++ (.cpp)': '.cpp',
            'C (.c)': '.c',
            'C# (.cs)': '.cs',
            'PHP (.php)': '.php',
            'Ruby (.rb)': '.rb',
            'Go (.go)': '.go',
            'Rust (.rs)': '.rs',
            'SQL (.sql)': '.sql',
            'Markdown (.md)': '.md',
            'Bash (.sh)': '.sh',
        }
