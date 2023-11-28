from tkinter import Tk, Canvas, Button, filedialog
from PIL import Image, ImageTk

class SobreposicaoImagensApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sobreposição de Imagens")

        # Variáveis para armazenar as imagens
        self.imagem_a = None
        self.imagem_b = None

        # Variáveis para armazenar as posições x e y
        self.posicao_x = 0
        self.posicao_y = 0

        # Variável para armazenar a referência PhotoImage da imagem resultante
        self.imagem_resultante_tk = None

        # Canvas para exibir as imagens
        self.canvas = Canvas(root)
        self.canvas.pack()

        # Botões para carregar imagens e realizar a sobreposição
        self.botao_imagem_a = Button(root, text="Carregar Imagem A", command=self.carregar_imagem_a)
        self.botao_imagem_a.pack()

        self.botao_imagem_b = Button(root, text="Carregar Imagem B", command=self.carregar_imagem_b)
        self.botao_imagem_b.pack()

        self.botao_sobrepor = Button(root, text="Sobrepor Imagens", command=self.sobrepor_imagens)
        self.botao_sobrepor.pack()

    def carregar_imagem_a(self):
        # Abrir o diálogo de seleção de arquivo para imagem A
        caminho_imagem_a = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])

        # Carregar a imagem A e exibi-la no canvas
        self.imagem_a = Image.open(caminho_imagem_a)
        self.imagem_a = self.imagem_a.convert("RGBA")
        imagem_a_tk = ImageTk.PhotoImage(self.imagem_a)
        self.canvas.create_image(0, 0, anchor="nw", image=imagem_a_tk)
        self.canvas.imagem_a_tk = imagem_a_tk  # Salvar uma referência para evitar que o garbage collector remova a imagem

    def carregar_imagem_b(self):
        # Abrir o diálogo de seleção de arquivo para imagem B
        caminho_imagem_b = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])

        # Carregar a imagem B e exibi-la no canvas
        self.imagem_b = Image.open(caminho_imagem_b)
        self.imagem_b = self.imagem_b.convert("RGBA")
        imagem_b_tk = ImageTk.PhotoImage(self.imagem_b)
        self.canvas.create_image(0, 0, anchor="nw", image=imagem_b_tk)
        self.canvas.imagem_b_tk = imagem_b_tk  # Salvar uma referência para evitar que o garbage collector remova a imagem

    def sobrepor_imagens(self):
        if self.imagem_a is not None and self.imagem_b is not None:
            # Calcular as coordenadas para centralizar a imagem A na imagem B
            largura_b, altura_b = self.imagem_b.size
            largura_a, altura_a = self.imagem_a.size

            x = (largura_b - largura_a) // 2
            y = (altura_b - altura_a) // 2

            # Sobrepor a imagem A na posição calculada na imagem B
            imagem_a_copiada = self.imagem_a.copy()
            self.imagem_b.paste(imagem_a_copiada, (x, y), imagem_a_copiada)

            # Exibir a imagem resultante no canvas
            if self.imagem_resultante_tk:
                self.canvas.delete(self.imagem_resultante_tk)

            imagem_resultante_tk = ImageTk.PhotoImage(self.imagem_b)
            self.canvas.create_image(0, 0, anchor="nw", image=imagem_resultante_tk)
            self.imagem_resultante_tk = imagem_resultante_tk  # Salvar uma referência para evitar que o garbage collector remova a imagem

            # Salvar a imagem resultante (opcional)
            self.imagem_b.save("./imagens/Resultados/sobreposicao.png")

if __name__ == "__main__":
    root = Tk()
    app = SobreposicaoImagensApp(root)
    root.mainloop()