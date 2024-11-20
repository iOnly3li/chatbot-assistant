import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient
import io

# Set up MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['procurement_db']
collection = db['purchases']

# Function to fetch data from MongoDB
def fetch_data(query):
    result = collection.aggregate(query)
    return list(result)

# Streamlit Interface
st.title("Procurement Dashboard")
st.sidebar.header("Select Query")

# 1. Year and Quarter Selection
years = ['2012', '2013', '2014', '2015', 'All Years']
quarters = ['Q1', 'Q2', 'Q3', 'Q4', 'All Quarters']
selected_year = st.sidebar.selectbox("Select Year", years)
selected_quarter = st.sidebar.selectbox("Select Quarter", quarters)

if st.sidebar.button("Generate Report"):
    # Query based on selected year and quarter
    if selected_year == 'All Years' and selected_quarter == 'All Quarters':
        query = [
            {"$group": {"_id": "$Quarter", "total_spending": {"$sum": "$Total Price"}}},
            {"$sort": {"_id": 1}}
        ]
        st.write("Showing data for all years and all quarters.")
    elif selected_year != 'All Years' and selected_quarter == 'All Quarters':
        query = [
            {"$match": {"Quarter": {"$regex": f"^{selected_year}"}}},  # Filter by year
            {"$group": {"_id": "$Quarter", "total_spending": {"$sum": "$Total Price"}}},
            {"$sort": {"_id": 1}}
        ]
        st.write(f"Showing data for {selected_year}, all quarters.")
    elif selected_year == 'All Years' and selected_quarter != 'All Quarters':
        query = [
            {"$match": {"Quarter": f"{selected_quarter}"}},  # Filter by quarter
            {"$group": {"_id": "$Quarter", "total_spending": {"$sum": "$Total Price"}}},
            {"$sort": {"_id": 1}}
        ]
        st.write(f"Showing data for all years, {selected_quarter}.")
    else:
        query = [
            {"$match": {"Quarter": f"{selected_year}{selected_quarter}"}} ,
            {"$group": {"_id": "$Quarter", "total_spending": {"$sum": "$Total Price"}}}
        ]
        st.write(f"Showing data for {selected_year} {selected_quarter}.")

    # Fetching and displaying data based on the dynamic query
    data = fetch_data(query)
    if data:
        df = pd.DataFrame(data)
        st.write(f"Total spending for {selected_year} {selected_quarter}: ${data[0]['total_spending']:.2f}")
        st.dataframe(df)

        # 2. Visualize the spending with a bar chart
        st.write("Spending by Quarter")
        st.bar_chart(df.set_index('_id')['total_spending'])

        # 3. Top Suppliers for selected Quarter/Year
        supplier_query = [
            {"$match": {"Quarter": f"{selected_year}{selected_quarter}"}} ,
            {"$group": {"_id": "$Supplier Name", "order_count": {"$sum": 1}}} ,
            {"$sort": {"order_count": -1}} ,
            {"$limit": 10}
        ]
        supplier_data = fetch_data(supplier_query)
        st.write("Top 10 Suppliers by Order Count:")
        for supplier in supplier_data:
            st.write(f"Supplier: {supplier['_id']}, Orders: {supplier['order_count']}")

        # 4. Breakdown of Items Purchased in the Selected Quarter/Year
        item_query = [
            {"$match": {"Quarter": f"{selected_year}{selected_quarter}"}} ,
            {"$group": {"_id": "$Item Name", "total_quantity": {"$sum": "$Quantity"}}} ,
            {"$sort": {"total_quantity": -1}} ,
            {"$limit": 10}
        ]
        item_data = fetch_data(item_query)
        st.write("Top 10 Items by Quantity:")
        for item in item_data:
            st.write(f"Item: {item['_id']}, Total Quantity: {item['total_quantity']}")

    else:
        st.write("No data found for the selected filters.")

# 3. Chatbot Interface for Dynamic Querying
st.sidebar.header("Ask a Me")
user_query = st.sidebar.text_input("Type your question here:")

