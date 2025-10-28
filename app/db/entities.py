from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime, func, UniqueConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base

class Country(Base):
    __tablename__ = 'country'
    __table_args__ = (
        UniqueConstraint("name", name="uq_country_name_currency"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    capital: Mapped[Optional[str]] = mapped_column(String(100))
    region: Mapped[Optional[str]] = mapped_column(String(100))
    population: Mapped[int]
    currency_code: Mapped[str] = mapped_column(String(10), nullable=True)
    exchange_rate: Mapped[float] = mapped_column(nullable=True)
    estimated_gdp: Mapped[float] = mapped_column(nullable=True)
    flag_url: Mapped[Optional[str]] = mapped_column(String(100))
    last_refreshed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


    def to_dict(self) -> dict:
        """Convert model instance to plain dict."""
        return {
            "id": self.id,
            "name": self.name,
            "region": self.region,
            "capital": self.capital,
            "population": self.population,
            "currency_code": self.currency_code,
            "exchange_rate": self.exchange_rate,
            "estimated_gdp": self.estimated_gdp,
            "flag_url": self.flag_url,
            "last_refreshed_at": self.last_refreshed_at.astimezone(timezone.utc).isoformat()
        }