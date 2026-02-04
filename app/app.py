import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

# ------------------------------------------------------------
# Page setup
# ------------------------------------------------------------
st.set_page_config(
    page_title="Yemen Signals (2019–2021)",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parents[1]  # repo root
DATA_DIR = BASE_DIR / "data_processed"

# ------------------------------------------------------------
# Data loading
# ------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_DIR / "yemen_health_cleaned_deduped.csv")
    df["month"] = pd.to_datetime(df["month"])

    syn = pd.read_csv(DATA_DIR / "synthesis_district_signals.csv")
    pri = pd.read_csv(DATA_DIR / "synthesis_priority_districts.csv")
    gov = pd.read_csv(DATA_DIR / "synthesis_governorate_summary.csv")

    return df, syn, pri, gov

df, syn, pri, gov = load_data()

# ------------------------------------------------------------
# Sidebar filters
# ------------------------------------------------------------
st.sidebar.title("Filters")

gov_options = ["All"] + sorted(syn["governorate"].dropna().unique().tolist())
selected_gov = st.sidebar.selectbox("Governorate", gov_options, index=0)

show_priority_only = st.sidebar.checkbox("Show only priority districts (≥2 signals)", value=False)

syn_picker = syn.copy()
if selected_gov != "All":
    syn_picker = syn_picker[syn_picker["governorate"] == selected_gov]
if show_priority_only:
    syn_picker = syn_picker[syn_picker["num_signals"] >= 2]

district_options = ["All"] + sorted(syn_picker["district"].dropna().unique().tolist())
selected_district = st.sidebar.selectbox("District", district_options, index=0)

min_month = df["month"].min()
max_month = df["month"].max()
month_range = st.sidebar.slider(
    "Month range",
    value=(min_month.to_pydatetime(), max_month.to_pydatetime()),
    min_value=min_month.to_pydatetime(),
    max_value=max_month.to_pydatetime()
)

start_month = pd.to_datetime(month_range[0]).to_period("M").to_timestamp()
end_month = pd.to_datetime(month_range[1]).to_period("M").to_timestamp()

st.sidebar.caption("Signals are descriptive. Correlation is not causation.")

# ------------------------------------------------------------
# Filtered views
# ------------------------------------------------------------
syn_view = syn.copy()
if selected_gov != "All":
    syn_view = syn_view[syn_view["governorate"] == selected_gov]
if selected_district != "All":
    syn_view = syn_view[syn_view["district"] == selected_district]

df_view = df[(df["month"] >= start_month) & (df["month"] <= end_month)].copy()
if selected_gov != "All":
    df_view = df_view[df_view["governorate"] == selected_gov]
if selected_district != "All":
    df_view = df_view[df_view["district"] == selected_district]

# Coverage calc (global)
coverage = (
    df.groupby("month")["pcode_2"].nunique()
    .reset_index(name="num_districts_reporting")
)
ABSOLUTE_FLOOR = 150
coverage["low_coverage_month"] = coverage["num_districts_reporting"] < ABSOLUTE_FLOOR

# ------------------------------------------------------------
# Header
# ------------------------------------------------------------
st.title("Yemen (2019–2021): Functionality & Cholera Decision Signals")
st.write(
    "This dashboard surfaces coverage-aware decision signals from district-level reported data. "
    "It supports prioritisation and hypothesis generation, not causal inference."
)

# Coverage warning for the selected date window
low_cov_months = coverage[
    (coverage["month"] >= start_month) &
    (coverage["month"] <= end_month) &
    (coverage["low_coverage_month"])
]
if len(low_cov_months) > 0:
    st.warning(
        f"Coverage warning: {len(low_cov_months)} month(s) in the selected range fall below "
        f"{ABSOLUTE_FLOOR} reporting districts. Interpret trends cautiously."
    )

# Quick selection summary (only if a district is selected)
if selected_district != "All" and len(syn_view) > 0:
    row = syn_view.iloc[0]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Governorate", row["governorate"])
    c2.metric("District", row["district"])
    c3.metric("Signals (count)", int(row["num_signals"]))
    c4.metric("Priority (≥2)", "Yes" if int(row["num_signals"]) >= 2 else "No")

    st.write(
        f"- Low functionality signal: **{'Yes' if bool(row['low_functionality_signal']) else 'No'}**\n"
        f"- Sustained cholera pressure: **{'Yes' if bool(row['sustained_cholera_pressure']) else 'No'}**\n"
        f"- Strong negative co-movement: **{'Yes' if bool(row['strong_negative_signal']) else 'No'}**"
    )
else:
    st.info("Tip: select a specific district to see focused evidence charts for Decisions 1–3.")

# ------------------------------------------------------------
# Tabs
# ------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview & Coverage",
    "Decision 1: Functionality",
    "Decision 2: Cholera pressure",
    "Decision 3: Co-movement",
    "Synthesis & Methods"
])

