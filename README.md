# CHM 转 Markdown 工具

一款用于将 CHM 帮助文件批量转换为 Markdown 格式的工具。

## 功能特点

- **批量解压**：一键解压文件夹中的所有 CHM 文件到 html 目录
- **HTML 转 MD**：将 HTML 文件转换为 Markdown 格式
- **图片处理**：自动提取并保存图片到统一目录
- **链接转换**：
  - 内部链接（同一 CHM 内的跳转）
  - 跨 CHM 链接（ms-its: 协议）
  - 锚点支持
- **GUI 界面**：提供文件夹选择对话框，操作简单

## 环境要求

- Windows 操作系统
- Python 3.10+
- 7-Zip（用于解压 CHM 文件）

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/Ray660/chm_to_md.git
cd chm_to_md
```

2. 安装依赖：
```bash
pip install html2text
```

3. 确保已安装 7-Zip（默认安装路径：`C:\Program Files\7-Zip\7z.exe`）

## 使用方法

### 方式一：GUI 交互

直接运行主程序，会弹出文件夹选择对话框：

```bash
python scripts/main.py
```

操作步骤：
1. 运行程序
2. 在弹出的对话框中选择包含 CHM 文件的文件夹
3. 程序会自动：
   - 在选择目录下创建 `html` 文件夹并解压 CHM 文件
   - 创建 `md` 文件夹并转换 HTML 为 Markdown
   - 提取图片到 `md/images/` 目录

### 方式二：测试单文件转换

```bash
python -c "
import sys
sys.path.insert(0, 'scripts')
from convert import html_to_md
from pathlib import Path

html_path = Path('test_source/html/APMU/APMUDefTopic.html')
md_path = Path('test_source/md/APMU/APMUDefTopic.md')
base_dir = Path('test_source/html')
md_dir = Path('test_source/md')
images_dir = Path('test_source/md/images')

html_to_md(html_path, md_path, base_dir, md_dir, images_dir)
"
```

## 项目结构

```
chm_to_md/
├── scripts/           # 源代码
│   ├── config.py     # 配置文件（7-zip 路径）
│   ├── ui.py         # GUI 文件夹选择
│   ├── extract.py    # CHM 解压
│   ├── convert.py    # HTML 转 Markdown
│   └── main.py       # 主入口
├── test_source/      # 测试数据（小 CHM 文件）
├── J750_HELP/        # 完整 CHM 文件（用于测试）
├── PLAN.md           # 项目规划
└── README.md         # 说明文档
```

## 输出结构

处理后的文件结构如下：

```
原始目录/
├── html/                    # 解压的 HTML 文件
│   ├── CHM1名/
│   │   ├── subdir/
│   │   │   └── file.html
│   │   └── index.html
│   └── CHM2名/
│       └── ...
├── md/                     # 转换后的 Markdown 文件
│   ├── CHM1名/
│   │   ├── subdir/
│   │   │   └── file.md
│   │   └── index.md
│   ├── CHM2名/
│   │   └── ...
│   └── images/             # 统一存放的图片
│       ├── CHM1名/
│       │   └── xxx.png
│       └── CHM2名/
│           └── ...
└── *.chm                   # 原始 CHM 文件
```

## 链接转换规则

| 原始链接 | 类型转换后格式 |
|-------------|-----------|
| 内部链接（同一HTML目录） | `filename.md` |
| 跨 CHM 链接（ms-its:） | `../其他CHM名/filename.md` |
| 图片链接 | `../images/CHM名/xxx.png` |
| 锚点（#id） | 保留到目标文件 |

示例：
- 原始：`ms-its:Safety.chm::/SafetyDefTopic.html#378965`
- 转换后：`../Safety/SafetyDefTopic.md#378965`

## 常见问题

### Q: 7-Zip 路径不在默认位置怎么办？

A: 修改 `scripts/config.py` 中的 `SEVEN_ZIP_PATHS` 列表，添加你的 7-Zip 路径。

### Q: 图片路径错误怎么办？

A: 检查生成的 md 文件中的图片路径，确保使用正确的相对路径。

### Q: 锚点跳转失效怎么办？

A: 确保目标 MD 文件中包含对应的锚点标签（`<a id="xxx"></a>`）。

## 技术栈

- Python 3.10+
- [html2text](https://github.com/aaronsw/html2text) - HTML 转 Markdown
- 7-Zip - CHM 解压

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
