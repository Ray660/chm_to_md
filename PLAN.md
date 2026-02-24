# CHM批量处理工具计划

## 功能一：CHM解压

批量解压CHM文件到以文件名命名的文件夹中，统一存放在`html`文件夹下

### 实现方式
- Python脚本 (extract_chm.py)
- 7-zip解压

### 处理流程
1. 弹出文件夹选择对话框，让用户选择要处理的文件夹
2. 在该文件夹下创建`html`文件夹
3. 遍历所有`.chm`文件
4. 对每个CHM文件：
   - 在`html`文件夹下创建以CHM文件名（不含扩展名）命名的子文件夹
   - 用`7z x -y`命令解压到该子文件夹

### 注意事项
- 如果子文件夹已存在，覆盖原内容
- 7-zip优先查找默认安装路径

---

## 功能二：HTML转MD

将html文件夹下所有CHM解压的HTML转换为MD文件

### 实现方式
- Python脚本 (html_to_md.py)
- 使用html2text或pandoc进行转换

### 处理流程
1. 遍历 `html/` 下每个CHM子文件夹，递归查找所有HTML
2. 对每个HTML：
   - 下载图片到 `md/images/`（保持目录结构）
   - 转换HTML内容为Markdown
   - CHM跳转 `chm://...` 转换为 `[xxx](其他MD文件链接)`
3. MD文件保存到 `md/` 目录（保持原有目录结构）

### 输出结构
```
原始目录/
  html/
    CHM1名/
      subdir/
        file.html
      index.html
    CHM2名/
      ...
  md/
    CHM1名/
      subdir/
        file.md
      index.md
    CHM2名/
      ...
    images/
      CHM1名/xxx.png
      CHM2名/xxx.png
```

### 注意事项
- 图片统一存放到 `md/images/` 目录
- CHM跳转链接需要转换为MD文件相对链接
- 保持原有目录结构
