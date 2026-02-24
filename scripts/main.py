import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from ui import select_folder
from extract import extract_all

def main():
    root = tk.Tk()
    root.withdraw()
    
    selected_folder = select_folder()
    if not selected_folder:
        messagebox.showinfo("取消", "已取消操作")
        return
    
    # Check if folder has CHM files
    chm_files = [f for f in os.listdir(selected_folder) if f.lower().endswith('.chm')]
    if not chm_files:
        messagebox.showinfo("提示", "所选文件夹中没有找到CHM文件")
        return
    
    # Create progress window
    progress_win = tk.Toplevel()
    progress_win.title("CHM 转 MD")
    progress_win.geometry("400x150")
    progress_win.resizable(False, False)
    
    tk.Label(progress_win, text="正在解压CHM文件...", font=("Microsoft YaHei", 12)).pack(pady=20)
    
    progress = ttk.Progressbar(progress_win, length=300, mode='determinate')
    progress.pack(pady=10)
    
    percent_label = tk.Label(progress_win, text="0%", font=("Microsoft YaHei", 9))
    percent_label.place(x=180, y=90)
    
    progress_win.update()
    
    try:
        # Extract CHM
        extract_all(selected_folder)
        
        # Update progress window for conversion
        tk.Label(progress_win, text="正在转换HTML为MD...", font=("Microsoft YaHei", 12)).pack(pady=20)
        progress_win.update()
        
        # Import and run conversion
        from convert import convert_folder
        
        # Count files for progress
        html_dir = os.path.join(selected_folder, 'html')
        total = 0
        if os.path.exists(html_dir):
            for root_dir, dirs, files in os.walk(html_dir):
                for f in files:
                    if f.lower().endswith(('.html', '.htm')):
                        total += 1
        
        current = 0
        def update_progress(c, t, status):
            nonlocal current
            current = c
            if t > 0:
                percent = int(c / t * 100)
                progress['value'] = percent
                percent_label.config(text=f"{percent}%")
                progress_win.update()
        
        convert_folder(selected_folder, progress_callback=update_progress)
        
        progress['value'] = 100
        percent_label.config(text="100%")
        progress_win.update()
        
        progress_win.destroy()
        messagebox.showinfo("完成", "CHM 转 MD 已完成！\n\n请查看输出目录下的 md 文件夹。")
        
    except Exception as e:
        progress_win.destroy()
        import traceback
        traceback.print_exc()
        messagebox.showerror("错误", f"发生错误：{str(e)}")

if __name__ == '__main__':
    main()
