import whisper
import sounddevice as sd
import numpy as np
import wave
import requests
import json
import paho.mqtt.client as mqtt
import subprocess
import soundfile as sf
import time
import os


# ============================
# CONFIGURAÇÕES
# ============================

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "aura-lite"

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "casa/sala"

PIPER_PATH = r"C:\piper\piper.exe"
PIPER_MODEL = r"C:\piper\voices\pt_BR-faber-medium.onnx"


ARQUIVO_VOZ = "voz.wav"

ARQUIVO_AUDIO = "voz.wav"
MIC_INDEX = 0   # ajuste conforme seu microfone


# caminho do ffmpeg
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"

# ============================
# MQTT
# ============================

mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

print("📡 MQTT conectado")

# ============================
# CARREGAR WHISPER
# ============================

print("🧠 Carregando Whisper...")
model = whisper.load_model("medium")
print("✅ Whisper carregado")

# ============================
# GRAVAR AUDIO
# ============================


def gravar_audio():

    print("🎤 Fale agora...")

    samplerate = 16000
    duration = 5

    audio = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype='float32',
        device=MIC_INDEX
    )

    sd.wait()

    # remover silêncio inicial e final
    audio = audio.flatten()

    # normalizar volume
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val

    # converter
    audio_int16 = np.int16(audio * 32767)

    # salvar wav
    with wave.open(ARQUIVO_AUDIO, "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(samplerate)
        f.writeframes(audio_int16.tobytes())

    print("✅ Áudio salvo")

# ============================
# TRANSCRIÇÃO
# ============================

def transcrever()   :

    result = model.transcribe(
   "voz.wav",
    language="pt",
    fp16=False,
    temperature=0,
    best_of=5
)

    texto = result["text"].strip()

    print("Você disse:", texto)

    return texto

# ============================
# OLLAMA
# ============================

def perguntar_llm(texto):

    prompt = f"""
Você é AURA, um assistente de automação residencial.

REGRAS OBRIGATÓRIAS:

- Responda SOMENTE em português do Brasil.
- Você controla dispositivos de uma casa.
- Seja direto, claro e amigável.
- Nunca responda em inglês.
- Nunca invente comandos.

COMANDOS DISPONÍVEIS:

Luz da sala:
COMANDO: LIGAR_SALA
COMANDO: DESLIGAR_SALA

COMPORTAMENTO:

Se o usuário disser algo como:

"ligue a luz"
"acenda a sala"
"quero luz"

Responda EXATAMENTE:

COMANDO: LIGAR_SALA
Luz da sala ligada.

Se disser:

"desligue a luz"
"apague a sala"

Responda:

COMANDO: DESLIGAR_SALA
Luz da sala desligada.

SE NÃO ENTENDER:

Responda:

Não entendi o comando. Você quer ligar ou desligar a luz da sala?

NUNCA invente comandos inexistentes.

Usuário disse:
"{texto}"

Resposta:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "top_p": 0.9,
                "num_predict": 100
            }
        }
    )

    data = response.json()

    resposta = data["response"]

    print("🤖 Resposta:", resposta)

    return resposta

# ============================
# MQTT
# ============================

def executar_comando(resposta):

    if "COMANDO: LIGAR_SALA" in resposta:

        mqtt_client.publish(MQTT_TOPIC, "ligar")
        print("💡 LED SALA LIGADO")

    elif "COMANDO: DESLIGAR_SALA" in resposta:

        mqtt_client.publish(MQTT_TOPIC, "desligar")
        print("💡 LED SALA DESLIGADO")

# ============================
# PIPER TTS OFFLINE
# ============================

def falar(texto):

    texto_limpo = texto.replace("COMANDO: LIGAR_SALA", "")
    texto_limpo = texto_limpo.replace("COMANDO: DESLIGAR_SALA", "")

    comando = f'echo {texto_limpo} | "{PIPER_PATH}" -m "{PIPER_MODEL}" -f "{ARQUIVO_VOZ}"'

    subprocess.run(comando, shell=True)

    data, fs = sf.read(ARQUIVO_VOZ)

    sd.play(data, fs)

    sd.wait()

# ============================
# LOOP PRINCIPAL
# ============================

print("\n🚀 Assistente Aura iniciado!\n")

falar("Aura iniciada e pronta.")

while True:

    gravar_audio()

    texto = transcrever()

    if texto == "":
        continue

    resposta = perguntar_llm(texto)

    executar_comando(resposta)

    falar(resposta)

    time.sleep(1)