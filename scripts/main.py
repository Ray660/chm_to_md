import tkinter as tk
from tkinter import ttk, messagebox
import threading
from ui import select_folder
from extract import extract_all

def convert_with_progress(root, progress, selected_folder):
    from convert import convert_folder
    
    try:
        def update_progress(current, total, status):
            percent = int(current / total * 100)
            progress['value'] = percent
            root.update_idletasks()
        
        convert_folder(selected_folder, progress_callback=update_progress)
        
        progress['value'] = 100
        root.destroy()
        messagebox.showinfo("完成", "CHM 转 MD 已完成！\n\n请查看输出目录下的 md 文件夹。")
    except Exception as e:
        root.destroy()
        messagebox.showerror("错误", f"发生错误：{str(e)}")

def main():
    root = tk.Tk()
    root.withdraw()
    
    selected_folder = select_folder()
    if not selected_folder:
        messagebox.showinfo("取消", "已取消操作")
        return

    root.deiconify()
    root.title("CHM 转 MD")
    root.geometry("400x150")
    root.resizable(False, False)
    
    tk.Label(root, text="正在转换，请稍候...", font=("Microsoft YaHei", 12)).pack(pady=20)
    
    progress = ttk.Progressbar(root, length=300, mode='determinate')
    progress.pack(pady=10)
    
    tk.Label(root, text="0%", font=("Microsoft YaHei", 9)).place(x=180, y=90)
    
    # Extract CHM first
    try:
        extract_all(selected_folder)
    except Exception as e:
        messagebox.showerror("错误", f"解压失败：{str(e)}")
        return
    
    # Start conversion in background thread
    thread = threading.Thread(target=convert_with_progress, args=(root, progress, selected_folder))
    thread.daemon = True
    thread.start()
    
    root.mainloop()

if __name__ == '__main__':
    main()
