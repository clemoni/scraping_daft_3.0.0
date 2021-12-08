from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool


def init_select(path, pool_size=1, max_overflow=7):
    engine = create_engine(path,
                           poolclass=QueuePool,
                           pool_size=pool_size,
                           max_overflow=max_overflow)

    def init_stmt(stmt):

        def run_sql(**kwargs):
            try:

                conn = engine.connect()
                exp = text(stmt)
                caching = conn.execute(exp, kwargs)
                return caching

            except Exception as e:
                return f"There was an error: {e}"
            finally:
                conn.close()

        return run_sql

    return init_stmt


def init_insert(path):
    engine = create_engine(path)
    conn = engine.connect()
    transaction = conn.begin()

    def init_stmt(stmt):
        exp = stmt

        def run_insert(records):
            try:
                stmt = text(exp)
                for record in records:
                    conn.execute(stmt, **record)
                transaction.commit()

            except Exception as e:
                print(f"Transaction failed! {e}")
                transaction.rollback()

            finally:
                conn.close()
        return run_insert
    return init_stmt


def insert_data_plus(path, stmt, records):
    engine = create_engine(path)
    conn = engine.connect()
    transaction = conn.begin()

    try:
        stmt = text(stmt)
        for record in records:
            conn.execute(stmt, **record)
        transaction.commit()

    except Exception as e:
        print(e)
        print("Transaction failed! Rolling back")
        transaction.rollback()

    finally:
        conn.close()


# db_daft = init_select('postgresql://localhost/scraping_daft')

# stnt_acounty_warea = 'SELECT COUNT(*) FROM county WHERE area > :area LIMIT 1'
# couty_area_over_4000 = db_daft(stnt_acounty_warea, area=4000)
# print(couty_area_over_4000()[0][0])
# print(couty_area_over_4000()[0][0])
# couty_area_over_2000 = db_daft(stnt_acounty_warea, area=2000)
# print(couty_area_over_2000()[0][0])
