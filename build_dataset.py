import pandas as pd

data = [
    # ── BUDGET SUMMARY (para 64-65) ──────────────────────────────────────
    ("Budget Summary", "Total budget FY 2083/84", 212434, "total", 64),
    ("Budget Summary", "Recurrent expenditure", 127058, "total", 64),
    ("Budget Summary", "Capital expenditure", 43110, "total", 64),
    ("Budget Summary", "Financial management expenditure", 42264, "total", 64),
    ("Budget Summary", "Revenue target", 140531, "revenue", 65),
    ("Budget Summary", "Foreign grants", 6174, "revenue", 65),
    ("Budget Summary", "Total deficit", 65729, "financing", 65),
    ("Budget Summary", "Foreign loans (gross)", 24728, "financing", 65),
    ("Budget Summary", "Domestic borrowing (gross)", 41000, "financing", 65),
    ("Budget Summary", "Domestic loan repayment", 24589, "financing", 65),
    ("Budget Summary", "Net domestic borrowing", 16411, "financing", 65),

    # ── FISCAL TRANSFERS (para 66) ────────────────────────────────────────
    ("Fiscal Transfer", "Equalization grant - provinces", 6150, "transfer", 66),
    ("Fiscal Transfer", "Equalization grant - local governments", 9020, "transfer", 66),
    ("Fiscal Transfer", "Complementary grant - provinces", 460, "transfer", 66),
    ("Fiscal Transfer", "Complementary grant - local governments", 893, "transfer", 66),
    ("Fiscal Transfer", "Special grant - provinces", 382, "transfer", 66),
    ("Fiscal Transfer", "Special grant - local governments", 940, "transfer", 66),
    ("Fiscal Transfer", "Conditional grant - provinces (federal projects)", 3972, "transfer", 66),
    ("Fiscal Transfer", "Conditional grant - local governments (federal projects)", 20608, "transfer", 66),
    ("Fiscal Transfer", "Revenue sharing to provinces and local govts (estimate)", 17500, "transfer", 66),

    # ── ROADS & URBAN (para 40-41) ────────────────────────────────────────
    ("Roads & Urban", "TOTAL roads and urban infrastructure sector", 28648, "sector_total", 41),
    ("Roads & Urban", "Purba-Paschim (East-West) Highway upgradation", 3746, "allocation", 40),
    ("Roads & Urban", "Kathmandu-Tarai-Madhes Fast Track (Rute Marg)", 1764, "allocation", 40),
    ("Roads & Urban", "Haluwakhola (Postal) Highway", 465, "allocation", 40),
    ("Roads & Urban", "Karnali Highway (Surkhet-Jumla-Gamgadhi)", 100, "allocation", 40),
    ("Roads & Urban", "Puspalal Mid-Hill Highway (65km + 5 bridges)", 216, "allocation", 40),
    ("Roads & Urban", "Madan Bhandari Highway (25km blacktopping)", 146, "allocation", 40),
    ("Roads & Urban", "National highway and strategic road bridges", 987, "allocation", 40),
    ("Roads & Urban", "Prithvi Highway + Nagdhunga tunnel", 655, "allocation", 40),
    ("Roads & Urban", "Three Corridors (Karnali 31km + Kaligandaki 21km + Koshi 15km)", 625, "allocation", 40),
    ("Roads & Urban", "Galchi-Syaphrubeshi-Rasuwagadhi upgradation", 135, "allocation", 40),
    ("Roads & Urban", "Road safety (signals, crash barriers, dividers)", 246, "allocation", 40),
    ("Roads & Urban", "Nationwide road maintenance campaign", 2852, "allocation", 40),
    ("Roads & Urban", "Landslide and climate-resilient highway structures", 317, "allocation", 40),
    ("Roads & Urban", "12 towns along Mid-Hill Highway land development", 183, "allocation", 41),
    ("Roads & Urban", "Urban waste management and river corridor greening", 419, "allocation", 41),
    ("Roads & Urban", "Suspension bridges (rural access)", 514, "allocation", 41),

    # ── WATER & SANITATION (para 42) ──────────────────────────────────────
    ("Water", "TOTAL water and sanitation sector", 3717, "sector_total", 42),
    ("Water", "280 incomplete Tarai drinking water projects", 250, "allocation", 42),
    ("Water", "Melamchi distribution expansion (Kirtipur, Jorpati etc.)", 726, "allocation", 42),
    ("Water", "Urban water supply - major cities (Damak, Dharan, Birgunj etc.)", 234, "allocation", 42),
    ("Water", "Kathmandu valley wastewater treatment (5 plants, 72.7M litres/day)", 346, "allocation", 42),

    # ── ENERGY (para 43) ──────────────────────────────────────────────────
    ("Energy", "TOTAL energy production, transmission and distribution", 8554, "sector_total", 43),
    ("Energy", "Transmission lines and substations construction", 7000, "allocation", 43),

    # ── IRRIGATION (para 44) ──────────────────────────────────────────────
    ("Irrigation", "Babai Irrigation + Rajpur + Bheri-Babai Diversion", 563, "allocation", 44),
    ("Irrigation", "Sikta Irrigation (5,000 hectares Banke)", 255, "allocation", 44),
    ("Irrigation", "Sun Koshi-Marin Diversion (dam + powerhouse)", 298, "allocation", 44),
    ("Irrigation", "Bagmati Irrigation upgrade (122,000 ha command area)", 53, "allocation", 44),
    ("Irrigation", "Mahakali Irrigation + Rani-Jamara-Kuleriya (Lamki section)", 513, "allocation", 44),
    ("Irrigation", "Brihad Dang Valley + Pragna-Badkapur (2,380 ha)", 121, "allocation", 44),
    ("Irrigation", "Canal maintenance (Sunsari-Morang, Chandra, Kamala, Koshi pump etc.)", 44, "allocation", 44),
    ("Irrigation", "Underground irrigation Tarai-Madhes (3,980 ha)", 183, "allocation", 44),
    ("Irrigation", "Lift irrigation in hill tars", 80, "allocation", 44),

    # ── ICT (para 45) ─────────────────────────────────────────────────────
    ("ICT", "TOTAL ICT and communications sector", 593, "sector_total", 45),
    ("ICT", "Public welfare advertisements (print and electronic)", 33, "allocation", 45),

    # ── SPORTS (para 46) ──────────────────────────────────────────────────
    ("Sports", "TOTAL sports sector", 403, "sector_total", 46),

    # ── EDUCATION (para 47) ───────────────────────────────────────────────
    ("Education", "TOTAL education sector", 21830, "sector_total", 47),
    ("Education", "Community school infrastructure mapping", 100, "allocation", 47),
    ("Education", "Scholarships - school to higher education", 860, "allocation", 47),
    ("Education", "Child care home infrastructure and management", 31, "allocation", 49),

    # ── HEALTH (para 48) ──────────────────────────────────────────────────
    ("Health", "TOTAL health sector", 10195, "sector_total", 48),
    ("Health", "Health insurance program", 1500, "allocation", 48),
    ("Health", "Free treatment + safe motherhood + free medicines", 1315, "allocation", 48),
    ("Health", "Basic hospital construction (336 hospitals over 3 years)", 590, "allocation", 48),
    ("Health", "B.P. Koirala Cancer Hospital - PET scan and cyclotron", 32, "allocation", 48),

    # ── SOCIAL SECURITY & WOMEN/CHILDREN (para 49) ────────────────────────
    ("Social Security", "TOTAL social security allocation", 12000, "sector_total", 49),
    ("Social Security", "Dalit children nutrition allowance (under-5, Rs.1000/month)", 300, "allocation", 49),
    ("Women & Children", "TOTAL women, children, gender and sexual minority sector", 227, "sector_total", 49),

    # ── AGRICULTURE (para 50) ─────────────────────────────────────────────
    ("Agriculture", "TOTAL agriculture and livestock sector", 4692, "sector_total", 50),
    ("Agriculture", "Chemical fertilizer procurement", 3246, "allocation", 50),
    ("Agriculture", "National agriculture modernization program", 207, "allocation", 50),
    ("Agriculture", "Crop insurance premium subsidy", 219, "allocation", 50),
    ("Agriculture", "Organic and green manure promotion (local govt grants)", 36, "allocation", 50),
    ("Agriculture", "Animal disease control (Khurpaka and other vaccines)", 24, "allocation", 50),

    # ── FOREST & ENVIRONMENT (para 51) ────────────────────────────────────
    ("Forest", "TOTAL forest, environment and climate sector", 1231, "sector_total", 51),
    ("Forest", "Chure and Tarai water source conservation and ponds", 100, "allocation", 51),

    # ── CULTURE, TOURISM & AVIATION (para 52-53) ──────────────────────────
    ("Culture & Tourism", "TOTAL culture and tourism sector", 734, "sector_total", 52),
    ("Culture & Tourism", "Lumbini development (Tilaurakot, Devdaha, Kapilvastu, Ramagrama)", 83, "allocation", 52),
    ("Aviation", "TOTAL civil aviation sector", 293, "sector_total", 53),
    ("Aviation", "Tribhuvan International Airport upgradation", 153, "allocation", 53),

    # ── LABOR & EMPLOYMENT (para 54) ──────────────────────────────────────
    ("Labor", "TOTAL labor and employment sector", 363, "sector_total", 54),

    # ── INDUSTRY, COMMERCE & SUPPLY (para 55-56) ──────────────────────────
    ("Industry", "TOTAL industry, commerce and supply sector", 831, "sector_total", 55),
    ("Industry", "Industrial infrastructure development (Motibur, Mayuradwaj)", 65, "allocation", 55),
    ("Industry", "Mining and industrial access roads", 50, "allocation", 55),

    # ── SCIENCE, TECHNOLOGY & STARTUPS (para 57) ──────────────────────────
    ("Science & Tech", "TOTAL science, technology and innovation", 400, "sector_total", 57),
    ("Science & Tech", "Nepal Enterprise Facility (startup platform)", 50, "allocation", 57),

    # ── DEFENSE & SECURITY (para 62, Annex 3/4) ───────────────────────────
    ("Defense", "TOTAL Nepal Army (Ministry 345)", 6496, "sector_total", 62),
    ("Defense", "Nepal Army housing upgradation", 200, "allocation", 62),
    ("Security", "TOTAL public peace and security (Annex 3 functional classification)", 9196, "sector_total", 62),
]

columns = ["sector", "description", "amount_crore", "amount_type", "para_ref"]
df = pd.DataFrame(data, columns=columns)
df.to_csv("nepal_budget_clean.csv", index=False)
print(f"Total rows: {len(df)}")
print(f"\nSector totals only:")
totals = df[df['amount_type'] == 'sector_total'].groupby('sector')['amount_crore'].sum()
print(totals.sort_values(ascending=False).to_string())
print(f"\nNote: Do NOT sum all rows - sector_totals already include their sub-items")
print(f"Actual total budget: Rs. 212,434 crore")