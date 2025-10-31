<h1 align="center">🛡️ CYSEN: Cowrie Honeypot Attack Analysis & Geo Intelligence</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" />
  <img src="https://img.shields.io/badge/Framework-Cowrie%20Honeypot-orange?logo=hackaday" />
  <img src="https://img.shields.io/badge/Status-Active-success" />
</p>

---

## 🔍 Project Goal

**Cysen** is an intelligent security system built around the **Cowrie honeypot**.  
Its purpose is to:
- Capture attacker logs and trap malicious users.  
- Automatically analyze and classify attacks using ML.  
- Enrich logs with **GeoIP** details like country and city.  
- Prepare for integration with a future **dashboard interface**.

---

## ⚙️ Features

✅ Real-time log extraction from Cowrie  
✅ Automated attack classification (ML model)  
✅ Geo enrichment via IPInfo API  
✅ Modular structure for easy extension  
✅ Ready for integration with visualization dashboards  

---

## 🧩 Project Structure

Cysen/
├── LICENSE.rst
├── README.md
├── demo/
│   └── sample_X_test.csv
├── pyproject.toml
├── requirements.txt
├── run_demo.sh
├── setup.py
├── src/
│   ├── build_features_from_real.py
│   ├── clean_and_balance.py
│   ├── extract_data_real.py
│   ├── generate_attack_logs.py
│   ├── test_geo.py
│   └── train_model_1.py
├── attack_classifier_model.pkl
├── X_test.csv
└── predictions_with_geo.csv


---

## 🚀 Setup & Run

### 1️⃣ Clone and enter project
```
git clone https://github.com/ThilakRajkumar/Cysen.git
cd Cysen
```
2️⃣ Create virtual environment
```
python3 -m venv cowrie-env
source cowrie-env/bin/activate
```
3️⃣ Install dependencies
```
pip install --upgrade pip
pip install -r requirements.txt
```
4️⃣ Add your IPInfo token

Create .env file:
```
IPINFO_TOKEN=your_api_token_here
```
5️⃣ Run demo 
```
chmod +x run_demo.sh
./run_demo.sh
```


🧠 Future Enhancements

🔹 Build interactive dashboard for live attack visualization

🔹 Real-time notifications on attack events

🔹 Dockerized deployment

🔹 Integration with external threat intelligence feeds



💡 Author

Thilak Rajkumar

Cybersecurity Enthusiast

📫 Connect: https://github.com/ThilakRajkumar
