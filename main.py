#!/usr/bin/env python3

import cv2
import tkinter as tk
import numpy as np
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
from PIL import Image, ImageTk
from lsb import LSB
from Leastsb import LeastSB
from aes import AESCipher


class Activity:
    # root window object
    master = tk.Tk()
    master.geometry('700x900')

    IMG_HEIGHT = None
    IMG_WEIGHT = None
    IMG_MODE = None

    # images defintion
    image = None
    secret_image = None
    cover_image = None
    stego_image = None
    imgPanel = None
    imgPanel2 = None

    # input variable initialization
    keyInput = None
    ivInput = None
    messageInput = None
    path = "./dst.png"

    def __init__(self):
        self.master.title('AES- Image Steganography')
        # use blank image when program started
        self.image = np.zeros(shape=[100, 100, 3], dtype=np.uint8)
        self.updateImage()

        self.image_enc = np.zeros(shape=[100, 100, 3], dtype=np.uint8)
        self.updateEnc(1)

        # configure cover and secret button
        cvi = tk.Label(self.master, text="select cover image")
        cvi.config(font=('courier', 10))
        cvi.pack()
        openBtn = tk.Button(self.master, text='Cover Image',
                            command=self.openImage,  padx=10)
        openBtn.config(font=('courier', 10))
        openBtn.pack()

        cvi1 = tk.Label(self.master, text="select secret image")
        cvi1.config(font=('courier', 10))
        cvi1.pack()
        secretBtn = tk.Button(self.master, text='Secret Image',
                              command=self.secretImage,  padx=10)
        secretBtn.config(font=('courier', 10))
        secretBtn.pack()

        '''
        Button section
        '''
        btnFrame = tk.Frame(self.master)
        btnFrame.pack()
        # defining the encoding button
        encodeBtn = tk.Button(btnFrame, text='Encode', command=self.encode)
        encodeBtn.config(font=('courier', 10))
        encodeBtn.pack(side=tk.LEFT)
        # defining the decode button
        decodeBtn = tk.Button(btnFrame, text='Decode', command=self.decode)
        decodeBtn.config(font=('courier', 10))
        decodeBtn.pack(side=tk.LEFT)
        # defining the save button
        savebtnFrame = tk.Frame(self.master)
        savebtnFrame.pack()

        # configure save button
        saveBtn = tk.Button(savebtnFrame, text='Save Image',
                            command=self.saveImage)
        saveBtn.config(font=('courier', 10))
        saveBtn.pack()

        # configure input box for key and initialization vector
        tk.Label(self.master, text='Key', padx=14).pack()
        self.keyInput = tk.Entry(self.master)
        self.keyInput.pack()
        tk.Label(self.master, text='Intialization Vector', padx=14).pack()
        self.ivInput = tk.Entry(self.master)
        self.ivInput.pack()

        # configure input box for secret message
        # tk.Label(self.master, text='Secret Message').pack()
        # self.messageInput = tk.Text(self.master, height=10, width=60)
        # self.messageInput.pack()

    # updateImage read image from cv2 object and preview on image window
    def updateImage(self):
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)

        if self.imgPanel == None:
            self.imgPanel = tk.Label(image=image)
            self.imgPanel.image = image
            self.imgPanel.pack(side="top", padx=10, pady=10)
        else:
            self.imgPanel.configure(image=image)
            self.imgPanel.image = image

    # cipher class call
    def cipher(self):
        key = self.keyInput.get()
        iv = self.ivInput.get()
        # key length must 16 character
        if len(key) != 16 or len(iv) != 16:
            messagebox.showwarning(
                "Warning", "Key and Iv must be 16 character each")
            return

        return AESCipher(self.keyInput.get(), self.ivInput.get())

    # encode encode image using AESCipher and embed cipher text to image
    def encode(self):
        cipher = self.cipher()
        if cipher == None:
            return
        img_size, img_mode, encrypted_img, encrypted_bytes = cipher.encrypt_image(
            self.secret_image)

        self.IMG_WEIGHT = img_size[0]
        self.IMG_HEIGHT = img_size[1]
        self.IMG_MODE = img_mode

        self.image_enc = encrypted_img
        self.updateEnc(id=2)

        obj = LeastSB(self.image)
        print("printing image")
        print(self.cover_image)
        cover_image = obj.encode_image(self.cover_image, self.secret_image)
        # self.image = encrypted_img

        # obj.embed(str(encrypted_bytes, 'latin1'))
        # self.image = cover_image
        # self.updateImage()
        # messagebox.showinfo("Info", "Encoded")
        messagebox.showinfo("Success", "Encoding completed successfully")

    def encodex(self):
        message = self.messageInput.get("1.0", 'end-1c')
        # message length will forced to be multiple of 16 by adding extra white space
        # at the end
        if len(message) % 16 != 0:
            message += (" " * (16-len(message) % 16))

        cipher = self.cipher()
        if cipher == None:
            return
        cipherText = cipher.encrypt(message)

        obj = LSB(self.image)
        obj.embed(cipherText)
        self.messageInput.delete(1.0, tk.END)
        self.image = obj.image

        # preview image after cipher text is embedded
        self.updateImage()
        messagebox.showinfo("Info", "Encoded")

    # decode extract cipher image from image and try decode it using provided secret key
    def decode(self):
        cipher = self.cipher()
        if cipher == None:
            return

        obj = LeastSB(self.image)
        print("stego image path ")
        print(self.stego_image)
        secret_image = obj.decode_image(self.stego_image)
        # imgx = cipher.decrypt_image(
        #     cipherText, self.IMG_MODE, self.IMG_WEIGHT, self.IMG_HEIGHT)

        # display the imag
        # self.image = imgx
        # self.updateImage()

        # # Save the decoded image as a new file
        secret_image.save('decoded_image.png')
        messagebox.showinfo("Success", "Decoding completed successfully")

    # extract secret byte from image and try decode it using provided secret key
    def decodex(self):
        cipher = self.cipher()
        if cipher == None:
            return

        obj = LSB(self.image)

        cipherText = obj.extract()
        msg = cipher(cipherText)

        # show decoded secret message to message input box
        self.messageInput.delete(1.0, tk.END)
        self.messageInput.insert(tk.INSERT, msg)

    # openImage ask user to select image
    def openImage(self):
        path = askopenfilename()
        if not isinstance(path, str):
            return

        self.cover_image = path
        print("image pathed")
        print(path)
        self.stego_image = path
        self.image = cv2.imread(path)
        messagebox.showinfo("Success", "Cover Image Selected")
        self.updateImage()

    # openImage ask user to select image

    def updateEnc(self, id):
        img = Image.open("./encrypted.png")

        if id == 1:
            image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)
        else:
            img = img.resize((100, 100))
            image = ImageTk.PhotoImage(img)

        if not img and not self.image_enc:
            print("image not found")
        # image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # print(img)
        # image = cv2.imread(img)
        # image = Image.fromarray(image)

        if self.imgPanel2 == None:
            self.imgPanel2 = tk.Label(image=image)
            self.imgPanel2.image = image
            self.imgPanel2.pack(side="top", padx=10, pady=10)
        else:
            self.imgPanel2.configure(image=image)
            self.imgPanel2.image = image

    def secretImage(self):
        path = askopenfilename()
        if not isinstance(path, str):
            return

        # self.secret_image = cv2.imread(path)
        self.secret_image = path
        print(path)
        messagebox.showinfo("Success", "Secret Image Selected")

    # openImage ask user to select image
    def openImage(self):
        path = askopenfilename()
        if not isinstance(path, str):
            return

        self.image = cv2.imread(path)
        self.cover_image = path
        self.stego_image = path
        messagebox.showinfo("Success", "Image Selected")
        self.updateImage()

    # saveImage save image on png format

    def saveImage(self):
        path = asksaveasfilename(title="Select file", filetypes=[
                                 ("png files", "*.png")])
        if path == '':
            return

        if ".png" not in path:
            path = path + ".png"

        obj = LSB(self.image)
        obj.save(path)

        messagebox.showinfo("Info", "Saved")

    def startLoop(self):
        self.master.mainloop()


if __name__ == "__main__":
    app = Activity()
    app.startLoop()
