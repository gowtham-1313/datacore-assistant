# backend/database.py
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import os

Base = declarative_base()

# Define database tables
class Movie(Base):
    __tablename__ = 'movies'
    movie_id = Column(Integer, primary_key=True)
    title = Column(String)
    genre = Column(String)
    release_date = Column(String)
    director = Column(String)
    budget_usd = Column(Integer)
    rating = Column(Float)

class Viewer(Base):
    __tablename__ = 'viewers'
    viewer_id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    country = Column(String)
    age_group = Column(String)
    subscription_tier = Column(String)

class WatchActivity(Base):
    __tablename__ = 'watch_activity'
    activity_id = Column(Integer, primary_key=True)
    viewer_id = Column(Integer)
    movie_id = Column(Integer)
    watch_date = Column(String)
    watch_duration_min = Column(Integer)
    completion_pct = Column(Integer)

class Review(Base):
    __tablename__ = 'reviews'
    review_id = Column(Integer, primary_key=True)
    viewer_id = Column(Integer)
    movie_id = Column(Integer)
    rating_stars = Column(Integer)
    sentiment_label = Column(String)
    review_date = Column(String)

class MarketingSpend(Base):
    __tablename__ = 'marketing_spend'
    campaign_id = Column(Integer, primary_key=True)
    movie_id = Column(Integer)
    channel = Column(String)
    spend_usd = Column(Integer)
    impressions = Column(Integer)
    clicks = Column(Integer)
    campaign_month = Column(String)

class RegionalPerformance(Base):
    __tablename__ = 'regional_performance'
    region_id = Column(Integer, primary_key=True)
    city = Column(String)
    country = Column(String)
    total_views = Column(Integer)
    avg_rating = Column(Float)
    growth_pct = Column(Float)
    report_month = Column(String)

def init_database():
    """Create database and load data from CSV files"""
    engine = create_engine('sqlite:///backend/data/datacore.db', echo=False)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    csv_path = 'backend/data/csv_files/'
    
    if session.query(Movie).count() == 0:
        print("📊 Loading data from CSV files...")
        
        movies_df = pd.read_csv(f'{csv_path}movies.csv')
        for _, row in movies_df.iterrows():
            session.add(Movie(**row.to_dict()))
        
        viewers_df = pd.read_csv(f'{csv_path}viewers.csv')
        for _, row in viewers_df.iterrows():
            session.add(Viewer(**row.to_dict()))
        
        watch_df = pd.read_csv(f'{csv_path}watch_activity.csv')
        for _, row in watch_df.iterrows():
            session.add(WatchActivity(**row.to_dict()))
        
        reviews_df = pd.read_csv(f'{csv_path}reviews.csv')
        for _, row in reviews_df.iterrows():
            session.add(Review(**row.to_dict()))
        
        marketing_df = pd.read_csv(f'{csv_path}marketing_spend.csv')
        for _, row in marketing_df.iterrows():
            session.add(MarketingSpend(**row.to_dict()))
        
        regional_df = pd.read_csv(f'{csv_path}regional_performance.csv')
        for _, row in regional_df.iterrows():
            session.add(RegionalPerformance(**row.to_dict()))
        
        session.commit()
        print("✅ Data loaded successfully into database!")
    else:
        print("✅ Database already has data.")
    
    session.close()
    return engine

if __name__ == "__main__":
    init_database()
    print("✅ Database setup complete!")
