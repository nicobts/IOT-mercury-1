import streamlit as st
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.database.connection import get_db
from src.database.models import SIMCard
from src.api.client import OnceAPIClient

st.set_page_config(page_title="SIM Management", page_icon="📱", layout="wide")

st.title("📱 SIM Management")
st.markdown("Manage and monitor individual SIM cards")

# Search and filters
st.markdown("### Search & Filter")
col1, col2, col3 = st.columns(3)

with col1:
    search_term = st.text_input("Search by ICCID or Label", "")

with col2:
    status_filter = st.selectbox("Status", ["All", "Enabled", "Disabled"])

with col3:
    sort_by = st.selectbox("Sort by", ["Last Updated", "ICCID", "Label", "Status"])

# Load SIM data
try:
    with get_db() as db:
        query = db.query(SIMCard)

        # Apply search filter
        if search_term:
            query = query.filter(
                (SIMCard.iccid.contains(search_term)) |
                (SIMCard.label.contains(search_term))
            )

        # Apply status filter
        if status_filter != "All":
            query = query.filter(SIMCard.status == status_filter)

        # Apply sorting
        if sort_by == "Last Updated":
            query = query.order_by(SIMCard.updated_at.desc())
        elif sort_by == "ICCID":
            query = query.order_by(SIMCard.iccid)
        elif sort_by == "Label":
            query = query.order_by(SIMCard.label)
        elif sort_by == "Status":
            query = query.order_by(SIMCard.status)

        sims = query.all()

        st.markdown(f"### Found {len(sims)} SIM cards")

        if sims:
            # Create DataFrame
            df = pd.DataFrame([
                {
                    'ICCID': sim.iccid,
                    'Label': sim.label or 'N/A',
                    'Status': sim.status,
                    'IMSI': sim.imsi or 'N/A',
                    'IP Address': sim.ip_address or 'N/A',
                    'Quota (MB)': f"{sim.current_quota_mb:.2f}" if sim.current_quota_mb else 'N/A',
                    'Last Updated': sim.updated_at.strftime('%Y-%m-%d %H:%M') if sim.updated_at else 'N/A'
                }
                for sim in sims
            ])

            # Display table with selection
            st.dataframe(df, use_container_width=True)

            st.markdown("---")
            st.markdown("### SIM Details")

            # Select SIM for detailed view
            selected_iccid = st.selectbox(
                "Select SIM for details",
                options=[sim.iccid for sim in sims],
                format_func=lambda x: f"{x} - {next((s.label for s in sims if s.iccid == x), 'N/A')}"
            )

            if selected_iccid:
                selected_sim = next((s for s in sims if s.iccid == selected_iccid), None)

                if selected_sim:
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("#### Basic Information")
                        st.text(f"ICCID: {selected_sim.iccid}")
                        st.text(f"Label: {selected_sim.label or 'N/A'}")
                        st.text(f"Status: {selected_sim.status}")
                        st.text(f"IMSI: {selected_sim.imsi or 'N/A'}")
                        st.text(f"MSISDN: {selected_sim.msisdn or 'N/A'}")
                        st.text(f"IP Address: {selected_sim.ip_address or 'N/A'}")
                        st.text(f"IMEI: {selected_sim.imei or 'N/A'}")
                        st.text(f"IMEI Lock: {'Yes' if selected_sim.imei_lock else 'No'}")

                    with col2:
                        st.markdown("#### Quota Information")
                        st.text(f"Data Quota: {selected_sim.current_quota_mb:.2f} MB" if selected_sim.current_quota_mb else "N/A")
                        st.text(f"SMS Quota: {selected_sim.current_quota_sms}" if selected_sim.current_quota_sms else "N/A")
                        st.text(f"Activation Date: {selected_sim.activation_date.strftime('%Y-%m-%d') if selected_sim.activation_date else 'N/A'}")
                        st.text(f"Last Synced: {selected_sim.last_synced_at.strftime('%Y-%m-%d %H:%M') if selected_sim.last_synced_at else 'N/A'}")

                    st.markdown("---")
                    st.markdown("#### Actions")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        if st.button("🔄 Refresh SIM Data", key=f"refresh_{selected_iccid}"):
                            with st.spinner("Refreshing SIM data..."):
                                try:
                                    from src.services.data_collector import DataCollector
                                    collector = DataCollector()
                                    api_client = OnceAPIClient()
                                    api_sim = api_client.get_sim(selected_iccid)

                                    with get_db() as db:
                                        collector._sync_single_sim(db, api_sim)

                                    st.success("✅ SIM data refreshed!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Failed to refresh: {str(e)}")

                    with col2:
                        new_label = st.text_input("Update Label", value=selected_sim.label or "")
                        if st.button("💾 Save Label", key=f"save_label_{selected_iccid}"):
                            if new_label:
                                with st.spinner("Updating label..."):
                                    try:
                                        api_client = OnceAPIClient()
                                        api_client.update_sim_label(selected_iccid, new_label)

                                        with get_db() as db:
                                            sim = db.query(SIMCard).filter(
                                                SIMCard.iccid == selected_iccid
                                            ).first()
                                            if sim:
                                                sim.label = new_label
                                                db.commit()

                                        st.success("✅ Label updated!")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"❌ Failed to update: {str(e)}")

                    with col3:
                        st.markdown("##### Enable/Disable")
                        if selected_sim.status == "Enabled":
                            if st.button("🔴 Disable SIM", key=f"disable_{selected_iccid}"):
                                if st.confirm("Are you sure you want to disable this SIM?"):
                                    try:
                                        api_client = OnceAPIClient()
                                        api_client.disable_sim(selected_iccid)
                                        st.success("✅ SIM disabled!")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"❌ Failed: {str(e)}")
                        else:
                            if st.button("🟢 Enable SIM", key=f"enable_{selected_iccid}"):
                                try:
                                    api_client = OnceAPIClient()
                                    api_client.enable_sim(selected_iccid)
                                    st.success("✅ SIM enabled!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Failed: {str(e)}")

        else:
            st.info("No SIM cards found. Try different filters or sync data from 1NCE API.")

except Exception as e:
    st.error(f"Error loading SIM data: {str(e)}")
