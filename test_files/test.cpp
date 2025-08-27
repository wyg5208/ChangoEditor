/**
 * C++测试文件
 * 用于验证C++语法高亮功能
 * 
 * @author Chango Team
 * @date 2024-01-01
 */

#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <memory>
#include <map>

// 命名空间
using namespace std;

// 类模板
template<typename T>
class Calculator {
private:
    T result;
    
public:
    Calculator() : result(0) {}
    
    // 构造函数
    explicit Calculator(T initial) : result(initial) {}
    
    // 模板方法
    template<typename U>
    auto add(const U& value) -> decltype(result + value) {
        result += value;
        return result;
    }
    
    // 操作符重载
    Calculator& operator+=(const T& value) {
        result += value;
        return *this;
    }
    
    // 获取结果
    T getResult() const noexcept {
        return result;
    }
    
    // 静态方法
    static T multiply(const T& a, const T& b) {
        return a * b;
    }
};

// 枚举类
enum class Status {
    SUCCESS = 0,
    ERROR = 1,
    PENDING = 2
};

// 结构体
struct Point {
    double x, y;
    
    Point(double x = 0.0, double y = 0.0) : x(x), y(y) {}
    
    // 操作符重载
    Point operator+(const Point& other) const {
        return Point(x + other.x, y + other.y);
    }
    
    // 友元函数
    friend ostream& operator<<(ostream& os, const Point& p) {
        os << "(" << p.x << ", " << p.y << ")";
        return os;
    }
};

// 函数模板
template<typename Container>
void printContainer(const Container& container) {
    cout << "容器内容: ";
    for (const auto& item : container) {
        cout << item << " ";
    }
    cout << endl;
}

// Lambda表达式示例
void lambdaDemo() {
    vector<int> numbers = {5, 2, 8, 1, 9, 3};
    
    // Lambda排序
    sort(numbers.begin(), numbers.end(), [](int a, int b) {
        return a < b;
    });
    
    cout << "排序后的数字: ";
    printContainer(numbers);
    
    // Lambda过滤
    vector<int> evenNumbers;
    copy_if(numbers.begin(), numbers.end(), back_inserter(evenNumbers),
            [](int n) { return n % 2 == 0; });
    
    cout << "偶数: ";
    printContainer(evenNumbers);
}

// 智能指针示例
void smartPointerDemo() {
    // unique_ptr
    auto uniqueCalc = make_unique<Calculator<double>>(10.5);
    uniqueCalc->add(5.3);
    cout << "unique_ptr计算结果: " << uniqueCalc->getResult() << endl;
    
    // shared_ptr
    auto sharedCalc = make_shared<Calculator<int>>(100);
    sharedCalc->add(50);
    cout << "shared_ptr计算结果: " << sharedCalc->getResult() << endl;
}

// 异常处理
void exceptionDemo() {
    try {
        vector<int> vec = {1, 2, 3};
        cout << "访问vec[10]: " << vec.at(10) << endl;
    }
    catch (const out_of_range& e) {
        cerr << "捕获异常: " << e.what() << endl;
    }
    catch (const exception& e) {
        cerr << "通用异常: " << e.what() << endl;
    }
    catch (...) {
        cerr << "未知异常" << endl;
    }
}

// 现代C++特性
void modernCppDemo() {
    // auto关键字
    auto number = 42;
    auto text = string("Hello, C++!");
    auto lambda = [](int x) { return x * x; };
    
    cout << "number: " << number << endl;
    cout << "text: " << text << endl;
    cout << "lambda(5): " << lambda(5) << endl;
    
    // 范围for循环
    vector<string> languages = {"C++", "Python", "JavaScript", "Rust"};
    cout << "编程语言: ";
    for (const auto& lang : languages) {
        cout << lang << " ";
    }
    cout << endl;
    
    // 初始化列表
    map<string, int> scores = {
        {"Alice", 95},
        {"Bob", 87},
        {"Charlie", 92}
    };
    
    cout << "成绩:" << endl;
    for (const auto& [name, score] : scores) {  // 结构化绑定 (C++17)
        cout << "  " << name << ": " << score << endl;
    }
}

// 主函数
int main() {
    cout << "=== Chango Editor C++测试 ===" << endl;
    
    // 基础计算器测试
    Calculator<int> intCalc;
    intCalc.add(10).add(20).add(30);
    cout << "整数计算器结果: " << intCalc.getResult() << endl;
    
    Calculator<double> doubleCalc(3.14);
    doubleCalc.add(2.86);
    cout << "浮点计算器结果: " << doubleCalc.getResult() << endl;
    
    // 点运算测试
    Point p1(3.0, 4.0);
    Point p2(1.0, 2.0);
    Point p3 = p1 + p2;
    cout << "点运算: " << p1 << " + " << p2 << " = " << p3 << endl;
    
    // Lambda演示
    cout << "\n=== Lambda演示 ===" << endl;
    lambdaDemo();
    
    // 智能指针演示
    cout << "\n=== 智能指针演示 ===" << endl;
    smartPointerDemo();
    
    // 异常处理演示
    cout << "\n=== 异常处理演示 ===" << endl;
    exceptionDemo();
    
    // 现代C++特性演示
    cout << "\n=== 现代C++特性演示 ===" << endl;
    modernCppDemo();
    
    cout << "\n=== 测试完成 ===" << endl;
    return 0;
}
