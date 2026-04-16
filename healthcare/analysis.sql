-- ============================================================
-- Measurement Gap: Healthcare
-- Divergence Score: Outreach Share vs. Appointment Kept Share
-- Dataset: Medical Appointment No-Shows (Kaggle — joniarroba)
-- 110,527 appointments, Brazil public hospitals 2015-2016
-- Tool: SQLite
-- ============================================================


-- ============================================================
-- SCHEMA REFERENCE
-- ============================================================
-- PatientId       TEXT    Unique patient identifier
-- AppointmentID   TEXT    Unique appointment identifier
-- Gender          TEXT    M / F
-- ScheduledDay    TEXT    Day patient scheduled the appointment
-- AppointmentDay  TEXT    Day of actual appointment
-- Age             INT     Patient age
-- Neighbourhood   TEXT    Location of appointment
-- Scholarship     INT     Welfare enrollment: 1=yes, 0=no
-- Hipertension    INT     1=yes, 0=no
-- Diabetes        INT     1=yes, 0=no
-- Alcoholism      INT     1=yes, 0=no
-- Handcap         INT     1=yes, 0=no
-- SMS_received    INT     Reminder sent: 1=yes, 0=no
-- No_show         TEXT    'Yes' = did not show up / 'No' = showed up
-- ============================================================


