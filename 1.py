import tkinter as tk
from tkinter import ttk, messagebox, ttk
import json
import os

class RangeCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("多工站测试范围检查工具")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # 预设的工站数据
        self.stations = {
            "工站1": {
                "parameters": ["中孔真空度", "中孔流量", "中孔吸功", 
                             "小孔真空度", "小孔流量", "小孔吸功", "全堵真空度"],
                "min_values": {
                    "中孔真空度": 4.05,
                    "中孔流量": 5.73,
                    "中孔吸功": 23.2065,
                    "小孔真空度": 7.77,
                    "小孔流量": 2.16,
                    "小孔吸功": 16.7832,
                    "全堵真空度": 9.17
                },
                "max_values": {
                    "中孔真空度": 4.95,
                    "中孔流量": 6.32,
                    "中孔吸功": 31.284,
                    "小孔真空度": 9.08,
                    "小孔流量": 2.33,
                    "小孔吸功": 21.1564,
                    "全堵真空度": 10.63
                },
                "param_types": {  # 参数类型：numeric或string
                    "中孔真空度": "numeric",
                    "中孔流量": "numeric",
                    "中孔吸功": "numeric",
                    "小孔真空度": "numeric",
                    "小孔流量": "numeric",
                    "小孔吸功": "numeric",
                    "全堵真空度": "numeric"
                }
            },
            "工站2": {
                "parameters": ["ccd高脏污", "语音写入", "屏幕软件版本号", 
                             "屏幕硬件版本号", "软件版本号", "语音国别", 
                             "语音版本号1", "无水AD"],
                "min_values": {
                    "ccd高脏污": 1,
                    "语音写入": 1,
                    "屏幕软件版本号": 3,
                    "屏幕硬件版本号": 3,
                    "软件版本号": 15,
                    "语音国别": "B",
                    "语音版本号1": 1,
                    "无水AD": 3532
                },
                "max_values": {
                    "ccd高脏污": 1,
                    "语音写入": 1,
                    "屏幕软件版本号": 3,
                    "屏幕硬件版本号": 3,
                    "软件版本号": 15,
                    "语音国别": "B",
                    "语音版本号1": 1,
                    "无水AD": 3598
                },
                "param_types": {
                    "ccd高脏污": "numeric",
                    "语音写入": "numeric",
                    "屏幕软件版本号": "numeric",
                    "屏幕硬件版本号": "numeric",
                    "软件版本号": "numeric",
                    "语音国别": "string",
                    "语音版本号1": "numeric",
                    "无水AD": "numeric"
                }
            }
        }
        
        # 当前选择的工站
        self.current_station = "工站1"
        
        # 创建界面组件
        self.create_widgets()
        
        # 尝试加载保存的工站数据
        self.load_stations()
    
    def create_widgets(self):
        # 顶部控制栏
        control_frame = tk.Frame(self.root, padx=20, pady=10)
        control_frame.pack(fill=tk.X)
        
        # 工站选择下拉框
        station_label = tk.Label(control_frame, text="选择工站:", 
                               font=("微软雅黑", 12))
        station_label.pack(side=tk.LEFT, padx=5)
        
        self.station_var = tk.StringVar(value=self.current_station)
        self.station_combobox = ttk.Combobox(control_frame, 
                                           textvariable=self.station_var,
                                           values=list(self.stations.keys()),
                                           width=15)
        self.station_combobox.pack(side=tk.LEFT, padx=5)
        self.station_combobox.bind("<<ComboboxSelected>>", self.on_station_change)
        
        # 添加新工站按钮
        add_station_btn = tk.Button(control_frame, text="添加工站", 
                                  command=self.add_station,
                                  font=("微软雅黑", 10),
                                  bg="#2196F3", fg="white",
                                  padx=10, pady=2)
        add_station_btn.pack(side=tk.LEFT, padx=10)
        
        # 删除工站按钮
        delete_station_btn = tk.Button(control_frame, text="删除工站", 
                                     command=self.delete_station,
                                     font=("微软雅黑", 10),
                                     bg="#f44336", fg="white",
                                     padx=10, pady=2)
        delete_station_btn.pack(side=tk.LEFT, padx=5)
        
        # 标题框架
        title_frame = tk.Frame(self.root, padx=20, pady=5)
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(title_frame, text="测试参数范围检查工具", 
                              font=("微软雅黑", 16, "bold"))
        title_label.pack()
        
        # 创建标签页
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 范围设置标签页
        range_frame = ttk.Frame(notebook)
        notebook.add(range_frame, text="参数范围设置")
        
        # 测试值输入标签页
        input_frame = ttk.Frame(notebook)
        notebook.add(input_frame, text="输入测试值")
        
        # 工站识别标签页
        identify_frame = ttk.Frame(notebook)
        notebook.add(identify_frame, text="工站自动识别")
        
        # 范围设置标签页内容
        self.create_range_settings(range_frame)
        
        # 测试值输入标签页内容
        self.create_input_values(input_frame)
        
        # 工站识别标签页内容
        self.create_station_identification(identify_frame)
        
        # 按钮框架
        btn_frame = tk.Frame(self.root, padx=20, pady=10)
        btn_frame.pack(fill=tk.X)
        
        check_btn = tk.Button(btn_frame, text="检查范围", 
                           command=self.check_range,
                           font=("微软雅黑", 12),
                           bg="#4CAF50", fg="white",
                           padx=20, pady=5)
        check_btn.pack(side=tk.LEFT, padx=10)
        
        reset_btn = tk.Button(btn_frame, text="重置为默认范围", 
                           command=self.reset_default_range,
                           font=("微软雅黑", 12),
                           bg="#f44336", fg="white",
                           padx=20, pady=5)
        reset_btn.pack(side=tk.LEFT, padx=10)
        
        save_btn = tk.Button(btn_frame, text="保存工站设置", 
                           command=self.save_stations,
                           font=("微软雅黑", 12),
                           bg="#2196F3", fg="white",
                           padx=20, pady=5)
        save_btn.pack(side=tk.LEFT, padx=10)
        
        # 结果显示框架
        result_frame = tk.LabelFrame(self.root, text="检查结果", 
                                  font=("微软雅黑", 12), padx=10, pady=10)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.result_text = tk.Text(result_frame, height=10, width=70,
                                 font=("微软雅黑", 10))
        self.result_text.pack(fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(self.result_text, command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                           bd=1, relief=tk.SUNKEN, anchor=tk.W, 
                           font=("微软雅黑", 10))
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_range_settings(self, parent):
        """创建参数范围设置界面"""
        frame = tk.Frame(parent, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # 参数名称、最小值、最大值输入框
        self.range_entries = {}
        
        # 创建参数类型框架
        type_frame = tk.Frame(frame)
        type_frame.pack(fill=tk.X, pady=5)
        
        param_label = tk.Label(type_frame, text="参数名称", width=15, 
                             font=("微软雅黑", 10, "bold"))
        param_label.pack(side=tk.LEFT, padx=5)
        
        type_label = tk.Label(type_frame, text="参数类型", width=10, 
                            font=("微软雅黑", 10, "bold"))
        type_label.pack(side=tk.LEFT, padx=5)
        
        min_label = tk.Label(type_frame, text="最小值", width=10, 
                           font=("微软雅黑", 10, "bold"))
        min_label.pack(side=tk.LEFT, padx=5)
        
        max_label = tk.Label(type_frame, text="最大值", width=10, 
                           font=("微软雅黑", 10, "bold"))
        max_label.pack(side=tk.LEFT, padx=5)
        
        # 为每个参数创建输入框
        self.range_frame = tk.Frame(frame)
        self.range_frame.pack(fill=tk.BOTH, expand=True)
        
        self.update_range_settings()
    
    def create_input_values(self, parent):
        """创建测试值输入界面"""
        frame = tk.Frame(parent, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # 工站选择下拉框
        station_label = tk.Label(frame, text="选择工站:", 
                               font=("微软雅黑", 12))
        station_label.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.input_station_var = tk.StringVar(value=self.current_station)
        self.input_station_combobox = ttk.Combobox(frame, 
                                                textvariable=self.input_station_var,
                                                values=list(self.stations.keys()),
                                                width=15)
        self.input_station_combobox.pack(side=tk.LEFT, padx=5, pady=5)
        self.input_station_combobox.bind("<<ComboboxSelected>>", self.on_input_station_change)
        
        # 为每个参数创建输入框
        self.input_entries = {}
        
        # 创建参数框架
        self.input_frame = tk.Frame(frame)
        self.input_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.update_input_values()
    
    def create_station_identification(self, parent):
        """创建工站自动识别界面"""
        frame = tk.Frame(parent, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # 说明标签
        desc_label = tk.Label(frame, text="输入测试值，系统将自动识别可能的工站", 
                            font=("微软雅黑", 12))
        desc_label.pack(fill=tk.X, pady=10)
        
        # 为所有工站的参数创建输入框
        self.identify_entries = {}
        
        # 创建参数框架
        self.identify_frame = tk.Frame(frame)
        self.identify_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.update_station_identification()
        
        # 识别按钮
        identify_btn = tk.Button(frame, text="识别工站", 
                              command=self.identify_station,
                              font=("微软雅黑", 12),
                              bg="#2196F3", fg="white",
                              padx=20, pady=5)
        identify_btn.pack(pady=10)
        
        # 识别结果
        self.identify_result_var = tk.StringVar()
        identify_result_label = tk.Label(frame, textvariable=self.identify_result_var,
                                      font=("微软雅黑", 12),
                                      wraplength=700)
        identify_result_label.pack(fill=tk.X, pady=10)
    
    def update_range_settings(self):
        """更新参数范围设置界面"""
        # 清空现有框架
        for widget in self.range_frame.winfo_children():
            widget.destroy()
        
        # 获取当前工站的参数
        station_data = self.stations[self.current_station]
        parameters = station_data["parameters"]
        
        # 为每个参数创建输入框
        for param in parameters:
            row_frame = tk.Frame(self.range_frame)
            row_frame.pack(fill=tk.X, pady=5)
            
            # 参数名称标签
            param_label = tk.Label(row_frame, text=param, width=15, 
                                 font=("微软雅黑", 10))
            param_label.pack(side=tk.LEFT, padx=5)
            
            # 参数类型下拉框
            type_var = tk.StringVar(value=station_data["param_types"][param])
            type_combobox = ttk.Combobox(row_frame, 
                                      textvariable=type_var,
                                      values=["numeric", "string"],
                                      width=8)
            type_combobox.pack(side=tk.LEFT, padx=5)
            
            # 最小值输入框
            min_label = tk.Label(row_frame, text="最小值:", width=8)
            min_label.pack(side=tk.LEFT, padx=5)
            min_entry = tk.Entry(row_frame, width=10)
            min_entry.insert(0, str(station_data["min_values"][param]))
            min_entry.pack(side=tk.LEFT, padx=5)
            
            # 最大值输入框
            max_label = tk.Label(row_frame, text="最大值:", width=8)
            max_label.pack(side=tk.LEFT, padx=5)
            max_entry = tk.Entry(row_frame, width=10)
            max_entry.insert(0, str(station_data["max_values"][param]))
            max_entry.pack(side=tk.LEFT, padx=5)
            
            # 保存条目引用
            self.range_entries[param] = {
                "type": type_var,
                "min": min_entry,
                "max": max_entry
            }
    
    def update_input_values(self):
        """更新测试值输入界面"""
        # 清空现有框架
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        
        # 获取当前工站的参数
        station_data = self.stations[self.input_station_var.get()]
        parameters = station_data["parameters"]
        
        # 为每个参数创建输入框
        for param in parameters:
            row_frame = tk.Frame(self.input_frame)
            row_frame.pack(fill=tk.X, pady=5)
            
            param_label = tk.Label(row_frame, text=param, width=15, 
                                 font=("微软雅黑", 10))
            param_label.pack(side=tk.LEFT, padx=5)
            
            input_entry = tk.Entry(row_frame, width=10)
            input_entry.pack(side=tk.LEFT, padx=5)
            
            # 保存条目引用
            self.input_entries[param] = input_entry
    
    def update_station_identification(self):
        """更新工站识别界面"""
        # 清空现有框架
        for widget in self.identify_frame.winfo_children():
            widget.destroy()
        
        # 收集所有工站的唯一参数
        all_parameters = set()
        for station, data in self.stations.items():
            all_parameters.update(data["parameters"])
        
        # 为每个参数创建输入框
        for param in sorted(all_parameters):
            row_frame = tk.Frame(self.identify_frame)
            row_frame.pack(fill=tk.X, pady=5)
            
            param_label = tk.Label(row_frame, text=param, width=15, 
                                 font=("微软雅黑", 10))
            param_label.pack(side=tk.LEFT, padx=5)
            
            input_entry = tk.Entry(row_frame, width=10)
            input_entry.pack(side=tk.LEFT, padx=5)
            
            # 保存条目引用
            self.identify_entries[param] = input_entry
    
    def on_station_change(self, event=None):
        """处理工站选择变化"""
        self.current_station = self.station_var.get()
        self.update_range_settings()
        self.status_var.set(f"已切换到 {self.current_station}")
    
    def on_input_station_change(self, event=None):
        """处理测试值输入界面的工站选择变化"""
        self.update_input_values()
    
    def add_station(self):
        """添加新工站"""
        # 创建对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("添加新工站")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        
        # 居中显示
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 200, 
                                  self.root.winfo_rooty() + 150))
        
        # 工站名输入
        name_frame = tk.Frame(dialog, pady=10)
        name_frame.pack(fill=tk.X)
        
        name_label = tk.Label(name_frame, text="工站名:", width=10)
        name_label.pack(side=tk.LEFT, padx=10)
        
        name_entry = tk.Entry(name_frame, width=20)
        name_entry.pack(side=tk.LEFT, padx=10)
        
        # 参数列表
        params_frame = tk.Frame(dialog)
        params_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        params_label = tk.Label(params_frame, text="参数列表 (每行一个):")
        params_label.pack(anchor=tk.W)
        
        params_text = tk.Text(params_frame, height=10, width=30)
        params_text.pack(fill=tk.BOTH, expand=True)
        
        # 按钮
        btn_frame = tk.Frame(dialog, pady=10)
        btn_frame.pack(fill=tk.X)
        
        def save_station():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("错误", "请输入工站名!")
                return
            
            if name in self.stations:
                messagebox.showerror("错误", f"工站 '{name}' 已存在!")
                return
            
            params = [p.strip() for p in params_text.get(1.0, tk.END).split("\n") if p.strip()]
            if not params:
                messagebox.showerror("错误", "请至少添加一个参数!")
                return
            
            # 创建新工站数据
            self.stations[name] = {
                "parameters": params,
                "min_values": {p: 0 for p in params},
                "max_values": {p: 1 for p in params},
                "param_types": {p: "numeric" for p in params}
            }
            
            # 更新工站列表
            self.station_combobox['values'] = list(self.stations.keys())
            self.input_station_combobox['values'] = list(self.stations.keys())
            
            # 选择新工站
            self.current_station = name
            self.station_var.set(name)
            self.input_station_var.set(name)
            
            # 更新界面
            self.update_range_settings()
            self.update_input_values()
            self.update_station_identification()
            
            dialog.destroy()
            messagebox.showinfo("成功", f"已添加工站 '{name}'")
        
        save_btn = tk.Button(btn_frame, text="保存", 
                          command=save_station,
                          bg="#4CAF50", fg="white",
                          padx=10, pady=2)
        save_btn.pack(side=tk.LEFT, padx=10)
        
        cancel_btn = tk.Button(btn_frame, text="取消", 
                            command=dialog.destroy,
                            bg="#f44336", fg="white",
                            padx=10, pady=2)
        cancel_btn.pack(side=tk.LEFT, padx=10)
    
    def delete_station(self):
        """删除当前工站"""
        station = self.current_station
        if len(self.stations) <= 1:
            messagebox.showerror("错误", "至少保留一个工站!")
            return
        
        if messagebox.askyesno("确认", f"确定要删除工站 '{station}' 吗?"):
            del self.stations[station]
            
            # 更新工站列表
            new_stations = list(self.stations.keys())
            self.station_combobox['values'] = new_stations
            self.input_station_combobox['values'] = new_stations
            
            # 选择第一个工站
            self.current_station = new_stations[0]
            self.station_var.set(self.current_station)
            self.input_station_var.set(self.current_station)
            
            # 更新界面
            self.update_range_settings()
            self.update_input_values()
            self.update_station_identification()
            
            messagebox.showinfo("成功", f"已删除工站 '{station}'")
    
    def check_range(self):
        """检查输入值是否在范围内"""
        # 获取当前工站
        station = self.input_station_var.get()
        station_data = self.stations[station]
        
        # 获取当前范围设置
        current_min = {}
        current_max = {}
        param_types = {}
        
        for param, entries in self.range_entries.items():
            param_types[param] = entries["type"].get()
            
            try:
                if param_types[param] == "numeric":
                    min_val = float(entries["min"].get())
                    max_val = float(entries["max"].get())
                    
                    if max_val <= min_val:
                        messagebox.showerror("输入错误", f"{param}的最大值必须大于最小值！")
                        return
                    
                    current_min[param] = min_val
                    current_max[param] = max_val
                else:  # string
                    current_min[param] = entries["min"].get()
                    current_max[param] = entries["max"].get()
            except ValueError:
                messagebox.showerror("输入错误", f"{param}的范围值格式不正确！")
                return
        
        # 获取输入值
        input_values = {}
        for param, entry in self.input_entries.items():
            value = entry.get().strip()
            if not value:
                messagebox.showerror("输入错误", f"请输入{param}的测试值！")
                return
            
            try:
                if param_types[param] == "numeric":
                    input_values[param] = float(value)
                else:  # string
                    input_values[param] = value
            except ValueError:
                messagebox.showerror("输入错误", f"{param}的测试值必须是数字！")
                return
        
        # 检查范围
        out_of_range = []
        for param, value in input_values.items():
            if param_types[param] == "numeric":
                if value < current_min[param] or value > current_max[param]:
                    out_of_range.append(f"{param}（值：{value}，范围：{current_min[param]}-{current_max[param]}）")
            else:  # string
                if value != current_min[param]:  # 对于字符串，要求完全匹配
                    out_of_range.append(f"{param}（值：{value}，要求：{current_min[param]}）")
        
        # 显示结果
        self.result_text.delete(1.0, tk.END)
        if out_of_range:
            result = f"以下参数不在设定范围内（工站：{station}）：\n\n" + "\n".join(out_of_range)
        else:
            result = f"所有测试值均在设定范围内（工站：{station}）！"
        
        self.result_text.insert(tk.END, result)
        self.status_var.set(f"已完成测试值检查（工站：{station}）")
    
    def reset_default_range(self):
        """重置为默认范围"""
        if messagebox.askyesno("确认", f"确定要重置 {self.current_station} 的参数范围为默认值吗?"):
            # 恢复到初始预设值
            if self.current_station == "工站1":
                # 工站1的初始预设值
                self.stations[self.current_station]["min_values"] = {
                    "中孔真空度": 4.05,
                    "中孔流量": 5.73,
                    "中孔吸功": 23.2065,
                    "小孔真空度": 7.77,
                    "小孔流量": 2.16,
                    "小孔吸功": 16.7832,
                    "全堵真空度": 9.17
                }
                self.stations[self.current_station]["max_values"] = {
                    "中孔真空度": 4.95,
                    "中孔流量": 6.32,
                    "中孔吸功": 31.284,
                    "小孔真空度": 9.08,
                    "小孔流量": 2.33,
                    "小孔吸功": 21.1564,
                    "全堵真空度": 10.63
                }
            elif self.current_station == "工站2":
                # 工站2的初始预设值
                self.stations[self.current_station]["min_values"] = {
                    "ccd高脏污": 1,
                    "语音写入": 1,
                    "屏幕软件版本号": 3,
                    "屏幕硬件版本号": 3,
                    "软件版本号": 15,
                    "语音国别": "B",
                    "语音版本号1": 1,
                    "无水AD": 3532
                }
                self.stations[self.current_station]["max_values"] = {
                    "ccd高脏污": 1,
                    "语音写入": 1,
                    "屏幕软件版本号": 3,
                    "屏幕硬件版本号": 3,
                    "软件版本号": 15,
                    "语音国别": "B",
                    "语音版本号1": 1,
                    "无水AD": 3598
                }
            
            # 更新界面
            self.update_range_settings()
            messagebox.showinfo("成功", f"已重置 {self.current_station} 的参数范围为默认值")
    
    def save_stations(self):
        """保存所有工站设置"""
        try:
            # 获取当前范围设置
            for param, entries in self.range_entries.items():
                param_type = entries["type"].get()
                
                if param_type == "numeric":
                    min_val = float(entries["min"].get())
                    max_val = float(entries["max"].get())
                else:  # string
                    min_val = entries["min"].get()
                    max_val = entries["max"].get()
                
                self.stations[self.current_station]["min_values"][param] = min_val
                self.stations[self.current_station]["max_values"][param] = max_val
                self.stations[self.current_station]["param_types"][param] = param_type
            
            # 保存到文件
            with open("station_settings.json", "w", encoding="utf-8") as f:
                json.dump(self.stations, f, ensure_ascii=False, indent=4)
            
            messagebox.showinfo("成功", "所有工站设置已保存！")
            self.status_var.set("工站设置已保存")
        except Exception as e:
            messagebox.showerror("错误", f"保存失败：{str(e)}")
    
    def load_stations(self):
        """从文件加载工站设置"""
        try:
            if os.path.exists("station_settings.json"):
                with open("station_settings.json", "r", encoding="utf-8") as f:
                    self.stations = json.load(f)
                
                # 更新界面
                self.station_combobox['values'] = list(self.stations.keys())
                self.input_station_combobox['values'] = list(self.stations.keys())
                
                # 确保current_station有效
                if self.current_station not in self.stations:
                    self.current_station = list(self.stations.keys())[0]
                    self.station_var.set(self.current_station)
                    self.input_station_var.set(self.current_station)
                
                self.update_range_settings()
                self.update_input_values()
                self.update_station_identification()
                
                self.status_var.set("已加载保存的工站设置")
        except Exception as e:
            messagebox.showerror("错误", f"加载设置失败：{str(e)}")
    
    def identify_station(self):
        """自动识别工站"""
        # 获取输入值
        input_values = {}
        for param, entry in self.identify_entries.items():
            value = entry.get().strip()
            if value:
                try:
                    input_values[param] = float(value)
                except ValueError:
                    input_values[param] = value
        
        if not input_values:
            messagebox.showerror("错误", "请至少输入一个测试值！")
            return
        
        # 检查每个工站的匹配度
        station_matches = {}
        for station, data in self.stations.items():
            match_count = 0
            total_params = 0
            
            for param in data["parameters"]:
                if param in input_values:
                    total_params += 1
                    
                    # 检查是否在范围内
                    if data["param_types"][param] == "numeric":
                        value = float(input_values[param])
                        if value >= data["min_values"][param] and value <= data["max_values"][param]:
                            match_count += 1
                    else:  # string
                        if input_values[param] == data["min_values"][param]:
                            match_count += 1
            
            if total_params > 0:
                match_rate = match_count / total_params
                station_matches[station] = {
                    "match_rate": match_rate,
                    "matched_params": match_count,
                    "total_params": total_params
                }
        
        # 排序并显示结果
        sorted_matches = sorted(station_matches.items(), 
                             key=lambda x: x[1]["match_rate"], 
                             reverse=True)
        
        result = "工站识别结果：\n\n"
        if not sorted_matches:
            result += "没有找到匹配的工站，请检查输入值。"
        else:
            for station, stats in sorted_matches:
                result += f"{station}: 匹配度 {stats['match_rate']*100:.1f}% "
                result += f"({stats['matched_params']}/{stats['total_params']} 参数匹配)\n"
        
        self.identify_result_var.set(result)
        self.status_var.set("已完成工站识别")


if __name__ == "__main__":
    root = tk.Tk()
    app = RangeCheckerApp(root)
    root.mainloop()