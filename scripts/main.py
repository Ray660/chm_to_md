import tkinter as tk
from tkinter import ttk, messagebox
import threading
import sys
import os
from ui import select_folder
from extract import extract_all

class ProgressWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        
        self.selected_folder = select_folder()
        if not self.selected_folder:
            messagebox.showinfo("取消", "已取消操作")
            self.root.destroy()
            return
        
        # Check if folder has CHM files
        chm_files = [f for f in os.listdir(self.selected_folder) if f.lower().endswith('.chm')]
        if not chm_files:
            messagebox.showinfo("提示", "所选文件夹中没有找到CHM文件")
            self.root.destroy()
            return
        
        self.root.deiconify()
        self.root.title("CHM 转 MD")
        self.root.geometry("400x150")
        self.root.resizable(False, False)
        
        tk.Label(self.root, text="正在转换，请稍候...", font=("Microsoft YaHei", 12)).pack(pady=20)
        
        self.progress = ttk.Progressbar(self.root, length=300, mode='determinate')
        self.progress.pack(pady=10)
        
        self.percent_label = tk.Label(self.root, text="0%", font=("Microsoft YaHei", 9))
        self.percent_label.place(x=180, y=90)
        
        self.status_label = tk.Label(self.root, text="", font=("Microsoft YaHei", 8))
        self.status_label.pack(side=tk.BOTTOM, pady=5)
        
        self.convert()
    
    def convert(self):
        try:
            extract_all(self.selected_folder)
        except Exception as e:
            messagebox.showerror("错误", f"解压失败：{str(e)}")
            self.root.destroy()
            return
        
        thread = threading.Thread(target=self.convert_thread)
        thread.daemon = True
        thread.start()
    
    def convert_thread(self):
        from convert import convert_folder
        
        try:
            def update_progress(current, total, status):
                if total > 0:
                    percent = int(current / total * 100)
                    self.progress['value'] = percent
                    self.percent_label.config(text=f"{percent}%")
                    self.status_label.config(text=status)
                    self.root.update_idletasks()
            
            convert_folder(self.selected_folder, progress_callback=update_progress)
            
            self.progress['value'] = 100
            self.percent_label.config(text="100%")
            self.root.update_idletasks()
            
            self.root.after(100, self.show_complete)
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.root.after(100, lambda: self.show_error(str(e)))
    
    def show_complete(self):
        self.root.destroy()
        messagebox.showinfo("完成", "CHM 转 MD 已完成！\n\n请查看输出目录下的 md 文件夹。")
    
    def show_error(self, msg):
        self.root.destroy()
        messagebox.showerror("错误", f"发生错误：{str(msg)}")

def main():
    ProgressWindow()

if __name__ == '__main__':
    main()
