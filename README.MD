# Image Processor

Este é um aplicativo simples de processamento de imagens que utiliza a biblioteca Tkinter para a interface gráfica, OpenCV para operações de processamento de imagem e a biblioteca Rembg para remover o fundo de uma imagem.

## Requisitos

- Python 3.7 ou superior e inferior a 3.12

## Instalação

1. Clone o repositório para o seu ambiente local:

```bash
git clone https://github.com/g1ovannab/PAI-trab-image.git
cd image-processor
```

1. Crie e ative um ambiente virtual (opcional, mas recomendado):
   
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
   ```

2. Instale as dependências:
   
   ```bash
   pip install -r requirements.txt
   ```

Execução
--------

Execute o script `main.py` para iniciar o aplicativo:

```bash
python main.py
```

Utilização
----------

* Clique no botão "Select Image" para selecionar uma imagem.
* Para remover o fundo da imagem, clique em "Remove Background".
* Utilize o botão "Apply GrabCut" para aplicar a técnica GrabCut à imagem.
* Siga as instruções na interface para interagir com a aplicação.

Notas
-----

* Este aplicativo foi desenvolvido e testado em Python 3.7 até 3.12. Certifique-se de ter uma versão do Python dentro deste intervalo.
* Recomenda-se o uso de um ambiente virtual para isolar as dependências do projeto.

Problemas conhecidos
--------------------

* Se encontrar problemas durante a execução, certifique-se de ter as dependências instaladas corretamente e que seu ambiente Python está configurado corretamente.


