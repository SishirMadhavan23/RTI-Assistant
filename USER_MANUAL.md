# RTI Assistant AI - User Manual

## Introduction

RTI Assistant AI is an AI-powered CivicTech application designed to help citizens understand and use the Right to Information (RTI) Act more easily.

The application provides:

* RTI-related question answering
* AI-powered RTI draft generation
* Source document access
* Suggested RTI questions
* Interactive and user-friendly interface

---

## System Requirements

To run RTI Assistant AI locally, ensure the following are installed:

* Python 3.10 or above
* Git
* Internet connection
* Modern web browser

---

## Installation Guide

### Clone Repository

```bash id="2urjlwm"
git clone <repository-url>
cd rti-assistant
```

### Create Virtual Environment

```bash id="w8yn3z"
python -m venv venv
```

### Activate Environment

Windows Git Bash:

```bash id="xbg3u5"
source venv/Scripts/activate
```

### Install Dependencies

```bash id="jx4n7m"
pip install -r requirements.txt
```

---

## Security Checklist

The project includes security validation recommendations for production readiness:

* Secret Scanning (Gitleaks / TruffleHog)
* Dependency Audit (uv audit / pip-audit / npm audit)
* Static Analysis (Bandit)

---

## Running the Application

Start the Streamlit server:

```bash id="iv9v6f"
streamlit run app.py
```

Open browser:

```text id="m1g95l"
http://localhost:8501
```

---

## Application Features

### 1. RTI Question Answering

Users can type RTI-related questions and receive AI-generated answers based on RTI documents.

Example questions:

* How to file RTI?
* What is RTI fee?
* Appeal process?
* RTI response time?

---

### 2. Suggested Questions

The application provides pre-built suggested questions to help users quickly explore RTI information.

Clicking a question automatically fills or triggers the query.

---

### 3. RTI Draft Generator

Users can describe their issue and generate a draft RTI application.

Example:

Issue:

Road repair delay in my area.

The AI generates:

* Subject
* RTI request body
* Formal application structure

---

### 4. Source PDF Access

The application allows users to open or download RTI reference documents used by the AI.

Available documents may include:

* RTI Act
* RTI Rules
* RTI FAQ documents

---

## User Workflow

Step 1:

Launch application.

Step 2:

Choose either:

* Ask RTI Question
* Generate RTI Draft

Step 3:

Review AI-generated response.

Step 4:

Open source PDFs if verification is needed.

---

## Troubleshooting

### Application not opening

Check:

```bash id="r0ym1q"
streamlit run app.py
```

Ensure virtual environment is active.

---

### Missing package error

Install dependencies again:

```bash id="u88w2w"
pip install -r requirements.txt
```

---

### Deployment issues

Ensure:

* requirements.txt exists
* GitHub repository is updated
* Streamlit Cloud is redeployed

---

## Safety and Usage Note

RTI Assistant AI is an informational support tool.

Users should verify generated drafts and legal information before official submission.

---

## Support

For project issues or improvements, refer to:

* README.md
* CONTRIBUTING.md

Thank you for using RTI Assistant AI.
