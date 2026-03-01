import tkinter
from tkinter import filedialog
import customtkinter
from PIL import ImageTk, Image
import os
import EXIFframe
from lang import LANGUAGES, CURRENT_LANG

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

bool_firstimport = True
tk_img = None
img_preview_id = None
outputdir = '/output'
first_file_path = None
current_language = CURRENT_LANG

def get_text(key):
    return LANGUAGES[current_language].get(key, key)

class App(customtkinter.CTk):

    def runWatermark():
        return 0

    def __init__(self):
        super().__init__()

        self.tk_img = None
        self.image_refs = []

        def getcurrentdir():
            return os.path.normpath(os.getcwd())

        def load_combobox_options(dir):
            list_logos = []
            try:
                list_filenames = os.listdir(dir)
                for n in list_filenames:
                    if n.endswith('.png'):
                        list_logos.append(n.replace('.png', ''))
            except Exception:
                pass
            return list_logos

        def change_language(lang):
            global current_language
            current_language = lang
            self.update_all_texts()

        def update_all_texts():
            self.title(get_text('app_title'))
            self.button_browsefile.configure(text=get_text('browse_image'))
            self.button_removefile.configure(text=get_text('remove'))
            self.button_removefileall.configure(text=get_text('remove_all'))
            self.label_preview.configure(text=get_text('preview'))
            self.label_logo.configure(text=get_text('logo'))
            self.label_outputpath.configure(text=get_text('output_path'))
            self.button_browsepath.configure(text=get_text('browse'))
            self.label_outputname.configure(text=get_text('output_filename'))
            self.label_outputstem.configure(text=get_text('original_filename_plus'))
            self.label_language.configure(text=get_text('language'))
            self.button_run.configure(text=get_text('run'))

        self.title(get_text('app_title'))
        self.geometry(f"{900}x{600}")
        self.minsize(900, 600)

        self.left_frame = customtkinter.CTkFrame(self, width=400, corner_radius=0)
        self.left_frame.pack(fill='y', side='left')

        self.lang_frame = customtkinter.CTkFrame(self.left_frame)
        self.lang_frame.pack(fill='x', padx=10, pady=5)
        self.label_language = customtkinter.CTkLabel(self.lang_frame, text=get_text('language'))
        self.label_language.pack(side='left', padx=5)
        lang_options = list(LANGUAGES.keys())
        self.combobox_language = customtkinter.CTkComboBox(self.lang_frame,
                                                          values=lang_options,
                                                          state="readonly",
                                                          width=120,
                                                          command=change_language)
        self.combobox_language.set(current_language)
        self.combobox_language.pack(side='left', padx=5)

        self.button_browsefile = customtkinter.CTkButton(self.left_frame,
                                                        text=get_text('browse_image'))
        self.button_browsefile.pack(fill='x', padx=20, pady=5)

        self.listbox_importedfile = tkinter.Listbox(self.left_frame, width=60,
                                                    selectmode=tkinter.MULTIPLE,
                                                    selectbackground="gray")
        self.listbox_importedfile.pack(fill='both', expand=True, padx=20, pady=5)

        remove_frame = customtkinter.CTkFrame(self.left_frame)
        remove_frame.pack(fill='x', padx=20, pady=5)
        self.button_removefile = customtkinter.CTkButton(remove_frame,
                                                        text=get_text('remove'))
        self.button_removefile.pack(side='left', padx=5, expand=True)
        self.button_removefileall = customtkinter.CTkButton(remove_frame,
                                                           text=get_text('remove_all'))
        self.button_removefileall.pack(side='left', padx=5, expand=True)

        self.right_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.right_frame.pack(fill='y', side='left')

        self.label_preview = customtkinter.CTkLabel(self.right_frame, text=get_text('preview'))
        self.label_preview.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="nesw")

        self.canvas_preview = tkinter.Canvas(self.right_frame, relief="solid")
        self.canvas_preview.configure(width=600, height=400, bg='#f0f0f0')
        self.canvas_preview.grid(row=1, columnspan=3, padx=40, pady=(10,20), sticky="nsew")

        self.label_logo = customtkinter.CTkLabel(self.right_frame, text=get_text('logo'))
        self.label_logo.grid(row=2, column=0, padx=20, pady=10, sticky="nsw")

        logo_option_list = load_combobox_options('./logo')
        default_var = customtkinter.StringVar()
        if logo_option_list:
            default_var.set(logo_option_list[0])
        else:
            default_var.set("")
        self.combobox_logo = customtkinter.CTkComboBox(self.right_frame,
                                                       values=logo_option_list,
                                                       state="readonly",
                                                       variable=default_var,
                                                       command=lambda choice: self.on_logo_changed())
        self.combobox_logo.grid(row=2, column=1, padx=20, pady=10, sticky="nesw")
        self.combobox_logo.bind("<<ComboboxSelected>>", lambda event: self.on_logo_changed())

        if logo_option_list:
            self.combobox_logo.set(logo_option_list[0])

        self.label_outputpath = customtkinter.CTkLabel(self.right_frame, text=get_text('output_path'))
        self.label_outputpath.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="nsw")

        self.button_browsepath = customtkinter.CTkButton(self.right_frame, text=get_text('browse'))
        self.button_browsepath.grid(row=4, column=2, padx=20, pady=10)

        self.text_outputpath = customtkinter.StringVar()
        self.text_outputpath.set(os.path.join(getcurrentdir(), "output"))
        self.entry_outputpath = customtkinter.CTkEntry(self.right_frame,
                                                       textvariable=self.text_outputpath,
                                                       state=tkinter.DISABLED)
        self.entry_outputpath.grid(row=5, column=0, columnspan=3, padx=20, pady=10, sticky="nesw")

        self.label_outputname = customtkinter.CTkLabel(self.right_frame, text=get_text('output_filename'))
        self.label_outputname.grid(row=6, column=0, padx=20, pady=10, sticky="nsw")

        self.label_outputstem = customtkinter.CTkLabel(self.right_frame, text=get_text('original_filename_plus'))
        self.label_outputstem.grid(row=6, column=1, padx=10, pady=10)

        text_suffix = customtkinter.StringVar()
        text_suffix.set("_with_frame")
        self.entry_outputsuffix = customtkinter.CTkEntry(self.right_frame, textvariable=text_suffix)
        self.entry_outputsuffix.grid(row=6, column=2, padx=10, pady=10)

        self.progressbar_run = customtkinter.CTkProgressBar(self.right_frame, width=100, mode="indeterminate")

        self.button_run = customtkinter.CTkButton(self.right_frame, text=get_text('run'))
        self.button_run.grid(row=8, column=2, padx=20, pady=10)

        self.button_browsefile.configure(command=self.browse_files)
        self.button_removefile.configure(command=self.removefromlistbox)
        self.button_removefileall.configure(command=self.removefromlistbox_all)
        self.button_browsepath.configure(command=self.browse_directory)
        self.button_run.configure(command=self.execute_generate)

        self.change_language = change_language
        self.update_all_texts = update_all_texts

    def getcurrentdir(self):
        return os.path.normpath(os.getcwd())

    def browse_files(self):
        files = filedialog.askopenfilenames(initialdir=self.getcurrentdir(),
                                            title="Select a File or Files",
                                            filetypes=(("JPG image", "*.jpg"),
                                                       ("PNG image", "*.png")))
        for f in files:
            self.addtolistbox(f)

    def browse_directory(self):
        global outputdir
        selecteddir = filedialog.askdirectory(initialdir=f"{self.getcurrentdir()}",
                                              title="Select a Folder")
        if selecteddir:
            self.text_outputpath.set(selecteddir)
            outputdir = selecteddir

    def get_preview_img(self):
        global first_file_path
        global tk_img
        global img_preview_id

        try:
            if first_file_path is None:
                return None

            logo = self.combobox_logo.get()
            if not logo:
                return None

            previewimg = EXIFframe.draw_watermark_frame(first_file_path, input_logo=logo)

            return previewimg
        except Exception:
            return None

    def on_logo_changed(self):
        global tk_img
        global img_preview_id
        global first_file_path

        if first_file_path is not None:
            if img_preview_id is not None:
                try:
                    previewimg = self.get_preview_img()
                    if previewimg is not None:
                        photo = ImageTk.PhotoImage(previewimg)
                        tk_img = photo
                        self.tk_img = photo
                        self.canvas_preview.itemconfig(img_preview_id, image=photo)
                except Exception:
                    pass
            else:
                self.show_preview()

    def addtolistbox(self, file_path):
        global tk_img
        global img_preview_id
        global bool_firstimport
        global first_file_path

        self.listbox_importedfile.insert("end", file_path)

        if bool_firstimport == True:
            first_file_path = file_path
            self.show_preview()

    def show_preview(self):
        global tk_img
        global img_preview_id
        global bool_firstimport
        global first_file_path

        try:
            previewimg = self.get_preview_img()
            if previewimg is not None:
                if img_preview_id is not None:
                    self.canvas_preview.delete(img_preview_id)

                photo = ImageTk.PhotoImage(image=previewimg)
                tk_img = photo
                self.tk_img = photo

                img_preview_id = self.canvas_preview.create_image(300, 200, anchor='center', image=tk_img)

                bool_firstimport = False
        except Exception:
            pass

    def removefromlistbox(self):
        global bool_firstimport
        global img_preview_id
        global tk_img
        global first_file_path

        if self.listbox_importedfile is None:
            return

        selected_index = self.listbox_importedfile.curselection()
        need_update_preview = False
        for i in reversed(selected_index):
            if (i == 0) and (self.listbox_importedfile.size() > 1):
                first_file_path = self.listbox_importedfile.get(1)
                need_update_preview = True
            self.listbox_importedfile.delete(i)

        if self.listbox_importedfile.size() == 0:
            bool_firstimport = True
            if img_preview_id is not None:
                self.canvas_preview.delete(img_preview_id)
                img_preview_id = None
            self.image_refs = []
        elif need_update_preview:
            if img_preview_id is not None:
                try:
                    previewimg = self.get_preview_img()
                    if previewimg is not None:
                        photo = ImageTk.PhotoImage(previewimg)
                        tk_img = photo
                        self.tk_img = photo
                        self.canvas_preview.itemconfig(img_preview_id, image=photo)
                except Exception:
                    pass

    def removefromlistbox_all(self):
        global bool_firstimport
        global img_preview_id
        global tk_img

        if self.listbox_importedfile is None:
            return

        self.listbox_importedfile.delete(0, tkinter.END)
        if self.listbox_importedfile.size() == 0:
            bool_firstimport = True
            if img_preview_id is not None:
                self.canvas_preview.delete(img_preview_id)
                img_preview_id = None
            self.image_refs = []

    def execute_generate(self):
        global bool_firstimport

        self.progressbar_run.grid(row=8, column=1, padx=20, pady=10)
        try:
            self.progressbar_run.start()
        except:
            pass

        self.button_run['state'] = tkinter.DISABLED
        paths = self.listbox_importedfile.get(0, tkinter.END)
        logo = self.combobox_logo.get()
        dir = self.text_outputpath.get()
        if dir == '':
            dir = "/output"
        dir = os.path.normpath(dir)
        text_entry = self.entry_outputsuffix.get()
        suffix = "_with_frame"
        if text_entry != '':
            suffix = text_entry

        i = EXIFframe.generate(paths, logo, dir, suffix)
        if i == 0:
            self.removefromlistbox_all()
            try:
                self.progressbar_run.stop()
            except:
                pass
            self.progressbar_run.grid_forget()
            self.button_run['state'] = tkinter.NORMAL


if __name__ == "__main__":
    app = App()
    app.mainloop()
