import json
from pathlib import Path

import pandas as pd
import streamlit as st

from styles import inject_css

ROOT = Path(__file__).parent
IMG = ROOT / "images"
ASSETS = ROOT / "assets"

st.set_page_config(page_title="AML Alert Prioritization — EDA", page_icon="🔎", layout="wide")

inject_css()

def todo(text):
    """Placeholder. Replace the call with st.markdown("...your text...")."""
    st.warning(f"To do: {text}")


def figure(name, caption):
    path = IMG / f"{name}.png"
    if path.exists():
        st.image(str(path), caption=caption, width="stretch")
    else:
        st.info(f"Chart {name}.png has not been generated yet. Run notebooks/02_eda.ipynb.")


def load_json(name):
    p = ASSETS / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


M = load_json("metrics.json")


def num(key, fmt="{:,}", default="—"):
    v = M.get(key)
    return fmt.format(v) if v is not None else default


# ---------- Navigation ----------
with st.sidebar:
    st.markdown("### Contents")
    st.markdown(
        "- [Approach](#approach)\n- [Dataset](#data)\n- [Target](#target)\n"
        "- [Transactions](#transactions)\n- [Pre-alert behaviour](#behavior)\n"
        "- [Features and model](#features)\n- [Conclusion](#conclusion)"
    )
    st.caption("System Web Analysis Group · E86FDEB5")

# ---------- Hero ----------
st.html(
    """
    <div class="hero">

        <div class="hero-kicker">
            SYSTEM WEB ANALYSIS GROUP · E86FDEB5
        </div>

        <div class="hero-title">
            AML Alert Prioritization 🚨
        </div>

        <div class="hero-subtitle">
            Using transaction histories to identify patterns associated with
            alert escalation and estimate the probability that an alert
            requires further investigation.
        </div>

    </div>
    """
)

if M:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Training alerts", num("n_train"))
    c2.metric("Test alerts", num("n_test"))
    c3.metric("Escalation rate", num("target_rate", "{:.1%}"))
    c4.metric("Cross-validated ROC-AUC", num("oof_auc", "{:.4f}"))

# ---------- 1. Approach ----------
st.markdown(
    '<div class="section-label">01 — APPROACH</div>',
    unsafe_allow_html=True,
)

st.header("From transaction history to escalation risk", anchor="approach")

st.markdown(
    """
    Each alert comes with a history of transactions, so the core of the task is turning
    a variable-length history into a fixed set of numbers a model can use. Our pipeline:
    """
)

a1, a2, a3, a4 = st.columns(4)

