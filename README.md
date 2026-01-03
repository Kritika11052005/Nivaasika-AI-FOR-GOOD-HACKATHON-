# 🏠 Nivaasika - AI-Powered Property Inspection Platform

[![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40-red?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![Snowflake](https://img.shields.io/badge/Snowflake-Cloud-29B5E8?style=for-the-badge&logo=snowflake)](https://www.snowflake.com/)
[![Gemini](https://img.shields.io/badge/Gemini-AI-4285F4?style=for-the-badge&logo=google)](https://deepmind.google/technologies/gemini/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> Making Property Purchases Transparent & Safe - An intelligent property inspection platform leveraging AI-powered defect detection and risk assessment to empower homebuyers.
<img width="1919" height="919" alt="image" src="https://github.com/user-attachments/assets/00b44199-1666-4897-9ccf-88c8292b77a0" />


## 🌐 Live Demo

**🔗 [Nivaasika](https://nivaasika.streamlit.app/)**

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Getting Started](#-getting-started)
- [Project Structure](#-project-structure)
- [Environment Variables](#-environment-variables)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)
- [Team](#-team)

---

## 🎯 Overview

**Nivaasika** is an AI-powered property inspection platform built for the **AI for Good Hackathon 2025** (Problem Statement 4). The platform connects property sellers, professional inspectors, and buyers through transparent, AI-driven property assessments.

### What Makes Nivaasika Special?

- **🤖 AI-Powered Defect Detection**: Gemini Vision API analyzes property images to identify structural issues, water damage, electrical problems
- **📊 Intelligent Risk Assessment**: Automated risk scoring (Low/Medium/High) based on defect severity and type
- **💰 Accurate Cost Estimation**: Smart algorithms calculate renovation costs with min-max ranges
- **📸 Visual Property Gallery**: Sellers upload photos, buyers view complete visual documentation
- **🎯 Prioritized Recommendations**: AI-generated improvement suggestions ranked by priority
- **📝 Plain-Language Reports**: AI-generated inspection summaries in easy-to-understand language
- **🌓 Dark/Light Theme**: Modern UI with theme switching support

---

## ✨ Key Features

### 🏪 For Sellers

- **Easy Property Listing** - Simple form with property details, pricing, and specifications
- **Photo Gallery Upload** - Add up to 10 high-quality property images
- **Inspection Tracking** - Monitor property status and view assessment results
- **Property Dashboard** - Track all listed properties in one place

### 🔍 For Inspectors

- **Room-by-Room Analysis** - Systematic inspection workflow (Kitchen, Bedrooms, Bathrooms, etc.)
- **AI-Assisted Detection** - Gemini Vision API processes images in real-time
- **Multi-Image Upload** - Upload multiple photos per room
- **Instant Report Generation** - One-click submission with automated calculations
- **Rate Limiting Protection** - Smart API quota management (10 requests/minute)

### 🏠 For Buyers

- **Advanced Filtering** - Filter by risk level, price, location, property type
- **Comprehensive Reports** - 5-tab detailed view:
  - **Inspection Summary** - Risk metrics and AI-generated overview
  - **Defects Found** - Room-wise breakdown with severity ratings
  - **Improvements Needed** - Prioritized recommendations with cost estimates
  - **House Gallery** - View all property photos
  - **Property Info** - Complete specifications and seller details
- **Risk-Based Browsing** - Color-coded risk badges (Green/Yellow/Red)
- **Market Statistics** - View total inspected properties and trends

---

## 🛠 Tech Stack

### Frontend
- **Framework**: [Streamlit](https://streamlit.io/) 1.40
- **Language**: Python 3.12+
- **Styling**: Custom CSS with theme support
- **UI Components**: Streamlit native components

### Backend & Database
- **Database**: [Snowflake](https://www.snowflake.com/) Cloud Data Platform
- **Warehouse**: Compute_WH (X-Small)
- **Connection**: Snowflake Python Connector
- **Storage**: Snowflake Stages (Base64-encoded images)

### AI & Machine Learning
- **Vision AI**: [Google Gemini Vision API](https://deepmind.google/technologies/gemini/) (gemini-2.0-flash-exp)
- **Text AI**: Gemini Pro for summary generation
- **Image Processing**: PIL (Python Imaging Library)
- **Rate Limiting**: Custom rate limiter (10 requests/minute)

### Additional Libraries
- `snowflake-connector-python` - Database connectivity
- `google-generativeai` - Gemini API integration
- `python-dotenv` - Environment variable management
- `Pillow` - Image processing
- `pandas` - Data manipulation

---

## 🏗 Architecture

### Application Flow
```
User Authentication
         ↓
Role Selection (Seller/Inspector/Buyer)
         ↓
    Dashboard Interface
         ↓
┌────────────────┬────────────────┬───────────────┐
│     SELLER     │    INSPECTOR   │     BUYER     │
├────────────────┼────────────────┼───────────────┤
│ List Property  │ Select Property│ Browse Props  │
│ Upload Photos  │ Upload Images  │ Apply Filters │
│ Track Status   │ AI Analysis    │ View Reports  │
│                │ Generate Report│ View Gallery  │
└────────────────┴────────────────┴───────────────┘
         ↓
  Snowflake Database
         ↓
    Gemini AI Analysis
         ↓
  Real-time Updates
```

### Database Schema (7 Tables)

1. **PROPERTIES** - Main property data with risk metrics
2. **INSPECTION_IMAGES** - Image metadata
3. **INSPECTION_FINDINGS** - AI-detected and inspector-noted defects
4. **IMPROVEMENT_RULES** - Reference data for recommendations (13 rules)
5. **PROPERTY_IMPROVEMENTS** - Generated recommendations
6. **INSPECTION_SUMMARY** - AI-generated summaries
7. **PROPERTY_GALLERY** - Property photos from sellers

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- Snowflake account (trial credits available)
- Google Gemini API key
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/nivaasika.git
cd nivaasika
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create `.env` file:
```env
SNOWFLAKE_ACCOUNT=your_account_identifier
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_DATABASE=SAFEHOME_DB
SNOWFLAKE_SCHEMA=INSPECTOR_SCHEMA
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_ROLE=ACCOUNTADMIN
GEMINI_API_KEY=your_gemini_api_key
```

5. **Set up Snowflake database**

Run SQL scripts to create tables:
```sql
CREATE DATABASE SAFEHOME_DB;
CREATE SCHEMA INSPECTOR_SCHEMA;
-- Create all 7 tables (see Database Schema)
-- Insert 13 improvement rules
CREATE STAGE PROPERTY_IMAGES_STAGE;
```

6. **Run the application**
```bash
streamlit run app.py
```

7. **Open browser**
Navigate to [http://localhost:8501](http://localhost:8501)

---

## 📁 Project Structure
```
nivaasika/
├── .streamlit/
│   └── config.toml              # Streamlit theme configuration
│
├── pages/                       # Multi-page app
│   ├── __init__.py
│   ├── 1_Seller_Dashboard.py   # Seller interface
│   ├── 2_Inspector_Dashboard.py # Inspector interface
│   └── 3_Buyer_Dashboard.py    # Buyer interface
│
├── utils/                       # Utility modules
│   ├── __init__.py
│   ├── ai_analysis.py          # Gemini API integration
│   ├── cost_calculator.py      # Risk & cost calculations
│   ├── database.py             # Snowflake operations
│   ├── rate_limiter.py         # API rate limiting
│   └── theme.py                # Theme management
│
├── venv/                        # Virtual environment
├── .gitignore
├── app.py                       # Main application
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

---

## 🔐 Environment Variables

### Required Variables

| Variable | Description |
|----------|-------------|
| `SNOWFLAKE_ACCOUNT` | Account identifier |
| `SNOWFLAKE_USER` | Username |
| `SNOWFLAKE_PASSWORD` | Password |
| `SNOWFLAKE_DATABASE` | Database name |
| `SNOWFLAKE_SCHEMA` | Schema name |
| `SNOWFLAKE_WAREHOUSE` | Warehouse name |
| `SNOWFLAKE_ROLE` | User role | 
| `GEMINI_API_KEY` | Gemini API key | 

### Getting API Keys

- **Snowflake**: Sign up at [snowflake.com](https://signup.snowflake.com/) ($400 trial credits)
- **Gemini**: Get API key at [Google AI Studio](https://makersuite.google.com/app/apikey) (15 requests/min free)

---

## 📸 Screenshots

### Landing Page
<img width="1919" height="920" alt="image" src="https://github.com/user-attachments/assets/d1d9c3dd-174a-43d3-8629-2e81d75de62d" />
<img width="1919" height="918" alt="image" src="https://github.com/user-attachments/assets/95a73a56-395d-4e0c-94a2-4ef15eed691f" />
<img width="1919" height="923" alt="image" src="https://github.com/user-attachments/assets/4cf20012-82fe-4e76-b711-0daf39cedf4d" />




### Seller Dashboard
<img width="1919" height="922" alt="image" src="https://github.com/user-attachments/assets/f506227e-fce0-4449-9c96-c5b8ed7a33c5" />
<img width="1919" height="922" alt="image" src="https://github.com/user-attachments/assets/6ef5a2c7-95bb-41cf-8206-823e2dadc5ee" />
<img width="1919" height="924" alt="image" src="https://github.com/user-attachments/assets/ec5e3210-68ea-4a4c-8688-d78ce5595651" />
<img width="1919" height="924" alt="image" src="https://github.com/user-attachments/assets/bca9b250-9ed9-4ed3-b0a5-fe291da457e3" />
<img width="1919" height="920" alt="image" src="https://github.com/user-attachments/assets/cbd66d94-1c7f-47d9-9dcd-624e57ff2613" />






### Inspector Dashboard
<img width="1919" height="920" alt="image" src="https://github.com/user-attachments/assets/4e6795c1-d209-4a60-aaa3-8b708e3cd417" />
<img width="1919" height="925" alt="image" src="https://github.com/user-attachments/assets/27f2403b-4320-41bc-b656-bda43e8a667b" />
<img width="1919" height="925" alt="image" src="https://github.com/user-attachments/assets/24578253-47de-4ec8-8528-1ee423885ab1" />
<img width="1919" height="934" alt="image" src="https://github.com/user-attachments/assets/78fb8d0f-512d-4c7b-a360-064fc2beeac6" />
<img width="1919" height="922" alt="image" src="https://github.com/user-attachments/assets/70b2026b-88ee-43ff-ba1c-7ba43d923412" />





### Buyer Dashboard - Property Listing
<img width="1919" height="933" alt="image" src="https://github.com/user-attachments/assets/caf56632-04c8-4072-9e5b-9473368a3e88" />
<img width="1919" height="922" alt="image" src="https://github.com/user-attachments/assets/12278016-27f8-40ca-98d8-ec21dad14d2c" />



### Buyer Dashboard - Detailed Report
<img width="1919" height="921" alt="image" src="https://github.com/user-attachments/assets/acf016d0-4636-4565-b499-e2631585cdc1" />
<img width="1919" height="925" alt="image" src="https://github.com/user-attachments/assets/c64396ea-faec-4ac3-bd86-27072c5ea5d3" />
<img width="1919" height="919" alt="image" src="https://github.com/user-attachments/assets/63b4dd43-c2c1-4a1e-8685-fad10191df0f" />
<img width="1918" height="925" alt="image" src="https://github.com/user-attachments/assets/b528f508-17ca-428e-b7da-01615a706300" />





### House Gallery
<img width="1919" height="920" alt="image" src="https://github.com/user-attachments/assets/6c4e8066-0294-4af6-872c-47792b4fc121" />
<img width="1919" height="925" alt="image" src="https://github.com/user-attachments/assets/74cee7d7-3ba5-4f86-aad2-56881ea6d9ee" />
<img width="1919" height="924" alt="image" src="https://github.com/user-attachments/assets/70d16279-1c48-4bb4-adfa-93d54dbe117c" />
<img width="1919" height="921" alt="image" src="https://github.com/user-attachments/assets/625d24f4-9d2d-4049-a161-cd0cd64f8b9b" />






### Dark Mode
<img width="1919" height="915" alt="image" src="https://github.com/user-attachments/assets/0753b937-c80f-4207-9590-89d64c1ad8f7" />


---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Coding Standards
- Follow PEP 8 style guide
- Add docstrings to functions
- Include type hints
- Test thoroughly

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 👥 Team

<div align="center">

### Built for AI for Good Hackathon 2025

**Problem Statement 4: AI ASSISTED HOME AND BUILDING INSPECTION**

Made with ❤️ by Kritika Benjwal

</div>

---

## 🙏 Acknowledgments

- **Snowflake** for cloud data platform and trial credits
- **Google** for Gemini AI API
- **Streamlit** for the amazing Python framework
- **AI for Good Hackathon 2025** organizers

---

## 🔮 Future Enhancements

- [ ] PDF report generation with download
- [ ] Email notifications for inspection updates
- [ ] Mobile-responsive design
- [ ] Multi-language support (Hindi, English)
- [ ] Video property walkthroughs
- [ ] Blockchain for immutable inspection records
- [ ] Advanced analytics dashboard
- [ ] Inspector mobile app

---

<div align="center">

### Built with Streamlit & Snowflake 🚀

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Snowflake](https://img.shields.io/badge/Snowflake-29B5E8?style=for-the-badge&logo=snowflake&logoColor=white)
![Google](https://img.shields.io/badge/Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)

⭐ **Star this repo if you find it helpful!**

[📧 Contact](mailto:your.email@example.com) | [💼 GitHub](https://github.com/yourusername)

---

© 2025 Nivaasika. All rights reserved.

*Empowering homebuyers with AI-driven transparency.*

</div>
