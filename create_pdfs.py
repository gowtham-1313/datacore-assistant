# create_pdfs.py
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os

# Create folder if doesn't exist
os.makedirs('backend/data/pdf_files', exist_ok=True)

def create_quarterly_report():
    """Create quarterly_report_q1_2025.pdf"""
    print("📄 Creating quarterly_report_q1_2025.pdf")
    
    doc = SimpleDocTemplate(
        "backend/data/pdf_files/quarterly_report_q1_2025.pdf",
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )

    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=12
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6
    )

    # Content
    story = []
    
    # Title
    story.append(Paragraph("QUARTERLY REPORT Q1 2025", title_style))
    story.append(Spacer(1, 0.25*inch))
    
    # Top Performing Titles
    story.append(Paragraph("TOP PERFORMING TITLES (by watch hours):", heading_style))
    story.append(Paragraph("1. Stellar Run - 1,200,000 hours", body_style))
    story.append(Paragraph("2. Dark Orbit - 980,000 hours", body_style))
    story.append(Paragraph("3. Last Kingdom - 875,000 hours", body_style))
    story.append(Paragraph("4. Cosmic Warriors - 720,000 hours", body_style))
    story.append(Paragraph("5. Shadow Hunters - 680,000 hours", body_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Genre Trends
    story.append(Paragraph("GENRE TRENDS:", heading_style))
    story.append(Paragraph("• Sci-Fi grew 15% compared to Q4 2024", body_style))
    story.append(Paragraph("• Drama remains stable with 25% of total views", body_style))
    story.append(Paragraph("• Comedy performance is weak, down 8%", body_style))
    story.append(Paragraph("• Action movies have highest completion rate (78%)", body_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Audience Growth
    story.append(Paragraph("AUDIENCE GROWTH SUMMARY:", heading_style))
    story.append(Paragraph("• Total viewers up 12% from last quarter", body_style))
    story.append(Paragraph("• Premium tier subscribers increased 22%", body_style))
    story.append(Paragraph("• Most growth in 25-34 age group (35% increase)", body_style))
    story.append(Paragraph("• International expansion: UK +30%, Canada +25%", body_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Key KPIs
    story.append(Paragraph("KEY KPIs:", heading_style))
    story.append(Paragraph("• Average watch time: 45 minutes", body_style))
    story.append(Paragraph("• Platform rating: 4.2 stars", body_style))
    story.append(Paragraph("• Subscriber retention: 89%", body_style))
    story.append(Paragraph("• Content library: 150 titles", body_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Regional Highlights
    story.append(Paragraph("REGIONAL HIGHLIGHTS:", heading_style))
    story.append(Paragraph("• New York: 45% of US viewership", body_style))
    story.append(Paragraph("• London: Top international market", body_style))
    story.append(Paragraph("• Berlin: Fastest growing market (40% growth)", body_style))
    
    # Build PDF
    doc.build(story)
    print("✅ Created quarterly_report_q1_2025.pdf")

def create_campaign_report():
    """Create campaign_performance_2025.pdf"""
    print("📄 Creating campaign_performance_2025.pdf")
    
    doc = SimpleDocTemplate(
        "backend/data/pdf_files/campaign_performance_2025.pdf",
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )

    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=12
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6
    )

    # Content
    story = []
    
    # Title
    story.append(Paragraph("CAMPAIGN PERFORMANCE REPORT 2025", title_style))
    story.append(Spacer(1, 0.25*inch))
    
    # Marketing Channels
    story.append(Paragraph("MARKETING CHANNELS USED:", heading_style))
    story.append(Paragraph("• Social Media: 40% of budget ($400,000)", body_style))
    story.append(Paragraph("• YouTube Ads: 25% of budget ($250,000)", body_style))
    story.append(Paragraph("• TV Commercials: 20% of budget ($200,000)", body_style))
    story.append(Paragraph("• Podcast Sponsorships: 10% of budget ($100,000)", body_style))
    story.append(Paragraph("• Email Campaigns: 5% of budget ($50,000)", body_style))
    story.append(Spacer(1, 0.1*inch))
    
    # ROI by Title
    story.append(Paragraph("ROI BY TITLE:", heading_style))
    story.append(Paragraph("• Stellar Run: 300% ROI (Highest)", body_style))
    story.append(Paragraph("• Dark Orbit: 150% ROI", body_style))
    story.append(Paragraph("• Last Kingdom: 120% ROI", body_style))
    story.append(Paragraph("• Other titles average: 80% ROI", body_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Stellar Run Campaign
    story.append(Paragraph("STELLAR RUN CAMPAIGN HIGHLIGHTS:", heading_style))
    story.append(Paragraph("• Largest marketing spend: $500,000", body_style))
    story.append(Paragraph("• Social media engagement: 2.5M impressions", body_style))
    story.append(Paragraph("• YouTube trailer views: 1.8M", body_style))
    story.append(Paragraph("• Most successful channel: TikTok with 800K views", body_style))
    story.append(Paragraph("• Campaign contributed to 40% of Q1 growth", body_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Recommendations
    story.append(Paragraph("RECOMMENDATIONS FOR NEXT QUARTER:", heading_style))
    story.append(Paragraph("1. Increase spend on Stellar Run franchise", body_style))
    story.append(Paragraph("2. Invest more in YouTube and TikTok campaigns", body_style))
    story.append(Paragraph("3. Target comedy genre with specific marketing", body_style))
    story.append(Paragraph("4. Expand international marketing in Europe", body_style))
    story.append(Paragraph("5. Consider influencer partnerships for new releases", body_style))
    
    # Build PDF
    doc.build(story)
    print("✅ Created campaign_performance_2025.pdf")

if __name__ == "__main__":
    print("="*50)
    print("📚 CREATING PDF DOCUMENTS")
    print("="*50)
    create_quarterly_report()
    create_campaign_report()
    print("\n🎉 Both PDF files created successfully!")
    print("📁 Location: backend/data/pdf_files/")