# ------------------------------------------------------------
# Tab 1
# ------------------------------------------------------------
with tab1:
    st.subheader("Governorate summary (districts with ≥2 signals)")
    st.dataframe(gov, use_container_width=True)

    st.subheader("Reporting coverage over time")
    cov_plot = coverage[(coverage["month"] >= start_month) & (coverage["month"] <= end_month)].copy()
    st.line_chart(cov_plot.set_index("month")["num_districts_reporting"])
    st.caption(
        "Coverage = number of districts reporting any data in a month. "
        "A sharp decline can create misleading trends if not handled."
    )

# ------------------------------------------------------------
# Tab 2: Decision 1
# ------------------------------------------------------------
with tab2:
    st.subheader("Decision 1: Persistently low reported health facility functionality")

    st.dataframe(
        syn_view[[
            "pcode_2", "district", "governorate",
            "low_functionality_signal", "num_signals"
        ]],
        use_container_width=True
    )

    ts = df_view[["month", "percent_functioning_health_centres"]].dropna()
    if ts.empty:
        st.info("No functionality data available for this selection in the chosen date range.")
    else:
        ts = ts.groupby("month", as_index=True)["percent_functioning_health_centres"].median()
        st.line_chart(ts)

    st.caption(
        "Interpretation: highlights districts where reported functionality stays consistently low over time "
        "(robust summaries; minimum reporting thresholds)."
    )

# ------------------------------------------------------------
# Tab 3: Decision 2
# ------------------------------------------------------------
with tab3:
    st.subheader("Decision 2: Sustained cholera pressure (suspected cases)")

    st.dataframe(
        syn_view[[
            "pcode_2", "district", "governorate",
            "sustained_cholera_pressure", "num_signals"
        ]],
        use_container_width=True
    )

    ts = df_view[["month", "num_suspected_cases_cholera"]].dropna()
    if ts.empty:
        st.info("No suspected cholera case data available for this selection in the chosen date range.")
    else:
        ts = ts.groupby("month", as_index=True)["num_suspected_cases_cholera"].sum()
        st.line_chart(ts)

    st.caption(
        "Interpretation: sustained pressure emphasises persistence over time rather than one-off spikes."
    )

# ------------------------------------------------------------
# Tab 4: Decision 3
# ------------------------------------------------------------
with tab4:
    st.subheader("Decision 3: Co-movement scan (functionality vs suspected cholera)")

    st.dataframe(
        syn_view[[
            "pcode_2", "district", "governorate",
            "strong_negative_signal", "num_signals"
        ]],
        use_container_width=True
    )

    paired = df_view[["month", "percent_functioning_health_centres", "num_suspected_cases_cholera"]].copy()
    paired = paired.dropna(subset=["percent_functioning_health_centres", "num_suspected_cases_cholera"])

    if len(paired) < 3:
        st.info("Not enough paired data points to display co-movement for this selection.")
    else:
        paired = paired.groupby("month", as_index=False).agg(
            functioning=("percent_functioning_health_centres", "median"),
            suspected_cases=("num_suspected_cases_cholera", "sum"),
        )

        corr = np.corrcoef(paired["functioning"], paired["suspected_cases"])[0, 1]

        # Correlation as descriptive evidence (can be NaN if no variation)
        corr = np.corrcoef(paired["functioning"], paired["suspected_cases"])[0, 1]
        if np.isnan(corr):
            st.metric("Within-district correlation", "NA")
            st.caption("Correlation is NA when one series has no variation in the selected window.")
        else:
            st.metric("Within-district correlation", f"{corr:.2f}")

        st.caption(
            "Interpretation: co-movement is descriptive. A strong negative signal means lower reported functionality "
            "tends to coincide with higher suspected cases within a district. Not causal proof."
        )

# ------------------------------------------------------------
# Tab 5: Synthesis
# ------------------------------------------------------------
with tab5:
    st.subheader("Synthesis: where multiple signals converge")

    only_2plus = st.checkbox("Show only districts with ≥2 signals", value=True)
    syn_show = syn.copy()
    if only_2plus:
        syn_show = syn_show[syn_show["num_signals"] >= 2]
    if selected_gov != "All":
        syn_show = syn_show[syn_show["governorate"] == selected_gov]
    if selected_district != "All":
        syn_show = syn_show[syn_show["district"] == selected_district]

    syn_show = syn_show[[
        "pcode_2", "district", "governorate",
        "num_signals",
        "low_functionality_signal",
        "sustained_cholera_pressure",
        "strong_negative_signal"
    ]].sort_values(["num_signals", "governorate", "district"], ascending=[False, True, True])

    st.dataframe(syn_show, use_container_width=True)

    st.markdown("---")
    st.subheader("Methods & limitations")
    st.markdown(
        """
- Signals are **descriptive** and designed for prioritisation/hypothesis generation.
- Reporting coverage declines sharply in 2021; low-coverage periods are flagged to reduce misinterpretation.
- Duplicate district–month records were resolved using documented rules (max for counts; median for percentages).
- Suspected cholera cases reflect surveillance reporting and may be influenced by access and reporting practices.
- Co-movement is a temporal alignment scan and does **not** imply causality.
        """.strip()
    )
