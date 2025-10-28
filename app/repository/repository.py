from fastapi import HTTPException
from sqlalchemy import func, select, asc, desc, delete
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.exc import SQLAlchemyError

from app.db.entities import Country
from app.db.session import SessionLocal
from app.exceptions.app_exceptions import NotFoundError, DatabaseError


def upsert(countries: list[dict]):

    with SessionLocal.begin() as session:
        try:
            if not countries:
                return

            stmt = insert(Country).values(countries)

            upsert_stmt = stmt.on_duplicate_key_update(
                    currency_code=stmt.inserted.currency_code,
                    exchange_rate=stmt.inserted.exchange_rate,
                    estimated_gdp=stmt.inserted.estimated_gdp,
                    last_refreshed_at=func.now()
            )

            session.execute(upsert_stmt)

        except SQLAlchemyError as e:
            raise DatabaseError(f"Internal Server Error: {e}")


def filter(region: str = None, currency_code: str = None, order_by: str = None, ascending: bool = None):

    with SessionLocal.begin() as session:
        try:
            stmt = select(Country)
            filters = []

            if region:
                filters.append(Country.region.ilike(region))
            if currency_code:
                filters.append(Country.currency_code.ilike(currency_code))

            if filters:
                stmt = stmt.where(*filters)

            if order_by:
                column = getattr(Country, order_by.lower(), None)
                if column is not None:
                    stmt = stmt.order_by(asc(column) if ascending else desc(column))

            result = session.execute(stmt).scalars().all()

            return [record.to_dict() for record in result]

        except SQLAlchemyError as e:
            raise DatabaseError(f"Internal Server Error: {e}")


def read_by_name(name: str):
    with SessionLocal.begin() as session:
        try:
            stmt = select(Country).where(Country.name.ilike(name))
            result = session.execute(stmt).scalar_one_or_none()

            if not result:
                raise NotFoundError("Country not found")

            return result.to_dict()

        except SQLAlchemyError as e:
            raise DatabaseError(f"Internal Server Error: {e}")


def delete_by_name(name: str):
    with SessionLocal.begin() as session:
        try:
            stmt = delete(Country).where(Country.name.ilike(name))
            result = session.execute(stmt)

            if result.rowcount == 0:
                raise NotFoundError("Country not found")

            return result

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


def compute_status_fields():
    with SessionLocal.begin() as session:
        try:
            stmt1 = select(func.max(Country.last_refreshed_at))
            stmt2 = select(func.count(Country.name))

            max_last_refresh_date = session.scalar(stmt1)
            total = session.scalar(stmt2)

            return max_last_refresh_date, total


        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


def compute_summary_data():
    with SessionLocal.begin() as session:
        try:
            stmt1 = select(func.max(Country.last_refreshed_at))
            stmt2 = select(func.count(Country.name))
            stmt3 = (
            select(Country)
            .where(Country.estimated_gdp.is_not(None))
            .order_by(desc(Country.estimated_gdp))
            .limit(5)
        )

            max_last_refresh_date = session.scalar(stmt1)
            total = session.scalar(stmt2)
            top_5 = session.execute(stmt3).scalars().all()

            top_5 = [record.to_dict() for record in top_5]

            return max_last_refresh_date, total, top_5


        except SQLAlchemyError as e:
            raise DatabaseError(f"Internal Server Error: {e}")