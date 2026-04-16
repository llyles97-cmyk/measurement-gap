# Data Sources

## Music

**Billboard Hot 100**
- Source: Kaggle — dhruvildave
- URL: https://www.kaggle.com/datasets/dhruvildave/billboard-the-hot-100-songs
- Records: 330,087 chart entries
- Coverage: 1958–2021
- Used in: music/analysis.sql (reference — full analysis in Billboard Audience Intelligence)

**Spotify Audio Features**
- Source: Kaggle — maharshipandya
- URL: https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset
- Records: 113,999 tracks
- Coverage: Multi-era
- Used in: music/analysis.sql (reference)

**Joined dataset**: Inner join on cleaned song + artist name — 24,676 matched entries, 2000–2021
Match rate: 21.63% of scoped chart entries. Bias checks run on era distribution drift, chart performance comparison, and low match rate causes. Findings are directional.

---

## Consumer Streaming

**Netflix Userbase Insights Dataset**
- Source: Kaggle
- URL: https://www.kaggle.com/datasets/
- Key columns: `user_id`, `subscription_type`, `watch_hours`, `content_genre`, `avg_session_duration`, `account_status` (Active/Churned), `device_type`
- Used in: streaming/analysis.sql, streaming/analysis.py
- Note: Dataset represents a generalized userbase model. Findings reflect structural patterns in the engagement-retention relationship, not Netflix-specific proprietary data.

---

## Healthcare

**Medical Appointment No-Shows**
- Source: Kaggle — joniarroba
- URL: https://www.kaggle.com/datasets/joniarroba/noshowappointments
- Records: 110,527 appointments
- Coverage: Brazil public hospitals, 2015–2016
- Key columns: `PatientId`, `AppointmentID`, `Gender`, `ScheduledDay`, `AppointmentDay`, `Age`, `Neighbourhood`, `Scholarship`, `Hipertension`, `Diabetes`, `Alcoholism`, `Handcap`, `SMS_received`, `No-show`
- Used in: healthcare/analysis.sql, healthcare/analysis.py
- Note: `No-show` column is the behavioral outcome variable. `SMS_received` serves as the institutional outreach metric proxy.

---

## Methodology Notes

All datasets are publicly available via Kaggle under open licenses. No proprietary or personally identifiable information is used. The healthcare dataset uses de-identified appointment records. Analysis is conducted for portfolio and research purposes only.

Divergence scores are computed at the segment level. They identify structural patterns and directional gaps — they are not definitive market share calculations. See framework.md for full methodology.
