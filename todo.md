
# Data Collection:

1. limit to 1000 webpages per website (**Don**)
2. run scrapy on the ScrapingHub to collect two kinds of data (**Alvin**)
    1. hyperlinks between websites (implemented)
    2. texts per websites (**Don**)

# Data Cleansing:

1. Remove irrelevant websites (Jenkins) -> Naive Bayes to filter based on words (**Don**)
OR
2. Find the source of institution descriptions (very difficult) 

# Data Analysis & Visualization:

- For hyperlinks
    - visualization: D3.js (**Vinitra**)
          - each node represents a data science institution
            - color-coded to represent the type of data science institution
            - size to represent the significance of institution
          - each link represent the collaboration between two institutions 
            - width of the link represent the strength of the tie 
            - lack of the link between two nodes should indicate the lack of collaboration
    - network analysis

- For texts
    - classification: build LDA in Apache Spark (**Louie** and **Don**)
    - visualization: Word cloud for each bucket 
    - performance: AWS EC2 instance (**Alvin**)




