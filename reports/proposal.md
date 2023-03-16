# Proposal: Vancouver Building Permit Summary

#### Authors
- Spencer Gerlach

> Note: this proposal has been modified from the original Group 19 proposal.

#### Date
- 2023-Mar-16

## Motivation and Purpose

Building permits are a source of valuable information about development in Vancouver. They are granted to approve new development, from single family houses to condo buildings, offices, retail and any other changes to private property. Building permits can be used to derive insights about development value (dollar amount), development type (low-, medium-, and high-density), permit fulfillment timelines, and how these factors vary across neighbourhoods.

City of Vancouver staff make building permit data available via the Vancouver Open Data Portal, but the useful information held in the data is not easily accessible for people that lack technical skills or that are unfamiliar with the building permit system. The data is also mostly available at the "project level", with limited funcitonality to filter or aggregate by neighborhood and development type. The open data portal provides some elementary data exploration functionality, but this funcionality is limited. If a more nuanced analysis of the data is required, the user would need to download the data and analyze it themselves.

> I hope to make insights on Vancouver development more accessible to those who depend on them, but are unable to access them due to various technical or other accessiblity constrains.

As such, this dashboard provides an accessible way to access and explore the data in an intuitive and simple way. 

This tool could benefit citizens of Vancouver who wish to be informed of recent and current trends in development, organizations who wish to develop property in the city, or those advocating for social change.

During development of the dashboard, I will assume the role of a City of Vancouver department making a purpose-built tool to deliver these insights to our interested citizens and organizations. 

## Data Description

The [dataset](https://opendata.vancouver.ca/explore/dataset/issued-building-permits/information/) contains one row per building permit approved by the City of Vancouver between 2017 - 2023. It is published in the City’s [Open Data Portal](https://opendata.vancouver.ca/pages/home/) and is updated daily. Each row contains temporal, geographical, numeric, and descriptive data on the project, and the data is mostly complete. Approximately 7,800 of the 35,000 permits are primarily focused on residential development permits for new buildings, which may contain one or more dwelling units. This is the primary development type of interest to our clients, will comprise the majority of data represented on the dashboard.

Ten of the 20 variables in the dataset are of interest:
- `PermitElaspedDays` (Number of days from permit submission to approval)
- `ProjectValue` (Estimated construction cost at the time of the permit issuance in dollars)
- `ProjectDescription` (detailed description of the project, including number of dwelling units)
- `PermitCategory` (type of permit granted – many NAs) 
- `PropertyUse` (general land use type, e.g. Dwelling, Retail, Office)
- `SpecificUseCategory` (specific land use type, e.g. Multiple Dwelling, Laneway House)
- `IssueYear` (the year the permit was issued)
- `GeoLocalArea` (the Vancouver neighbourhood of the development)
- `YearMonth` (the year and month the permit was issued)
- `Geo_point_2d` (lat/lon coordinates)

## Target Personas and Usage Scenarios

My target audience is citizens and organizations that would like to be informed on recent development approvals across the city, and how development varies by neighborhood.

#### User Persona:

Arman is a Vancouverite passionate about the history of development approvals across the city. Arman wants to explore the trends in residential development value, type, and activity (number of planned developments). Ideally, he would be able to explore these trends at both an aggregated citywide level, but also to explore differences in these trends at the neighbourhood level. My dashboard will give Arman a simple interface where he see a little bit of both citywide and neighbourhood level statistics. 

- To get a quick comparison of which neighbourhoods take the longest to get permits approved, or have the highest project values, he can use the bar chart on the top left. This helps him understand which neighbourhoods are easier to get a permit approved in (shorter average approval times), or which neighbourhoods are experiencing the most investment (highest average project value).

- If Arman wants to explore the geospatial nuances between different building permit statistics, he can mouse over the chloropleth map on the right. This map allows Arman to choose his summary statistic of interest and view the results in the map below. He can choose between various statistics for permit approval times and project value, as well as permit counts. Arman is a visual learner, so this is helpful for him to get a sense of the statistics in a spatial manner.

- For example, say Arman lives in West Point Grey, he can then get an idea of the average time it takes to get a building permit approved, or the average value of the development in the neighbourhood. With this information, Arman can make informed decisions about city leadership, and can become more involved in community discussions about current and planned development.

- Finally, if Arman wanted to understand how building permits for high-density developments are trending, he could use the line chart to select various types of high-density development, and see if permit approval counts are increasing, decreasing, or staying constant over time.