import tkinter as tk
import cv2
from PIL import Image, ImageTk
from main import BrightnessControl
import threading
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Điều chỉnh ánh sáng')
        screen_width = self.winfo_screenwidth()
        
        screen_height = self.winfo_screenheight()
        self.geometry(f'{screen_width}x{screen_height}')
        self.running = False
        self.capture = None
        self.brightness_control = BrightnessControl()
        #Tạo tiêu đề cho ứng dụng
        self.title_label = tk.Label(self,
                                    text='Ứng dụng điều chỉnh ánh sáng qua cử chỉ bàn tay',
                                    font=('calibri', 20, 'bold'),
                                    )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10, sticky='nsew')

        #Tạo các text widget cho row1, row2, row3
        self.text_widget_intro = tk.Text(self,
                                          bg='mistyrose',
                                          fg='black',
                                          height=10,
                                          width=10)
        self.text_widget_intro.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        self.text_widget_intro.insert('end', 'Ứng dụng điều chỉnh ánh sáng\n', 'bold')
        self.text_widget_intro.tag_config('bold', font=('calibri', 16, 'bold'))
        self.text_widget_intro.insert('end', 'Ứng dụng này giúp người dùng điều chỉnh độ sáng màn hình thông qua cử chỉ bàn tay, mang đến một trải nghiệm tiện lợi.\n\n', 'normal')
        self.text_widget_intro.insert('end', 'Các tính năng chính:\n', 'bold')
        self.text_widget_intro.insert('end', '- Điều chỉnh độ sáng bằng cử chỉ tay.\n', 'normal')
        self.text_widget_intro.insert('end', '- Giao diện thân thiện, dễ sử dụng.\n', 'normal')
        self.text_widget_intro.insert('end', '- Tự động nhận diện và điều chỉnh ánh sáng.\n', 'normal')
        self.text_widget_intro.config(state='disabled')
        self.text_widget_members = tk.Text(self,
                                            bg='mistyrose',
                                            fg='black',
                                            height=10,
                                            width=10)
        self.text_widget_members.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')
        self.text_widget_members.insert('end', 'Nhóm 1\n', 'bold')
        self.text_widget_members.insert('end', 'Lớp học phần: Xử lý ảnh và thị giác máy tính\n', 'normal')
        self.text_widget_members.insert('end', 'Mã lớp học phần: 010100086904 \n', 'normal')
        self.text_widget_members.tag_config('bold', font=('calibri', 16, 'bold'))
        self.text_widget_members.insert('end', 'Thành viên nhóm:\n', 'bold')
        self.text_widget_members.insert('end', 'Đặng Gia Bảo\n', 'normal')
        self.text_widget_members.insert('end', 'Nguyễn Lê Hưng\n', 'normal')
        self.text_widget_members.insert('end', 'Phạm Nguyễn Gia Huy\n', 'normal')
        self.text_widget_members.insert('end', 'Nguyễn Đức Anh Khoa\n', 'normal')
        self.text_widget_members.insert('end', 'Nguyễn Hoàng Trung Nguyên', 'normal')
        self.text_widget_members.config(state='disabled')

        self.text_widget_use = tk.Text(self,
                                        bg='mistyrose',
                                        fg='black',
                                        height=10,
                                        width=10)
        self.text_widget_use.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')
        self.text_widget_use.insert('end', 'Cách sử dụng\n', 'bold')
        self.text_widget_use.tag_config('bold', font=('calibri', 16, 'bold'))
        self.text_widget_use.insert('end', '- Hãy bấm vào nút bắt đầu để ứng dụng nhận camera của bạn.\n', 'normal')
        self.text_widget_use.insert('end', '- Ứng dụng nhận diện độ dài từ ngón trỏ đến ngón cái của bạn để tăng giảm độ sáng.\n', 'normal')
        self.text_widget_use.insert('end', '- Thu nhỏ khoảng cách giữa 2 ngón sẽ giảm độ sáng và ngược lại.\n', 'normal')
        self.text_widget_use.config(state='disabled')

        #Gộp cột 2 từ row1 đến row3 để chứa camera
        self.camera_frame = tk.Frame(self,
                                     bd=2,
                                     bg='pink',
                                     relief='groove')
        self.camera_frame.grid(row=1, column=1, rowspan=3, padx=10, pady=10, sticky='nsew')
        
        self.camera_label = tk.Label(self.camera_frame)
        self.camera_label.pack(expand=True, fill='both')

        #Row 4, cột 1: Chia thành 3 cột nhỏ hơn cho các button, tất cả nằm trong cột 1
        self.button_frame = tk.Frame(self)
        
        self.button_frame.grid(row=4, column=1, padx=10, pady=10, sticky='n')

        self.button1 = tk.Button(self.button_frame,
                                 text='Dừng',
                                 font=('calibri', 12),
                                 bd=2,
                                 relief='groove',
                                 height=2,
                                 command=self.stop_camera)
        
        self.button2 = tk.Button(self.button_frame,
                                 text='Bắt đầu',
                                 font=('calibri', 12),
                                 bd=2,
                                 relief='groove', 
                                 command=self.start_camera)
        
        
        #Đặt các nút vào trong khung với layout 3 cột nhỏ
        self.button1.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.button2.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

        #Cấu hình để 3 cột này có kích thước bằng nhau
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)

        #Cấu hình các hàng và cột để mở rộng đều nhau
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
    def update_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img_tk = ImageTk.PhotoImage(image=img)
        self.camera_label.imgtk = img_tk
        self.camera_label.configure(image=img_tk)

    def start_camera(self):
        if not self.running:
            self.running = True
        # Chạy camera trên luồng riêng
            threading.Thread(
            target=self.brightness_control.start_camera,
            args=(self.update_frame,),
            daemon=True
        ).start()

    def stop_camera(self):
        if self.running:
            self.running = False
            self.brightness_control.stop_camera()
            self.camera_label.config(image='')
if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()