Report on Developing the Smart Assistant with MongoDB and Streamlit
1. Setting Up the Environment
The project began with selecting the required tools and technologies to build the smart assistant. The core tools used were:

MongoDB: For storing procurement data in an organized way that can be easily queried.
Streamlit: To build the interactive user interface for visualizing and interacting with the data.
Python: The main programming language used to write the code, with libraries like pandas and matplotlib used for data manipulation and visualization.
2. Setting Up the MongoDB Database
MongoDB was set up to store data related to procurement, which includes information about items, suppliers, quantities, and prices.
Data was organized in collections within the MongoDB database, and aggregation queries were written to retrieve data based on year, quarter, supplier, and items.
3. Developing the User Interface with Streamlit
The user interface was developed using Streamlit to allow users to interact with the data and visualize it in an intuitive way. Several interactive components were added to make it easier to explore the data.

Key Features of the Interface:
Year and Quarter Selection: A dropdown menu was provided for users to select a specific year and quarter to view data.
Displaying Total Spending: The total spending for the selected year and quarter is shown using a bar chart.
Time Series Analysis: A line chart was added to show spending trends over the years.
Top Suppliers: A pie chart was added to show the distribution of orders among the top suppliers.
4. Interacting with the Smart Assistant using Dynamic Queries
One of the key features of the smart assistant is the ability to interact with it through a chatbot interface. Users can ask questions, and the assistant will query the database and provide answers.

Total Spending: Queries were written to calculate the total spending for a given year and quarter, and these results are displayed in a table and graph.
Top Suppliers: The assistant queries the database to list the top suppliers based on order count for a given time period.
Most Frequently Ordered Items: The assistant retrieves and displays the top 10 most frequently ordered items by quantity.
5. Using Jupyter Notebooks for Data Analysis
Jupyter Notebooks were used for analyzing the data and preparing the aggregation queries. The process included:

Fetching data from MongoDB using aggregation queries to sum total spending per quarter or group data by supplier or item.
Using pandas to convert the data into a DataFrame, which made it easy to process and display.
6. Interactive Visualizations Using Streamlit
Interactive visualizations were created using matplotlib and Streamlit to allow users to easily view and analyze the data:

Bar Chart: Displayed total spending by quarter.
Pie Chart: Showed the distribution of orders among the top suppliers.
Line Chart: Tracked spending over time to identify trends.
7. Error Handling and Solutions
Throughout the development of the assistant, several common challenges were encountered:

Managing Large Datasets: Handling large datasets in MongoDB required optimizing the aggregation queries to ensure efficient retrieval.
Integrating Streamlit with MongoDB: There was a need to integrate Streamlit seamlessly with MongoDB so that the user could interact with real-time data.
8. Enhancing User Interaction and Interface Design
The user interface was designed to be user-friendly, with enhancements such as:

Dropdown menus for selecting year and quarter, making it easier for users to filter and navigate the data.
Displaying detailed data in tables so users could view specific information related to spending, suppliers, and items.
9. Final Results and Outcomes
The smart assistant was successfully developed using MongoDB and Streamlit. The system allows the user to:

View total spending by quarter and year.
Display spending distribution among top suppliers.
Analyze the top 10 most frequently ordered items.
The assistant also provides interactive charts that help visualize trends in spending, supplier contributions, and item purchases.

10. Model Results:
During the analysis, the following models were used to aggregate and display data:

Time Series Model: Aggregated total spending for each quarter, resulting in a line chart showing how spending has changed over time.

Results:

The total spending trend shows periodic spikes in certain quarters, particularly in Q4 of each year, indicating higher procurement activity during the end of the fiscal year.
Top Suppliers Model: Aggregated the total number of orders for each supplier, resulting in a pie chart of the top 5 suppliers.

Results:

The top 5 suppliers by order count were highlighted, with Supplier A receiving the highest number of orders, followed by Supplier B and others. This helps identify the most reliable and frequently used suppliers.
Most Frequently Ordered Items Model: Aggregated the total quantity ordered for each item, showing the top 10 most frequently ordered items.

Results:

Item X emerged as the most ordered item, followed by Item Y and others. This information can be useful for analyzing demand and procurement strategies.
11. Future Recommendations:
Improve User Interface: More filters and sorting options could be added to allow users to drill down into the data even further.
Add More Reports: Future versions of the assistant could include additional reports such as cost analysis by product category, or predictive analytics for future procurement based on historical trends.
