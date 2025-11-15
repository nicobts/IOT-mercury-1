import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.database.connection import get_db
from src.database.models import SIMCard, UsageRecord

st.set_page_config(page_title="Overview", page_icon="📊", layout="wide")

st.title("📊 Overview")
st.markdown("Complete overview of your IoT fleet")

# Time period selector
col1, col2 = st.columns([3, 1])
with col2:
    time_period = st.selectbox(
        "Time Period",
        ["Last 7 days", "Last 30 days", "Last 90 days", "Last 180 days"]
    )

days_map = {
    "Last 7 days": 7,
    "Last 30 days": 30,
    "Last 90 days": 90,
    "Last 180 days": 180
}
days = days_map[time_period]

# Key Metrics
st.markdown("### Key Metrics")
col1, col2, col3, col4 = st.columns(4)

try:
    with get_db() as db:
        # Total SIMs
        total_sims = db.query(SIMCard).count()
        active_sims = db.query(SIMCard).filter(SIMCard.status == 'Enabled').count()
        inactive_sims = total_sims - active_sims

        # Usage data
        start_date = datetime.now() - timedelta(days=days)
        total_usage = db.query(
            db.func.sum(UsageRecord.data_volume_mb)
        ).filter(UsageRecord.date >= start_date).scalar() or 0

        # Average daily usage
        avg_daily_usage = total_usage / days if days > 0 else 0

        with col1:
            st.metric("Total SIMs", f"{total_sims:,}")
        with col2:
            st.metric("Active SIMs", f"{active_sims:,}", delta=f"{active_sims - inactive_sims:+}")
        with col3:
            st.metric(f"Total Data ({time_period})", f"{total_usage:,.1f} MB")
        with col4:
            st.metric("Avg Daily Usage", f"{avg_daily_usage:.1f} MB")

except Exception as e:
    st.error(f"Error loading metrics: {str(e)}")

st.markdown("---")

# Charts
col1, col2 = st.columns(2)

try:
    with get_db() as db:
        # SIM Status Distribution
        with col1:
            st.markdown("### SIM Status Distribution")
            status_data = db.query(
                SIMCard.status,
                db.func.count(SIMCard.id).label('count')
            ).group_by(SIMCard.status).all()

            if status_data:
                df_status = pd.DataFrame(status_data, columns=['Status', 'Count'])
                fig = px.pie(df_status, values='Count', names='Status',
                           color_discrete_sequence=px.colors.qualitative.Set3)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No SIM data available")

        # Daily Usage Trend
        with col2:
            st.markdown("### Daily Usage Trend")
            start_date = datetime.now() - timedelta(days=days)

            usage_trend = db.query(
                UsageRecord.date,
                db.func.sum(UsageRecord.data_volume_mb).label('total_mb')
            ).filter(
                UsageRecord.date >= start_date
            ).group_by(UsageRecord.date).order_by(UsageRecord.date).all()

            if usage_trend:
                df_trend = pd.DataFrame(usage_trend, columns=['Date', 'Usage (MB)'])
                fig = px.line(df_trend, x='Date', y='Usage (MB)',
                            markers=True, line_shape='spline')
                fig.update_layout(hovermode='x unified')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No usage data available for selected period")

except Exception as e:
    st.error(f"Error loading charts: {str(e)}")

st.markdown("---")

# Top Consumers
st.markdown("### Top 10 Data Consumers")

try:
    with get_db() as db:
        start_date = datetime.now() - timedelta(days=days)

        top_consumers = db.query(
            SIMCard.iccid,
            SIMCard.label,
            db.func.sum(UsageRecord.data_volume_mb).label('total_usage')
        ).join(
            UsageRecord, SIMCard.id == UsageRecord.sim_card_id
        ).filter(
            UsageRecord.date >= start_date
        ).group_by(
            SIMCard.id, SIMCard.iccid, SIMCard.label
        ).order_by(
            db.func.sum(UsageRecord.data_volume_mb).desc()
        ).limit(10).all()

        if top_consumers:
            df_top = pd.DataFrame(top_consumers, columns=['ICCID', 'Label', 'Total Usage (MB)'])
            df_top['Label'] = df_top['Label'].fillna('N/A')
            df_top['Total Usage (MB)'] = df_top['Total Usage (MB)'].round(2)

            # Create bar chart
            fig = px.bar(df_top, x='ICCID', y='Total Usage (MB)',
                        hover_data=['Label'],
                        color='Total Usage (MB)',
                        color_continuous_scale='Blues')
            st.plotly_chart(fig, use_container_width=True)

            # Show table
            st.dataframe(df_top, use_container_width=True)
        else:
            st.info("No usage data available")

except Exception as e:
    st.error(f"Error loading top consumers: {str(e)}")
