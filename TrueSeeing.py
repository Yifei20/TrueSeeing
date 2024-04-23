
import unicodedata
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import filedialog
from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto import Random
import os


class TrueSeeingApp:



    def init_list(self):
        self.graphical_characters_ascii:list = []
        self.graphical_characters_ascii.extend(chr(i) for i in range(65, 91))
        self.graphical_characters_ascii.extend(chr(i) for i in range(97, 123))
        self.graphical_characters_ascii.extend(str(i) for i in range(0,10))
        self.graphical_characters_ascii.extend("""!"#$%&"()*+,-./:;<=>?@[\]^_`{|}~""")

        self.graphical_characters_unicode:list  = []
        self.harmful_format_unicode:list = []
        self.harmless_format:list = ["\t", "\n", "\r"]
        for code_point in range(0, 0x110000):
            char = chr(code_point)
            category = unicodedata.category(char)
            if char.isascii():
                if (not char.isprintable()) and (not char in self.harmless_format):
                   self.harmful_format_unicode.append(char)
            elif char.isprintable():
                self.graphical_characters_unicode.append(char)
            else:
                self.harmful_format_unicode.append(char)


    def __init__(self):
        self.root = tk.Tk()
        self.GUI_init()
        self.GUI_choose_encoding_format()


        # self.check_button = tk.Button(self.root, text="Check Text", command=self.check_text)
        # self.check_button.pack(pady=5)

        # self.signature_signature_label = tk.Label(self.root, text="Digital Signature:")
        # self.signature_signature_label.pack(pady=5)

        # self.signature = tk.Entry(self.root, width=60)
        # self.signature.pack(pady=5)



    def show_original_text(self):
        pass

    def show_true_text(self,event):
        originalText:str = self.text_area_p1.get("1.0","end")
        self.text_area_p2.configure(state="normal")
        self.text_area_p2.delete("1.0","end")
        originalText = originalText[0:len(originalText)-1]
        self.is_benign = False
        for c in originalText:
            if c in self.graphical_characters_ascii:
                self.text_area_p2.insert("end",c,"n")
                self.text_area_p2.tag_add("n","end")
            elif c in self.graphical_characters_unicode:
                self.text_area_p2.insert("end",c,"color1")
                self.text_area_p2.tag_add("color1","end")
                self.text_area_p2.tag_config("color1",foreground="blue")
                self.is_benign = True
            elif c in self.harmful_format_unicode:
                real = repr(c)
                idx = self.text_area_p2.index("end-1c")
                self.text_area_p2.insert("end",real,"color2")
                self.text_area_p2.tag_add("color2","end-1c")
                self.text_area_p2.tag_config("color2",foreground="red")
            elif c in self.harmless_format:
                idx = self.text_area_p2.index("end-1c")
                self.text_area_p2.insert("end",repr(c),"color3")
                self.text_area_p2.tag_add("color3","end-1c")
                self.text_area_p2.tag_config("color3",foreground="green")
                self.is_benign = True
        self.text_area_p2.configure(state="disabled")
        if (self.is_benign):
            self.signature_button.config(state="disabled")
        else:
            self.signature_button.config(state="normal")

    # init the GUI panel
    def GUI_init(self):
        self.root.title("TrueSeeing")
        self.root.iconbitmap("TrueSeeingIcon.ico")
        self.root.geometry("500x800+200+200")
        self.root.resizable(False, False)

        self.frame_panel_labels = tk.Frame(self.root)
        self.frame_panel_labels.pack()
        self.label_encoding_format = tk.Label(self.frame_panel_labels, text="Encoding Format", relief="raised")
        self.label_encoding_format.pack(side="left")
        self.label_text_examination = tk.Label(self.frame_panel_labels, text="Text examination", relief="raised")
        self.label_text_examination.pack(side="left")
        self.label_signature = tk.Label(self.frame_panel_labels, text="Signature", relief="raised")
        self.label_signature.pack(side="left")



    # choose encode format panel
    def GUI_choose_encoding_format(self):
        # init the panel head
        self.label_encoding_format.config(relief="sunken")

        self.encoding_format = tk.StringVar()
        self.encoding_format.set("UTF-8")

        # panel body
        self.frame_CEF = tk.Frame(self.root)
        self.frame_CEF.pack()
        self.label = tk.Label(self.frame_CEF, text="Select Encoding:")
        self.label.pack()
        self.radio_button_UTF_8 = tk.Radiobutton(self.frame_CEF, text="UTF-8", variable=self.encoding_format, value="UTF-8")
        self.radio_button_UTF_8.pack()
        self.radio_button_UTF_16 = tk.Radiobutton(self.frame_CEF, text="UTF-16", variable=self.encoding_format, value="UTF-16")
        self.radio_button_UTF_16.pack()
        self.button_choose_encoding_format = tk.Button(self.frame_CEF, cursor="hand2", text="OK", command=lambda: self.GUI_text_examination(self.encoding_format.get()))
        self.button_choose_encoding_format.pack()

        # panel bottom
        self.label_frame_SCF = tk.LabelFrame(self.frame_CEF, text="tip")
        self.label_frame_SCF.pack(fill="both", padx=4)
        self.label_tip_CEF = tk.Label(self.label_frame_SCF, text="You have to choose the encoding format from UTF-8 and UTF-16.\n")
        self.label_tip_CEF.pack()




    # text examination panel
    def GUI_text_examination(self, encoding_format):
        # init the panel head
        self.frame_CEF.pack_forget()
        self.label_encoding_format.config(relief="raised")
        self.label_text_examination.config(relief="sunken")
        self.init_list()

        self.encoding_format = encoding_format

        # panel body
        self.frame_TE = tk.Frame(self.root)
        self.frame_TE.pack()

        # p1
        self.label_p1 = tk.Label(self.frame_TE,text="original")
        self.label_p1.pack(padx=10, pady=10)

        #p1 text area frame
        self.frame_text_area_p1 = tk.Frame(self.frame_TE)
        self.frame_text_area_p1.pack()

        self.scrollbar_p1 = tk.Scrollbar(self.frame_text_area_p1)
        self.scrollbar_p1.pack(side="right", fill="y")

        self.text_area_p1 = tk.Text(self.frame_text_area_p1,height=10, yscrollcommand=self.scrollbar_p1.set)
        self.text_area_p1.pack(padx=5)

        self.scrollbar_p1.config(command=self.text_area_p1.yview)

        # get content from clipboard
        self.button_clipboard = tk.Button(self.frame_TE, text="paste", command=lambda: self.input_from_clipboard())
        self.button_clipboard.pack(padx=10, pady=10)

        # get content from local file
        self.button_import_local_file = tk.Button(self.frame_TE, text="import local file", command=lambda: self.import_local_file(encoding_format))
        self.button_import_local_file.pack(padx=10, pady=10)

        # get content from typing, update p2 as long as enter any content in p1
        self.text_area_p1.bind("<KeyRelease>",self.show_true_text)

        # paste
        # callback function will read binary buffer from clipboard and decode using encoding format
        # self.text_area_p1.bind("<Control-v>",self.input_from_clipboard)
        # self.text_area_p1.bind("<Control-V>",self.input_from_clipboard)

        # get content from clipboard
        # if self.root.clipboard_get().strip():
        #     self.text_area_p1.insert("1.0", self.root.clipboard_get())

        # p1 tip
        self.label_frame_TE_p1 = tk.LabelFrame(self.frame_TE, text="tip")
        self.label_frame_TE_p1.pack(fill="both", padx=4)
        self.label_tip_p1 = tk.Label(self.label_frame_TE_p1,
                                          text="To examine the text, \n"
                                               "you can copy an external text to the above text area \n"
                                               "or import a local file, and edit on the text.\n"
                                               "And we show the original appearance of the input in above text area.\n")
        self.label_tip_p1.pack()

        # p2
        self.label_p2 = tk.Label(self.frame_TE,text="True text")
        self.label_p2.pack(padx=10, pady=10)
        # p2 text area frame
        self.frame_text_area_p2 = tk.Frame(self.frame_TE)
        self.frame_text_area_p2.pack(padx=5)

        self.scrollbar_p2 = tk.Scrollbar(self.frame_text_area_p2)
        self.scrollbar_p2.pack(side="right", fill="y")

        self.text_area_p2 = tk.Text(self.frame_text_area_p2,height=10, yscrollcommand=self.scrollbar_p2.set)
        self.text_area_p2.pack()

        self.scrollbar_p2.config(command=self.text_area_p2.yview)

        self.text_area_p2.config(state="disabled")

        # p2 tip
        self.label_frame_TE_p2 = tk.LabelFrame(self.frame_TE, text="tip")
        self.label_frame_TE_p2.pack(fill="both", padx=4)
        self.label_tip_p2 = tk.Label(self.label_frame_TE_p2,
                                          text="As long as you input, we check the content instantly.\n"
                                               "In the above text area, \n"
                                               "the characters are divided into four categories and shown in different colors:\n"
                                               "1. English graphic characters: in black\n"
                                               "2. All other Unicode graphic characters: in blue\n"
                                               "3. Harmless Unicode format characters: in red\n"
                                               "4. All other Unicode format characters that are potentially harmful: in green\n"
                                               "As long as the character category 2 and 4 exist, the signature button stays disabled.\n")
        self.label_tip_p2.pack()


        # signature button
        self.signature_button = tk.Button(self.frame_TE,text="Generate signature",command=lambda:self.GUI_signature())
        self.signature_button.pack(padx=10, pady=10)



    def GUI_signature(self):
        # init the panel
        self.frame_TE.pack_forget()
        self.label_text_examination.config(relief="raised")
        self.label_signature.config(relief="sunken")

        self.frame_S = tk.Frame(self.root)
        self.frame_S.pack()

        # generate signature
        # signature frame
        self.frame_signature_text = tk.Frame(self.frame_S)
        self.frame_signature_text.pack()

        self.scrollbar_signature = tk.Scrollbar(self.frame_signature_text)
        self.scrollbar_signature.pack(side="right", fill="y")

        self.signature_text = tk.Text(self.frame_signature_text,height=10, yscrollcommand=self.scrollbar_signature.set)
        self.signature_text.pack(padx=5)

        self.scrollbar_signature.config(command=self.signature_text.yview)
        self.signature_text.config(state="disabled")

        self.generate_signature(self.text_area_p1.get("1.0", tk.END))


        # self.public_key = tk.StringVar(self.frame_S,"Public key:(N = NaN,e = NaN)")
        # self.public_key_label = tk.Label(self.frame_S,textvariable=self.public_key)
        # self.public_key_label.pack(padx=10,pady=10)

        # show algorithm
        self.algorithm_label = tk.Label(self.frame_S,text="We have successfully generate the signature for this text\n"
                                                          "in the above text area with the algorithm:\n"
                                                          "RSA-FDH: RSA full-domain hash.\n")
        self.algorithm_label.pack(padx=10,pady=10)

        # algorithm tip
        self.label_frame_S_algorithm = tk.LabelFrame(self.frame_S, text="tip")
        self.label_frame_S_algorithm.pack(fill="both", padx=4)
        self.label_tip_algorithm = tk.Label(self.label_frame_S_algorithm,
                                          text="You can find the file named \"private.pem\" for private key and \"public.pem\" for public key.\n")
        self.label_tip_algorithm.pack()

    # import local file to p1
    def import_local_file(self,encoding_format):
        local_file_path = filedialog.askopenfilename()
        # max file size 10MB
        if local_file_path:
            try:
                with open(local_file_path, "rb") as file:
                    local_file_content = file.read()
                self.text_area_p1.delete("1.0", tk.END)
                # 尝试用用户提供的编码格式解码文件内容
                decoded_content = local_file_content.decode(encoding_format)
                self.text_area_p1.insert("1.0", decoded_content)
                self.show_true_text(None)
            except UnicodeDecodeError as e:
                # 如果解码失败，弹出一个警告框
                messagebox.showerror("Encoding error", f"File encoding is not {encoding_format}")
            except Exception as e:
                # 处理其他可能的异常
                messagebox.showerror("Error", f"Error: {str(e)}")


    def input_from_clipboard(self):
        try:
            clipboard_content = self.root.clipboard_get()
            self.text_area_p1.insert("1.0", clipboard_content)
            self.show_true_text(None)
        except tk.TclError as e:
            messagebox.showerror("Clipboard Error", "Failed to get clipboard content.")

    def check_text(self):
        text = self.text_area_p1.get("1.0", tk.END).strip()

        # Check for potentially harmful characters
        harmful_characters = self.detect_harmful_characters(text)

        if harmful_characters:
            self.display_warning("Potentially harmful characters detected!")
        else:
            # self.signature_label.config(text="Digital Signature:")
            # self.signature_entry.delete(0, tk.END)
            signature = self.generate_signature(text)
            self.signature.config(text=signature)
        

    def detect_harmful_characters(self, text):
        # Example: Detecting harmful characters (e.g., non-ASCII characters)
        harmful_characters = [char for char in text if char in self.graphical_characters_unicode or char in self.harmful_format_unicode]
        return len(harmful_characters) > 0

    def display_warning(self, message):
        warning_window = tk.Toplevel(self.root)
        warning_window.title("Warning!")

        warning_label = tk.Label(warning_window, text=message)
        warning_label.pack(padx=20, pady=10)

        ok_button = tk.Button(warning_window, text="OK", command=warning_window.destroy)
        ok_button.pack(pady=5)


    # create public and private key pair
    def generate_keys(self,bits):
        private_key_path = "private.pem"
        public_key_path = "public.pem"
        private_key = None
        public_key = None
        # 检查私钥和公钥文件是否都存在
        if os.path.exists(private_key_path) and os.path.exists(public_key_path):
            # 导入现有密钥
            with open(private_key_path, "rb") as priv_file:
                private_key = RSA.import_key(priv_file.read())
            with open(public_key_path, "rb") as pub_file:
                public_key = RSA.import_key(pub_file.read())
        else:
            # 生成新的密钥对
            key = RSA.generate(bits, Random.new().read)
            private_key = key.export_key()
            public_key = key.publickey().export_key()
            
            # 保存私钥和公钥到文件
            with open(private_key_path, "wb") as priv_file:
                priv_file.write(private_key)
            with open(public_key_path, "wb") as pub_file:
                pub_file.write(public_key)

            # 重新导入密钥，确保一致性
            private_key = RSA.import_key(private_key)
            public_key = RSA.import_key(public_key)

        return private_key, public_key

    def sign_text(self,text:str):
        key_bits = 2048
        private_key, public_key = self.generate_keys(key_bits)
        # private_key = RSA.import_key(private_key_bytes)
        # public_key = RSA.import_key(public_key_bytes)
        modulus = private_key.n
        text_buffer = text.encode(encoding=self.encoding_format)
        hash_obj = SHA256.new(text_buffer)
        hashed_integer = int.from_bytes(hash_obj.digest(), byteorder="big")
        signature = pow(hashed_integer, private_key.d, private_key.n)
        return signature.to_bytes(key_bits//8,byteorder="big")


    # only runs until all characters in text belong to category 1 or 3
    def generate_signature(self, text):
        if self.detect_harmful_characters(text):
            self.display_warning("Harmful characters exist")
            return
        signature= self.sign_text(text)
        self.signature_text.config(state="normal")
        self.signature_text.delete("1.0",tk.END)
        self.signature_text.insert("end",signature.hex())
        self.signature_text.config(state="disabled")
        
    def run(self):
        self.root.mainloop()
        

# Create the main window

app = TrueSeeingApp()
app.run()