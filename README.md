# GreenGrid AI — Software Prototype

## What this version demonstrates
- Interactive solar generation, battery charge, household demand and grid availability inputs
- Automatic source selection: solar → battery → grid
- Solar-first, grid-first and manual demonstration modes
- Estimated hourly cost using clearly labelled illustrative assumptions
- Charts and downloadable simulation history

**Important:** This first version uses transparent decision rules. It is not yet a trained ML model and does not control physical hardware. Do not present simulated readings as live sensor data.

## Run on a laptop

1. Install Python 3.10 or newer.
2. Open this folder in VS Code.
3. Open the VS Code terminal.
4. Create a virtual environment (recommended):

   Windows:
   ```bash
   py -m venv .venv
   .venv\Scripts\activate
   ```

   macOS/Linux:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

5. Install packages:
   ```bash
   python -m pip install -r requirements.txt
   ```

6. Start the dashboard:
   ```bash
   streamlit run app.py
   ```

7. Streamlit will open the dashboard in your browser. If it does not, copy the local URL shown in the terminal (usually http://localhost:8501).

## Suggested demonstration
1. Keep Auto mode selected.
2. Set solar generation above demand: Solar should be selected.
3. Reduce solar generation below demand while battery is above 10%: Battery should be selected.
4. Set battery to 10% or below: Grid should be selected if available.
5. Turn grid availability off too: the dashboard should report that no source is available.
6. Try Manual mode and record a few simulations.

## Before presenting
- Change the illustrative tariff/cost assumptions to values your supervisor approves, or explain that they are placeholders.
- Say clearly that inputs are simulated in this software stage.
- Explain that ESP32 sensor integration and machine-learning forecasting are planned next stages.
