# FDI System (Backend + Telegram Bot)

Minimal scaffold to start with FastAPI (backend) and aiogram (Telegram bot).

## Requisiti
- Python 3.10+
- Token Bot Telegram

## Setup ambiente virtuale (venv)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Configurazione
- Copia `bot/.env.example` in `bot/.env` e imposta:
```
TELEGRAM_BOT_TOKEN=xxxxx
API_BASE_URL=http://127.0.0.1:8000
```

## Avvio backend (FastAPI)
```bash
source .venv/bin/activate
chmod +x scripts/run_api.sh
./scripts/run_api.sh
```
Apri http://127.0.0.1:8000/api/health per verificare.

## Avvio bot (aiogram)
```bash
source .venv/bin/activate
chmod +x scripts/run_bot.sh
./scripts/run_bot.sh
```
Nel bot usa `/start` e `/health` per testare la connessione al backend.

## Struttura
```
backend/
  app/
    main.py
bot/
  main.py
scripts/
  run_api.sh
  run_bot.sh
requirements.txt
README.md
```

## Come usare il bot Telegram per registrazione utenti e accesso ai canali

### Registrazione dall'utente
1. L'utente trova il bot su Telegram (cerca il username associato al token).
2. Inizia una conversazione con `/start` per accogliere il bot.
3. Per registrarsi, usa il comando `/register` (livello 1 di default) o `/register <livello>` dove livello è 1-4.
   - Livello 1: Automaticamente attivo, riceve messaggio di aggiunta al canale Livello 1.
   - Livelli 2-4: Stato iniziale "pending", richiede approvazione amministrativa.

### Approvazione amministrativa
L'amministratore accede al pannello admin su http://127.0.0.1:8000/static/admin.html per:
- Esaminare utenti pendenti.
- Approvare utenti: Clicca "Approva" per cambiare stato a "active".
- Dopo l'approvazione, l'utente può essere aggiunto manualmente ai canali Telegram corrispondenti al livello.
  - Canali da aggiungere: Liv1 (-1003004275721), Liv2 (-1003104779162), Liv3 (-1003171947222), Liv4 (-1002914092542).
- Gli amministratori del canale devono generare link di invito e condividerli con gli utenti attivi tramite chat privata o altri mezzi.

### Informazioni aggiuntive
- Usa `/health` per verificare lo stato del backend.
- Usa `/channels` per vedere gli ID dei canali configurati.
- Gli utenti attivi dovrebbero ricevere accessi ai canali di livello appropriato tramite inviti amministrativi.

## Prossimi passi
- Aggiungere modelli, router (`users`, `contents`) e DB (SQLAlchemy + Alembic).
- Implementare webhook bot (opzionale) e flussi di registrazione.
- Automatizzare invio link inviti canali tramite bot (richiede bot amministratore nei canali).
