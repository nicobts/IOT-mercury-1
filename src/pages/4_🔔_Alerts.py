import streamlit as st
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.database.connection import get_db
from src.database.models import Alert, SIMCard
from src.services.alert_service import AlertService

st.set_page_config(page_title="Alerts", page_icon="🔔", layout="wide")

st.title("🔔 Alerts & Notifications")
st.markdown("Monitor and manage system alerts")

# Alert service
alert_service = AlertService()

# Action buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 Check for New Alerts", use_container_width=True):
        with st.spinner("Checking for alerts..."):
            try:
                new_alerts = alert_service.check_quota_alerts()
                st.success(f"✅ Check complete. Found {len(new_alerts)} new alerts.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

with col2:
    if st.button("🧹 Cleanup Old Alerts", use_container_width=True):
        with st.spinner("Cleaning up..."):
            try:
                deleted = alert_service.cleanup_old_alerts(days=30)
                st.success(f"✅ Deleted {deleted} old resolved alerts")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

st.markdown("---")

# Alert statistics
try:
    with get_db() as db:
        total_active = db.query(Alert).filter(Alert.is_resolved == False).count()
        critical = db.query(Alert).filter(
            Alert.severity == 'critical',
            Alert.is_resolved == False
        ).count()
        warning = db.query(Alert).filter(
            Alert.severity == 'warning',
            Alert.is_resolved == False
        ).count()
        info = db.query(Alert).filter(
            Alert.severity == 'info',
            Alert.is_resolved == False
        ).count()

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Active", total_active)
        with col2:
            st.metric("🔴 Critical", critical)
        with col3:
            st.metric("🟡 Warning", warning)
        with col4:
            st.metric("🔵 Info", info)

except Exception as e:
    st.error(f"Error loading alert statistics: {str(e)}")

st.markdown("---")

# Filter alerts
st.markdown("### Active Alerts")

col1, col2 = st.columns(2)
with col1:
    severity_filter = st.selectbox(
        "Filter by Severity",
        ["All", "Critical", "Warning", "Info"]
    )

with col2:
    alert_type_filter = st.selectbox(
        "Filter by Type",
        ["All", "Quota Warning", "SMS Quota Warning", "Connectivity Issue"]
    )

# Load and display alerts
try:
    with get_db() as db:
        query = db.query(Alert).join(
            SIMCard, Alert.sim_card_id == SIMCard.id, isouter=True
        ).filter(Alert.is_resolved == False)

        # Apply filters
        if severity_filter != "All":
            query = query.filter(Alert.severity == severity_filter.lower())

        type_map = {
            "Quota Warning": "quota_warning",
            "SMS Quota Warning": "sms_quota_warning",
            "Connectivity Issue": "connectivity_issue"
        }
        if alert_type_filter != "All":
            query = query.filter(Alert.alert_type == type_map[alert_type_filter])

        alerts = query.order_by(Alert.created_at.desc()).all()

        if alerts:
            for alert in alerts:
                # Get SIM info
                sim = db.query(SIMCard).filter(SIMCard.id == alert.sim_card_id).first()

                # Create alert card
                severity_emoji = {
                    'critical': '🔴',
                    'warning': '🟡',
                    'info': '🔵'
                }

                with st.container():
                    col1, col2 = st.columns([4, 1])

                    with col1:
                        st.markdown(
                            f"{severity_emoji.get(alert.severity, '⚪')} **{alert.message}**"
                        )
                        if sim:
                            st.caption(
                                f"ICCID: {sim.iccid} | "
                                f"Label: {sim.label or 'N/A'} | "
                                f"Created: {alert.created_at.strftime('%Y-%m-%d %H:%M')}"
                            )

                    with col2:
                        if st.button("✅ Resolve", key=f"resolve_{alert.id}"):
                            alert_service.resolve_alert(alert.id)
                            st.success("Alert resolved!")
                            st.rerun()

                    st.markdown("---")

        else:
            st.success("🎉 No active alerts! Everything looks good.")

except Exception as e:
    st.error(f"Error loading alerts: {str(e)}")

# Recent resolved alerts
st.markdown("### Recently Resolved Alerts")

try:
    with get_db() as db:
        resolved_alerts = db.query(Alert).filter(
            Alert.is_resolved == True
        ).order_by(Alert.resolved_at.desc()).limit(10).all()

        if resolved_alerts:
            df = pd.DataFrame([
                {
                    'Severity': alert.severity,
                    'Type': alert.alert_type,
                    'Message': alert.message,
                    'Created': alert.created_at.strftime('%Y-%m-%d %H:%M'),
                    'Resolved': alert.resolved_at.strftime('%Y-%m-%d %H:%M') if alert.resolved_at else 'N/A'
                }
                for alert in resolved_alerts
            ])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No resolved alerts in history")

except Exception as e:
    st.error(f"Error loading resolved alerts: {str(e)}")
