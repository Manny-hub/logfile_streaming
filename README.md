
---

# **Apache Log Streaming ETL Pipeline (Python)**

This project implements a simple **Extract–Transform–Load (ETL)** pipeline for ingesting and processing **streaming Apache logs** from a remote API endpoint.

The system continuously fetches log data, normalizes it, parses each log entry using regular expressions, and prints out the structured results.

---

## 🚀 **Features**

* **Continuous streaming** log extraction from a remote API
* Supports **list-based** and **dict-based** API data formats
* Log parsing using a strict **Apache access log regex**
* Separates parsed logs from non-matching entries
* Prints structured logs using `pprint`
* Lightweight and dependency-free (uses only Python standard libraries + `requests`)

---

## 📂 **Project Structure**

```
project/
│
├── etl.py        # Main ETL script
├── README.md     # Project documentation
└── requirements.txt
```

---

## 📦 **Requirements**

Install dependencies using:

```bash
pip install -r requirements.txt
```

Your `requirements.txt` should include:

```
requests
pandas
```

(Although `pandas` is imported, the ETL does not rely heavily on it yet.)

---

## 🏗️ **How the ETL Works**

The ETL pipeline consists of three main components:

### 1️⃣ **Extract**

The `extract()` function is a generator that continuously retrieves logs from the server:

* Calls `GET https://apache-api.onrender.com/logs`
* Extracts JSON data + timestamp
* Yields a dictionary once every 0.5 seconds
* Never stops unless interrupted (Ctrl+C)

Example yield:

```python
{
    "response": [...], 
    "timestamp": "14:35:22"
}
```

---

### 2️⃣ **Transform**

The `processor()` function:

* Accepts raw log text (`str`)
* Splits into lines
* Uses a regular expression to extract fields:

  * IP address
  * Timestamp
  * HTTP method
  * Path
  * Protocol
  * Status code
  * Bytes sent
  * Referrer
  * User agent
* Returns two lists:

  * `log_entries`: valid parsed logs
  * `error_entries`: lines that didn’t match

---

### 3️⃣ **Load / Output**

The `etl()` function orchestrates the process:

* Calls `extract()` to stream logs
* Converts each API response into clean log lines
* Calls `processor()` on each batch
* Prints:

  * Count of parsed logs
  * Count of non-matching lines
  * Samples of parsed entries

Example output:

```
12:04:55 — parsed 5 entries, 1 errors
[{'ipaddress': '192.168.0.1', 'timestamp': '12/Jan...', ...}, ...]
Sample non-matching lines:
['INVALID LOG FORMAT LINE']
```

---

## ▶️ **Running the ETL**

Run the ETL by executing:

```bash
python etl.py
```

You should immediately see:

```
Starting ETL process...
14:02:10 — parsed X entries, Y errors
...
```

To stop the stream, press:

```
CTRL + C
```

---

## 🧪 **Testing with a Local File (optional)**

Inside the `extract()` function, there is support for reading from a static JSON file:

```python
# file_path = "/path/to/logs.json"
# with open(file_path, "r") as f:
#     data = json.load(f)
```

Uncomment these lines and comment out the API request if testing offline.

---

## 🔍 **Troubleshooting**

### **1. ETL prints nothing**

Likely causes:

* `etl()` was not called
* Infinite extractor loop never reaches processing
* API returned unexpected format

### **2. Regex doesn’t match any logs**

Your logs may differ from standard Apache format.
Paste a sample log into the regex tester to adjust the pattern.

### **3. API unreachable**

Try opening the URL manually in a browser:

```
https://apache-api.onrender.com/logs
```

If unreachable, test with a local JSON file.

---

## 🛠️ **Next Steps (Planned Enhancements)**

* Add **command-line arguments (argparse)**
* Save parsed logs to a file or database
* Integrate Spark or Kafka for real-time processing
* Create a Superset dashboard for visualization

---

## 👤 **Author**

Built as part of a Data Engineering learning project.

---
