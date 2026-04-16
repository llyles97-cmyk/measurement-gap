# Consumer Streaming — Divergence Score Findings

## The Institutional Metric
Watch time / engagement share by content genre

## The Behavioral Outcome
Retention share (active subscriber proportion) by content genre

## The Formula
```
divergence_score = engagement_share (%) − retention_share (%)
```

---

## Dataset
- Netflix Userbase Insights Dataset via Kaggle
- Key fields: watch hours, content genre, account status (Active/Churned), avg session duration, subscription type
- Analysis covers 10 content genre categories

---

## Key Findings

### Finding 1 — Reality TV Has the Highest Divergence Score
Reality TV generates the highest average watch hours per user — but also the highest churn rate in the dataset (42%). It appears dominant in engagement reporting while actively losing subscribers at the highest rate of any genre. A platform optimizing for watch time would invest more in Reality TV. A platform optimizing for retention would not.

**Divergence score: strongly positive** — overrepresented in engagement, underrepresented in retention.

### Finding 2 — Documentary Is the Clearest Alignment Gap
Documentary generates below-average watch hours but has the lowest churn rate in the dataset (12%). Subscribers who watch documentary content stay. The genre is invisible in engagement reporting and underweighted in content investment decisions, despite being a leading retention signal.

**Divergence score: negative** — underrepresented in engagement, overrepresented in retention.

### Finding 3 — Session Depth Predicts Retention Better Than Volume
Users with longer average session durations churn at significantly lower rates than users with high total watch hours but short sessions. A user who watches 4 hours in one focused sitting behaves differently from a user who accumulates 4 hours across 12 fragmented 20-minute sessions. Platforms that report total watch time without session depth are losing the signal that actually predicts whether a subscriber stays.

### Finding 4 — The High Engagement / High Churn Quadrant
Action, Thriller, Horror, and Reality TV cluster in the upper-right quadrant: above-average watch hours, above-average churn rate. These genres drive the engagement numbers on dashboards. They are also the genres most associated with subscriber departure. The quadrant map makes the institutional blindspot visible.

### Finding 5 — Premium Subscribers Show Stronger Engagement-Retention Alignment
Across subscription tiers, Premium subscribers show the smallest gap between engagement share and retention share by genre. Basic subscribers show the largest. The measurement gap is not uniform — it is amplified in lower-tier, higher-churn subscriber populations, where engagement metrics are most misleading about retention likelihood.

---

## Strategic Takeaway
Streaming platforms report engagement because it is visible, attributable, and grows over time. Retention is harder to measure, slower to respond, and less flattering in a quarterly report. The divergence score applied to genre-level data surfaces which content categories are being overvalued by engagement metrics and undervalued by the behavior that actually determines subscriber lifetime value.

**Proposed metric**: Retention-Weighted Engagement Index — weight genre-level watch time by the retention rate of the subscribers consuming it. A genre with 10% of watch time and 4% churn should be valued differently than a genre with 10% of watch time and 35% churn. The current metric cannot tell the difference.