with a1:
    st.markdown(
        """
        <div class="content-card">
            <div class="insight-title">01 · Data checks</div>
            <div class="insight-text">
                Date ranges, transactions after the alert date (none found), train/test similarity.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with a2:
    st.markdown(
        """
        <div class="content-card">
            <div class="insight-title">02 · Exploratory Analysis</div>
            <div class="insight-text">
                How escalated and dismissed alerts differ in volume, timing, direction, transaction type and size (the charts below).
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with a3:
    st.markdown(
        f"""
        <div class="content-card">
            <div class="insight-title">03 · Feature engineering</div>
            <div class="insight-text">
                80 features per alert, each motivated by an EDA observation or a known money-laundering pattern.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with a4:
    st.markdown(
        """
        <div class="content-card">
            <div class="insight-title">04 · Modelling</div>
            <div class="insight-text">
                LightGBM, CatBoost and XGBoost were evaluated using 5-fold stratified cross-validation and combined via rank averaging. ROC-AUC depends solely on prediction ordering, so ranking alerts correctly is the first priority.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------- 2. Dataset ----------
st.markdown(
    '<div class="section-label">02 — DATASET</div>',
    unsafe_allow_html=True,
)
st.header("Dataset overview", anchor="data")
st.markdown(
    """
| File | Contents |
|---|---|
| `train_signals.csv` | one alert per row: `signal_id`, `signal_sanasi` (alert date), `eskalatsiya` (target) |
| `train_transactions.parquet` | transaction history: timestamp, direction (kirim = incoming, chiqim = outgoing), type (karta, bank_otkazmasi, naqd, xalqaro), `miqdor_indeksi` (standardised size) |
| `test_signals.csv`, `test_transactions.parquet` | the same for the hidden test set, without the target |
"""
)
if M:
    td, sd = M.get("train_dates", ["?", "?"]), M.get("test_dates", ["?", "?"])
    st.markdown(
        f"""
- **{num('n_train')}** training alerts with **{num('n_tx_train')}** transactions, and **{num('n_test')}**
  test alerts with **{num('n_tx_test')}** transactions.
- A typical alert has about **{num('tx_per_alert_median', '{:,.0f}')}** transactions in its history (median),
  so each alert is summarised from a rich activity log.
- Alert dates: train **{td[0]} – {td[1]}**, test **{sd[0]} – {sd[1]}**. Both sets cover the same period,
  so random stratified cross-validation mirrors the hidden test well.
- No transaction occurs after its alert date, so there is no look-ahead leakage.
- **Adversarial validation:** a model trying to tell train rows from test rows scored ROC-AUC
  **{num('adversarial_auc', '{:.3f}')}** (0.5 = indistinguishable). Train and test follow the same
  distribution, so our validation score should transfer to the hidden test.
"""
    )
figure("02_signals_over_time", "Weekly alerts in train and test")
st.markdown(
    """
    The train set and test set represent the same time frame: January 1, 2025, to December 31, 2026
    (the time frames coincide exactly). This is confirmed by the adversarial validation results
    (AUC = 0.4987) — the value shows that train and test sets cannot be distinguished from each other,
    meaning random (time-agnostic) cross-validation can safely be used. The weekly escalation rate
    ranges from 6.8% to 28.4% (std ≈ 3.7 p.p.).
    """
)

# ---------- 3. Target ----------
st.markdown(
    '<div class="section-label">03 — TARGET</div>',
    unsafe_allow_html=True,
)
st.header("Target distribution", anchor="target")
figure("01_target_distribution", "Dismissed vs escalated alerts")
st.markdown(
    f"""
Only **{num('target_rate', '{:.1%}')}** of alerts are escalated, so the classes are imbalanced.
We did not resample or reweight: ROC-AUC measures how well escalated alerts are ranked above dismissed
ones and is not affected by the class ratio. Stratified folds keep the same escalation rate in every fold.
"""
)

# ---------- 4. Transactions ----------
st.markdown(
    '<div class="section-label">04 — TRANSACTIONS</div>',
    unsafe_allow_html=True,
)
st.header("Transactions: time, types, sizes", anchor="transactions")
figure("03_tx_over_time", "Transactions per month")
st.markdown(
    """
    This graph has the form of a triangle: it increases from about 19k transactions/month (July 2024)
    to its maximum value of 388k (July/October 2025) and decreases to about 23k (December 2026).
    However, this has nothing to do with customer behavior — it is caused by the structure of the
    database. Each alert consists of a transaction history of about 180 days before its signal date,
    and the signal dates themselves are spread across 2025-2026.
    """
)
figure("04_direction_type", "Transaction types and directions")
st.markdown(
    """
    The combination of transaction types is almost the same for escalated and dismissed cases:
    karta 53.8% vs 53.7%, bank_otkazmasi 39.4% vs 39.3%, naqd (cash) 6.29% vs 6.50%, xalqaro
    (international) 0.45% vs 0.47%. The difference is negligible; however, the pattern is as
    expected — the shares of naqd and xalqaro transactions are somewhat higher in escalated cases,
    which is a typical (if weak) AML signal.
    """
)
figure("05_amount_distribution", "Distribution of miqdor_indeksi")
st.markdown(
    """
    Escalated alerts show slightly lower average miqdor_indeksi (mean −0.18, median −0.29)
    compared to dismissed alerts (mean −0.12, median −0.24) — escalation is not linked with
    "larger" amounts; if anything, the opposite. There is much more variance by transaction type:
    the "largest" type is xalqaro (mean 1.99), followed by naqd (0.53) and bank_otkazmasi (0.14),
    while karta is the smallest and negative (−0.43).
    """
)

# ---------- 5. Pre-alert behaviour ----------
st.markdown(
    '<div class="section-label">05 — PRE-ALERT BEHAVIOUR</div>',
    unsafe_allow_html=True,
)
st.header("Transaction Activity Before an Alert", anchor="behavior")
figure("06_activity_before_signal", "Activity during the 90 days before the alert")
st.markdown(
    """
    Background activity far from the signal (days 85-89) is steady at ~2.9-3.1 transactions/alert/day.
    On the day before the signal there is a sharp spike of ~40-42 transactions/alert (~14x the
    background rate), slightly higher for escalated cases (41.9 vs 40.3). Activity on the signal
    day itself (day=0) is very low, but escalated cases show three times as much (0.136 vs 0.044).
    Part of this spike may be a date-grouping artifact (signal_sanasi has no timestamp, so the
    whole last calendar day falls into one bin), but the elevated activity right before the signal
    is already captured by the window features (w1/w3/w7, etc.) in final.py.
    """
)
figure("07_class_comparison", "Escalated vs dismissed alerts")
st.markdown(
    """
    For simple aggregates, the class differences are quite small: slightly more transactions
    (523.8 vs 494.0 on average), slightly higher recent (7-day) activity (47.3 vs 45.5), slightly
    higher shares of cash/international/outgoing transactions, and a slightly lower mean transaction
    value. No single feature separates the classes on its own. This is consistent with final.py,
    where the best OOF AUC on simple aggregates is only about 0.63, and advanced features
    (time-decay, pass-through patterns, type entropy) are needed to push it above 0.64.
    """
)
figure("08_hour_weekday", "Hour of day and day of week")
st.markdown(
    """
    Timestamps are not always midnight, so time-of-day is real. Activity is otherwise evenly spread
    across weekdays (14.2-14.4% per day in both groups), with no meaningful weekend effect (weekend
    transactions are 28.5% in both groups) and no difference in night-time activity (00:00-05:00,
    ~23.1-23.2% in both groups).

    🚩 Anomaly: transactions at hour 23:00 occur about three times more often (11.7% of all
    transactions) than at any other hour (~3.8% each) — clearly not a random distribution. It looks
    like a technical/data-quality artifact (e.g. records without an exact timestamp defaulting to
    end-of-day) rather than a behavioral pattern, and is flagged here as a data-quality issue for
    the team.
    """
)

# ---------- 6. Features and model ----------
st.markdown(
    '<div class="section-label">06 — FEATURES AND MODEL</div>',
    unsafe_allow_html=True,
)
st.header("Features motivated by the EDA", anchor="features")
st.markdown(
    """
| Observation | Features built from it |
|---|---|
| Alerts differ in overall activity volume and transaction size | count, sum, mean, std, min, max, median and 90th percentile of `miqdor_indeksi` |
| Escalation depends on *what kind* of money moves | counts, sums and shares by direction, by type and by direction × type (e.g. share of outgoing cash) |
| Activity often intensifies right before an alert | activity in 1 / 3 / 7 / 14 / 30 / 90-day windows and ratios such as 7-day vs 30-day activity |
| Recent behaviour matters more than old behaviour | time-decayed counts and sums (`exp(-days/τ)`, τ = 3, 14, 60 days), statistics of the last 10 transactions |
| Irregular rhythm is suspicious | days since last transaction, history length, gaps between transactions, max and std of daily counts |
| Money passing straight through an account is a classic laundering pattern | outgoing transactions within 1 / 24 / 72 h after an incoming one, pass-through share with similar amounts |
| Splitting a large sum into equal parts (structuring) | share of repeated amounts, number of unique amounts |
| Unusual recent amounts | z-score of the last week's max and mean vs the alert's own history |
"""
)
if M:
    ma = M.get("model_auc", {})
    names = {"lgb": "LightGBM (3 seeds)", "cat": "CatBoost", "xgb": "XGBoost"}
    rows = "\n".join(f"| {names.get(k, k)} | {v:.4f} |" for k, v in ma.items())
    w = ", ".join(f"{names.get(k, k)} {v:.0%}" for k, v in M.get("weights", {}).items())
    st.subheader("Model results")
    st.markdown(
        f"""
5-fold out-of-fold ROC-AUC, {num('n_features')} features:

| Model | ROC-AUC |
|---|---|
{rows}
| **Rank-averaged ensemble** | **{num('oof_auc', '{:.4f}')}** |

Ensemble weights, chosen on out-of-fold predictions: {w}.
Before training the final models we automatically compared different numbers of top features and
more or less regularised LightGBM settings, and kept the combination with the best cross-validated AUC.
"""
    )
fi_path = ASSETS / "feature_importance.csv"
if fi_path.exists():
    fi = pd.read_csv(fi_path).head(15)
    st.markdown("**Top-15 features** (share of total LightGBM gain)")
    st.bar_chart(fi.set_index("feature")["importance"], horizontal=True)
    st.markdown(
        """
        The top-15 are dominated by size statistics split by direction × type — especially the
        overall minimum transaction amount (`all_min`, ~11% of total gain) and the mean/max/sum of
        bank_otkazmasi and karta amounts by direction, with naqd-related features close behind. This
        matches the EDA: transaction size mainly differs by type rather than by outcome (see the
        `miqdor_indeksi` chart), so direction × type breakdowns of size carry more signal than the
        outcome-level differences alone. Window and time-decay features (e.g. `decay60_in_share`,
        `w90_max`) also make the top-20, reflecting the pre-alert activity spike identified earlier.
        """
    )
else:
    st.info("Feature importance will appear after running notebooks/final.ipynb.")

# ---------- 7. Conclusion ----------
st.markdown(
    '<div class="section-label">07 — CONCLUSION</div>',
    unsafe_allow_html=True,
)
st.header("Conclusion", anchor="conclusion")
st.markdown(
    f"""
- Train and test come from the same period and the same distribution (adversarial AUC ≈ 0.5, no leakage),
  so cross-validation is a reliable guide.
- The escalation signal in transaction histories is real but modest: our ensemble reaches a cross-validated
  ROC-AUC of **{num('oof_auc', '{:.4f}')}**. Specialists' decisions likely also depend on information that
  is not in the transaction log.
"""
)
st.markdown(
    """
- The target is imbalanced, with only 17.2% escalated cases, so we use stratified cross-validation and
  PR-AUC as an additional evaluation metric.
- Train and test sets cover an identical period (2025-01-01 to 2026-12-31). Adversarial validation shows
  the samples cannot be distinguished (AUC ≈ 0.50), so standard random cross-validation can safely be used.
- Simple aggregated features computed over the whole period (transaction count, type shares, average
  amount) show very little difference between escalated and dismissed alerts — the signal is weak and
  spread across many features.
- A sharp one-day spike in activity right before the signal (~14x the background rate) is the most
  informative pattern, and it is somewhat stronger for escalated alerts — this motivated the window and
  time-decay features in the model.
- Indeed, the classical AML features (the proportion of cash and international operations) are slightly
  greater for cases with escalation, but the impact is very small by itself.
- A technical anomaly has been found: 23:00 hour has 3 times more transactions than any other hour –
  this is probably the default time for those transactions for which the exact time was not specified.
- The final model (ensemble of LightGBM, CatBoost and XGBoost with 80 features) provides OOF AUC of
  0.6425; the problem is quite challenging, with the simplest features providing a random score and
  feature engineering giving the main contribution to the result.
    """
)
