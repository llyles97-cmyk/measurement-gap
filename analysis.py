"""
Measurement Gap: Consumer Streaming
Divergence Score — Engagement Share vs. Retention Share by Genre
Dataset: Netflix Customer Churn and Engagement Dataset (Kaggle)
Real columns: Genre Preference, Daily Watch Time (Hours),
              Churn Status (Yes/No), Subscription Plan, Engagement Rate (1-10)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# LOAD DATA
# ============================================================
df = pd.read_excel('/mnt/user-data/uploads/netflix_userbase_csv_.xlsx')

df = df.rename(columns={
    'Genre Preference':                   'content_genre',
    'Daily Watch Time (Hours)':           'watch_hours',
    'Churn Status (Yes/No)':              'churn_status',
    'Subscription Plan':                  'subscription_type',
    'Engagement Rate (1-10)':             'engagement_rate',
    'Customer Satisfaction Score (1-10)': 'satisfaction_score',
    'Support Queries Logged':             'support_queries',
    'Customer ID':                        'user_id',
})
df['account_status'] = df['churn_status'].map({'Yes': 'Churned', 'No': 'Active'})

print(f"Dataset loaded: {len(df):,} users | {df['content_genre'].nunique()} genres")
print(f"Overall churn rate: {(df['account_status']=='Churned').mean()*100:.1f}%")
print(f"Avg daily watch hours: {df['watch_hours'].mean():.2f}")

# ============================================================
# CORE DIVERGENCE CALCULATION
# ============================================================
genre_totals = df.groupby('content_genre').agg(
    total_users    = ('user_id', 'count'),
    total_watch    = ('watch_hours', 'sum'),
    retained_users = ('account_status', lambda x: (x=='Active').sum()),
    churned_users  = ('account_status', lambda x: (x=='Churned').sum()),
    avg_watch      = ('watch_hours', 'mean'),
    avg_engagement = ('engagement_rate', 'mean'),
).reset_index()

platform_watch    = genre_totals['total_watch'].sum()
platform_retained = genre_totals['retained_users'].sum()

genre_totals['engagement_share_pct'] = (genre_totals['total_watch'] / platform_watch * 100).round(2)
genre_totals['retention_share_pct']  = (genre_totals['retained_users'] / platform_retained * 100).round(2)
genre_totals['divergence_score']     = (genre_totals['engagement_share_pct'] - genre_totals['retention_share_pct']).round(2)
genre_totals['churn_rate_pct']       = (genre_totals['churned_users'] / genre_totals['total_users'] * 100).round(1)
genre_totals = genre_totals.sort_values('divergence_score', ascending=False)

print("\n" + "="*72)
print("DIVERGENCE SCORE: ENGAGEMENT SHARE vs. RETENTION SHARE BY GENRE")
print("="*72)
print(genre_totals[['content_genre','engagement_share_pct','retention_share_pct','divergence_score','churn_rate_pct']].to_string(index=False))

# ============================================================
# QUADRANT CLASSIFICATION
# ============================================================
pavg_watch = genre_totals['avg_watch'].mean()
pavg_churn = genre_totals['churn_rate_pct'].mean()

def classify(row):
    hi_w = row['avg_watch'] > pavg_watch
    hi_c = row['churn_rate_pct'] > pavg_churn
    if hi_w and hi_c:     return 'High Engagement / High Churn'
    if hi_w and not hi_c: return 'High Engagement / Low Churn'
    if not hi_w and hi_c: return 'Low Engagement / High Churn'
    return 'Low Engagement / Low Churn'

genre_totals['classification'] = genre_totals.apply(classify, axis=1)
print("\n" + "="*72)
print("GENRE CLASSIFICATION")
print("="*72)
print(genre_totals[['content_genre','avg_watch','churn_rate_pct','classification']].to_string(index=False))

# ============================================================
# VIZ 1: Divergence Score Bar
# ============================================================
fig, ax = plt.subplots(figsize=(11,6))
fig.patch.set_facecolor('#0d1117')
ax.set_facecolor('#0d1117')

colors = ['#ef4444' if x > 0 else '#22d3ee' for x in genre_totals['divergence_score']]
bars = ax.barh(genre_totals['content_genre'], genre_totals['divergence_score'],
               color=colors, edgecolor='none', height=0.55)
ax.axvline(0, color='white', linewidth=0.8, linestyle='--', alpha=0.4)

for bar, val in zip(bars, genre_totals['divergence_score']):
    offset = 0.03 if val >= 0 else -0.03
    ha = 'left' if val >= 0 else 'right'
    ax.text(val+offset, bar.get_y()+bar.get_height()/2,
            f'{val:+.2f}', va='center', ha=ha, color='white', fontsize=9, fontweight='bold')

ax.set_xlabel('Divergence Score  (Engagement Share % − Retention Share %)', color='#94a3b8', fontsize=10)
ax.set_title('Consumer Streaming: Where Engagement and Retention Diverge\nby Content Genre',
             color='white', fontsize=13, fontweight='bold', pad=15)
ax.tick_params(colors='#94a3b8', labelsize=10)
for spine in ax.spines.values(): spine.set_visible(False)
note = 'Positive → over-indexed in watch time vs. subscriber retention     Negative → under-indexed in watch time vs. subscriber retention'
fig.text(0.12, 0.01, note, color='#64748b', fontsize=7.5)

plt.tight_layout(rect=[0,0.06,1,1])
plt.savefig('/home/claude/measurement-gap/visuals/streaming_divergence_score.png',
            dpi=150, bbox_inches='tight', facecolor='#0d1117')
plt.close()
print("\nSaved: streaming_divergence_score.png")

# ============================================================
# VIZ 2: Quadrant Scatter
# ============================================================
fig, ax = plt.subplots(figsize=(10,7))
fig.patch.set_facecolor('#0d1117')
ax.set_facecolor('#0d1117')

quad_colors = {
    'High Engagement / High Churn': '#ef4444',
    'High Engagement / Low Churn':  '#22d3ee',
    'Low Engagement / High Churn':  '#f59e0b',
    'Low Engagement / Low Churn':   '#64748b',
}

for _, row in genre_totals.iterrows():
    color = quad_colors[row['classification']]
    ax.scatter(row['avg_watch'], row['churn_rate_pct'],
               color=color, s=200, zorder=5, edgecolors='white', linewidths=0.6)
    ax.annotate(row['content_genre'], (row['avg_watch'], row['churn_rate_pct']),
                textcoords='offset points', xytext=(9,4), color='white', fontsize=10)

ax.axvline(pavg_watch, color='white', linewidth=0.6, linestyle='--', alpha=0.25)
ax.axhline(pavg_churn, color='white', linewidth=0.6, linestyle='--', alpha=0.25)
ax.set_xlabel('Avg Daily Watch Hours per User', color='#94a3b8', fontsize=11)
ax.set_ylabel('Churn Rate (%)', color='#94a3b8', fontsize=11)
ax.set_title('Engagement vs. Retention: The Genre Quadrant Map',
             color='white', fontsize=13, fontweight='bold', pad=15)
ax.tick_params(colors='#94a3b8')
for spine in ax.spines.values(): spine.set_color('#1e293b')

legend_elements = [mpatches.Patch(facecolor=c, label=l) for l,c in quad_colors.items()]
ax.legend(handles=legend_elements, loc='upper left',
          facecolor='#1e293b', edgecolor='none', labelcolor='white', fontsize=9)

plt.tight_layout()
plt.savefig('/home/claude/measurement-gap/visuals/streaming_engagement_churn_quadrant.png',
            dpi=150, bbox_inches='tight', facecolor='#0d1117')
plt.close()
print("Saved: streaming_engagement_churn_quadrant.png")

# ============================================================
# VIZ 3: Side-by-side share comparison
# ============================================================
seg = genre_totals.sort_values('engagement_share_pct', ascending=True)
fig, ax = plt.subplots(figsize=(12,6))
fig.patch.set_facecolor('#0d1117')
ax.set_facecolor('#0d1117')

x = np.arange(len(seg))
w = 0.35
ax.barh(x-w/2, seg['engagement_share_pct'], w, label='Engagement Share (Watch Time)', color='#f59e0b', alpha=0.85)
ax.barh(x+w/2, seg['retention_share_pct'],  w, label='Retention Share (Active Subscribers)', color='#22d3ee', alpha=0.85)

ax.set_yticks(x)
ax.set_yticklabels(seg['content_genre'], color='#94a3b8', fontsize=10)
ax.set_xlabel('Share of Platform Total (%)', color='#94a3b8', fontsize=11)
ax.set_title('Watch Time Share vs. Subscriber Retention Share by Genre',
             color='white', fontsize=13, fontweight='bold', pad=15)
ax.tick_params(colors='#94a3b8')
ax.legend(facecolor='#1e293b', edgecolor='none', labelcolor='white', fontsize=9)
for spine in ax.spines.values(): spine.set_color('#1e293b')

plt.tight_layout()
plt.savefig('/home/claude/measurement-gap/visuals/streaming_share_comparison.png',
            dpi=150, bbox_inches='tight', facecolor='#0d1117')
plt.close()
print("Saved: streaming_share_comparison.png")
print("\nStreaming analysis complete.")
