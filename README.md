# pvz_click_start

植物大战僵尸无尽模式自动点击工具，基于OpenCV实现。

## 功能
- 自动点击"重选"按钮
- 自动点击"摇滚"按钮
- 循环执行操作

## 环境要求
- Python 3.7+
- Windows系统
- 植物大战僵尸杂交版（窗口模式运行）

## 安装
1. 克隆仓库
```bash
git clone https://github.com/HGYJLLK/pvz_click_start.git
cd pvz_click_start
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

## 使用方法
1. 确保游戏窗口标题为"植物大战僵尸杂交版"
2. 运行脚本：
```bash
python pvz_click_start.py
```

## 注意事项
- 确保游戏窗口在前台
- 确保模板图片(chongxuan.png, yaogun.png)在脚本同目录下
- 使用Ctrl+C可以停止程序

## 项目结构
```
pvz_click_start/
├── pvz_click_start.py  # 主程序
├── chongxuan.png      # 重选按钮模板
├── yaogun.png         # 摇滚按钮模板
└── requirements.txt   # 依赖文件
```