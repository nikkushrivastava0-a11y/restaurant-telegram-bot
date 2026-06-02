# 🤖 AI-Powered Restaurant Order Management Bot

A fully functional Telegram bot that handles restaurant orders using **natural language processing** — powered by Google Gemini (LLM), n8n automation workflows, and Google Sheets as a live database.

> Built by [Nitanshu Shrivastava](https://github.com/nikkushrivastava0-a11y) — CSE-AI Student @ GL Bajaj Institute of Technology & Management

---


## 🚀 Demo

> 📹 *Watch the bot take a real order in real time — customer messages in plain language, bot confirms and logs it instantly.*

▶️ **[Click Here to Watch the Full Live Demo Video on YouTube](https://youtu.be/-9gJui16PdA?si=n-u2CLOzgz8CINUD)**

---

## ✨ Features

- 🗣️ **Natural Language Ordering** — Customer types order in plain language, Gemini understands and extracts items
- ✅ **Order Confirmation Flow** — Bot confirms order details before finalizing
- 📊 **Live Google Sheets Logging** — Every order auto-logged with timestamp, items, and status
- ⚡ **Fully Automated Pipeline** — Zero manual intervention from order received to data saved
- 🔄 **Webhook-based Architecture** — Real-time message handling via n8n webhooks

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Messaging Platform | Telegram Bot API |
| Automation Engine | n8n (self-hosted workflows) |
| AI / LLM Backend | Google Gemini API |
| Database | Google Sheets API |
| Version Control | Git & GitHub |

---

## 🏗️ Architecture

```
Customer Message (Telegram)
        ↓
  n8n Webhook Trigger
        ↓
  Google Gemini API
  (understands order)
        ↓
  Order Confirmation
  (sent back to user)
        ↓
  Google Sheets
  (order logged live)
```

---

## ⚙️ How It Works

1. Customer sends a message to the Telegram bot (e.g. *"I want 2 burgers and a coke"*)
2. n8n webhook receives the message and triggers the workflow
3. Google Gemini processes the message and extracts structured order data
4. Bot replies with an order confirmation for the customer to approve
5. Confirmed order gets logged into Google Sheets with timestamp and details

---

## 📦 Setup & Installation

### Prerequisites
- n8n account (cloud or self-hosted)
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- Google Gemini API Key
- Google Sheets API credentials

### Steps

```bash
# 1. Clone this repository
git clone https://github.com/nikkushrivastava0-a11y/restaurant-telegram-bot.git

# 2. Import the n8n workflow
# Open n8n → Import workflow → upload the workflow.json file

# 3. Add your credentials in n8n
# - Telegram Bot Token
# - Gemini API Key
# - Google Sheets OAuth

# 4. Activate the workflow
# Hit the Activate toggle in n8n — bot is live!
```

---

## 📁 Project Structure
## 📁 Project Structure
---

## 🎯 What I Learned

- Designing **multi-step automation workflows** with conditional logic
- Integrating **LLM APIs** (Gemini) for real-world NLP tasks
- Working with **webhooks** and event-driven architecture
- Connecting multiple APIs (Telegram + Gemini + Google Sheets) in a single pipeline

---

## 👨‍💻 Author

**Nitanshu Shrivastava**
- 🎓 B.Tech CSE-AI @ GL Bajaj ITM, Greater Noida (AKTU) | 2024–2028
- 💼 [LinkedIn](https://www.linkedin.com/in/nitanshu-shrivastav-878406413/)

)
- 🐙 [GitHub](https://github.com/nikkushrivastava0-a11y)

---

## 🏆 Certifications

- 📜 Introduction to Modern AI — **Cisco Networking Academy** (May 2026)

---

*⭐ If you found this useful, consider starring the repo!*
