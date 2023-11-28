import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import cv2 #Biblioteca de visão computacional 
import numpy as np
from rembg import remove ## biblioteca aom IA

class ImageProcessor:
    def __init__(self, root, canvas, output_label):
        self.root = root
        self.canvas = canvas
        self.output_label = output_label
        self.original_img = None
        self.processed_img = None
        self.background_img = None
        self.rect_start_x = None
        self.rect_start_y = None
        self.rect_end_x = None
        self.rect_end_y = None
        self.create_widgets()

    def create_widgets(self):
        self.canvas.grid(row=0, column=0, padx=20, pady=20)
        self.output_label.grid(row=0, column=1, padx=20, pady=20)

        button_browse_image = ttk.Button(self.root, text="Select Image", command=self.select_image)
        button_browse_image.grid(row=1, column=0, pady=(10, 10))

        button_remove_bg = ttk.Button(self.root, text="Remover com IA", command=self.remove_background)
        button_remove_bg.grid(row=1, column=2, pady=(10, 10))

        button_apply_grabcut = ttk.Button(self.root, text="Segmentação", command=self.apply_grabcut)
        button_apply_grabcut.grid(row=1, column=3, pady=(10, 10))

        button_save_removed_bg = ttk.Button(self.root, text="Salvar IA", command=self.save_removed_background)
        button_save_removed_bg.grid(row=2, column=0, pady=(10, 10))

        button_save_grabcut = ttk.Button(self.root, text="Salvar Segmentação", command=self.save_grabcut_result)
        button_save_grabcut.grid(row=2, column=3, pady=(10, 10))

        # Adiciona eventos de mouse para a seleção do retângulo
        self.canvas.bind("<ButtonPress-1>", self.on_rect_start)
        self.canvas.bind("<B1-Motion>", self.on_rect_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_rect_end)

    def select_image(self):
        # Limpa os dados existentes ao selecionar uma nova imagem
        self.reset()

        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            image = Image.open(file_path)
            self.original_img = image
            self.display_image(image, self.canvas)

    def reset(self): ## ao carregar imagem resetar todos os valores
        # Limpa os dados existentes
        self.original_img = None
        self.processed_img = None
        self.background_img = None
        self.rect_start_x = None
        self.rect_start_y = None
        self.rect_end_x = None
        self.rect_end_y = None
        self.canvas.delete("rect")  # Limpa o retângulo no canvas

    def remove_background(self): ## remove o fundo da imagem usando rembg
        if self.original_img:
            processed_img = remove(self.original_img)
            self.processed_img = processed_img
            self.display_output_image(processed_img)

    def apply_grabcut(self):
        if self.original_img:
            print("Applying GrabCut")
            img_cv2 = np.array(self.original_img)
            img_cv2 = cv2.cvtColor(np.array(self.original_img), cv2.COLOR_RGBA2BGR)  

            mask = np.zeros(img_cv2.shape[:2], np.uint8)
            rect = (
                int(self.rect_start_x),
                int(self.rect_start_y),
                int(self.rect_end_x - self.rect_start_x),
                int(self.rect_end_y - self.rect_start_y),
            )

            modeloFundo = np.zeros((1, 65), np.float64)
            modeloObjeto = np.zeros((1, 65), np.float64)
            
            # Invoca o GrabCut
            #o 5 é o numero de iterações quanto maior as iterações mais chances tem de melhorar
            #o GC_INIT_WITH_RECT é o modo de inicialização do grabcut, nesse caso é com um retangulo
            cv2.grabCut(img_cv2, mask, rect, modeloFundo, modeloObjeto, 5, cv2.GC_INIT_WITH_RECT)
            
            #valor 0 -> posição é fundo
            #valor 1 -> pregião faz parte do objeto final
            #valor 2 -> região é provavelmente fundo
            #valor 3 -> região é provavelmente objeto
            
            # cria uma mascara para a imagem
            # np.where -> troca os valores -> se a posição da máscara for 2 ou 0, então o valor é 0, se não é 1 
            # converte pra inteiro de 8 bits
            mask_final = np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")
            img_final = img_cv2 * mask_final[:, :, np.newaxis]

            # Aplica a máscara à imagem original
            for x in range(0, img_cv2.shape[0]):
                for y in range(0, img_cv2.shape[1]):
                    if mask_final[x, y] == 0:
                        img_final[x][y][0] = img_final[x][y][1] = img_final[x][y][2] = 255

            img_final = cv2.cvtColor(img_final, cv2.COLOR_BGR2RGB)
            self.img_final_pil = Image.fromarray(img_final)
            
            #remove o fundo da imagem preenchido por pixels brancos
            self.img_final_pil = remove(self.img_final_pil)
            
            #converte a imagem pill para png e salva
            self.img_final_pil.save('grabcut.png')

            self.display_output_image(self.img_final_pil)

    def save_removed_background(self): # salva a imagem sem fundo pela IA
        if self.processed_img:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                self.processed_img.save(file_path)

    def save_grabcut_result(self): # salva a imagem sem fundo pela segmentação
        if self.original_img:
            #converte a imagem pill para png e salva
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                self.img_final_pil.save(file_path)

    def display_image(self, img, target): # exibe a imagem no canvas
        img.thumbnail((300, 300))
        img_tk = ImageTk.PhotoImage(img)
        target.configure(width=300, height=300)
        target.create_image(0, 0, anchor="nw", image=img_tk)
        target.image = img_tk

    def display_output_image(self, img): # exibe a imagem no label
        img.thumbnail((300, 300))
        img_tk = ImageTk.PhotoImage(img)
        self.output_label.configure(image=img_tk)
        self.output_label.image = img_tk

    def on_rect_start(self, event): # evento de click do mouse
        self.rect_start_x = event.x
        self.rect_start_y = event.y

    def on_rect_drag(self, event): # evento de arrastar o mouse
        self.rect_end_x = event.x
        self.rect_end_y = event.y
        self.canvas.delete("rect")
        self.canvas.create_rectangle(
            self.rect_start_x, self.rect_start_y, self.rect_end_x, self.rect_end_y, outline="blue", tags="rect"
        )

    def on_rect_end(self, event): # evento de soltar o mouse
        pass

def main():
    window = tk.Tk() # cria a janela
    window.title("Image Processor") # titulo da janela

    style = ttk.Style()
    style.configure("TButton", padding=(10, 5), font=("Helvetica", 12), background="#4CAF50", foreground="black") #estilo do botão
    style.configure("TLabel", font=("Helvetica", 12), background="#f0f0f0", padding=(10, 5), anchor="w") #estilo do label
    style.configure("TEntry", font=("Helvetica", 12), padding=(10, 5)) #estilo da entrada de texto
    style.configure("TFrame", background="#f0f0f0") #estilo do frame
    style.configure("TCheckbutton", background="#f0f0f0") #estilo do checkbutton

    frame = ttk.Frame(window) #cria o frame
    frame.grid(row=0, column=0, padx=20, pady=20) #posiciona o frame

    canvas = tk.Canvas(frame, relief="solid", borderwidth=1, width=400, height=300) #cria o canvas
    output_label = ttk.Label(frame, style="TLabel", relief="solid", borderwidth=1) #cria o label

    image_processor = ImageProcessor(window, canvas, output_label) #cria o objeto da classe ImageProcessor

    window.mainloop() #loop da janela

if __name__ == "__main__":
    main()
