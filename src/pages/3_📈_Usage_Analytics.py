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

st.set_page_config(page_title="Usage Analytics", page_icon="📈", layout="wide")

st.title("📈 Usage Analytics")
st.markdown("Detailed usage analytics and trends")

# Date range selector
col1, col2, col3 = st.columns(3)

with col1:
    start_date = st.date_input(
        "Start Date",
        value=datetime.now() - timedelta(days=30)
    )

with col2:
    end_date = st.date_input(
        "End Date",
        value=datetime.now()
    )

with col3:
    metric_type = st.selectbox(
        "Metric",
        ["Data Usage (MB)", "SMS Usage", "Both"]
    )

st.markdown("---")

try:
    with get_db() as db:
        # Overall usage statistics
        st.markdown("### Overall Statistics")

        total_usage = db.query(
            db.func.sum(UsageRecord.data_volume_mb)
        ).filter(
            UsageRecord.date >= start_date,
            UsageRecord.date <= end_date
        ).scalar() or 0

        total_sms = db.query(
            db.func.sum(UsageRecord.sms_volume)
        ).filter(
            UsageRecord.date >= start_date,
            UsageRecord.date <= end_date
        ).scalar() or 0

        days_diff = (end_date - start_date).days + 1
        avg_daily_data = total_usage / days_diff if days_diff > 0 else 0
        avg_daily_sms = total_sms / days_diff if days_diff > 0 else 0

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Data", f"{total_usage:,.1f} MB")
        with col2:
            st.metric("Total SMS", f"{total_sms:,}")
        with col3:
            st.metric("Avg Daily Data", f"{avg_daily_data:.1f} MB")
        with col4:
            st.metric("Avg Daily SMS", f"{avg_daily_sms:.0f}")

        st.markdown("---")

        # Time series chart
        st.markdown("### Usage Over Time")

        usage_trend = db.query(
            UsageRecord.date,
            db.func.sum(UsageRecord.data_volume_mb).label('data_mb'),
            db.func.sum(UsageRecord.sms_volume).label('sms')
        ).filter(
            UsageRecord.date >= start_date,
            UsageRecord.date <= end_date
        ).group_by(UsageRecord.date).order_by(UsageRecord.date).all()

        if usage_trend:
            df_trend = pd.DataFrame(
                usage_trend,
                columns=['Date', 'Data (MB)', 'SMS']
            )

            if metric_type == "Data Usage (MB)":
                fig = px.line(df_trend, x='Date', y='Data (MB)',
                            markers=True, line_shape='spline')
            elif metric_type == "SMS Usage":
                fig = px.line(df_trend, x='Date', y='SMS',
                            markers=True, line_shape='spline')
            else:  # Both
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df_trend['Date'], y=df_trend['Data (MB)'],
                    name='Data (MB)', mode='lines+markers'
                ))
                fig.add_trace(go.Scatter(
                    x=df_trend['Date'], y=df_trend['SMS'],
                    name='SMS', mode='lines+markers',
                    yaxis='y2'
                ))
                fig.update_layout(
                    yaxis=dict(title='Data (MB)'),
                    yaxis2=dict(title='SMS', overlaying='y', side='right')
                )

            fig.update_layout(hovermode='x unified', height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No usage data available for selected period")

        st.markdown("---")

        # SIM-level breakdown
        st.markdown("### SIM-Level Breakdown")

        sim_usage = db.query(
            SIMCard.iccid,
            SIMCard.label,
            db.func.sum(UsageRecord.data_volume_mb).label('total_data'),
            db.func.sum(UsageRecord.sms_volume).label('total_sms'),
            db.func.avg(UsageRecord.data_volume_mb).label('avg_data')
        ).join(
            UsageRecord, SIMCard.id == UsageRecord.sim_card_id
        ).filter(
            UsageRecord.date >= start_date,
            UsageRecord.date <= end_date
        ).group_by(
            SIMCard.id, SIMCard.iccid, SIMCard.label
        ).order_by(
            db.func.sum(UsageRecord.data_volume_mb).desc()
        ).all()

        if sim_usage:
            df_sims = pd.DataFrame(
                sim_usage,
                columns=['ICCID', 'Label', 'Total Data (MB)', 'Total SMS', 'Avg Daily Data (MB)']
            )
            df_sims['Label'] = df_sims['Label'].fillna('N/A')
            df_sims['Total Data (MB)'] = df_sims['Total Data (MB)'].round(2)
            df_sims['Avg Daily Data (MB)'] = df_sims['Avg Daily Data (MB)'].round(2)

            # Show top 20
            st.dataframe(df_sims.head(20), use_container_width=True)

            # Download full data
            csv = df_sims.to_csv(index=False)
            st.download_button(
                label="📥 Download Full Report (CSV)",
                data=csv,
                file_name=f"usage_report_{start_date}_{end_date}.csv",
                mime="text/csv"
            )

            # Usage distribution
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### Data Usage Distribution")
                fig = px.histogram(
                    df_sims,
                    x='Total Data (MB)',
                    nbins=20,
                    title="Distribution of Data Usage"
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.markdown("#### Top 10 Data Users")
                fig = px.bar(
                    df_sims.head(10),
                    x='ICCID',
                    y='Total Data (MB)',
                    hover_data=['Label'],
                    color='Total Data (MB)',
                    color_continuous_scale='Viridis'
                )
                st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("No usage data available for selected SIMs and period")

except Exception as e:
    st.error(f"Error loading analytics: {str(e)}")
