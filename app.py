"""
app.py — Kitesurf School Analytics Dashboard
Run: streamlit run app.py
"""
import streamlit as st
import sqlite3, pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Kitesurf School Analytics",
    page_icon="🪁",
    layout="wide",
)

# ── Load data ────────────────────────────────────────────────────
@st.cache_resource
def get_conn():
    return sqlite3.connect("watersports.db", check_same_thread=False)

@st.cache_data(ttl=60)
def load():
    df = pd.read_sql("SELECT * FROM bookings", get_conn())
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month
    MONTH_NAMES = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
                   7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
    df["month_name"] = df["month"].map(MONTH_NAMES)
    return df

df  = load()
rev = df[df["status"] == "completed"]   # only completed bookings for revenue

# ── Header ───────────────────────────────────────────────────────
st.title("🪁 Kitesurf School Analytics")
st.caption("Data, Operations & Performance Insights")

# ── Sidebar filters ──────────────────────────────────────────────
with st.sidebar:
    st.header("Filters")
    sports_sel = st.multiselect("Sport", df["sport"].unique(),
                                default=list(df["sport"].unique()))
    inst_sel   = st.multiselect("Instructor", df["instructor"].unique(),
                                default=list(df["instructor"].unique()))
    status_sel = st.multiselect("Status", df["status"].unique(),
                                default=list(df["status"].unique()))

mask = (
    df["sport"].isin(sports_sel) &
    df["instructor"].isin(inst_sel) &
    df["status"].isin(status_sel)
)
filt     = df[mask]
filt_rev = filt[filt["status"] == "completed"]

# ── Tabs ─────────────────────────────────────────────────────────
t1, t2, t3, t4, t5 = st.tabs([
    "📊 Overview",
    "📅 Seasonality",
    "👨‍🏫 Instructors",
    "🏄 Equipment",
    "🗄️ SQL Explorer",
])

