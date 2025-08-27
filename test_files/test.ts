/**
 * TypeScript测试文件
 * 展示TypeScript的类型系统和现代特性
 */

// 接口定义
interface User {
    id: number;
    name: string;
    email?: string;
    roles: Role[];
}

interface Role {
    id: number;
    name: string;
    permissions: Permission[];
}

interface Permission {
    action: string;
    resource: string;
}

// 类型别名
type UserStatus = 'active' | 'inactive' | 'pending';
type ApiResponse<T> = {
    success: boolean;
    data: T;
    message?: string;
};

// 枚举
enum LogLevel {
    DEBUG = 0,
    INFO = 1,
    WARN = 2,
    ERROR = 3
}

// 泛型类
class DataService<T> {
    private items: T[] = [];
    
    constructor(private apiUrl: string) {}
    
    // 泛型方法
    async fetchAll(): Promise<ApiResponse<T[]>> {
        try {
            const response = await fetch(this.apiUrl);
            const data = await response.json();
            return {
                success: true,
                data: data
            };
        } catch (error) {
            return {
                success: false,
                data: [],
                message: error instanceof Error ? error.message : 'Unknown error'
            };
        }
    }
    
    // 类型守卫
    isValidItem(item: any): item is T {
        return typeof item === 'object' && item !== null;
    }
    
    // 装饰器示例
    @deprecated('Use fetchAll instead')
    getItems(): T[] {
        return this.items;
    }
}

// 装饰器定义
function deprecated(message: string) {
    return function (target: any, propertyName: string, descriptor: PropertyDescriptor) {
        console.warn(`${propertyName} is deprecated: ${message}`);
    };
}

// 用户服务类
class UserService extends DataService<User> {
    constructor() {
        super('/api/users');
    }
    
    // 方法重载
    findUser(id: number): Promise<User | null>;
    findUser(email: string): Promise<User | null>;
    async findUser(idOrEmail: number | string): Promise<User | null> {
        if (typeof idOrEmail === 'number') {
            return this.findById(idOrEmail);
        } else {
            return this.findByEmail(idOrEmail);
        }
    }
    
    private async findById(id: number): Promise<User | null> {
        // 实现查找逻辑
        return null;
    }
    
    private async findByEmail(email: string): Promise<User | null> {
        // 实现查找逻辑
        return null;
    }
    
    // 可选链和空值合并
    getUserDisplayName(user: User): string {
        return user.name ?? user.email ?? 'Unknown User';
    }
    
    // 条件类型
    filterActiveUsers<T extends User>(users: T[]): T[] {
        return users.filter(user => this.isActiveUser(user));
    }
    
    private isActiveUser(user: User): boolean {
        return user.roles.length > 0;
    }
}

// 工具类型示例
type PartialUser = Partial<User>;
type RequiredUser = Required<User>;
type UserKeys = keyof User;
type UserValues = User[keyof User];

// 映射类型
type ReadonlyUser = {
    readonly [K in keyof User]: User[K];
};

// 条件类型
type NonNullable<T> = T extends null | undefined ? never : T;

// 高阶函数
function createLogger(level: LogLevel) {
    return function(message: string): void {
        if (level >= LogLevel.INFO) {
            console.log(`[${LogLevel[level]}] ${message}`);
        }
    };
}

// 异步生成器
async function* generateUsers(): AsyncGenerator<User, void, unknown> {
    for (let i = 1; i <= 10; i++) {
        yield {
            id: i,
            name: `User ${i}`,
            email: `user${i}@example.com`,
            roles: []
        };
        
        // 模拟异步延迟
        await new Promise(resolve => setTimeout(resolve, 100));
    }
}

// 主函数
async function main(): Promise<void> {
    const userService = new UserService();
    const logger = createLogger(LogLevel.INFO);
    
    try {
        // 使用异步生成器
        logger('开始生成用户数据...');
        for await (const user of generateUsers()) {
            logger(`生成用户: ${user.name}`);
        }
        
        // 测试用户服务
        const response = await userService.fetchAll();
        if (response.success) {
            logger(`获取到 ${response.data.length} 个用户`);
            
            // 使用方法重载
            const userById = await userService.findUser(1);
            const userByEmail = await userService.findUser('test@example.com');
            
            logger('用户查找完成');
        } else {
            logger(`错误: ${response.message}`);
        }
        
    } catch (error) {
        logger(`未处理的错误: ${error}`);
    }
}

// 模块导出
export { User, UserService, LogLevel, DataService };
export type { ApiResponse, UserStatus };

// 执行主函数
main().catch(console.error);
