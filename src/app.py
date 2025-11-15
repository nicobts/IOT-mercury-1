import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.connection import get_db
from src.database.models import SIMCard, UsageRecord
from src.utils.logger import setup_logging

# Setup
setup_logging()

# Page config
st.set_page_config(
    page_title="1NCE IoT Management",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main > div {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    # Header
    st.title("📡 1NCE IoT Management Dashboard")
    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.markdown("### 1NCE Dashboard")
        st.markdown("Navigate using the pages in the sidebar")

        st.markdown("---")
        st.markdown("### Quick Stats")

        try:
            with get_db() as db:
                total_sims = db.query(SIMCard).count()
                active_sims = db.query(SIMCard).filter(
                    SIMCard.status == 'Enabled'
                ).count()

                st.metric("Total SIMs", total_sims)
                st.metric("Active SIMs", active_sims)
        except Exception as e:
            st.error(f"Database connection error: {str(e)}")

    # Main content
    col1, col2, col3, col4 = st.columns(4)

    try:
        with get_db() as db:
            # Total SIMs
            with col1:
                total = db.query(SIMCard).count()
                st.metric("Total SIMs", f"{total:,}")

            # Active SIMs
            with col2:
                active = db.query(SIMCard).filter(
                    SIMCard.status == 'Enabled'
                ).count()
                st.metric("Active SIMs", f"{active:,}")

            # Today's data usage
            with col3:
                today = datetime.now().date()
                usage_today = db.query(
                    db.func.sum(UsageRecord.data_volume_mb)
                ).filter(
                    UsageRecord.date >= today
                ).scalar() or 0
                st.metric("Today's Data Usage", f"{usage_today:.1f} MB")

            # Quota alerts
            with col4:
                alerts = db.query(SIMCard).filter(
                    SIMCard.quota_status_id.in_([1, 2])
                ).count()
                st.metric("Quota Alerts", alerts)

    except Exception as e:
        st.error(f"Error loading metrics: {str(e)}")

    st.markdown("---")

    # Recent activity
    st.subheader("Recent Activity")

    try:
        with get_db() as db:
            recent_sims = db.query(SIMCard).order_by(
                SIMCard.updated_at.desc()
            ).limit(10).all()

            if recent_sims:
                df = pd.DataFrame([
                    {
                        'ICCID': sim.iccid,
                        'Label': sim.label or 'N/A',
                        'Status': sim.status,
                        'Last Updated': sim.updated_at.strftime('%Y-%m-%d %H:%M') if sim.updated_at else 'N/A'
                    }
                    for sim in recent_sims
                ])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No SIM cards found. Use the sync button below to import SIM data.")
    except Exception as e:
        st.error(f"Error loading recent activity: {str(e)}")

    # Quick actions
    st.markdown("---")
    st.subheader("Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔄 Sync All SIMs", use_container_width=True):
            with st.spinner("Syncing SIM data..."):
                try:
                    from src.services.data_collector import DataCollector
                    collector = DataCollector()
                    result = collector.sync_all_sims()
                    st.success(f"✅ Synced {result['processed']} SIMs")
                    if result['errors'] > 0:
                        st.warning(f"⚠️ {result['errors']} SIMs had errors")
                except Exception as e:
                    st.error(f"❌ Sync failed: {str(e)}")

    with col2:
        if st.button("📊 Collect Usage Data", use_container_width=True):
            with st.spinner("Collecting usage data..."):
                try:
                    from src.services.data_collector import DataCollector
                    collector = DataCollector()
                    collector.collect_all_usage_data(days_back=7)
                    st.success("✅ Usage data collected successfully")
                except Exception as e:
                    st.error(f"❌ Collection failed: {str(e)}")

    with col3:
        if st.button("📈 View Reports", use_container_width=True):
            st.info("Navigate to Reports page in the sidebar")

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>1NCE IoT Management Dashboard | "
        f"Version 1.0 | {datetime.now().year}</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
