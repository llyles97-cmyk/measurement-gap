# Insights

## The Through-Line

Three industries. Three datasets. One consistent finding: the metric institutions report is not the metric that predicts the outcome they care about. The divergence score makes that gap quantifiable — and in every case, the gap is structural, not incidental.

---

## Music

**Dataset:** 24,676 matched Billboard Hot 100 + Spotify records, 2000–2021

The Billboard chart was built for radio. Streaming eliminated the infrastructure advantage radio created. The divergence score reveals which genres benefited from that infrastructure and which were undervalued by it.

- Uptempo Country: **+1.38** — the most overrepresented genre. More chart space than audience demand justifies. Radio infrastructure, not listener preference.
- Viral & Streaming Native: **-3.11** — the most underrepresented. Highest average Spotify popularity in the dataset (78.68). Longest chart tenure when it does break through (28.62 weeks). The system is not looking where the audience already is.
- Rock: **~0** — not undervalued. Declined. Chart presence and streaming popularity fell in parallel. A structural audience shift the data validates.
- Melancholic Indie: popularity up **+18.6%** while chart entries fell **-76%**. The next blind spot forming now.

**The gap:** Billboard rewards distribution. Streaming rewards behavior. They are not measuring the same thing and are being treated as if they are.

---

## Consumer Streaming

**Dataset:** 1,000 users, 7 genres — Netflix Customer Churn and Engagement Dataset via Kaggle

Streaming platforms report watch time. Watch time does not predict whether a subscriber stays. The divergence score applied to genre-level engagement and churn data surfaces which genres look strong on dashboards and which actually retain subscribers.

- Thriller: **+1.48** divergence, **57.9%** churn rate — the genre most overrepresented in watch time relative to retention. Drives hours. Loses subscribers.
- Romance: **+1.43** divergence, **56.9%** churn rate — same pattern. High engagement, high departure.
- Comedy: **-2.35** divergence, **46.9%** churn rate — the most underrepresented genre in watch time relative to its share of retained subscribers. Lowest churn in the dataset. A platform optimizing for watch time would underinvest here. A platform optimizing for subscriber lifetime value would not.
- Documentary: lowest churn, below-average watch hours — invisible in engagement reporting, strong in retention signal.

**The gap:** The genres that dominate engagement dashboards are not the genres keeping subscribers. The measurement system cannot distinguish between a viewer who watches and leaves and a viewer who watches and stays.

---

## Healthcare

**Dataset:** 110,527 medical appointments, Brazil public hospitals, 2015–2016 via Kaggle

Healthcare outreach is measured by activity — reminders sent, campaigns deployed. The behavioral outcome is an appointment kept. The divergence score applied to SMS outreach share vs. appointment kept share by patient condition reveals where the system is concentrating effort and where it is failing to convert.

- Overall no-show rate: **20.2%** — one in five scheduled appointments abandoned.
- No Condition segment: **+1.58** divergence — receives the largest share of outreach, keeps appointments at below its outreach share. The system's largest investment produces median returns.
- Hypertension + Diabetes: **-0.60** — keeps appointments at a higher rate than its outreach share reflects. Underserved relative to behavioral reliability.
- Alcoholism: **32.7%** no-show rate *despite receiving an SMS reminder*. Outreach coverage is being reported. Outreach conversion is not. They are not the same number.
- Same-day appointments: **6.6%** no-show rate. Appointments scheduled 30+ days out: **33.0%**. A **5x gap** that has nothing to do with whether a reminder was sent — and everything to do with scheduling infrastructure.

**The gap:** The outreach system reports what it did. It should report what changed. Scheduling lag is the strongest behavioral predictor in the dataset and is absent from standard outreach reporting.

---

## Cross-Industry Pattern

| Industry | Institutional Metric | Behavioral Outcome | Divergence Direction |
|---|---|---|---|
| Music | Billboard chart share | Spotify popularity share | Infrastructure genres overrepresented |
| Streaming | Watch time share | Retained subscriber share | High-churn genres overrepresented |
| Healthcare | SMS outreach share | Appointment kept share | Low-conversion segments overserved |

In every case the institution is measuring something real. The data is not wrong. The problem is that activity has been substituted for outcome — and the substitution has become invisible because the metric is reported so consistently that no one asks what it was supposed to represent.

The divergence score does not fix this. It makes the distance visible. Visibility is the first condition for changing what gets measured.
