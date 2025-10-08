# Messaging App - Docker Containerization

## Overview
This project containerizes the **Building Robust APIs** Django messaging app using **Docker**.  
It ensures that the application runs consistently across different environments by packaging dependencies and code together.

---

## Data Requirements:
The app handles user data such as:
- **email**
- **firstName**
- **lastName**
- **profilePic**

---

## Steps to Run the App

### 1️⃣ Create a Requirements File
Freeze all dependencies:
```bash
pip freeze > requirements.txt
