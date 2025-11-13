import pandas as pd
import plotly.graph_objects as go
import numpy as np
import taipy.gui.builder as tgb
from taipy.gui import Gui, notify

# Initialize data loading functions (adapt your existing functions)
def load_data(file_path, metric_type):
    """Load data and return both long and wide formats"""
    df = pd.read_csv(file_path)
    # Create wide format - pivot on Year
    df_wide = df.pivot_table(
        index=['Country', 'Product', 'Company'],
        columns='Year',
        values=metric_type,
        aggfunc='sum'
    ).reset_index()
    return df, df_wide

def wide_to_long(df_wide, metric_name):
    """Convert wide format back to long format"""
    text_cols = ['Country', 'Product', 'Company']
    year_cols = [col for col in df_wide.columns if col not in text_cols]
    
    df_long = pd.melt(
        df_wide,
        id_vars=text_cols,
        value_vars=year_cols,
        var_name='Year',
        value_name=metric_name
    )
    df_long['Year'] = df_long['Year'].astype(int)
    return df_long

def create_plot(data, title, latest_year):
    """Create plotly visualization"""
    fig = go.Figure()
    
    # Group by Year and sum sales
    yearly_data = data.groupby('Year')['Sales'].sum().reset_index()
    
    # Split historical and forecast
    historical = yearly_data[yearly_data['Year'] <= latest_year]
    forecast = yearly_data[yearly_data['Year'] >= latest_year]
    
    # Add historical line
    fig.add_trace(go.Scatter(
        x=historical['Year'],
        y=historical['Sales'],
        mode='lines+markers',
        name='Historical',
        line=dict(color='blue', width=2)
    ))
    
    # Add forecast line
    fig.add_trace(go.Scatter(
        x=forecast['Year'],
        y=forecast['Sales'],
        mode='lines+markers',
        name='Forecast',
        line=dict(color='red', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title='Year',
        yaxis_title='Sales',
        hovermode='x unified'
    )
    
    return fig

def create_individual_plot(data, latest_year, metric):
    """Create individual company plots"""
    fig = go.Figure()
    
    companies = data['Company'].unique()
    
    for company in companies:
        company_data = data[data['Company'] == company].groupby('Year')[metric].sum().reset_index()
        
        historical = company_data[company_data['Year'] <= latest_year]
        forecast = company_data[company_data['Year'] >= latest_year]
        
        # Historical
        fig.add_trace(go.Scatter(
            x=historical['Year'],
            y=historical[metric],
            mode='lines+markers',
            name=f'{company} (Historical)',
            line=dict(width=2)
        ))
        
        # Forecast
        if len(forecast) > 0:
            fig.add_trace(go.Scatter(
                x=forecast['Year'],
                y=forecast[metric],
                mode='lines+markers',
                name=f'{company} (Forecast)',
                line=dict(width=2, dash='dash'),
                showlegend=False
            ))
    
    fig.update_layout(
        title=f'{metric} by Company',
        xaxis_title='Year',
        yaxis_title=metric,
        hovermode='x unified'
    )
    
    return fig

# Global variables for Taipy state
min_year = 2020
latest_year = 2023
fcst_year = 2025

# Load initial data
df, df_wide = load_data('./data/mktdata/Unit.csv', 'Unit')
asp_df, asp_wide = load_data('./data/mktdata/ASP.csv', 'ASP')

# Initialize variables
selected_metrics = "Sales"
selected_countries_1 = sorted(df["Country"].unique())[0:1]
selected_products_1 = sorted(df["Product"].unique())[0:1]
selected_companies_1 = sorted(df["Company"].unique())
select_all_companies_1 = True

selected_countries_2 = sorted(df["Country"].unique())[0:1]
selected_products_2 = sorted(df["Product"].unique())[0:1]
selected_companies_2 = sorted(df["Company"].unique())
select_all_companies_2 = True

show_sidebar = True
filter_set_1_expanded = True
filter_set_2_expanded = True

filtered_df_wide = df_wide.copy()
updated_df = pd.read_csv('historical_data.csv')

# Figures
fig1 = go.Figure()
fig2 = go.Figure()
fig3 = go.Figure()
fig4 = go.Figure()
cagr_1 = 0.0
cagr_2 = 0.0

# Callback functions
def on_select_all_1_change(state):
    """Handle select all companies toggle for set 1"""
    if state.select_all_companies_1:
        state.selected_companies_1 = sorted(df["Company"].unique())
    update_visualizations(state)

def on_select_all_2_change(state):
    """Handle select all companies toggle for set 2"""
    if state.select_all_companies_2:
        state.selected_companies_2 = sorted(df["Company"].unique())
    update_visualizations(state)

def on_filter_change(state):
    """Handle any filter change"""
    update_filtered_data(state)
    update_visualizations(state)

def update_filtered_data(state):
    """Update the filtered dataframe for editing"""
    countries_to_show = list(set(state.selected_countries_1 + state.selected_countries_2))
    products_to_show = list(set(state.selected_products_1 + state.selected_products_2))
    companies_to_show = list(set(state.selected_companies_1 + state.selected_companies_2))
    
    state.filtered_df_wide = df_wide[
        df_wide["Country"].isin(countries_to_show) &
        df_wide["Product"].isin(products_to_show) &
        df_wide["Company"].isin(companies_to_show)
    ].copy()

def on_table_edit(state):
    """Handle table edits"""
    # Convert edited data back to long format
    df_long_edited = wide_to_long(state.filtered_df_wide, state.selected_metrics)
    
    # Update the historical data file
    full_df = pd.read_csv('historical_data.csv')
    
    # Update only the edited rows
    for _, row in df_long_edited.iterrows():
        mask = (
            (full_df['Country'] == row['Country']) &
            (full_df['Product'] == row['Product']) &
            (full_df['Company'] == row['Company']) &
            (full_df['Year'] == row['Year'])
        )
        full_df.loc[mask, state.selected_metrics] = row[state.selected_metrics]
    
    # Save updated data
    full_df.to_csv('historical_data.csv', index=False)
    state.updated_df = full_df.copy()
    
    notify(state, "success", "Data updated successfully!")
    update_visualizations(state)

def update_visualizations(state):
    """Update all visualizations based on current filters"""
    # Filter data for visualization 1
    filtered_data_1 = state.updated_df[
        state.updated_df["Country"].isin(state.selected_countries_1) &
        state.updated_df["Product"].isin(state.selected_products_1) &
        state.updated_df["Company"].isin(state.selected_companies_1)
    ]
    
    # Filter data for visualization 2
    filtered_data_2 = state.updated_df[
        state.updated_df["Country"].isin(state.selected_countries_2) &
        state.updated_df["Product"].isin(state.selected_products_2) &
        state.updated_df["Company"].isin(state.selected_companies_2)
    ]
    
    # Calculate CAGR for set 1
    end_sales1 = filtered_data_1[filtered_data_1['Year'] == fcst_year]['Sales'].sum()
    start_sales1 = filtered_data_1[filtered_data_1['Year'] == min_year]['Sales'].sum()
    if start_sales1 > 0:
        state.cagr_1 = round(pow(end_sales1/start_sales1, 1/(fcst_year-min_year)) - 1, 2) * 100
    
    # Calculate CAGR for set 2
    end_sales2 = filtered_data_2[filtered_data_2['Year'] == fcst_year]['Sales'].sum()
    start_sales2 = filtered_data_2[filtered_data_2['Year'] == min_year]['Sales'].sum()
    if start_sales2 > 0:
        state.cagr_2 = round(pow(end_sales2/start_sales2, 1/(fcst_year-min_year)) - 1, 2) * 100
    
    # Create plots
    title_1 = f"Growth Rate from {min_year} to {fcst_year} is {state.cagr_1}%"
    state.fig1 = create_plot(filtered_data_1, title_1, latest_year)
    
    title_2 = f"Growth Rate from {min_year} to {fcst_year} is {state.cagr_2}%"
    state.fig2 = create_plot(filtered_data_2, title_2, latest_year)
    
    state.fig3 = create_individual_plot(filtered_data_2, latest_year, 'Sales')
    state.fig4 = create_individual_plot(filtered_data_2, latest_year, 'MarketShare')

def download_data(state):
    """Trigger download of updated data"""
    notify(state, "info", "Preparing download...")

# Build UI using taipy.gui.builder
with tgb.Page() as page:
    tgb.toggle(theme=True)
    
    tgb.toggle("{show_sidebar}", label="☰ Toggle Filters", on_change=on_filter_change)
    
    with tgb.layout(columns="300px 1" if show_sidebar else "1"):
        # Sidebar
        if show_sidebar:
            with tgb.part(class_name="sidebar"):
                tgb.text("# 🎛️ Filters", mode="md")
                
                tgb.selector(
                    value="{selected_metrics}",
                    lov=["Sales", "MarketShare"],
                    label="Select Metrics",
                    on_change=on_filter_change
                )
                
                tgb.text("---", mode="md")
                
                # Filter Set 1
                with tgb.expandable(title="Filter Set 1", expanded="{filter_set_1_expanded}"):
                    tgb.text("### Countries", mode="md")
                    tgb.selector(
                        value="{selected_countries_1}",
                        lov=sorted(df["Country"].unique()),
                        multiple=True,
                        dropdown=True,
                        label="Countries",
                        on_change=on_filter_change
                    )
                    
                    tgb.text("### Products", mode="md")
                    tgb.selector(
                        value="{selected_products_1}",
                        lov=sorted(df["Product"].unique()),
                        multiple=True,
                        dropdown=True,
                        label="Products",
                        on_change=on_filter_change
                    )
                    
                    tgb.text("### Companies", mode="md")
                    tgb.toggle(
                        value="{select_all_companies_1}",
                        label="Select All Companies",
                        on_change=on_select_all_1_change
                    )
                    
                    tgb.selector(
                        value="{selected_companies_1}",
                        lov=sorted(df["Company"].unique()),
                        multiple=True,
                        dropdown=True,
                        label="Companies",
                        active="{not select_all_companies_1}",
                        on_change=on_filter_change
                    )
                
                tgb.text("---", mode="md")
                
                # Filter Set 2
                with tgb.expandable(title="Filter Set 2", expanded="{filter_set_2_expanded}"):
                    tgb.text("### Countries", mode="md")
                    tgb.selector(
                        value="{selected_countries_2}",
                        lov=sorted(df["Country"].unique()),
                        multiple=True,
                        dropdown=True,
                        label="Countries",
                        on_change=on_filter_change
                    )
                    
                    tgb.text("### Products", mode="md")
                    tgb.selector(
                        value="{selected_products_2}",
                        lov=sorted(df["Product"].unique()),
                        multiple=True,
                        dropdown=True,
                        label="Products",
                        on_change=on_filter_change
                    )
                    
                    tgb.text("### Companies", mode="md")
                    tgb.toggle(
                        value="{select_all_companies_2}",
                        label="Select All Companies",
                        on_change=on_select_all_2_change
                    )
                    
                    tgb.selector(
                        value="{selected_companies_2}",
                        lov=sorted(df["Company"].unique()),
                        multiple=True,
                        dropdown=True,
                        label="Companies",
                        active="{not select_all_companies_2}",
                        on_change=on_filter_change
                    )
        
        # Main Content
        with tgb.part(class_name="main-content"):
            tgb.text("# 📊 Market Data Analysis & Forecasting", mode="md")
            
            tgb.text("## Edit Forecast Data", mode="md")
            tgb.table(
                data="{filtered_df_wide}",
                editable=True,
                on_edit=on_table_edit,
                width="100%",
                page_size=20
            )
            
            tgb.text("---", mode="md")
            tgb.text("## 📈 Visualizations", mode="md")
            
            with tgb.layout(columns="1 1"):
                with tgb.part():
                    tgb.text("### Sales Visualization 1", mode="md")
                    tgb.text("**Growth Rate: {cagr_1}%**", mode="md")
                    tgb.chart(figure="{fig1}")
                
                with tgb.part():
                    tgb.text("### Sales Visualization 2", mode="md")
                    tgb.text("**Growth Rate: {cagr_2}%**", mode="md")
                    tgb.chart(figure="{fig2}")
            
            with tgb.layout(columns="1 1"):
                with tgb.part():
                    tgb.text("### Sales by Company", mode="md")
                    tgb.chart(figure="{fig3}")
                
                with tgb.part():
                    tgb.text("### Market Share by Company", mode="md")
                    tgb.chart(figure="{fig4}")
            
            tgb.text("---", mode="md")
            tgb.text("## 💾 Download Data", mode="md")
            
            tgb.file_download(
                content="{updated_df}",
                label="Download Updated Data",
                name="Updated_Forecast_Data.csv",
                on_action=download_data
            )

if __name__ == "__main__":
    gui = Gui(page, css_file="style.css")
    gui.run(
        title="Market Data Analysis",
        port=5000,
        debug=True,
        use_reloader=True
    )


    ---------------------------------
    /* style.css */
.sidebar {
    background-color: #f8f9fa;
    padding: 20px;
    height: 100vh;
    overflow-y: auto;
    border-right: 1px solid #dee2e6;
}

.main-content {
    padding: 20px;
    overflow-y: auto;
}

.taipy-expandable {
    margin-bottom: 15px;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 10px;
}