from datetime import datetime
from typing import List, Dict, Any
import logging

from src.database.connection import get_db
from src.database.models import Alert, SIMCard

logger = logging.getLogger(__name__)


class AlertService:
    """Service for managing alerts and notifications"""

    def check_quota_alerts(self) -> List[Alert]:
        """Check and create quota alerts for SIMs with low quota"""
        alerts_created = []

        with get_db() as db:
            # Find SIMs with low data quota (status_id 1 or 2)
            # status_id 1: < 20%, status_id 2: < 10%
            low_quota_sims = db.query(SIMCard).filter(
                SIMCard.quota_status_id.in_([1, 2])
            ).all()

            for sim in low_quota_sims:
                # Check if alert already exists
                existing = db.query(Alert).filter(
                    Alert.sim_card_id == sim.id,
                    Alert.alert_type == 'quota_warning',
                    Alert.is_resolved == False
                ).first()

                if not existing:
                    severity = 'critical' if sim.quota_status_id == 2 else 'warning'
                    percentage = '10%' if sim.quota_status_id == 2 else '20%'

                    alert = Alert(
                        sim_card_id=sim.id,
                        alert_type='quota_warning',
                        severity=severity,
                        message=f"SIM {sim.iccid} ({sim.label or 'No Label'}) has less than {percentage} data quota remaining"
                    )
                    db.add(alert)
                    alerts_created.append(alert)
                    logger.info(f"Created quota alert for SIM {sim.iccid}")

            # Find SIMs with low SMS quota
            low_sms_sims = db.query(SIMCard).filter(
                SIMCard.quota_sms_status_id.in_([1, 2])
            ).all()

            for sim in low_sms_sims:
                existing = db.query(Alert).filter(
                    Alert.sim_card_id == sim.id,
                    Alert.alert_type == 'sms_quota_warning',
                    Alert.is_resolved == False
                ).first()

                if not existing:
                    severity = 'critical' if sim.quota_sms_status_id == 2 else 'warning'
                    percentage = '10%' if sim.quota_sms_status_id == 2 else '20%'

                    alert = Alert(
                        sim_card_id=sim.id,
                        alert_type='sms_quota_warning',
                        severity=severity,
                        message=f"SIM {sim.iccid} ({sim.label or 'No Label'}) has less than {percentage} SMS quota remaining"
                    )
                    db.add(alert)
                    alerts_created.append(alert)
                    logger.info(f"Created SMS quota alert for SIM {sim.iccid}")

            db.commit()

        return alerts_created

    def resolve_alert(self, alert_id: int) -> bool:
        """Mark an alert as resolved"""
        with get_db() as db:
            alert = db.query(Alert).filter(Alert.id == alert_id).first()

            if alert:
                alert.is_resolved = True
                alert.resolved_at = datetime.utcnow()
                db.commit()
                logger.info(f"Resolved alert {alert_id}")
                return True

            return False

    def get_active_alerts(self) -> List[Alert]:
        """Get all active (unresolved) alerts"""
        with get_db() as db:
            return db.query(Alert).filter(Alert.is_resolved == False).order_by(
                Alert.created_at.desc()
            ).all()

    def get_alerts_by_severity(self, severity: str) -> List[Alert]:
        """Get alerts by severity level"""
        with get_db() as db:
            return db.query(Alert).filter(
                Alert.severity == severity,
                Alert.is_resolved == False
            ).order_by(Alert.created_at.desc()).all()

    def get_sim_alerts(self, sim_card_id: int) -> List[Alert]:
        """Get all alerts for a specific SIM"""
        with get_db() as db:
            return db.query(Alert).filter(
                Alert.sim_card_id == sim_card_id
            ).order_by(Alert.created_at.desc()).all()

    def cleanup_old_alerts(self, days: int = 30) -> int:
        """Delete resolved alerts older than specified days"""
        from datetime import timedelta

        cutoff_date = datetime.utcnow() - timedelta(days=days)

        with get_db() as db:
            deleted = db.query(Alert).filter(
                Alert.is_resolved == True,
                Alert.resolved_at < cutoff_date
            ).delete()

            db.commit()
            logger.info(f"Deleted {deleted} old resolved alerts")
            return deleted
