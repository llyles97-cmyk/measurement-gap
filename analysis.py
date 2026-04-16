"""
Measurement Gap: Healthcare
Divergence Score — Outreach Share vs. Appointment Kept Share
Dataset: Medical Appointment No-Shows (Kaggle — joniarroba)
110,527 appointments, Brazil public hospitals, 2015-2016
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
df = pd.read_csv('/mnt/user-data/uploads/noshowappointments-kagglev2-may-2016_csv.csv')
df = df.rename(columns={'No-show': 'No_show'})

print(f"Dataset loaded: {len(df):,} appointments")
print(f"Overall no-show rate: {(df['No_show']=='Yes').mean()*100:.1f}%")
print(f"SMS coverage: {df['SMS_received'].mean()*100:.1f}% of appointments")

# ============================================================
# BUILD CONDITION SEGMENTS
# ============================================================
def segment(row):
    h, d, a = row['Hipertension'], row['Diabetes'], row['Alcoholism']
    if a == 1:                          return 'Alcoholism'
    if h == 1 and d == 1:               return 'Hypertension + Diabetes'
    if h == 1 and d == 0:               return 'Hypertension Only'
    if d == 1 and h == 0:               return 'Diabetes Only'
    return 'No Condition'

df['condition_segment'] = df.apply(segment, axis=1)

# ============================================================
# CORE DIVERGENCE CALCULATION
# Outreach share  = segment's share of total SMS reminders sent
# Kept share      = segment's share of appointments actually attended
# ============================================================
seg = df.groupby('condition_segment').agg(
    total_appointments = ('No_show', 'count'),
    sms_sent           = ('SMS_received', 'sum'),
    kept_appointments  = ('No_show', lambda x: (x=='No').sum()),
    no_show_count      = ('No_show', lambda x: (x=='Yes').sum()),
).reset_index()

total_sms  = seg['sms_sent'].sum()
total_kept = seg['kept_appointments'].sum()

seg['outreach_share_pct'] = (seg['sms_sent'] / total_sms * 100).round(2)
seg['kept_share_pct']     = (seg['kept_appointments'] / total_kept * 100).round(2)
seg['divergence_score']   = (seg['outreach_share_pct'] - seg['kept_share_pct']).round(2)
seg['no_show_rate_pct']   = (seg['no_show_count'] / seg['total_appointments'] * 100).round(1)
seg = seg.sort_values('divergence_score', ascending=False)

print("\n" + "="*70)
print("DIVERGENCE SCORE: OUTREACH SHARE vs. APPOINTMENT KEPT SHARE")
print("="*70)
print(seg[['condition_segment','outreach_share_pct','kept_share_pct',
           'divergence_score','no_show_rate_pct']].to_string(index=False))

# ============================================================
# SMS EFFECTIVENESS
# ============================================================
sms_df  = df[df['SMS_received'] == 1]
sms_eff = sms_df.groupby('condition_segment').agg(
    received_sms        = ('SMS_received', 'count'),
    no_show_despite_sms = ('No_show', lambda x: (x=='Yes').sum()),
).reset_index()
sms_eff['no_show_rate_despite_sms'] = (
    sms_eff['no_show_despite_sms'] / sms_eff['received_sms'] * 100
).round(1)

print("\n" + "="*70)
print("SMS EFFECTIVENESS: NO-SHOW RATE DESPITE RECEIVING A REMINDER")
print("="*70)
print(sms_eff.sort_values('no_show_rate_despite_sms', ascending=False).to_string(index=False))

# ============================================================
# WAIT TIME ANALYSIS
# ============================================================
df['ScheduledDay']   = pd.to_datetime(df['ScheduledDay'])
df['AppointmentDay'] = pd.to_datetime(df['AppointmentDay'])
df['wait_days']      = (df['AppointmentDay'] - df['ScheduledDay']).dt.days.clip(lower=0)

def wait_bucket(d):
    if d == 0:          return '0 — Same Day'
    if d <= 7:          return '1–7 Days'
    if d <= 30:         return '8–30 Days'
    return '30+ Days'

df['wait_bucket'] = df['wait_days'].apply(wait_bucket)
wait = df.groupby('wait_bucket').agg(
    total = ('No_show','count'),
    no_show_rate = ('No_show', lambda x: (x=='Yes').mean()*100)
).round(1).reset_index().sort_values('no_show_rate')

print("\n" + "="*70)
print("WAIT TIME vs. NO-SHOW RATE")
print("="*70)
print(wait.to_string(index=False))

# ============================================================
# VIZ 1: Divergence Score by Condition Segment
# ============================================================
fig, ax = plt.subplots(figsize=(11,6))
fig.patch.set_facecolor('#0d1117')
ax.set_facecolor('#0d1117')

colors = ['#ef4444' if x > 0 else '#22d3ee' for x in seg['divergence_score']]
bars = ax.barh(seg['condition_segment'], seg['divergence_score'],
               color=colors, edgecolor='none', height=0.5)
ax.axvline(0, color='white', linewidth=0.8, linestyle='--', alpha=0.4)

for bar, val in zip(bars, seg['divergence_score']):
    offset = 0.05 if val >= 0 else -0.05
    ha = 'left' if val >= 0 else 'right'
    ax.text(val+offset, bar.get_y()+bar.get_height()/2,
            f'{val:+.2f}', va='center', ha=ha, color='white', fontsize=9, fontweight='bold')

ax.set_xlabel('Divergence Score  (Outreach Share % − Appointment Kept Share %)', color='#94a3b8', fontsize=10)
ax.set_title('Healthcare: Where Outreach and Attendance Diverge\nby Patient Condition Segment',
             color='white', fontsize=13, fontweight='bold', pad=15)
ax.tick_params(colors='#94a3b8', labelsize=10)
for spine in ax.spines.values(): spine.set_visible(False)
note = 'Positive → condition group receives more outreach than its share of kept appointments     Negative → keeps more appointments than its share of outreach'
fig.text(0.12, 0.01, note, color='#64748b', fontsize=7.5)

plt.tight_layout(rect=[0,0.06,1,1])
plt.savefig('/home/claude/measurement-gap/visuals/healthcare_divergence_score.png',
            dpi=150, bbox_inches='tight', facecolor='#0d1117')
plt.close()
print("\nSaved: healthcare_divergence_score.png")

# ============================================================
# VIZ 2: Outreach vs. Attendance Side-by-Side
# ============================================================
seg_s = seg.sort_values('outreach_share_pct', ascending=True)
fig, ax = plt.subplots(figsize=(12,6))
fig.patch.set_facecolor('#0d1117')
ax.set_facecolor('#0d1117')

x = np.arange(len(seg_s))
w = 0.35
ax.barh(x-w/2, seg_s['outreach_share_pct'], w,
        label='Outreach Share (SMS Sent)', color='#f59e0b', alpha=0.85)
ax.barh(x+w/2, seg_s['kept_share_pct'], w,
        label='Kept Share (Appointments Attended)', color='#22d3ee', alpha=0.85)

ax.set_yticks(x)
ax.set_yticklabels(seg_s['condition_segment'], color='#94a3b8', fontsize=10)
ax.set_xlabel('Share of Platform Total (%)', color='#94a3b8', fontsize=11)
ax.set_title('Outreach Distribution vs. Appointment Attendance\nby Patient Condition Segment',
             color='white', fontsize=13, fontweight='bold', pad=15)
ax.tick_params(colors='#94a3b8')
ax.legend(facecolor='#1e293b', edgecolor='none', labelcolor='white', fontsize=9)
for spine in ax.spines.values(): spine.set_color('#1e293b')

plt.tight_layout()
plt.savefig('/home/claude/measurement-gap/visuals/healthcare_outreach_vs_attendance.png',
            dpi=150, bbox_inches='tight', facecolor='#0d1117')
plt.close()
print("Saved: healthcare_outreach_vs_attendance.png")

# ============================================================
# VIZ 3: No-show rate despite SMS
# ============================================================
sms_s = sms_eff.sort_values('no_show_rate_despite_sms', ascending=True)
fig, ax = plt.subplots(figsize=(10,5))
fig.patch.set_facecolor('#0d1117')
ax.set_facecolor('#0d1117')

bars = ax.barh(sms_s['condition_segment'], sms_s['no_show_rate_despite_sms'],
               color='#ef4444', alpha=0.8, edgecolor='none', height=0.45)
for bar, val in zip(bars, sms_s['no_show_rate_despite_sms']):
    ax.text(val+0.2, bar.get_y()+bar.get_height()/2,
            f'{val:.1f}%', va='center', color='white', fontsize=9)

ax.set_xlabel('No-Show Rate Despite Receiving SMS Reminder (%)', color='#94a3b8', fontsize=10)
ax.set_title('Outreach Without Impact: No-Show Rate by Condition\n(Among Patients Who Received a Reminder)',
             color='white', fontsize=12, fontweight='bold', pad=15)
ax.tick_params(colors='#94a3b8', labelsize=10)
for spine in ax.spines.values(): spine.set_visible(False)

plt.tight_layout()
plt.savefig('/home/claude/measurement-gap/visuals/healthcare_sms_effectiveness.png',
            dpi=150, bbox_inches='tight', facecolor='#0d1117')
plt.close()
print("Saved: healthcare_sms_effectiveness.png")

# ============================================================
# VIZ 4: Wait time vs. no-show rate
# ============================================================
wait_order = ['0 — Same Day','1–7 Days','8–30 Days','30+ Days']
wait['wait_bucket'] = pd.Categorical(wait['wait_bucket'], categories=wait_order, ordered=True)
wait = wait.sort_values('wait_bucket')

fig, ax = plt.subplots(figsize=(9,5))
fig.patch.set_facecolor('#0d1117')
ax.set_facecolor('#0d1117')

bar_colors = ['#22d3ee','#a3e635','#f59e0b','#ef4444']
bars = ax.bar(wait['wait_bucket'], wait['no_show_rate'], color=bar_colors,
              edgecolor='none', width=0.5)
for bar, val in zip(bars, wait['no_show_rate']):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
            f'{val:.1f}%', ha='center', va='bottom', color='white', fontsize=10, fontweight='bold')

ax.set_ylabel('No-Show Rate (%)', color='#94a3b8', fontsize=11)
ax.set_xlabel('Days Between Scheduling and Appointment', color='#94a3b8', fontsize=11)
ax.set_title('Scheduling Lag vs. No-Show Rate\nLonger Wait = More Drop-Off',
             color='white', fontsize=12, fontweight='bold', pad=15)
ax.tick_params(colors='#94a3b8', labelsize=10)
ax.set_ylim(0, wait['no_show_rate'].max() * 1.2)
for spine in ax.spines.values(): spine.set_visible(False)

plt.tight_layout()
plt.savefig('/home/claude/measurement-gap/visuals/healthcare_wait_time.png',
            dpi=150, bbox_inches='tight', facecolor='#0d1117')
plt.close()
print("Saved: healthcare_wait_time.png")
print("\nHealthcare analysis complete.")
