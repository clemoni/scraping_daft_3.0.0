# Scraping Daft

## The genesis of the Project

Lately, my partner, our dog and I had to look for a new place to live in Cork Ireland. Whoever has experienced living in Ireland knows the hassles of such a venture.

Rent runs high for lettings with a quality far from optimal. In November 2021 a deep analysis of the Housing Market has been published by the Irish Government. This study is very complete and provides a deep understanding of the Irish housing market.
I thought it would be interesting to compare their observation with our own findings especially by focusing on an individual aspect through the access to the rental house market.

## The project

People when looking for a house mainly goes to one website Daft.com. There is, unfortunately, no accessible data regarding rent advertisements. The first step of this project was to remedy this by creating a database.

This project runs on Docker, it uses Airflow to run Spark jobs. Basically, for each county, Airflow is used to schedule everyday tasks. It consists of scraping a webpage and persisting the data in a database (PostgreSQL). Every time, the data has been successfully persisted in the database a notification is sent to a dedicated slack channel.

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

## Some Insights

### Docker architecture

### How scraping the adverts for county works: main functionalities

![schema of scraping script](https://github.com/clemoni/scraping_daft_3.0.0/blob/dev/img/scraping_daft_schema.png)

![schema of scraping script](https://github.com/clemoni/scraping_daft_3.0.0/blob/dev/img/scraping_daft_schema_2.png)

### Updating the database, 3 possible outcomes

![3 outcomes](https://github.com/clemoni/scraping_daft_3.0.0/blob/dev/img/dag_example.png)

### Example of a DAG (Directed Acyclic Graph) to scrap adverts

![example of dag](https://github.com/clemoni/scraping_daft_3.0.0/blob/dev/img/dag_example.png)

- **run_init_county**: initialises Xcom with a given county.
- **scrap_data**: where most of the magic happens. The adverts are collected and inserted into a JSON file.
- **waiting_for_file**: FileSensor, wait for the file containing the adverts to be created.
- **persist_data**: compares the collected adverts with the open adverts in the database for this given county.
  - Status “open” in the database but not scraped > they have been removed therefore, they must be closed.
  - “Status “open” in the database and scraped > they are still available on daft.ie, we don’t do anything else.
  - Not available in the datable but scraped > they have been created, they need to be inserted in the database.
- **get_reporting**: triggers a Postgres SQL function that counts the number of adverts closed and inserted in the database for the given country on this day. Inserts the result to Xcom.
- **notify_slack**: reads the Xcom to get the reporting and sent a message to the dedicated Slack channel.
- **remove_file**: delete the file containing the scraped adverts.

## Slack Channel: Ireland Housing Market

To access the slack channel, please click on the following [link](https://join.slack.com/t/irelandhousingmarket/shared_invite/zt-15sa2u18x-r6Cf0wxR2SVC2iF~aiH~XA).
