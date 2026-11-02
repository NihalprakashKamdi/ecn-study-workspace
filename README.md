# CIRCUIT / OS — ECN Unit I Study App

A single-interface, Nothing-inspired white study workspace for MSBTE ECN 313332 Unit I. It includes lessons, an interactive phasor lab, an RLC calculator, AI-generated questions, and an in-app AI tutor.

## Security first

The API key shared in the chat must be considered exposed. Revoke it in the OpenAI API dashboard and create a **new** key. Do not paste a key into the HTML, JavaScript, screenshots, GitHub, or the chat. This app reads `OPENAI_API_KEY` from a private `.env` file on the server.

API usage is billed separately from a ChatGPT subscription. Check your API billing and project limits before using the tutor.

## Run on Windows

1. Install Python 3.10 or newer.
2. Extract this ZIP into a folder.
3. Open Command Prompt or PowerShell in that folder.
4. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .venv\Scripts\activate
   ```

5. Install packages:

   ```powershell
   pip install -r requirements.txt
   ```

6. Copy `.env.example` to `.env`. Open `.env` and replace `your_new_api_key_here` with your **new** key. Keep the quotes optional; do not add spaces around the `=` sign.
7. Start the app:

   ```powershell
   uvicorn main:app --host 127.0.0.1 --port 8000
   ```

8. Open `http://127.0.0.1:8000` in your browser.

## Run on Android with Termux

1. Install Python in Termux if it is not already available: `pkg install python`.
2. Extract this ZIP and `cd` into the extracted `ECN_Nothing_Study_App` folder.
3. Install dependencies: `pip install -r requirements.txt`.
4. Copy `.env.example` to `.env`, then edit `.env` and add your **new** API key.
5. Start the server: `uvicorn main:app --host 127.0.0.1 --port 8000`.
6. Open `http://127.0.0.1:8000` in the phone browser. Keep Termux running while using the app.

## Features

- Unit I lessons: AC generation and waveform, RMS/average values, phasor basics, R/L/C response, RL/RC/RLC, power and power factor, series resonance and Q-factor.
- Phasor lab with adjustable phase angle and leading/lagging interpretation.
- Series RLC calculator for reactance, impedance, current, voltage drops, phase, power factor and power.
- AI tutor using OpenAI's Responses API through the Python backend.
- On-demand AI question generation with topic, difficulty and question-type controls.
- API key stays on the server and is never sent to the browser.

## Notes and limitations

- This is an application you run locally, not a hosted service. The Python backend must remain running for AI features.
- The lesson/calculator/lab interface works locally; AI tutor and AI question generation require internet, a valid API key, an API project with billing/limits configured, and access to the configured model.
- The default model is set in `.env` as `gpt-5.5`. Change it to a model available to your API project if needed.
- This app does not connect to your ChatGPT consumer subscription or open the ChatGPT app. It uses separate API access.
- No API key is included in this ZIP.
