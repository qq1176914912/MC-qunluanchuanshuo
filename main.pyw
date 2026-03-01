# -*- coding: utf-8 -*-
"""
敲击步骤计算器 - 双击运行
开始前提示：先将红色和绿色箭头对齐
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from solver import OPERATIONS, solve

NAMES = [name for name, _ in OPERATIONS]


def run_calc():
    choices = [var1.get(), var2.get(), var3.get()]
    if not all(choices):
        messagebox.showinfo("提示", "请按物品要求，从左到右把三个「最后步骤」都选好。")
        return
    result = solve(choices)
    if "error" in result:
        messagebox.showerror("错误", result["error"])
        return
    out = result_text
    out.delete("1.0", tk.END)
    if not result["success"]:
        out.insert(tk.END, "无法用现有操作凑出目标值，请换一组最后三步试试。")
    else:
        out.insert(tk.END, "【完整点击顺序】先平衡再最后三步:\n  " + " → ".join(result["full_sequence"]))


def main():
    global var1, var2, var3, result_text

    root = tk.Tk()
    root.title("敲击步骤计算器")
    root.geometry("520x380")
    root.resizable(True, True)

    frame_top = ttk.Frame(root, padding="10")
    frame_top.pack(fill=tk.X)

    # 顶部红字提示：先保证红色和绿色箭头对齐
    ttk.Label(
        frame_top,
        text="开始前请先保证红色和绿色箭头对齐。",
        foreground="red",
    ).pack(anchor=tk.W, pady=(0, 4))

    ttk.Label(frame_top, text="按照物品要求的最后三个敲击要求（从左到右）选择：").pack(anchor=tk.W)

    row = ttk.Frame(frame_top)
    row.pack(fill=tk.X, pady=4)
    var1 = tk.StringVar()
    var2 = tk.StringVar()
    var3 = tk.StringVar()
    ttk.Label(row, text="第1格:").pack(side=tk.LEFT, padx=(0, 4))
    ttk.Combobox(row, textvariable=var1, values=NAMES, state="readonly", width=8).pack(side=tk.LEFT, padx=2)
    ttk.Label(row, text="第2格:").pack(side=tk.LEFT, padx=(12, 4))
    ttk.Combobox(row, textvariable=var2, values=NAMES, state="readonly", width=8).pack(side=tk.LEFT, padx=2)
    ttk.Label(row, text="第3格:").pack(side=tk.LEFT, padx=(12, 4))
    ttk.Combobox(row, textvariable=var3, values=NAMES, state="readonly", width=8).pack(side=tk.LEFT, padx=2)

    ttk.Button(frame_top, text="计算最少点击方案", command=run_calc).pack(pady=8)

    result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=16, font=("Consolas", 10), padx=8, pady=8)
    result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    root.mainloop()


if __name__ == "__main__":
    main()
