from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging

from src.api.client import OnceAPIClient
from src.database.connection import get_db
from src.database.models import (
    SIMCard, UsageRecord, ConnectivityLog,
    SIMEvent, DataCollectionLog
)

logger = logging.getLogger(__name__)


class DataCollector:
    """Service for collecting data from 1NCE API"""

    def __init__(self):
        self.api_client = OnceAPIClient()

    def sync_all_sims(self) -> Dict[str, Any]:
        """Sync all SIM cards from API to database"""
        log_entry = DataCollectionLog(
            collection_type='full_sync',
            started_at=datetime.utcnow(),
            status='running'
        )

        try:
            with get_db() as db:
                db.add(log_entry)
                db.commit()

                # Fetch all SIMs from API
                api_sims = self.api_client.get_all_sims()

                processed = 0
                errors = []

                for api_sim in api_sims:
                    try:
                        self._sync_single_sim(db, api_sim)
                        processed += 1
                    except Exception as e:
                        errors.append({
                            'iccid': api_sim.get('iccid'),
                            'error': str(e)
                        })
                        logger.error(f"Failed to sync SIM {api_sim.get('iccid')}: {e}")

                # Update log
                log_entry.completed_at = datetime.utcnow()
                log_entry.status = 'success' if not errors else 'partial'
                log_entry.sims_processed = processed
                log_entry.errors_count = len(errors)
                log_entry.error_details = errors if errors else None
                db.commit()

                return {
                    'success': True,
                    'processed': processed,
                    'errors': len(errors)
                }

        except Exception as e:
            logger.error(f"Full sync failed: {e}")
            log_entry.status = 'failed'
            log_entry.completed_at = datetime.utcnow()
            with get_db() as db:
                db.add(log_entry)
                db.commit()
            raise

    def _sync_single_sim(self, db, api_sim: Dict[str, Any]):
        """Sync single SIM card data"""
        iccid = api_sim['iccid']

        # Find or create SIM record
        sim = db.query(SIMCard).filter(SIMCard.iccid == iccid).first()

        if not sim:
            sim = SIMCard(iccid=iccid)
            db.add(sim)

        # Update fields
        sim.iccid_with_luhn = api_sim.get('iccid_with_luhn')
        sim.imsi = api_sim.get('imsi')
        sim.imsi_2 = api_sim.get('imsi_2')
        sim.current_imsi = api_sim.get('current_imsi')
        sim.msisdn = api_sim.get('msisdn')
        sim.imei = api_sim.get('imei')
        sim.imei_lock = api_sim.get('imei_lock', False)
        sim.status = api_sim.get('status')
        sim.ip_address = api_sim.get('ip_address')
        sim.label = api_sim.get('label')

        # Activation date
        if api_sim.get('activation_date'):
            sim.activation_date = datetime.fromisoformat(
                api_sim['activation_date'].replace('Z', '+00:00')
            )

        # Quota data
        sim.current_quota_mb = api_sim.get('current_quota')
        if api_sim.get('quota_status'):
            sim.quota_status_id = api_sim['quota_status'].get('id')

        sim.current_quota_sms = api_sim.get('current_quota_SMS')
        if api_sim.get('quota_status_SMS'):
            sim.quota_sms_status_id = api_sim['quota_status_SMS'].get('id')

        sim.last_synced_at = datetime.utcnow()
        sim.updated_at = datetime.utcnow()

        db.commit()

    def collect_usage_data(
        self,
        iccid: str,
        start_date: str,
        end_date: str
    ):
        """Collect and store usage data for a SIM"""
        with get_db() as db:
            sim = db.query(SIMCard).filter(SIMCard.iccid == iccid).first()
            if not sim:
                raise ValueError(f"SIM {iccid} not found in database")

            # Fetch usage from API
            usage_data = self.api_client.get_sim_usage(iccid, start_date, end_date)

            for daily_stat in usage_data.get('stats', []):
                date = datetime.fromisoformat(daily_stat['date'].replace('Z', '+00:00'))

                # Check if record exists
                existing = db.query(UsageRecord).filter(
                    UsageRecord.sim_card_id == sim.id,
                    UsageRecord.date == date
                ).first()

                if existing:
                    # Update existing record
                    usage_record = existing
                else:
                    # Create new record
                    usage_record = UsageRecord(
                        sim_card_id=sim.id,
                        date=date
                    )
                    db.add(usage_record)

                # Update data usage
                data = daily_stat.get('data', {})
                usage_record.data_volume_mb = float(data.get('volume', 0))
                usage_record.data_volume_rx_mb = float(data.get('volume_rx', 0))
                usage_record.data_volume_tx_mb = float(data.get('volume_tx', 0))

                # Update SMS usage
                sms = daily_stat.get('sms', {})
                usage_record.sms_volume = int(sms.get('volume', 0))
                usage_record.sms_volume_mo = int(sms.get('volume_rx', 0))
                usage_record.sms_volume_mt = int(sms.get('volume_tx', 0))

            db.commit()

    def collect_all_usage_data(self, days_back: int = 7):
        """Collect usage data for all SIMs"""
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

        with get_db() as db:
            sims = db.query(SIMCard).all()

            for sim in sims:
                try:
                    self.collect_usage_data(sim.iccid, start_date, end_date)
                    logger.info(f"Collected usage for {sim.iccid}")
                except Exception as e:
                    logger.error(f"Failed to collect usage for {sim.iccid}: {e}")

    def collect_connectivity_info(self, iccid: str):
        """Collect and store connectivity information for a SIM"""
        with get_db() as db:
            sim = db.query(SIMCard).filter(SIMCard.iccid == iccid).first()
            if not sim:
                raise ValueError(f"SIM {iccid} not found in database")

            # Fetch connectivity info from API
            conn_data = self.api_client.get_sim_connectivity(iccid)

            # Create connectivity log
            conn_log = ConnectivityLog(
                sim_card_id=sim.id,
                current_location_retrieved=conn_data.get('current_location_retrieved'),
                age_of_location_minutes=conn_data.get('age_of_location_minutes'),
                cid=conn_data.get('cid'),
                lac=conn_data.get('lac'),
                mcc=conn_data.get('mcc'),
                mnc=conn_data.get('mnc'),
                request_timestamp=datetime.fromisoformat(
                    conn_data['request_timestamp'].replace('Z', '+00:00')
                ) if conn_data.get('request_timestamp') else None,
                reply_timestamp=datetime.fromisoformat(
                    conn_data['reply_timestamp'].replace('Z', '+00:00')
                ) if conn_data.get('reply_timestamp') else None
            )

            db.add(conn_log)
            db.commit()
