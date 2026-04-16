# The Divergence Score — Framework Documentation

## Origin

The divergence score was first developed in [Billboard Audience Intelligence](https://github.com/llyles97-cmyk/billboard-audience-intelligence) to measure the structural gap between Billboard chart share and Spotify streaming popularity across seven audience segments (2000–2021).

The core finding: the gap between what Billboard reported and what audiences actually streamed was not random. It was genre-specific, structurally predictable, and directionally consistent across decades. Country was systematically overrepresented. Streaming-native music was systematically undercounted. The chart was measuring distribution infrastructure, not audience behavior.

This framework extends that logic across industries.

---

## The Formula

```
divergence_score = institutional_metric_share (%) − behavioral_outcome_share (%)
```

**Positive score** → the institutional metric overrepresents this segment
**Negative score** → the institutional metric underrepresents this segment
**Near zero** → institutional measurement and behavior are aligned

---

## Operationalization by Industry

The formula stays constant. What changes is what gets plugged in.

### Music
```
divergence_score = billboard_chart_share (%) − spotify_popularity_share (%)
```
- **Institutional metric**: Billboard Hot 100 chart entries by genre segment
- **Behavioral outcome**: Spotify popularity-weighted share by genre segment
- **Unit of analysis**: Audience archetype (7 rule-based segments)
- **Dataset**: 24,676 matched Billboard + Spotify records, 2000–2021

### Consumer Streaming
```
divergence_score = engagement_share (%) − retention_share (%)
```
- **Institutional metric**: Watch time / engagement rate by content genre
- **Behavioral outcome**: Return viewing behavior / churn rate by content genre
- **Unit of analysis**: Content genre category
- **Dataset**: Netflix userbase dataset via Kaggle — watch hours, content genre, account status (active/churned), subscription type, session duration

### Healthcare
```
divergence_score = reminder_sent_share (%) − appointment_kept_share (%)
```
- **Institutional metric**: Share of SMS reminders sent by patient condition group
- **Behavioral outcome**: Share of appointments actually kept by patient condition group
- **Unit of analysis**: Patient condition segment (hypertension, diabetes, alcoholism, no condition)
- **Dataset**: Medical Appointment No-Shows dataset via Kaggle — 110,527 appointments in Brazil, 2015–2016

---

## Segmentation Philosophy

Rule-based segmentation is used in all three industries instead of clustering. Two reasons:

**1. Interpretability.** Business stakeholders need to act on segments, not explain them. A rule like `energy > 0.75 AND danceability > 0.60` is actionable. A cluster centroid is not.

**2. Stability.** Rule-based segments are reproducible. Clustering output shifts with random seed, sample size, and distance metric. Reproducibility matters for a framework meant to be applied across industries.

---

## What the Score Measures — and What It Doesn't

The divergence score measures the **distance between institutional reporting and behavioral outcome at the segment level**. It is not:

- A measure of data quality (the institutional data is often accurate)
- A causal claim (divergence identifies the gap, not the mechanism)
- A recommendation engine (the score surfaces where to look, not what to do)

It is a **diagnostic tool**. It answers: *where is the system measuring the wrong thing?*

---

## Limitations

**Match rate constraints.** In the music analysis, the inner join on song + artist produced a 21.63% match rate. Findings are directional. Divergence scores identify structural patterns in the matched sample and should be treated as leading indicators, not definitive market share calculations.

**Proxy variables.** In streaming and healthcare, the behavioral outcome variable is a proxy — account status as a proxy for retention, appointment attendance as a proxy for health engagement conversion. These are reasonable proxies with documented validity in the literature, but they are not perfect.

**Time scope.** The healthcare dataset covers 2015–2016. The streaming dataset is synthetic/generalized. Findings reflect structural patterns rather than current-state market conditions.

**Directionality, not magnitude.** The divergence score is most reliable for identifying *which* segments are misrepresented and *in which direction* — not for precise quantification of the size of the gap.

---

## How to Apply This Framework to a New Industry

1. **Identify the institutional metric** — what does the industry report to leadership, investors, or the public? What KPI sits on every executive dashboard?

2. **Identify the behavioral outcome** — what does the institution actually *want* to produce? Not the metric — the outcome. Subscribers. Appointments. Purchases. Loyalty.

3. **Define segments** — what meaningful groupings exist in this industry? Genre. Condition. Product category. Customer type. Rule-based where possible.

4. **Compute shares** — for each segment, calculate its share of the institutional metric and its share of the behavioral outcome.

5. **Calculate divergence** — subtract. Sort. The outliers are where the measurement system is failing.

6. **Ask why** — the score surfaces where. Explaining why requires domain knowledge. That's the strategic layer.
