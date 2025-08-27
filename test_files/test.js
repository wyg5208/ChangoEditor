/**
 * JavaScript测试文件
 * 用于验证语法高亮功能
 */

'use strict';

// 类定义
class Calculator {
    constructor() {
        this.result = 0;
    }
    
    // 方法定义
    add(a, b) {
        return a + b;
    }
    
    multiply(x, y) {
        const result = x * y;
        return result;
    }
}

// 函数定义
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// 箭头函数
const greet = (name) => {
    return `Hello, ${name}!`;
};

// 异步函数
async function fetchData(url) {
    try {
        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

// 主程序
function main() {
    const calc = new Calculator();
    const sum = calc.add(10, 20);
    
    console.log('计算结果:', sum);
    console.log('斐波那契数列:', fibonacci(10));
    console.log(greet('Chango Editor'));
    
    // 数组操作
    const numbers = [1, 2, 3, 4, 5];
    const doubled = numbers.map(x => x * 2);
    const filtered = numbers.filter(x => x % 2 === 0);
    
    console.log('原数组:', numbers);
    console.log('翻倍后:', doubled);
    console.log('偶数:', filtered);
}

// 执行主程序
main();
