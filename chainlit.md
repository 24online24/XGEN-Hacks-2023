# Chat GiPiTi! 🤖📚

Salutare! 👋 Chat GiPiTi este un chatbot care te ajută să aprofundezi textul unei cărți, într-un mod interactiv și distractiv. 🤓

## Cum functioneaza? 🤔

Chat GiPiTi are la bază un LLM, mai exact Llama2_7b 🦙, care împreună cu un RAG (Retrieve and Generate) model, oferă răspunsuri bazate pe context. 🤖

Utilizatorul poate încărca o carte în format PDF, iar chatbot-ul va extrage textul și va crea un context pentru a putea răspunde la întrebări. 📚

## Cum se folosește Chat GipiTi? 🤓

### Dedependențe

Avem nevoie de următoarele dependențe pentru a rula aplicația:

- Ollama Desktop 🦙 -> aplicatie de gestionare și gazduire a modelelor LLM (găzduită în mod local local)
- Python 3.10 🐍 -> împreună cu packetele pip specificate în fisierul requirements.txt
- cheie pentru translator 🔑 -> obținută de la serviciul de traducere al [Microsoft Azure](https://portal.azure.com/#create/Microsoft.CognitiveServicesTextTranslation)

### Instalare

Recomandam folosirea unui virtual environment pentru a instala dependențele. Pentru a crea un virtual environment, rulați următoarele comenzi:

```bash
python3 -m venv venv
source venv/bin/activate # Linux
venv\Scripts\activate # Windows
```

Pentru a instala dependențele, rulați următoarea comandă:

```bash
pip3 install -r requirements.txt
```

### Configurare

Pentru a configura chatbot-ul, trebuie să creați un fișier `.env` în directorul rădăcină al proiectului. Acesta trebuie să conțină următoarele variabile de mediu:

```bash
MSKEY=[Keys and Endpoint > Key 1 / Key 2 (una dintre ele)]
ENDPOINT=[Keys and Endpoint > Text Translation]
REGION=[Keys and Endpoint > Location/Region]
```

### Utilizare

Pentru a încărca datele în Ollama Desktop, rulați următoarea comandă:

```bash
python3 load_data_vdb.py
```

Pentru a rula chatbot-ul, rulați următoarea comandă:

```bash
python3 RAG.py
```

Chatbot-ul va rula pe portul 8000.
