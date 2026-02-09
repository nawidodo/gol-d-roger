"""Database models for gold portfolio tracker."""
from sqlalchemy import Column, Integer, String, DateTime, Numeric
from datetime import datetime
from database import Base

class Purchase(Base):
    """Model for gold purchase records."""
    __tablename__ = "purchases"
    
    id = Column(Integer, primary_key=True, index=True)
    weight = Column(Numeric(10, 2), nullable=False)  # Gold weight in grams
    purchase_price = Column(Numeric(15, 2), nullable=False)  # Price per gram
    total_paid = Column(Numeric(15, 2), nullable=False)  # Total amount paid
    purchase_date = Column(DateTime, nullable=False)
    notes = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "weight": float(self.weight),
            "purchase_price": float(self.purchase_price),
            "total_paid": float(self.total_paid),
            "purchase_date": self.purchase_date.isoformat(),
            "notes": self.notes,
            "created_at": self.created_at.isoformat()
        }
