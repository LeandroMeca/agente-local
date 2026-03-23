# 🧠 Aura - Assistente de Automação Residencial com Voz

Aura é um assistente de automação residencial desenvolvido em **Python e ESP32**, capaz de ouvir comandos de voz, interpretar utilizando um **modelo de linguagem local com Ollama** e controlar dispositivos físicos através do protocolo **MQTT**.

O sistema utiliza **Whisper para reconhecimento de voz**, **Piper para síntese de voz**, e um **ESP32 conectado ao MQTT** para controlar dispositivos como luzes.

---

# 🚀 Funcionalidades

- 🎤 Reconhecimento de voz offline com Whisper
- 🤖 Processamento de linguagem natural com Ollama
- 🗣️ Síntese de voz offline com Piper
- 📡 Comunicação com dispositivos via MQTT
- 💡 Controle de dispositivos físicos utilizando ESP32
- 🏠 Base para projetos de automação residencial com IA

---

# 🏗 Arquitetura do Sistema

Fluxo de funcionamento do sistema:

```
Usuário (voz)
      │
      ▼
Whisper (Speech-to-Text)
      │
      ▼
Ollama (LLM)
      │
      ▼
Python envia comando MQTT
      │
      ▼
ESP32 recebe mensagem
      │
      ▼
Dispositivo é acionado (LED / Luz)
```

---

# 📂 Estrutura do Projeto

```
aura-assistente
│
├── aura.py
├── voz.wav
│
├── esp32
│   └── esp32_led.ino
│
└── README.md
```

---

# 🧰 Tecnologias Utilizadas

- Python
- Whisper
- Ollama
- Piper TTS
- MQTT
- ESP32
- Wokwi
- SoundDevice
- NumPy

---

# 📦 Instalação das Dependências

Instale as bibliotecas Python necessárias:

```bash
pip install openai-whisper
pip install sounddevice
pip install numpy
pip install requests
pip install paho-mqtt
pip install soundfile
```

---

# ⚙️ Requisitos

Também é necessário instalar:

- FFmpeg
- Ollama
- Piper TTS

---

# 🤖 Instalação do Ollama

Instale o Ollama:

https://ollama.ai

Depois execute o modelo utilizado no projeto:

```bash
ollama run aura-lite
```

---

# 🔊 Instalação do Piper TTS

Baixe o Piper no repositório oficial:

https://github.com/rhasspy/piper

Configure os caminhos no código Python:

```python
PIPER_PATH = "C:\\piper\\piper.exe"
PIPER_MODEL = "C:\\piper\\voices\\pt_BR-faber-medium.onnx"
```

---

# 🔌 Configuração MQTT

Broker MQTT utilizado:

```
broker.hivemq.com
```

Tópico utilizado:

```
joao123/esp32/led
```

Comandos enviados:

```
ligar
desligar
```

---

# 📟 ESP32

O ESP32 conecta ao broker MQTT e aguarda comandos para controlar o LED.

Componentes utilizados:

- ESP32
- LED
- Resistor 220Ω

Pino utilizado:

```
GPIO 2
```

---

# 🧪 Testando o Projeto

Execute o script Python:

```bash
python aura.py
```

Depois fale um comando como:

```
"Ligue a luz da sala"
```

O sistema irá:

1. Capturar o áudio
2. Converter o áudio para texto com Whisper
3. Interpretar o comando com Ollama
4. Enviar comando MQTT
5. ESP32 ligar ou desligar o LED

---

# 💡 Exemplos de Comandos

```
ligue a luz
acenda a sala
desligue a luz
apague a sala
```

---

# 🧪 Simulação no Wokwi

O ESP32 pode ser simulado online utilizando a plataforma:

https://wokwi.com/

Monte o circuito:

```
ESP32 → Resistor → LED → GND
```

---

# 📈 Melhorias Futuras

- Ativação por palavra-chave ("Aura")
- Escuta contínua
- Controle de múltiplos dispositivos
- Integração com sensores
- Dashboard web
- Integração com Home Assistant

---

# 👨‍💻 Autor

Leandro Cruz

Estudante de Engenharia de Software com interesse em:

- Inteligência Artificial
- Sistemas embarcados
- Automação residencial
- Desenvolvimento Backend

---

# 📜 Licença

Projeto open-source para fins educacionais.
