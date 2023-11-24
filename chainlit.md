# Chat GiPiTi! 🤖📚

Salutare! 👋 Chat GiPiTi este un chatbot care te ajută să aprofundezi textul unei cărți, într-un mod interactiv și distractiv. 🤓

## Cum functioneaza? 🤔

Chat GiPiTi are la bază un LLM, mai exact Llama2_7b 🦙, care împreună cu un RAG (Retrieval Augmented Generation) model, oferă răspunsuri bazate pe context. 🤖

1. Pentru a se realiza această procedură, primul pas este preprocesarea cărților. Ștergerea caracterelor invizibile/ whitespace inutile (care nu separă cuvinte), a numerotării paginilor și a segmentelor goale din carte.

2. Urmează traducerea din orice limbă ar fi cărțile, în engleză. Acest proces folosește Azure AI Translator, tehnologie aleasă după o analiză de piață (comparativ cu T5 Small, Libre, My Memory și DeepL Translator). Apoi, acestea sunt separate în șiruri mai scurte de caractere și serializate în vector embeddings, care urmează a fi stocate într-o bază de tip vector store (Chroma DB).
De asemenea, la acest pas se realizează analizarea conținutului. Sunt eliminate stop words și sunt extrase cuvinte comune, entitățile (caractere) și subiectele generale (topics).

3. Traducerea în engleză ne permite folosirea modelelor precum Llama 2 sau Mistral. Acestea sunt bine cunoscute și dispun de o vastă bază de cunoștiințe. Modelului ales îi este de asemenea pus la dispoziție contextul (datele din carte) pentru a interpreta conținutul și a putea susține conversații cu utilizatorul.

4. Interfața pentru utilizatori este generată folosind Chainlit, o bibliotecă specializată în crearea de interfețe web pentru LLM-urile dezvoltate în Python. Aceasta a fost personalizată pentru tematica proiectului nostru. La fel ca în analizarea cărților, mesajele generate de LLM-ul ales sunt traduse înapoi din engleză în limba selectată la rularea programului. Astfel, utilizatorul poate utiliza limba sa nativă pe întreg parcursul conversației.

Utilizatorul poate încărca o carte în format PDF, iar chatbot-ul va extrage textul și va crea un context pentru a putea răspunde la întrebări. 📚