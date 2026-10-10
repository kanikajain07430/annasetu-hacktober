<div align="center">

# 🌾 AnnaSetu (अन्नसेतु)

### Smart Agricultural Procurement & Zero-Waste Surplus Food Redistribution Platform

![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-F7DF1E?logo=javascript&logoColor=black)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?logo=tailwindcss&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

</div>

---

## 📖 About

**AnnaSetu** ("the bridge of food") is a dual-impact AgTech and social welfare platform built to solve two systemic challenges at once:

- **Agricultural price exploitation** of smallholder farmers by middlemen.
- **Commercial food waste** from kitchens, hotels, and retailers while people go hungry.

By connecting farmers directly to institutional buyers, and surplus food directly to verified NGOs, AnnaSetu builds a bridge from field to plate with less waste and fairer income along the way.

---

## 🚀 Key Features

### 1. 👨‍🌾 Agri-Procurement & Farmer Pocket Ledger

| Feature | Description |
|---|---|
| **Live Mandi & MSP Benchmarks** | Compare Government Minimum Support Prices (MSP) with local market procurement rates across districts. |
| **Direct Harvest Listings** | Farmers log harvest yields (crop type, quantity in quintals, expected rate) in an integrated digital ledger. |
| **Instant Order Matching** | Pooled village-cluster harvests are matched directly with institutional buyers, bypassing middleman markups. |

### 2. 🤝 Zero-Waste Surplus Food Bridge

| Feature | Description |
|---|---|
| **Commercial Kitchen Listings** | Hotels, canteens, banquet halls, and supermarkets broadcast batches of safe, edible surplus food. |
| **Immediate NGO Reservation** | A real-time, location-based directory lets verified shelters and community networks claim meal pickups within a safe freshness window (**under 3 hours**). |

### 3. 🚚 Smart Match & Dynamic Transit Simulator

| Feature | Description |
|---|---|
| **Corridor Route Optimization** | An interactive simulation engine matches harvest cluster origins to urban distribution depots. |
| **Digital Agricultural Transit Pass** | Instantly generates digital e-Way passes with cryptographic verification hashes and QR validation for fast-track green corridor transit. |

### 4. 📊 Admin Oversight & Support Systems

| Feature | Description |
|---|---|
| **Real-time Analytics** | Visual breakdown of procurement volumes, food rescue efficiency (**94.8%+ target**), and farmer income uplift (**+18.2%**). |
| **Grievance Resolution Desk** | Integrated ticketing for payment settlement and weight verification queries. |

---

## 🛠️ Tech Stack & Architecture

### Current Client Platform

| Layer | Technology |
|---|---|
| UI/UX Framework | Pure HTML5, ES6 JavaScript, Tailwind CSS |
| Iconography | [Lucide Icons](https://lucide.dev) |
| Architecture | Responsive Single-Page Application (SPA) with dynamic tab switching and real-time client-side state synchronization |

### Recommended Backend Stack (Target Integration)

| Layer | Options |
|---|---|
| Framework | Node.js (Express) **or** Python (FastAPI) |
| Database | PostgreSQL with PostGIS (spatial district routing) **or** MongoDB |
| External APIs | Government **Agmarknet API** (mandi prices), **Twilio / WhatsApp Business API** (SMS alerts), **Razorpay / UPI** (instant payments) |

---

## 📂 File Structure

```text
annasetu/
├── index.html    # Main SPA UI and dynamic JavaScript application logic
└── README.md     # Documentation & API integration guide
```

---

## ⚡ Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-username/annasetu.git
cd annasetu
```

### 2. Run locally

Open `index.html` directly in any modern web browser, or serve it with a local static server:

```bash
# Using Python 3
python -m http.server 8000

# Using Node.js
npx serve .
```

Then visit `http://localhost:8000` (or the port shown in your terminal).

### 3. Explore the demo

1. **Switch roles** using the dropdown in the top-right header: *Farmer, Procurement/Vendor, NGO, Admin*.
2. **Submit harvest details** in the Farmer Pocket Ledger.
3. **List surplus meals** in the Surplus Food Bridge.
4. Click **Run Smart Match Algorithm** in the logistics tab to view route optimization and digital transit passes.

---

## 🔌 API Integration Guide

The current build runs entirely client-side with simulated data. To go live, replace the mock state with the integrations below.

| Integration | Purpose | Where it plugs in |
|---|---|---|
| **Agmarknet API** | Live mandi prices for the MSP vs. market comparison | Agri-Procurement tab |
| **Twilio / WhatsApp Business API** | SMS and WhatsApp alerts for order matches, surplus listings, and pickup windows | Order matching and Surplus Food Bridge |
| **Razorpay / UPI** | Instant farmer payments and settlement | Order matching and Grievance Desk |
| **PostgreSQL + PostGIS** | Spatial queries for district routing and nearest-NGO lookup | Smart Match and Surplus Food Bridge |

> 💡 **Tip:** Keep API keys and secrets on the backend only. Never embed them in `index.html`.

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m "Add your feature"`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.

---

<div align="center">

*Bridging farms, kitchens, and communities. 🌱*

</div>
