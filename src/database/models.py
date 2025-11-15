from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class SIMCard(Base):
    """SIM Card master data"""
    __tablename__ = 'sim_cards'

    id = Column(Integer, primary_key=True)
    iccid = Column(String(20), unique=True, nullable=False, index=True)
    iccid_with_luhn = Column(String(21))
    imsi = Column(String(15))
    imsi_2 = Column(String(15))
    current_imsi = Column(String(15))
    msisdn = Column(String(15))
    imei = Column(String(15))
    imei_lock = Column(Boolean, default=False)
    status = Column(String(20))  # Enabled/Disabled
    activation_date = Column(DateTime)
    ip_address = Column(String(15))
    label = Column(String(255))

    # Quota information
    current_quota_mb = Column(Float)
    quota_status_id = Column(Integer)
    quota_threshold_date = Column(DateTime)
    quota_exceeded_date = Column(DateTime)

    current_quota_sms = Column(Integer)
    quota_sms_status_id = Column(Integer)
    quota_sms_threshold_date = Column(DateTime)
    quota_sms_exceeded_date = Column(DateTime)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_synced_at = Column(DateTime)

    # Relationships
    usage_records = relationship("UsageRecord", back_populates="sim_card", cascade="all, delete-orphan")
    events = relationship("SIMEvent", back_populates="sim_card", cascade="all, delete-orphan")
    connectivity_logs = relationship("ConnectivityLog", back_populates="sim_card", cascade="all, delete-orphan")


class UsageRecord(Base):
    """Daily usage records (time-series data)"""
    __tablename__ = 'usage_records'

    id = Column(Integer, primary_key=True)
    sim_card_id = Column(Integer, ForeignKey('sim_cards.id'), nullable=False)
    date = Column(DateTime, nullable=False, index=True)

    # Data usage
    data_volume_mb = Column(Float, default=0)
    data_volume_rx_mb = Column(Float, default=0)
    data_volume_tx_mb = Column(Float, default=0)

    # SMS usage
    sms_volume = Column(Integer, default=0)
    sms_volume_mo = Column(Integer, default=0)  # Mobile Originated
    sms_volume_mt = Column(Integer, default=0)  # Mobile Terminated

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    sim_card = relationship("SIMCard", back_populates="usage_records")


class SIMEvent(Base):
    """SIM card events"""
    __tablename__ = 'sim_events'

    id = Column(Integer, primary_key=True)
    sim_card_id = Column(Integer, ForeignKey('sim_cards.id'), nullable=False)
    event_type = Column(String(50), nullable=False)
    event_description = Column(String(500))
    event_data = Column(JSON)
    occurred_at = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    sim_card = relationship("SIMCard", back_populates="events")


class ConnectivityLog(Base):
    """Connectivity and location logs"""
    __tablename__ = 'connectivity_logs'

    id = Column(Integer, primary_key=True)
    sim_card_id = Column(Integer, ForeignKey('sim_cards.id'), nullable=False)

    # Location data
    current_location_retrieved = Column(Boolean)
    age_of_location_minutes = Column(Integer)
    cid = Column(Integer)  # Cell ID
    lac = Column(Integer)  # Location Area Code
    mcc = Column(String(3))  # Mobile Country Code
    mnc = Column(String(3))  # Mobile Network Code

    # Timestamps
    request_timestamp = Column(DateTime)
    reply_timestamp = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    sim_card = relationship("SIMCard", back_populates="connectivity_logs")


class Alert(Base):
    """System alerts"""
    __tablename__ = 'alerts'

    id = Column(Integer, primary_key=True)
    sim_card_id = Column(Integer, ForeignKey('sim_cards.id'), nullable=True)
    alert_type = Column(String(50), nullable=False)  # quota_warning, connectivity_issue, etc.
    severity = Column(String(20))  # info, warning, critical
    message = Column(String(500))
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    resolved_at = Column(DateTime)


class DataCollectionLog(Base):
    """Log of data collection runs"""
    __tablename__ = 'data_collection_logs'

    id = Column(Integer, primary_key=True)
    collection_type = Column(String(50))  # full_sync, usage_update, etc.
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    status = Column(String(20))  # success, failed, partial
    sims_processed = Column(Integer, default=0)
    errors_count = Column(Integer, default=0)
    error_details = Column(JSON)
