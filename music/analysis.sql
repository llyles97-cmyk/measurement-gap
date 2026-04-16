-- ============================================================
-- Measurement Gap: Consumer Streaming
-- Divergence Score: Engagement Share vs. Retention Share by Genre
-- Dataset: Netflix Userbase Insights Dataset (Kaggle)
-- Tool: SQLite
-- ============================================================


-- ============================================================
-- SCHEMA REFERENCE
-- ============================================================
-- user_id            TEXT    Unique user identifier
-- subscription_type  TEXT    Basic / Standard / Premium
-- watch_hours        REAL    Total hours watched
-- content_genre      TEXT    Primary content genre
-- avg_session_dur    REAL    Average session duration in minutes
-- account_status     TEXT    Active / Churned
-- device_type        TEXT    Smart TV / Mobile / Desktop / Tablet
-- ============================================================


-- ============================================================
-- QUERY 1: Baseline — Total users, engagement, and churn by genre
-- ============================================================
SELECT
    content_genre,
    COUNT(*) AS total_users,
    ROUND(AVG(watch_hours), 2) AS avg_watch_hours,
    ROUND(AVG(avg_session_dur), 2) AS avg_session_minutes,
    SUM(CASE WHEN account_status = 'Churned' THEN 1 ELSE 0 END) AS churned_users,
    SUM(CASE WHEN account_status = 'Active' THEN 1 ELSE 0 END) AS active_users,
    ROUND(
        100.0 * SUM(CASE WHEN account_status = 'Churned' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS churn_rate_pct
FROM netflix_users
GROUP BY content_genre
ORDER BY avg_watch_hours DESC;


-- ============================================================
-- QUERY 2: Engagement share vs. retention share by genre
-- This is the core divergence calculation
-- ============================================================
WITH genre_totals AS (
    SELECT
        content_genre,
        COUNT(*) AS total_users,
        SUM(watch_hours) AS total_watch_hours,
        SUM(CASE WHEN account_status = 'Active' THEN 1 ELSE 0 END) AS retained_users
    FROM netflix_users
    GROUP BY content_genre
),
platform_totals AS (
    SELECT
        SUM(total_watch_hours) AS platform_watch_hours,
        SUM(retained_users) AS platform_retained_users
    FROM genre_totals
)
SELECT
    g.content_genre,
    g.total_users,
    ROUND(100.0 * g.total_watch_hours / p.platform_watch_hours, 2) AS engagement_share_pct,
    ROUND(100.0 * g.retained_users / p.platform_retained_users, 2) AS retention_share_pct,
    ROUND(
        (100.0 * g.total_watch_hours / p.platform_watch_hours) -
        (100.0 * g.retained_users / p.platform_retained_users),
        2
    ) AS divergence_score
FROM genre_totals g
CROSS JOIN platform_totals p
ORDER BY divergence_score DESC;


-- ============================================================
-- QUERY 3: High-engagement, high-churn genres
-- The core finding: which genres drive watch time but not retention?
-- ============================================================
WITH genre_metrics AS (
    SELECT
        content_genre,
        ROUND(AVG(watch_hours), 2) AS avg_watch_hours,
        ROUND(
            100.0 * SUM(CASE WHEN account_status = 'Churned' THEN 1 ELSE 0 END) / COUNT(*),
            2
        ) AS churn_rate_pct,
        COUNT(*) AS total_users
    FROM netflix_users
    GROUP BY content_genre
),
platform_avg AS (
    SELECT
        ROUND(AVG(avg_watch_hours), 2) AS platform_avg_watch,
        ROUND(AVG(churn_rate_pct), 2) AS platform_avg_churn
    FROM genre_metrics
)
SELECT
    g.content_genre,
    g.avg_watch_hours,
    g.churn_rate_pct,
    g.total_users,
    CASE
        WHEN g.avg_watch_hours > p.platform_avg_watch
         AND g.churn_rate_pct > p.platform_avg_churn
        THEN 'High Engagement / High Churn — Measurement Gap'
        WHEN g.avg_watch_hours > p.platform_avg_watch
         AND g.churn_rate_pct <= p.platform_avg_churn
        THEN 'High Engagement / Low Churn — Aligned'
        WHEN g.avg_watch_hours <= p.platform_avg_watch
         AND g.churn_rate_pct > p.platform_avg_churn
        THEN 'Low Engagement / High Churn — At Risk'
        ELSE 'Low Engagement / Low Churn — Passive Retained'
    END AS segment_classification
FROM genre_metrics g
CROSS JOIN platform_avg p
ORDER BY g.churn_rate_pct DESC;


-- ============================================================
-- QUERY 4: Session duration vs. churn — does depth of engagement predict retention?
-- ============================================================
SELECT
    CASE
        WHEN avg_session_dur < 20 THEN 'Short Session (<20 min)'
        WHEN avg_session_dur BETWEEN 20 AND 40 THEN 'Medium Session (20-40 min)'
        WHEN avg_session_dur BETWEEN 40 AND 60 THEN 'Long Session (40-60 min)'
        ELSE 'Extended Session (60+ min)'
    END AS session_bucket,
    COUNT(*) AS total_users,
    ROUND(AVG(watch_hours), 2) AS avg_watch_hours,
    ROUND(
        100.0 * SUM(CASE WHEN account_status = 'Churned' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS churn_rate_pct
FROM netflix_users
GROUP BY session_bucket
ORDER BY churn_rate_pct ASC;


-- ============================================================
-- QUERY 5: Subscription tier divergence
-- Does engagement-retention alignment vary by tier?
-- ============================================================
WITH tier_genre AS (
    SELECT
        subscription_type,
        content_genre,
        COUNT(*) AS users,
        ROUND(AVG(watch_hours), 2) AS avg_watch_hours,
        ROUND(
            100.0 * SUM(CASE WHEN account_status = 'Churned' THEN 1 ELSE 0 END) / COUNT(*),
            2
        ) AS churn_rate_pct
    FROM netflix_users
    GROUP BY subscription_type, content_genre
)
SELECT
    subscription_type,
    content_genre,
    users,
    avg_watch_hours,
    churn_rate_pct
FROM tier_genre
ORDER BY subscription_type, churn_rate_pct DESC;
