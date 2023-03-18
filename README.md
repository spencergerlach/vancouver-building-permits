# Vancouver Building Permit Explorer

- Link to app: **https://vancouver-building-permits-ia.onrender.com**

## Proposal Document

The proposal for this dashboard is a modified version of a proposal written for a group project dashboard (DSCI 532 Group 19). The updated proposal can be found [here](https://github.com/spencergerlach/vancouver-building-permits/blob/main/reports/proposal.md)

This dashboard uses the same data that the [original group project](https://github.com/UBC-MDS/dsci532-group19-buildingpermits) did. However, two different visuals have been used. I have kept the chloropleth map, as it was a learning opportunity for me to create a chloropleth map within a Dash app.

## Usage

- There are multiple ways users can interact with the app. Below is a high-level overview of the intended app usage.

### Neighbourhood Bar Chart

- Users are invited to use the dropdown menu to choose either Permit Elapsed Days (i.e. days elapsed before permit approved) or Project Value (i.e. construction value in CAD). Based on the selection, users will be able to see a comparison of mean values for each Vancouver neighbourhood.

### Neighbourhood Chloropleth Map

- If users are interested in exploring the spatial differences in neighbourhood summary statistics, they should use this map. This map allows users to select various descriptive summary statistics about the building permit data from the drop down menu. After selection, users can mouse over the map to see these values for each neighbourhood. A legend is provided for convenience and overall spatial comparison.

### Permit Count Line Chart

- Finally, if users are interested in the trends of building permit approvals for specific building types, this chart will be helpful for them. Users can select one or multiple building types, and the chart below will show users how the count of permit approvals has changed over time.

### More Information

- Users can find links to more information about Vancouver's building permit process, or the building permit data.

## Reference

Data for this project was retrieved from the [Vancouver Open Data Portal](https://opendata.vancouver.ca/explore/dataset/issued-building-permits/information/)

## License

Licensed under the terms of the MIT License.