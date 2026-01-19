# 🐒 Lemur Network: Social Network Analysis & Survival Prediction

**A double project portfolio exploring the intersection of Social Network Analysis (Graph Theory) and Conservation Biology. This repository contains two distinct applications built on the Duke Lemur Center dataset.**

---

## 📌 Project 1: The "Jungle Book" Graph Theory App
**A Streamlit application that visualizes the hidden social structures of lemur communities.**

### **Business Context: Why Graph Theory?**
Understanding "Who knows Whom" is the foundation of modern tech giants. The concepts used here to map lemur interactions are the exact same algorithms used by:
* **Facebook/LinkedIn:** To suggest "People You May Know" (Link Prediction).
* **Google:** To rank web pages via PageRank (Centrality).
* **Pinterest:** To recommend content based on user-item graphs.

In this project, we apply these **Social Network Analysis (SNA)** techniques to biology to identify "Key Influencers" within lemur troops—animals whose removal would collapse the social structure.

### **Technical Implementation**
* **NetworkX:** Used to build the graph where Nodes = Lemurs and Edges = Social Interactions (Grooming/Playing).
* **Centrality Algorithms:**
    * **Degree Centrality:** Who is the most popular?
    * **Betweenness Centrality:** Who is the "Bridge" connecting different cliques?
* **Streamlit:** Deployed as an interactive web app allowing users to filter by Species and Interaction Type.

<img width="3018" height="1426" alt="image" src="https://github.com/user-attachments/assets/f731cdf5-896e-4dbe-8200-20f1e1201e43" />


---

## 📌 Project 2: Infant Survival Prediction (ML)
**A Machine Learning pipeline to predict infant lemur mortality, enabling targeted veterinary intervention.**

### **Business Impact**
Endangered species conservation is a resource-limited field. Zoos and sanctuaries cannot monitor every animal 24/7.
* **The Problem:** Infant mortality rates in captivity can be high due to unobserved rejection by mothers or environmental factors.
* **The Solution:** A predictive model that flags "High Risk" infants *before* tragedy strikes, allowing staff to intervene with supplemental feeding or incubators.

### **Technical Implementation**
* **Data Engineering:** Processed 30+ years of Duke Lemur Center records, handling complex "Left Censored" data (animals still alive).
* **Feature Engineering:** Created domain-specific features like `Dam_Age_at_Conception` (Mother's Age) and `Litter_Size`.
* **Modeling:**
    * **Decision Trees:** For interpretability (explaining *why* an infant is at risk).
    * **XGBoost:** For maximum predictive accuracy.
* **Handling Imbalance:** Used **SMOTE (Synthetic Minority Over-sampling Technique)** to address the class imbalance (since most infants survive).

---

## 🚀 Key Insights

### **1. The "Grandmother Hypothesis" in Graph Theory**
Our network analysis revealed that **older females** often hold the highest **Betweenness Centrality**. They act as social bridges, keeping the troop cohesive. This parallels human social networks where matriarchs are central to family stability.

### **2. The "Goldilocks Zone" for Survival**
The Decision Tree discovered a non-linear relationship with **Mother's Age**:
* **Too Young (<3 years):** High risk of infant mortality (inexperience).
* **Too Old (>15 years):** High risk (biological decline).
* **Middle Age:** The "Safe Zone" for reproduction.

---

## 💻 How to Run

### **Prerequisites**
```bash
pip install pandas networkx streamlit matplotlib scikit-learn xgboost

```

### **Running the Graph App**

```bash
streamlit run lemur_graph_app.py

```

### **Running the Survival Model**

Open `Lemur_Survival_Prediction.ipynb` in Jupyter Notebook or Google Colab.

---
**Data Source:** Duke Lemur Center (DLC)

**Tech Stack:** Python, Streamlit, NetworkX, XGBoost

## 👤 Author

* **Shagun Sharma** - *Machine Learning Engineer*

**Graduate Student, Duke University - Fuqua School of Business**

  * [GitHub Profile](https://github.com/Shaguns26)
