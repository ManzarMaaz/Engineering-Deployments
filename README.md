<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=28&pause=1000&color=2E86C1&center=true&vCenter=true&width=900&lines=Systems+Engineering+%26+Applied+AI+Portfolio;Distributed+Systems+%7C+Cloud+Architecture+%7C+Data+Engineering;Mohammed+Manzar+Maaz" />
</p>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&height=100&color=0E2A47&section=header" />
</p>

# 🏛️ **Systems Engineering & Research Portfolio**

**Author:** Mohammed Manzar Maaz  
**Focus:** Distributed Systems, Cloud Architecture, and Data Engineering  
**Contact:** [Email](mohammadmanzarmaaz@gmail.com) | [LinkedIn Profile](https://www.linkedin.com/in/mohammed-manzar-maaz)

---

## 🔬 **Research & Engineering Focus**
This repository documents the source code and architectural design of my independent engineering projects. Unlike standard academic coursework, these systems were built to solve specific engineering challenges regarding **latency**, **concurrency**, and **data persistence** in distributed environments.

* **Distributed Systems:** Optimizing backend performance and handling high-concurrency API connections.
* **Data Engineering:** Architecting automated ETL pipelines for unstructured web data.
* **Applied AI:** Deploying Research-grade models (Faster R-CNN, RL) into usable web applications.

---

## 🛠️ **Featured Engineering Systems**

### 1. [Async Distributed Fare Engine](./01-Async-Distributed-Fare-Engine)
> *Target Domain: Distributed Systems / Network Optimization*

A high-concurrency notification engine designed to monitor volatile data streams in real-time.
* **Architecture:** Python `asyncio` + `aiohttp` (Non-blocking I/O).
* **Key Challenge:** "Head-of-Line" blocking when querying multiple external APIs sequentially.
* **Engineering Solution:** Implemented an asynchronous event loop to manage **50+ concurrent connections**, utilizing persistent connection pooling.
* **Outcome:** Reduced data refresh intervals from **60s to <5s**.

### 2. [High-Volume ETL Pipeline](./02-High-Volume-ETL-Pipeline)
> *Target Domain: Data Engineering / Infoclouds*

A robust automated pipeline for harvesting unstructured real estate data from dynamic web sources.
* **Architecture:** Selenium WebDriver & BeautifulSoup4.
* **Key Challenge:** Bypassing anti-scraping heuristics and parsing inconsistent DOM structures.
* **Engineering Solution:** Developed "Human-Mimicry" algorithms (randomized headers/intervals) and a custom DOM parser to sanitize raw HTML.
* **Outcome:** Successfully harvested and cleaned **1,000+ data points**, transforming unstructured web data into SQL-compatible formats.

### 3. [Secure RBAC Content System](./03-Secure-RBAC-CMS)
> *Target Domain: Systems Security / Database Design*

A full-stack Content Management System focusing on data integrity and access control.
* **Architecture:** Flask (Python) + PostgreSQL + SQLAlchemy.
* **Key Challenge:** Preventing Privilege Escalation and IDOR vulnerabilities.
* **Engineering Solution:** Implemented **Role-Based Access Control (RBAC)** decorators and secure password hashing/salting protocols (Werkzeug).
* **Outcome:** Achieved strict privilege separation between Admin and User roles with persistent storage.

### 4. [Faster R-CNN Calorie Vision](./04-Faster-RCNN-Calorie-Vision)
> *Target Domain: Computer Vision / System Integration*

End-to-end deployment of a deep learning model for dietary analysis.
* **Architecture:** Django Backend + Faster R-CNN (PyTorch).
* **Engineering Solution:** Led the system integration to deploy a heavy research model as a responsive web application, managing the inference pipeline between the frontend image upload and the backend model.

### 5. [RL Smart Irrigation System](./05-RL-Smart-Irrigation-System)
> *Target Domain: IoT / Reinforcement Learning*

An autonomous water management system driven by algorithmic logic.
* **Architecture:** IoT Sensors + Python RL Agent.
* **Engineering Solution:** Coded the logic flow allowing a Reinforcement Learning agent to interpret soil moisture sensor data and make autonomous irrigation decisions.

---

## ⚙️ **Technical Arsenal**

| Domain | Technologies & Tools |
| :--- | :--- |
| **Languages** | Python (Advanced), SQL, JavaScript, HTML/CSS |
| **Backend & Systems** | Flask, Django, Asyncio, RESTful API Design |
| **Data & ML** | Pandas, NumPy, Scikit-Learn, Selenium, SQLAlchemy |
| **Infrastructure** | Git, PostgreSQL, SQLite, Render (Cloud Deployment) |
| **Security** | OAuth 2.0, RBAC, Hashing/Salting |

---


## 📊 **Engineering Activity**

<p align="center">
  <a href="https://github.com/anuraghazra/github-readme-stats">
    <img src="https://github-readme-stats.vercel.app/api?username=ManzarMaaz&show_icons=true&theme=radical" alt="GitHub Stats" />
  </a>
  <a href="https://github.com/anuraghazra/github-readme-stats">
    <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=ManzarMaaz&layout=compact&theme=radical&hide=html,css" alt="Top Languages" />
  </a>
</p>

---

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&height=80&color=0E2A47&section=footer" />
</p>
