# Research Proposal

Data science as a nascent academic field grows rapidly in many directions, and
its understanding vastly differs depending on each individual and each
organization. Such lack of common understanding veils the shared goal among data
science institutions and hampers their potential collaborative effort.

The goal of this research project is to better understand what data science is
by observing what data science institutions do and by doing so, to coordinate
and improve research collaboration between data science institutions based on
their strength and weakness. Furthermore, this project simplifies comparing data
science ecosystems between universities by automating the characterization process.

# TODOs

## data collection
### web-scraper
- build Naive Bayes to filter out unncessary websites
- collect enough information for data analysis stage

## data analysis
### LDA algorithm
- build LDA 
- AWS to improve performance

## data visualization
### graph
- use D3.js to visualize the ecosystem
  - each node represents a data science institution
    - color-coded to represent the type of data science institution
    - size to represent the significance of institution
  - each link represent the collaboration between two institutions 
    - width of the link represent the strength of the tie 
    - lack of the link between two nodes should indicate the lack of collaboration
