# Scraping Daft

## The genesis of the Project

Lately, my partner, our dog and I had to look for a new place to live in Cork Ireland. Whoever has experienced living in Ireland know in advance the hassles of such a venture.

Rent runs high for lettings with a quality far from optimal: old electric heater, mould, lack of isolation, etc. Finding a place to live is hard but with a dog on top of that is nearly impossible. The demand runs so high that landlords do not care anymore to let you know when a candidature has been declined. Some don't come to agreed appointments. Some other asks you to pay an extra to be kept in a pool of candidates.

My exasperation ran high and so did my incomprehension regarding these different practices. When this happens, it is always good to try to understand what's going on. Unfortunately, I did not find any data to explore regarding the housing market, therefore, I thought it would be interesting to create one.

## The project

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
