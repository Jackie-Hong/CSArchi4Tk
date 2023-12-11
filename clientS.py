import tkinter as tk
from tkinter import simpledialog, messagebox
import requests


class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Chat Client')

        self.text_area = tk.Text(root, wrap=tk.WORD, width=40, height=10)
        self.text_area.pack(padx=10, pady=10)

        self.entry = tk.Entry(root, width=40)
        self.entry.pack(pady=10)

        self.login_button = tk.Button(root, text='Login', command=self.login)
        self.login_button.pack(side=tk.LEFT, padx=5)

        self.send_button = tk.Button(root, text='Send', command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=5)

        self.logout_button = tk.Button(root, text='Logout', command=self.logout)
        self.logout_button.pack(side=tk.LEFT, padx=5)

        self.user_id = None
        # 创建 Session 对象，并将 CookieJar 对象传递给它
        self.session = requests.Session()

    def login(self):
        self.user_id = tk.simpledialog.askstring("Login", "Enter your user ID:")
        if self.user_id:
            data = {'user_id': self.user_id}
            response = self.session.post('http://127.0.0.1:5000/login', data=data)
            print(response.text)
            print(response.json())
            self.text_area.insert(tk.END, f'{response.json()["message"]}\n')

        # 发送登录请求
        login_data = {'user_id': self.user_id}
        response = self.session.post('http://127.0.0.1:5000/login', data=login_data)

        # 打印登录结果
        print("text", response.text)
        print("json", response.json())

    def send_message(self):
        if not self.user_id:
            tk.messagebox.showinfo("Error", "Please login first.")
            return

        message = self.entry.get()
        if message:
            data = {'user_id': self.user_id, 'message': message}
            response = self.session.post('http://127.0.0.1:5000/api', data=data)

            if response.status_code == 200:
                response_data = response.json()
                user_id = response_data.get('user_id')
                received_message = response_data.get('message')
                self.text_area.insert(tk.END, f'{user_id}: {received_message}\n')

            self.entry.delete(0, tk.END)

    def logout(self):
        if not self.user_id:
            tk.messagebox.showinfo("Error", "You are not logged in.")
            return

        response = self.session.get('http://127.0.0.1:5000/logout')
        print(response.json())
        self.text_area.insert(tk.END, f'{response.json()["message"]}\n')
        self.user_id = None
        self.session.close()


if __name__ == '__main__':
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()
