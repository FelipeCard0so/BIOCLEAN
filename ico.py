# gerar_ico.py  — rode uma vez na raiz do projeto
from PIL import Image

img = Image.open("assets/vsr.png").convert("RGBA")
img = img.resize((256, 256))
img.save("assets/icone.ico", format="ICO", sizes=[(256,256),(128,128),(64,64),(32,32),(16,16)])
print("icone.ico gerado!")