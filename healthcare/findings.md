# Healthcare — Divergence Score Findings

## The Institutional Metric
Share of SMS appointment reminders sent by patient condition group

## The Behavioral Outcome
Share of appointments actually kept by patient condition group

## The Formula
```
divergence_score = outreach_share (%) − appointment_kept_share (%)
```

---

## Dataset
- Medical Appointment No-Shows — Kaggle (joniarroba)
- 110,527 appointments across Brazil public hospitals, 2015–2016
- Key fields: condition flags (hypertension, diabetes, alcoholism), SMS_received, No-show
- Overall no-show rate: ~20.2% of all scheduled appointments

---

## Key Findings

### Finding 1 — Outreach Is Not Proportional to Attendance Likelihood
The distribution of SMS reminders across patient condition groups does not reflect which groups are most likely to attend. Patients with chronic conditions (hypertension, diabetes) receive a higher share of outreach — and show up at higher rates. Patients with alcoholism receive proportionally less outreach — and show up at the lowest rates. The outreach system is concentrating effort where behavior is already stronger, and underinvesting where the gap is widest.

### Finding 2 — Receiving a Reminder Does Not Reliably Predict Attendance
The no-show rate among patients who *received* an SMS reminder is counterintuitively high for certain condition groups. For patients with alcoholism, the no-show rate despite receiving a reminder exceeds 30%. For no-condition patients, it approaches 22%. The reminder — the institution's primary outreach metric — is being reported as coverage. It should be reported as conversion. The two numbers are not the same.

### Finding 3 — Wait Time Is the Strongest Behavioral Predictor
Appointments scheduled for the same day have dramatically lower no-show rates than appointments scheduled 30+ days out. The scheduling lag is more predictive of attendance than condition status, SMS receipt, or patient age. This signal is present in the data but absent from standard outreach reporting, which focuses on whether a reminder was sent — not on when the appointment was scheduled relative to when the patient made it.

### Finding 4 — The No-Condition Group Drives Volume but Not Fidelity
Patients with no recorded condition represent the largest segment by appointment volume and receive a proportionally high share of SMS outreach. Their attendance rate is close to average — not significantly better than lower-outreach groups. The system's largest outreach investment produces median returns. The divergence score for this segment is mildly positive: outreach share slightly exceeds their kept appointment share.

### Finding 5 — Age Is a Signal, Not a Category
Attendance rates are not linear by age. Elderly patients (75+) show some of the highest attendance rates in the dataset — which makes sense given appointment urgency. Young adults (18–34) show the highest no-show rates. SMS coverage does not differ meaningfully between these groups. An outreach system calibrated to attendance likelihood would weight these segments differently. The current system sends reminders based on appointment existence, not behavioral risk.

---

## Strategic Takeaway
Healthcare outreach is measured by activity — reminders sent, campaigns deployed, content published. The gap between outreach volume and actual patient behavior is the same structural problem as engagement vs. retention in streaming or chart position vs. streaming behavior in music. The institution reports what it did. It should be reporting what changed.

**Proposed metric**: Behavioral Conversion Rate — appointments kept divided by reminders sent, segmented by condition group and scheduling lag. A system optimizing for this metric would send fewer reminders to low-risk patients and invest more in higher-risk, longer-lag segments where the gap between outreach and attendance is widest.
