import base64
import cv2
import os
from datetime import datetime
import time


local_script = os.path.dirname(os.path.abspath(__file__)) # acha o caminho onde está o scrip para criar a pasta no mesmo lugar
pasta_imagem= os.path.join(local_script, "capturas") # junta o caminho da pasta com o nome
intervalo_captura = 1 # intervalo entre capturas

# cria a pasta, se não existir
os.makedirs(pasta_imagem, exist_ok=True)

# inicia a captura da webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Não foi possível acessar a webcam.")
    exit()

try:
    while True:
        ret, frame = cap.read() # tentativa de captura de frame
        if not ret:
            print("Erro ao capturar o frame.")
            continue

        # converte o frame em jpg em memoria
        sucesso, buffer = cv2.imencode(".jpg", frame)
        if not sucesso:
            print("Erro ao codificar o frame.")
            continue

        # codifica jpg em memoria para base
        imagem_base64 = base64.b64encode(buffer).decode("utf-8")
        print(f"Imagem convertida para base64 (tamanho: {len(imagem_base64)} caracteres)")

        # gera o nome do arquivo com data e hora
        data_atual = datetime.now()
        nome_arquivo = data_atual.strftime("frame_%Y-%m-%d_%H-%M-%S.jpg")
        caminho_completo = os.path.join(pasta_imagem, nome_arquivo)

        nome_arquivo64 = data_atual.strftime("frame_%Y-%m-%d_%H-%M-%S.txt")
        caminho_completo64 = os.path.join(pasta_imagem, nome_arquivo64)

        # salva o frame jpg
        cv2.imwrite(caminho_completo, frame)
        print(f"Frame salvo: {caminho_completo}")

        # salva o frame base64
        with open(caminho_completo64, "w") as f:
            f.write(imagem_base64)

        time.sleep(intervalo_captura)

except KeyboardInterrupt:
    print("\nCaptura interrompida pelo usuário.")

finally:
    cap.release()
    print("Webcam liberada.")