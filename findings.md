# Music — Divergence Score Findings

*Full analysis: [Billboard Audience Intelligence](https://github.com/llyles97-cmyk/billboard-audience-intelligence)*

---

## The Institutional Metric
Billboard Hot 100 chart share by audience archetype

## The Behavioral Outcome
Spotify popularity-weighted share by audience archetype

## The Formula
```
divergence_score = billboard_chart_share (%) − spotify_popularity_share (%)
```

---

## Dataset
- 24,676 matched Billboard + Spotify records, 2000–2021
- 7 rule-based audience archetypes
- Bias checks run on era distribution, chart performance, and match rate causes

---

## Key Findings

### Finding 1 — Billboard Overweights Country (+1.38)
Uptempo Country holds 3.75% of chart entries but only 2.37% of Spotify popularity share — the highest divergence score of any segment. The lowest average popularity of any archetype (41.23), yet consistently more chart space than audience demand justifies. Radio infrastructure advantage, not listener preference.

### Finding 2 — Streaming-Native Music Is Systematically Undercounted (-3.11)
The segment with the highest average Spotify popularity (78.68) and longest chart tenure (28.62 weeks) is the most underrepresented on Billboard. The tracks with the largest sustained audiences are discounted by a methodology still weighted toward how music gets distributed, not how it gets consumed.

### Finding 3 — Rock Didn't Get Undervalued. It Declined. (~0)
Rock dropped from 2,760 chart entries (2000s) → 705 (2010s) → 36 (2020s). Divergence score near zero — chart presence and streaming popularity declined in parallel. A structural audience shift, not a measurement failure.

### Finding 4 — Groove & Flow Aligns Perfectly (-0.16)
The only segment where chart presence and streaming popularity grew together across every decade. Hip-hop's streaming dominance was too significant to be filtered out by infrastructure bias.

### Finding 5 — Melancholic Indie Is the Next Blind Spot
Popularity rose from 64.51 → 76.49 (+18.6%) while chart entries fell from 1,386 to 334 (-76%). Growing audience, shrinking visibility. The measurement system is not looking in the right place.

---

## Strategic Takeaway
Billboard rewards distribution infrastructure. Streaming rewards audience behavior. The two systems are not in conflict — they are measuring different things and being treated as if they measure the same thing. That confusion has real consequences for A&R investment, catalog strategy, and platform curation.

**Proposed metric**: Streaming Parity Index — publish the divergence score alongside chart position to position Billboard as the honest broker between infrastructure and behavior.
