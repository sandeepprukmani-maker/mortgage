from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Customer(db.Model):
    """
    SCD Type 2 implementation for Customer history tracking.
    Each change creates a new row with version tracking.
    """
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    customer_key = db.Column(db.String(50), nullable=False, index=True)  # Unique business key
    version = db.Column(db.Integer, nullable=False, default=1)

    # Customer details
    name = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(200))

    # Financial details
    current_monthly_payment = db.Column(db.Float)
    remaining_balance = db.Column(db.Float)
    property_value = db.Column(db.Float)
    credit_score = db.Column(db.Integer)
    monthly_income = db.Column(db.Float)

    # Property details
    property_zip = db.Column(db.String(10))
    property_county = db.Column(db.String(100))
    property_state = db.Column(db.String(2))

    # SCD Type 2 fields
    effective_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    is_current = db.Column(db.Boolean, nullable=False, default=True, index=True)

    # Audit fields
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_by = db.Column(db.String(100))

    __table_args__ = (
        db.Index('ix_customer_key_current', 'customer_key', 'is_current'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'customer_key': self.customer_key,
            'version': self.version,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'current_monthly_payment': self.current_monthly_payment,
            'remaining_balance': self.remaining_balance,
            'property_value': self.property_value,
            'property_zip': self.property_zip,
            'property_county': self.property_county,
            'property_state': self.property_state,
            'credit_score': self.credit_score,
            'monthly_income': self.monthly_income,
            'effective_date': self.effective_date.isoformat() if self.effective_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_current': self.is_current,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    @staticmethod
    def get_current_customers():
        """Get all current (active) customer records"""
        return Customer.query.filter_by(is_current=True).all()

    @staticmethod
    def get_customer_history(customer_key):
        """Get all versions of a customer"""
        return Customer.query.filter_by(customer_key=customer_key).order_by(Customer.version.desc()).all()

    @staticmethod
    def get_current_by_key(customer_key):
        """Get the current version of a customer by key"""
        return Customer.query.filter_by(customer_key=customer_key, is_current=True).first()