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
todo("insight for the alerts-over-time chart (from Member 2)")

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
todo("insight for the activity-over-time chart (from Member 2)")
figure("04_direction_type", "Transaction types and directions")
todo("insight: which types are more frequent for escalated alerts (from Member 2)")
figure("05_amount_distribution", "Distribution of miqdor_indeksi")
todo("insight about transaction sizes (from Member 2)")

# ---------- 5. Pre-alert behaviour ----------
st.markdown(
    '<div class="section-label">05 — PRE-ALERT BEHAVIOUR</div>',
    unsafe_allow_html=True,
)
st.header("Transaction Activity Before an Alert", anchor="behavior")
figure("06_activity_before_signal", "Activity during the 90 days before the alert")
todo("insight: how activity changes before escalated vs dismissed alerts (from Member 2)")
figure("07_class_comparison", "Escalated vs dismissed alerts")
todo("insight: which features differ most between the classes (from Member 2)")
figure("08_hour_weekday", "Hour of day and day of week")
todo("insight about time of day / weekday, or delete this block if the data has no time of day (from Member 2)")

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
    todo("1–2 sentences: which feature groups dominate the top-15 and how that matches the EDA (Member 1 reviews)")
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
todo("add 2–3 bullet points with the team's most important EDA findings (from Member 2's key findings)")