# ════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ════════════════════════════════════════════════════════════════
with t1:
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total bookings",  len(filt))
    c2.metric("Completed",       len(filt_rev))
    c3.metric("Total revenue",   f"R$ {filt_rev['price'].sum():,.0f}")
    c4.metric("Total profit",    f"R$ {filt_rev['profit'].sum():,.0f}")
    c5.metric("Avg price/session", f"R$ {filt_rev['price'].mean():,.0f}" if len(filt_rev) else "—")
    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Revenue by sport")
        fig = px.pie(filt_rev, values="price", names="sport",
                     color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.subheader("Bookings by status")
        status_counts = filt["status"].value_counts().reset_index()
        status_counts.columns = ["status", "count"]
        fig2 = px.bar(status_counts, x="status", y="count",
                      color="status",
                      color_discrete_map={
                          "completed":"#1D9E75","cancelled":"#D85A30","no_show":"#888780"
                      })
        fig2.update_layout(showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Revenue by spot")
    spot_rev = filt_rev.groupby("spot")["price"].sum().reset_index().sort_values("price", ascending=True)
    fig3 = px.bar(spot_rev, x="price", y="spot", orientation="h",
                  labels={"price":"Total revenue (R$)","spot":""},
                  color="price", color_continuous_scale="teal")
    fig3.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig3, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# TAB 2 — SEASONALITY
# ════════════════════════════════════════════════════════════════
with t2:
    MONTH_ORDER = ["Jan","Feb","Mar","Apr","May","Jun",
                   "Jul","Aug","Sep","Oct","Nov","Dec"]

    st.subheader("Monthly revenue by sport")
    monthly = (filt_rev.groupby(["month_name","sport"])["price"]
               .sum().reset_index())
    monthly["month_name"] = pd.Categorical(monthly["month_name"],
                                           categories=MONTH_ORDER, ordered=True)
    monthly = monthly.sort_values("month_name")
    fig = px.bar(monthly, x="month_name", y="price", color="sport",
                 barmode="stack",
                 labels={"price":"Revenue (R$)","month_name":"Month"},
                 color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Avg price by month")
        avg_m = (filt_rev.groupby("month_name")["price"]
                 .mean().reset_index())
        avg_m["month_name"] = pd.Categorical(avg_m["month_name"],
                                             categories=MONTH_ORDER, ordered=True)
        avg_m = avg_m.sort_values("month_name")
        fig2 = px.line(avg_m, x="month_name", y="price", markers=True,
                       labels={"price":"Avg price (R$)","month_name":""})
        st.plotly_chart(fig2, use_container_width=True)
    with c2:
        st.subheader("Bookings by month")
        cnt_m = (filt.groupby("month_name")
                 .size().reset_index(name="bookings"))
        cnt_m["month_name"] = pd.Categorical(cnt_m["month_name"],
                                             categories=MONTH_ORDER, ordered=True)
        cnt_m = cnt_m.sort_values("month_name")
        fig3 = px.bar(cnt_m, x="month_name", y="bookings",
                      labels={"month_name":"","bookings":"Bookings"},
                      color="bookings", color_continuous_scale="tealgrn")
        fig3.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Avg profit vs session duration")
    dur_profit = (filt_rev.groupby("duration_hours")["profit"]
                  .mean().reset_index())
    fig4 = px.bar(dur_profit, x="duration_hours", y="profit",
                  labels={"duration_hours":"Duration (hours)","profit":"Avg profit (R$)"},
                  color="profit", color_continuous_scale="RdYlGn")
    fig4.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig4, use_container_width=True)
    st.caption("Shorter sessions tend to be more profitable per session — longer ones require pricing review.")

# ════════════════════════════════════════════════════════════════
# TAB 3 — INSTRUCTORS
# ════════════════════════════════════════════════════════════════
with t3:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Total profit by instructor")
        inst_profit = (filt_rev.groupby("instructor")["profit"]
                       .sum().reset_index().sort_values("profit", ascending=True))
        fig = px.bar(inst_profit, x="profit", y="instructor", orientation="h",
                     labels={"profit":"Total profit (R$)","instructor":""},
                     color="profit", color_continuous_scale="teal")
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.subheader("Avg profit per session")
        inst_avg = (filt_rev.groupby("instructor")["profit"]
                    .mean().reset_index().sort_values("profit", ascending=True))
        fig2 = px.bar(inst_avg, x="profit", y="instructor", orientation="h",
                      labels={"profit":"Avg profit (R$)","instructor":""},
                      color="profit", color_continuous_scale="bluyl")
        fig2.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Monthly profit by instructor")
    MONTH_ORDER = ["Jan","Feb","Mar","Apr","May","Jun",
                   "Jul","Aug","Sep","Oct","Nov","Dec"]
    mp = (filt_rev.groupby(["month_name","instructor"])["profit"]
          .sum().reset_index())
    mp["month_name"] = pd.Categorical(mp["month_name"],
                                      categories=MONTH_ORDER, ordered=True)
    mp = mp.sort_values("month_name")
    fig3 = px.line(mp, x="month_name", y="profit", color="instructor",
                   markers=True,
                   labels={"profit":"Profit (R$)","month_name":""},
                   color_discrete_sequence=px.colors.qualitative.Set1)
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Instructor breakdown table")
    tbl = filt_rev.groupby("instructor").agg(
        sessions      = ("id","count"),
        total_revenue = ("price","sum"),
        total_profit  = ("profit","sum"),
        avg_price     = ("price","mean"),
        avg_profit    = ("profit","mean"),
        avg_duration  = ("duration_hours","mean"),
    ).round(2).sort_values("total_profit", ascending=False)
    st.dataframe(tbl, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# TAB 4 — EQUIPMENT
# ════════════════════════════════════════════════════════════════
with t4:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Equipment usage count")
        eq_use = filt["equipment"].value_counts().reset_index()
        eq_use.columns = ["equipment","count"]
        fig = px.bar(eq_use, x="count", y="equipment", orientation="h",
                     color="count", color_continuous_scale="teal",
                     labels={"count":"Times used","equipment":""})
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.subheader("Revenue by equipment")
        eq_rev = (filt_rev.groupby("equipment")["price"]
                  .sum().reset_index().sort_values("price"))
        fig2 = px.bar(eq_rev, x="price", y="equipment", orientation="h",
                      color="price", color_continuous_scale="bluyl",
                      labels={"price":"Total revenue (R$)","equipment":""})
        fig2.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Revenue per hour by sport")
    rph = (filt_rev.groupby("sport")["revenue_per_hour"]
           .mean().reset_index().sort_values("revenue_per_hour", ascending=False))
    fig3 = px.bar(rph, x="sport", y="revenue_per_hour",
                  labels={"revenue_per_hour":"Avg revenue/hour (R$)","sport":""},
                  color="sport",
                  color_discrete_sequence=px.colors.qualitative.Set2)
    fig3.update_layout(showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# TAB 5 — SQL EXPLORER
# ════════════════════════════════════════════════════════════════
with t5:
    st.subheader("Run SQL queries directly")
    st.caption("Query the watersports.db database. Table: `bookings`")

    PRESETS = {
        "Revenue by instructor":
            "SELECT instructor, COUNT(*) AS sessions,\n"
            "       SUM(price) AS total_revenue,\n"
            "       ROUND(AVG(price),2) AS avg_price\n"
            "FROM bookings\n"
            "WHERE status = 'completed'\n"
            "GROUP BY instructor\n"
            "ORDER BY total_revenue DESC",
        "Monthly revenue":
            "SELECT strftime('%m', date) AS month,\n"
            "       SUM(price) AS total_revenue\n"
            "FROM bookings\n"
            "WHERE status = 'completed'\n"
            "GROUP BY month ORDER BY month",
        "Profit by duration":
            "SELECT duration_hours,\n"
            "       ROUND(AVG(profit),2) AS avg_profit\n"
            "FROM bookings\n"
            "WHERE status = 'completed'\n"
            "GROUP BY duration_hours\n"
            "ORDER BY duration_hours",
        "Equipment usage + revenue":
            "SELECT equipment,\n"
            "       COUNT(*) AS uses,\n"
            "       SUM(price) AS total_revenue\n"
            "FROM bookings\n"
            "WHERE status = 'completed'\n"
            "GROUP BY equipment\n"
            "ORDER BY uses DESC",
        "Custom query": "",
    }
    preset = st.selectbox("Preset queries", list(PRESETS))
    query  = st.text_area("SQL", value=PRESETS[preset], height=140)

    if st.button("Run query →"):
        try:
            result = pd.read_sql(query, get_conn())
            st.dataframe(result, use_container_width=True)
            st.caption(f"{len(result)} rows returned")
        except Exception as e:
            st.error(f"SQL error: {e}")