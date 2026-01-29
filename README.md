# ✈️ BearFlights

BearFlights is a fullstack project built to strengthen my understanding of **backend-to-frontend data flow**, data enrichment, and real-world API integration.

The project collects live flight data from the OpenSky Network, processes and enriches it using Python, stores it in Supabase, and presents it in a Next.js frontend in a clear and engaging way.

---

## 🎯 Purpose of the Project:

The goal of BearFlights was not just to “make something work”, but to deeply understand:

- how backend data flows all the way to the UI
- how Supabase can act as a bridge between backend and frontend
- how to work with real, imperfect API data
- how structured data can be transformed into something understandable and fun to explore

This project helped solidify my mental model of how:

> Python → Database → Frontend → UI  

works in practice.

---

## ✈️ Personal Motivation:

I have always found it fun to watch aircraft and wonder where they are going.  
Over time, that curiosity turned into an interest in tracking flights and understanding the data behind them.

With BearFlights, that interest became more automated — instead of physically watching the sky to see if an aircraft passed by, I can now let the system do the observing and tell me what happened.

This made the project both technically educational and genuinely enjoyable to build.

---

## 🧠 What the Project Does:

### Backend (Python)
- Authenticates with the OpenSky Network using OAuth2
- Fetches live aircraft state data
- Filters aircraft within a defined geographic radius
- Enriches data by:
  - calculating distance using the Haversine formula
  - identifying nearest and farthest aircraft
  - attempting to infer departure country
- Stores and updates enriched data in Supabase
- Uses **strict typing** to improve reliability, clarity, and maintainability

This significantly improved my understanding of Python, especially around:
- type safety
- defensive programming
- explicit data validation
- clean function boundaries

---

### Database (Supabase)
- Acts as the central data layer
- Stores:
  - individual flight observations
  - enriched flight metadata
  - daily flight summaries
- Makes it easy to share the same dataset between:
  - backend ingestion scripts
  - frontend Server Components

---

### Frontend (Next.js)
- Built using the App Router and Server Components
- Fetches data directly from Supabase
- Displays:
  - a flight overview table
  - a detailed view for each flight via dynamic routes
- Focuses on:
  - clarity
  - structure
  - readable data presentation

---

## 🧩 Key Learnings:

Through this project I gained:

- a stronger understanding of fullstack data flow
- hands-on experience with real API integrations
- practical experience using Supabase in production-like scenarios
- improved confidence with Python strict typing
- a deeper understanding of Next.js routing and Server Components
- experience turning raw data into meaningful UI

---

## 🟢 Working on now: 

- Debugging not collecting data

---

## 🚀 Future Ideas:

- Build my own API w/ FastAPI, containing flight data collected in Bearflights. 
- Collecting full flight route w/vizualising frontend. 
- Intergrate a AI to either further explain about the flights or the company.

---

Built to understand how data survives the journey from Python to pixels.

---

## Run Locally:

- Get your API keys from https://opensky-network.org/
- Make sure to have installed .venv 
- Run .venv\Scripts\Activate.ps1 in Terminal

### Run Scripts:
- python -m scripts.ingest_opensky
---
- python -m scripts.enrich_routes
---
- python -m scripts.build_daily_fligts
---
- python -m scripts.enrich.enrich_all





