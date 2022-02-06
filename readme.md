# Scraping Daft

## The genesis of the Project

Lately, my partner, our dog and I had to look for a new place to live in Cork Ireland. Whoever has experienced living in Ireland knows the hassles of such a venture.

Rent runs high for lettings with a quality far from optimal. Lately, a deep analysis of the Housing Market has been published by the Irish Government. [This study](file:///Users/clementliscoet/Downloads/205477_d744837d-8f03-4ff0-82dd-4763df823c95.pdf) is very complete and provides a deep understanding of the Irish housing market. 
I thought it would be interesting to compare their observations with our own findings especially by focusing on an individual aspect by observing the access to the rental house market.

## The project

There is no public accessible data regarding rent advertismebts
It happens that almost all Ireland letting advertisement is centralised to one place, daft.com, a website owned by Distilled SCH. As it wasn't possible to access daft.com database, it had to create one. Hence, this project.

This project runs on Docker, it uses Airflow to run Spark jobs. Basically, for each country, Airflow is used to schedule everyday tasks that consist of scraping a webpage and persisting the data in a database (Postgres). Every time, the data has been successfully persisted in the database a notification is sent to a dedicated slack channel. In a later phase, the data would be used for analysis.

## Running the Project

### Instruction

#### Initiating the Project

```linux
sh init-project.sh
```

#### Stopping the project

```linux
sh kill-project.sh
```
