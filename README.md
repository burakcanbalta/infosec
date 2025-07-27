# 📘 DBMS Fingerprint Tool - README

## 🔍 What is this Tool?

`info.py` is a professional-grade database fingerprinting tool developed in Python. It is designed to identify the backend Database Management System (DBMS) used by a target web application via automated error-based injection techniques.

By sending carefully crafted payloads to injectable parameters in the URL and analyzing the returned error messages, this tool determines whether the backend DBMS is MySQL, PostgreSQL, MSSQL, Oracle, or SQLite.

---

## 🚀 Key Features

- 🔎 Supports MySQL, PostgreSQL, MSSQL, Oracle, and SQLite
- ⚡ Multi-threaded scanning for high performance
- 🧱 WAF bypass support using encoded payloads
- 🎯 Proxy support (compatible with Burp Suite and others)
- ⏱️ Adjustable delay between requests
- 🔇 Silent mode for clean scripting output
- 📄 Outputs results in JSON format for later analysis

---

## 🛠 Installation & Requirements

### ✅ Requirements

- Python 3.7 or later
- Packages: `requests`, `colorama`, `urllib3`

Install dependencies:

```bash
pip install requests colorama urllib3
```

### 🧪 Convert to EXE (Optional)

To convert the tool into a standalone `.exe` file:

```bash
pip install pyinstaller
pyinstaller --onefile --name=dbms-fingerprint info.py
```

After compilation, the executable will be in the `dist/` directory.

---

## ⚙️ Usage Instructions

### ✅ Basic Usage

```bash
python info.py "http://example.com/page.php?id=1"
```

### 📌 Required Argument

- `url`: Target URL with an injectable parameter (e.g., `?id=1`)

### 🔧 Optional Arguments

| Option         | Description                                                         |
| -------------- | ------------------------------------------------------------------- |
| `--proxy`      | Set proxy (e.g., `http://127.0.0.1:8080`) for tools like Burp Suite |
| `--waf-bypass` | Use encoded payloads to help bypass basic WAFs                      |
| `--delay`      | Delay in seconds between requests (e.g., `--delay 1.5`)             |
| `--silent`     | Silent mode, disables verbose testing messages                      |

### 📂 Output File

If a DBMS is detected, results will be saved to:

```
dbms_fingerprint_result.json
```

---

## 🧪 Example Commands

### 🔎 Simple Scan

```bash
python info.py "http://vulnerable.site/item.php?id=2"
```

### 🌐 With Proxy and WAF Bypass

```bash
python info.py "http://test.site/page.php?id=5" --proxy http://127.0.0.1:8080 --waf-bypass
```

### 🤫 Silent, Delayed Mode

```bash
python info.py "http://target.com/view.php?item=3" --silent --delay 2
```

---

## 📤 Sample Output (Terminal)

```
[+] PostgreSQL signature matched: PostgreSQL.*ERROR
[!] Likely DBMS detected: PostgreSQL
```

## 📝 Sample Output (JSON)

```json
{
  "url_tested": "http://target.com/page.php?id=1",
  "dbms_detected": ["MySQL"],
  "details": {
    "MySQL": {
      "payload": "'",
      "signature": "You have an error in your SQL syntax",
      "url": "http://target.com/page.php?id=1%27"
    }
  }
}
```

---

## ⚠️ Legal Disclaimer

This tool is for **educational and authorized testing purposes only**. Do not use it on websites or systems you do not own or have permission to test. Misuse may be illegal. The author is not responsible for any misuse or damage caused.

---

## 👨‍💻 Author & Contributions

Developed by a cybersecurity enthusiast passionate about web exploitation and automation.

Suggestions and contributions are welcome. Future versions may include:

- GUI interface
- SQLMap integration
- Active fingerprinting support
- CVE-based detection modules

Hack responsibly. 🛡️

