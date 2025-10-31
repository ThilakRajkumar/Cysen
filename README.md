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
```
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
```

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

<br>
<br>

<h3 align="center">🌍 (Optional) Real-World Usage</h3>

This project can be deployed in real-world cybersecurity environments to analyze attacker behavior and monitor honeypot data automatically.
Follow these steps to use Cysen in a real-world setup 👇

<h3>🧩 Step 1️⃣ — Setup the Honeypot</h3>
<ul>
<li>Install and configure Cowrie Honeypot on your desktop or cloud instance.</li>


<li>Cowrie will simulate a fake SSH/Telnet server to attract and log attacker activities.</li>


<li>Once started, it automatically records attacker IPs, login attempts, and command executions.</li>
</ul>

<h3>⚙️ Step 2️⃣ — Create Virtual Environment</h3>

```
python3 -m venv cowrie-env
source cowrie-env/bin/activate
pip install -r requirements.txt
```

This ensures all dependencies are installed in an isolated environment.

<h3>🧠 Step 3️⃣ — Run the Data Processing Pipeline</h3>

Use the provided scripts to extract logs, clean data, and train or test the model:
```
python3 src/extract_data_real.py
python3 src/clean_and_balance.py
python3 src/train_model_1.py
```

This will:
<ul>
<li>Parse real attack data from Cowrie logs</li>
  
<li>Perform feature engineering and data balancing</li>

<li>Train an ML model to classify attacker behavior</li>
</ul>
<h3>🌐 Step 4️⃣ — Geo-Location & Attack Enrichment</h3>

To analyze attackers’ origin and ISP:
```
python3 src/test_geo.py
```

This will:
<ul>
<li>Fetch the attacker’s location (country, city, ISP) using their IP</li>
<li>Save the enriched results in predictions_with_geo.csv</li>
</ul>

<h3>📊 Step 5️⃣ — Analyze the Results</h3>

Open the output CSV to explore the following:
<ul>
<li>Attacker IPs</li>

<li>Predicted Attack Category</li>

<li>Attack Confidence Score</li>

<li>Geographical Location (Country, City)</li>

</ul>
<br>

<section>
  <h3>📊 Example Results</h3>
  <p>Sample output saved in <code>predictions_with_geo.csv</code>:</p>
  <div style="overflow-x:auto;">
    <table style="border-collapse:collapse; width:100%; max-width:900px;">
      <thead>
        <tr style="background:#0b6fa4; color:#fff; text-align:left;">
          <th style="padding:10px 12px;">🧾 src_ip</th>
          <th style="padding:10px 12px;">🧠 pred_label</th>
          <th style="padding:10px 12px;">🎯 pred_proba_max</th>
          <th style="padding:10px 12px;">🌍 geo_country</th>
          <th style="padding:10px 12px;">🏙️ geo_city</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-top:1px solid #e6e6e6;">
          <td style="padding:10px 12px;">8.8.8.8</td>
          <td style="padding:10px 12px;">BruteForce</td>
          <td style="padding:10px 12px;">0.97</td>
          <td style="padding:10px 12px;">US</td>
          <td style="padding:10px 12px;">Mountain View</td>
        </tr>
        <tr style="border-top:1px solid #e6e6e6; background:#fafafa;">
          <td style="padding:10px 12px;">8.8.4.4</td>
          <td style="padding:10px 12px;">Malware</td>
          <td style="padding:10px 12px;">0.95</td>
          <td style="padding:10px 12px;">US</td>
          <td style="padding:10px 12px;">Mountain View</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>

<br>
<h3>🖥️ Step 6️⃣ — (Upcoming) Dashboard Integration</h3>

In future releases, you can:
<ul>
<li>Install this honeypot and run it directly from a desktop dashboard</li>

<li>View live attack statistics, geo maps, and ML-based threat predictions</li>

<li>Automatically upload reports to your central monitoring server</li>
</ul>
<br>
<section>
  <h3>🚀 Real-World Applications</h3>
  <div style="overflow-x:auto;">
    <table style="border-collapse:collapse; width:100%; max-width:1000px;">
      <thead>
        <tr style="background:#1f8f4f; color:#fff; text-align:left;">
          <th style="padding:10px 12px; min-width:220px;">🏷️ Use Case</th>
          <th style="padding:10px 12px;">🧩 Description</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-top:1px solid #e6e6e6;">
          <td style="padding:10px 12px; vertical-align:top;">🧑‍💻 Cybersecurity Research</td>
          <td style="padding:10px 12px;">Analyze real attacker behaviors, commands, and IP-based targeting patterns to improve defensive models and publish findings.</td>
        </tr>
        <tr style="border-top:1px solid #e6e6e6; background:#fafafa;">
          <td style="padding:10px 12px; vertical-align:top;">🏢 Enterprise Network Defense</td>
          <td style="padding:10px 12px;">Deploy on corporate servers to detect and study intrusion attempts and train internal detection systems.</td>
        </tr>
        <tr style="border-top:1px solid #e6e6e6;">
          <td style="padding:10px 12px; vertical-align:top;">🧪 Threat Intelligence</td>
          <td style="padding:10px 12px;">Build IP-based threat databases, correlate attack types, and share actionable intel with SOC teams.</td>
        </tr>
        <tr style="border-top:1px solid #e6e6e6; background:#fafafa;">
          <td style="padding:10px 12px; vertical-align:top;">🎓 Academic Projects</td>
          <td style="padding:10px 12px;">Ideal for learning honeypot deployment, data engineering, and ML for cybersecurity courses and research projects.</td>
        </tr>
        <tr style="border-top:1px solid #e6e6e6;">
          <td style="padding:10px 12px; vertical-align:top;">🔍 Incident Response</td>
          <td style="padding:10px 12px;">Quickly trace attacker origins and attack vectors using enriched logs to support faster response and containment.</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>