if st.sidebar.button("Submit"):
    if "time series analysis" in user_query.lower():  # Check if the query is asking for time series analysis
        # Perform Time Series Query
        time_series_query = [
            {"$group": {"_id": "$Quarter", "total_spending": {"$sum": "$Total Price"}}} ,
            {"$sort": {"_id": 1}}
        ]
        time_series_data = fetch_data(time_series_query)
        time_series_df = pd.DataFrame(time_series_data)
        st.write("Time Series Analysis of Spending")
        st.line_chart(time_series_df.set_index('_id')['total_spending'])

    elif "pie chart" in user_query.lower():  # Check if the query is asking for a pie chart
        # Perform Pie Chart Query for Top Suppliers
        supplier_query = [
            {"$group": {"_id": "$Supplier Name", "order_count": {"$sum": 1}}} ,
            {"$sort": {"order_count": -1}} ,
            {"$limit": 5}
        ]
        supplier_data = fetch_data(supplier_query)
        df = pd.DataFrame(supplier_data)
        st.write("Top 5 Suppliers by Order Count (Pie Chart)")

        # Generate Pie Chart for the Top Suppliers
        fig = df.set_index('_id').plot.pie(y='order_count', autopct='%1.1f%%', legend=False).get_figure()
        fig.legend(loc='upper left', bbox_to_anchor=(1, 1))  # Move the legend to the right
        st.pyplot(fig)

    elif "total spending" in user_query.lower():
        year = selected_year
        quarter = selected_quarter
        query = [
            {"$match": {"Quarter": f"{year}{quarter}"}} ,
            {"$group": {"_id": "$Quarter", "total_spending": {"$sum": "$Total Price"}}}
        ]
        data = fetch_data(query)
        if data:
            st.write(f"Total spending for {year} {quarter}: ${data[0]['total_spending']:.2f}")
        else:
            st.write("No data available for the selected quarter.")
    elif "top supplier" in user_query.lower():
        query = [
            {"$group": {"_id": "$Supplier Name", "order_count": {"$sum": 1}}} ,
            {"$sort": {"order_count": -1}} ,
            {"$limit": 5}
        ]
        data = fetch_data(query)
        st.write("Top 5 Suppliers by Order Count:")
        for supplier in data:
            st.write(f"Supplier: {supplier['_id']}, Orders: {supplier['order_count']}")
    elif "most frequently ordered items" in user_query.lower():
        if "q4" in user_query and "2014" in user_query:
            query = [
                {"$match": {"Quarter": "2014Q4"}} ,
                {"$group": {"_id": "$Item Name", "total_quantity": {"$sum": "$Quantity"}}} ,
                {"$sort": {"total_quantity": -1}} ,
                {"$limit": 10}
            ]
            data = fetch_data(query)
            st.write("Top 10 Items Ordered in Q4 2014:")
            for item in data:
                st.write(f"Item: {item['_id']}, Quantity: {item['total_quantity']}")
        else:
            st.write("Sorry, I can't process that query yet.")
    elif "highest spending quarter" in user_query.lower():
        query = [
            {"$group": {"_id": "$Quarter", "total_spending": {"$sum": "$Total Price"}}},
            {"$sort": {"total_spending": -1}},
            {"$limit": 1}
        ]
        data = fetch_data(query)
        if data:
            st.write(f"The highest spending quarter is {data[0]['_id']} with a total spending of ${data[0]['total_spending']:.2f}")
    elif "total orders" in user_query.lower():
        query = [
            {"$match": {"Quarter": f"{selected_year}{selected_quarter}"}} ,
            {"$group": {"_id": "$Quarter", "total_orders": {"$sum": 1}}}
        ]
        data = fetch_data(query)
        if data:
            st.write(f"Total number of orders for {selected_year} {selected_quarter}: {data[0]['total_orders']}")
    elif "acquisition type" in user_query.lower():
        query = [
            {"$match": {"Acquisition Type": {"$exists": True}}} ,
            {"$group": {"_id": "$Acquisition Type", "total_spending": {"$sum": "$Total Price"}}}
        ]
        data = fetch_data(query)
        st.write("Total spending by Acquisition Type:")
        for entry in data:
            st.write(f"Acquisition Type: {entry['_id']}, Total Spending: ${entry['total_spending']:.2f}")
    elif "fiscal year" in user_query.lower():
        query = [
            {"$match": {"Fiscal Year": {"$exists": True}}} ,
            {"$group": {"_id": "$Fiscal Year", "total_spending": {"$sum": "$Total Price"}}}
        ]
        data = fetch_data(query)
        st.write("Total spending by Fiscal Year:")
        for entry in data:
            st.write(f"Fiscal Year: {entry['_id']}, Total Spending: ${entry['total_spending']:.2f}")
    elif "lpa number" in user_query.lower():
        query = [
            {"$match": {"LPA Number": {"$exists": True}}} ,
            {"$group": {"_id": "$LPA Number", "total_spending": {"$sum": "$Total Price"}}}
        ]
        data = fetch_data(query)
        st.write("Total spending by LPA Number:")
        for entry in data:
            st.write(f"LPA Number: {entry['_id']}, Total Spending: ${entry['total_spending']:.2f}")
    else:
        st.write("Sorry, I can't process that query yet.")

# 4. Download CSV Reports
st.sidebar.subheader("Download Reports")
if st.sidebar.button("Download CSV Report"):
    query = [{"$project": {"_id": 0}}]  # Adjust query as needed
    data = fetch_data(query)
    df = pd.DataFrame(data)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='report.csv',
        mime='text/csv',
    )