-- ============================================================
-- QUERY 1: Baseline — overall show/no-show rate
-- ============================================================
SELECT
    COUNT(*) AS total_appointments,
    SUM(CASE WHEN No_show = 'No' THEN 1 ELSE 0 END) AS showed_up,
    SUM(CASE WHEN No_show = 'Yes' THEN 1 ELSE 0 END) AS no_show,
    ROUND(
        100.0 * SUM(CASE WHEN No_show = 'Yes' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS no_show_rate_pct
FROM appointments;


-- ============================================================
-- QUERY 2: SMS reminder effectiveness — the institutional metric
-- Does sending a reminder (the outreach action) predict attendance?
-- ============================================================
SELECT
    SMS_received,
    COUNT(*) AS total_appointments,
    SUM(CASE WHEN No_show = 'No' THEN 1 ELSE 0 END) AS showed_up,
    ROUND(
        100.0 * SUM(CASE WHEN No_show = 'No' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS show_rate_pct,
    ROUND(
        100.0 * SUM(CASE WHEN No_show = 'Yes' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS no_show_rate_pct
FROM appointments
GROUP BY SMS_received;


-- ============================================================
-- QUERY 3: Core divergence calculation
-- Segment: patient condition group
-- Institutional metric: share of SMS reminders sent to each group
-- Behavioral outcome: share of appointments kept by each group
-- ============================================================
WITH condition_segments AS (
    SELECT
        AppointmentID,
        SMS_received,
        No_show,
        CASE
            WHEN Hipertension = 1 AND Diabetes = 0 AND Alcoholism = 0
                THEN 'Hypertension Only'
            WHEN Diabetes = 1 AND Hipertension = 0 AND Alcoholism = 0
                THEN 'Diabetes Only'
            WHEN Alcoholism = 1
                THEN 'Alcoholism'
            WHEN Hipertension = 1 AND Diabetes = 1
                THEN 'Hypertension + Diabetes'
            WHEN Hipertension = 0 AND Diabetes = 0 AND Alcoholism = 0
                THEN 'No Condition'
            ELSE 'Other Combination'
        END AS condition_segment
    FROM appointments
),
segment_totals AS (
    SELECT
        condition_segment,
        COUNT(*) AS total_appointments,
        SUM(SMS_received) AS sms_sent,
        SUM(CASE WHEN No_show = 'No' THEN 1 ELSE 0 END) AS kept_appointments
    FROM condition_segments
    GROUP BY condition_segment
),
platform_totals AS (
    SELECT
        SUM(sms_sent) AS total_sms,
        SUM(kept_appointments) AS total_kept
    FROM segment_totals
)
SELECT
    s.condition_segment,
    s.total_appointments,
    s.sms_sent,
    s.kept_appointments,
    ROUND(100.0 * s.sms_sent / p.total_sms, 2) AS outreach_share_pct,
    ROUND(100.0 * s.kept_appointments / p.total_kept, 2) AS kept_share_pct,
    ROUND(
        (100.0 * s.sms_sent / p.total_sms) -
        (100.0 * s.kept_appointments / p.total_kept),
        2
    ) AS divergence_score
FROM segment_totals s
CROSS JOIN platform_totals p
ORDER BY divergence_score DESC;


-- ============================================================
-- QUERY 4: Wait time effect on attendance
-- Does scheduling lag predict no-show behavior?
-- ============================================================
SELECT
    CASE
        WHEN JULIANDAY(AppointmentDay) - JULIANDAY(ScheduledDay) = 0
            THEN 'Same Day'
        WHEN JULIANDAY(AppointmentDay) - JULIANDAY(ScheduledDay) BETWEEN 1 AND 7
            THEN '1–7 Days'
        WHEN JULIANDAY(AppointmentDay) - JULIANDAY(ScheduledDay) BETWEEN 8 AND 30
            THEN '8–30 Days'
        ELSE '30+ Days'
    END AS wait_bucket,
    COUNT(*) AS total_appointments,
    ROUND(
        100.0 * SUM(CASE WHEN No_show = 'Yes' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS no_show_rate_pct
FROM appointments
GROUP BY wait_bucket
ORDER BY no_show_rate_pct ASC;


-- ============================================================
-- QUERY 5: SMS + condition interaction
-- Which patient groups are most misserved by current outreach?
-- High SMS received + high no-show = outreach not working
-- ============================================================
WITH condition_sms AS (
    SELECT
        CASE
            WHEN Hipertension = 1 AND Diabetes = 0 AND Alcoholism = 0
                THEN 'Hypertension Only'
            WHEN Diabetes = 1 AND Hipertension = 0 AND Alcoholism = 0
                THEN 'Diabetes Only'
            WHEN Alcoholism = 1 THEN 'Alcoholism'
            WHEN Hipertension = 1 AND Diabetes = 1
                THEN 'Hypertension + Diabetes'
            WHEN Hipertension = 0 AND Diabetes = 0 AND Alcoholism = 0
                THEN 'No Condition'
            ELSE 'Other Combination'
        END AS condition_segment,
        SMS_received,
        No_show
    FROM appointments
)
SELECT
    condition_segment,
    SUM(CASE WHEN SMS_received = 1 THEN 1 ELSE 0 END) AS received_sms,
    SUM(CASE WHEN SMS_received = 1 AND No_show = 'Yes' THEN 1 ELSE 0 END) AS sms_and_no_show,
    ROUND(
        100.0 * SUM(CASE WHEN SMS_received = 1 AND No_show = 'Yes' THEN 1 ELSE 0 END) /
        NULLIF(SUM(CASE WHEN SMS_received = 1 THEN 1 ELSE 0 END), 0),
        2
    ) AS no_show_rate_despite_sms
FROM condition_sms
GROUP BY condition_segment
ORDER BY no_show_rate_despite_sms DESC;


-- ============================================================
-- QUERY 6: Age group attendance patterns
-- ============================================================
SELECT
    CASE
        WHEN Age < 18 THEN 'Under 18'
        WHEN Age BETWEEN 18 AND 34 THEN '18–34'
        WHEN Age BETWEEN 35 AND 54 THEN '35–54'
        WHEN Age BETWEEN 55 AND 74 THEN '55–74'
        ELSE '75+'
    END AS age_group,
    COUNT(*) AS total_appointments,
    ROUND(
        100.0 * SUM(CASE WHEN No_show = 'No' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS show_rate_pct,
    ROUND(AVG(SMS_received) * 100, 2) AS sms_coverage_pct
FROM appointments
GROUP BY age_group
ORDER BY show_rate_pct DESC;
