# The Measurement Gap

**A cross-industry audit of where institutional metrics diverge from real behavior**

`SQL` `Python` `Audience Intelligence` `Cross-Industry` `Framework`

---

## The Thesis

Every industry has built its measurement infrastructure around the wrong signals.

Music measures chart position. Streaming measures watch time. Healthcare measures content engagement. Each of these metrics was designed to count something visible and reportable — not to capture the behavior that actually matters to the business.

The result is a structural gap: institutions optimize for the metric they can measure, and quietly lose track of the outcome they were trying to produce.

This project makes that gap quantifiable.

Using a consistent **divergence score framework** applied across three industries, it argues that the measurement problem is not industry-specific — it is systemic. And that the same analytical approach that surfaces misrepresentation in music charts can surface it in streaming retention, healthcare conversion, and beyond.

---

## The Framework

### Divergence Score

The divergence score measures the distance between what an institution reports and what audiences actually do.

```
divergence_score = institutional_metric_share (%) − behavioral_outcome_share (%)
```

- **Positive score** → the institutional metric overrepresents this segment relative to real behavior
- **Negative score** → the institutional metric underrepresents this segment relative to real behavior
- **Near zero** → institutional measurement and behavior are aligned

The framework was first developed in [Billboard Audience Intelligence](https://github.com/llyles97-cmyk/billboard-audience-intelligence), where it measured the gap between Billboard chart share and Spotify streaming popularity across seven audience segments. This project extends that logic across industries.

### Operationalization by Industry

| Industry | Institutional Metric | Behavioral Outcome | What the Gap Reveals |
|---|---|---|---|
| **Music** | Billboard chart share | Spotify streaming popularity share | Which genres are overvalued by radio infrastructure vs. actual listener demand |
| **Consumer Streaming** | Engagement rate / watch time | Retention / return behavior | Which content types drive views but not subscribers |
| **Healthcare** | Content engagement (views, clicks) | Action conversion (appointments, follow-through) | Where patient education content fails to produce clinical behavior |

The mathematical structure is consistent across all three. What changes is the domain — and that consistency is the argument.

---

## Why This Matters

The measurement gap is not a data quality problem. The data is often accurate. The problem is that industries have confused **activity** with **outcome**, and built entire reporting systems — dashboards, KPIs, executive reports — around the former.

The consequences differ by industry:

- In **music**, it means labels invest in radio promotion for genres audiences have already left
- In **streaming**, it means platforms report engagement numbers that don't predict churn
- In **healthcare**, it means campaigns are optimized for clicks that never become appointments

In each case, the institution is measuring something real. It just isn't measuring the right thing.

---

## Project Structure

```
measurement-gap/
│
├── README.md                   ← You are here
├── framework.md                ← Full divergence score methodology
│
├── music/
│   ├── findings.md             ← Summary + link to full Billboard project
│   └── analysis.sql            ← Core divergence queries (reference)
│
├── streaming/
│   ├── findings.md
│   ├── analysis.sql
│   └── analysis.py
│
├── healthcare/
│   ├── findings.md
│   ├── analysis.sql
│   └── analysis.py
│
├── data/
│   └── dataset_citations.md    ← All data sources and methodology notes
│
└── visuals/
    ├── streaming_divergence_score.png
    ├── streaming_engagement_churn_quadrant.png
    ├── streaming_share_comparison.png
    ├── healthcare_divergence_score.png
    ├── healthcare_outreach_vs_attendance.png
    ├── healthcare_sms_effectiveness.png
    └── healthcare_wait_time.png
```

---

## Industry Findings — Summary

### Music
*Full analysis: [Billboard Audience Intelligence](https://github.com/llyles97-cmyk/billboard-audience-intelligence)*

Billboard's chart methodology was built for radio — a system defined by scarcity, geography, and gatekeeping. Streaming eliminated all three. The divergence score applied to 24,676 matched chart and streaming records reveals the gap is not random: it is genre-specific, structurally predictable, and directionally consistent across decades.

Key finding: Uptempo Country holds a divergence score of **+1.38** — overrepresented on Billboard relative to streaming demand. Viral & Streaming Native holds **-3.11** — the most underrepresented segment despite the highest average Spotify popularity in the dataset. The chart rewards distribution infrastructure. Streaming rewards audience behavior. They are not the same system.

→ [music/findings.md](music/findings.md)

---

### Consumer Streaming
*Dataset: Netflix Customer Churn and Engagement Dataset — 1,000 users, 7 genres via Kaggle*

Streaming platforms report engagement — watch time, completion rates, title views. But engagement does not predict retention, and retention is what determines subscriber lifetime value. A title can drive hours of viewing and contribute nothing to the reason a subscriber stays.

The divergence score applied to genre-level watch time and churn data reveals the gap is not random — it is genre-specific and directionally consistent.

Thriller holds a divergence score of **+1.48** and a churn rate of **57.9%** — the highest in the dataset. It is the genre most overrepresented in watch time relative to subscriber retention. Romance follows at **+1.43** with a **56.9%** churn rate. Both genres look strong on an engagement dashboard. Both are losing subscribers at above-average rates.

Comedy sits at **-2.35** — the most underrepresented genre in watch time relative to its share of retained subscribers. It has the lowest churn rate in the dataset at **46.9%**. A platform optimizing for watch time would underinvest in Comedy. A platform optimizing for subscriber lifetime value would not.

The genres that dominate engagement reporting are not the genres keeping subscribers. The measurement system cannot tell the difference.

→ [streaming/findings.md](streaming/findings.md)

---

### Healthcare
*Dataset: Medical Appointment No-Shows — 110,527 appointments, Brazil public hospitals, 2015–2016 via Kaggle*

Healthcare outreach is measured by activity — reminders sent, campaigns deployed, content published. But in healthcare, the behavioral outcome is not a stream or a subscription. It is an appointment kept, a treatment followed through, a screening completed.

The divergence score applied to 110,527 appointment records measures the gap between outreach share (SMS reminders sent by patient condition group) and kept share (appointments actually attended). The overall no-show rate across the dataset is **20.2%** — one in five scheduled appointments is abandoned.

The No Condition segment holds a divergence score of **+1.58** — it receives a disproportionate share of outreach relative to the appointments it keeps. Patients with chronic conditions (Hypertension + Diabetes: **-0.60**, Hypertension Only: **-0.23**) keep appointments at higher rates than their share of outreach reflects. The outreach system is concentrating effort where behavior is already stronger.

The starkest finding is not in the divergence score — it is in the SMS effectiveness data. Among patients who received a reminder, the Alcoholism segment still no-shows at **32.7%**. Receiving a reminder is being reported as outreach coverage. It should be reported as conversion. The two numbers are not the same.

The strongest behavioral predictor in the dataset is scheduling lag. Same-day appointments have a no-show rate of **6.6%**. Appointments scheduled 30+ days out reach **33.0%** — a 5x gap that has nothing to do with whether a reminder was sent.

→ [healthcare/findings.md](healthcare/findings.md)

---

## The Unifying Insight

Three industries. Three different institutional metrics. Three different behavioral outcomes. One consistent finding:

**The gap between what institutions measure and what audiences actually do is not a bug — it is a feature of how measurement systems get built.** Institutions optimize for what is countable, reportable, and defensible in an executive report. Behavior is messier, slower, and harder to attribute. So it gets approximated — and then the approximation becomes the goal.

The divergence score does not fix this. It makes the distance visible. And visibility is the first condition for changing what gets measured.

---

## SQL Techniques Used

`JOINs` `CTEs` `Window Functions` `CASE WHEN segmentation` `GROUP BY + HAVING` `Subqueries` `Aggregation` `Multi-label classification`

---

## About

Built as part of a data analytics portfolio targeting roles in audience intelligence, consumer insights, and measurement strategy.

**Lyles Mom** — Audience Intelligence & Personalization Strategist
Portfolio: [lylesmomportfolio.my.canva.site](https://lylesmomportfolio.my.canva.site)
Brand: [@cultcirculation](https://instagram.com/cultcirculation)
