# PhonePe
PhonePe Transaction Insights
PhonePe Data Analysis Project

Project Overview
This project involves a comprehensive analysis of PhonePe transaction, Insurance and user data to provide actionable insights for market expansion, user engagement, and growth strategies. The analysis covers state, district, and pin code levels to identify trends, high-performing regions, and opportunities in various domains such as transactions, user registrations, and insurance activities.

The project leverages Python, Streamlit, and MySQL for data extraction, analysis, and visualization.
________________________________________
Table of Contents
•	Project Overview
•	Case Studies
•	Technologies Used
•	Dataset
•	Project Structure
•	Installation
•	Usage
•	Key Findings
•	License
________________________________________
Case Studies
1.	Transaction Analysis for Market Expansion
o	Analyzed state-level transaction dynamics to identify trends, opportunities, and potential areas for market expansion.
2.	User Engagement and Growth Strategy
o	Explored user engagement patterns (app opens, active users) across states and districts to inform growth strategies.
3.	Transaction Analysis Across States and Districts
o	Identified top-performing regions based on transaction volume and value to target marketing efforts effectively.
4.	User Registration Analysis
o	Analyzed user registration data to identify states, districts, and pin codes with the highest number of new users in specific year-quarter combinations.
5.	Insurance Transactions Analysis
o	Examined insurance-related transactions to determine top regions with high insurance activity, aiding strategic decisions in the insurance sector.
________________________________________
Technologies Used
•	Python – Data processing and analysis
•	Streamlit – Interactive web application for visualization
•	MySQL – Data storage and querying
•	Pandas – Data manipulation
•	Plotly – Data visualization
________________________________________
Dataset
•	The project uses publicly available PhonePe Pulse data from GitHub:
          Source: PhonePe Pulse Data

•	This data has been structured to provide details of following three sections with data cuts on Transactions, Users and Insurance of PhonePe Pulse - Explore tab.
1.	Aggregated - Aggregated values of various payment categories as shown under Categories section
2.	Map - Total values at the State and District levels.
3.	Top - Totals of top States / Districts /Pin Codes
________________________________________
Project Structure
PhonePe/
│
├── data/                              # Raw JSON files from PhonePe Pulse
├── scripts/                           # Python scripts for ETL and analysis
│   └── DataExtraction.ipynb
├── streamlit_app/                     # Streamlit application for visualization
│   └── DataVisualisation.py
├── Phonepe_Insights_Recommendation.pdf  # Documentation
├── README.md
└── PhonePay_SqlQuerie.sql             # MySQL schema and sample queries
________________________________________
Installation
1.	Clone the repository:
•	git clone https://github.com/JananiDevarajan-Dev/PhonePe
•	cd PhonePe
2.	Install dependencies:
•	streamlit,Pandas,sqlalchemy,plotly.express
      3.Run the Streamlit app:
          streamlit run DataVisualisation.py
________________________________________
Usage
•	Explore transaction trends by state, district, and pin code.
•	Analyze user registrations and app engagement patterns.
•	Identify high-performing regions for insurance transactions.
•	Interactive visualizations provide actionable insights for strategic decision-making.
________________________________________
Key Findings (Sample)
•	Certain states consistently show high transaction volumes, indicating strong market presence.
•	User engagement patterns vary across districts, highlighting areas for potential growth.
•	Insurance transactions are concentrated in specific regions, suggesting targeted marketing opportunities.
•	Pin code-level analysis enables precise insights for regional strategies.
________________________________________

