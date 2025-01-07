from google.cloud import bigquery
from google.cloud import storage
import io
import time

start_time = time.time()
client =  bigquery.Client.from_service_account_json('service_account.json')

        # """
        # SELECT to_address,from_address 
        # FROM `woven-patrol-384204.NewETHTable01.eth_oneday_18_19_data` 
        # LIMIT 100;
        # """
def query_stack(client):
    query_job = client.query(
        """  
            SELECT from_address,count(*) as trans_count
            FROM `bigquery-public-data.crypto_ethereum.transactions`
            WHERE DATE(block_timestamp) BETWEEN "2023-07-01" AND "2023-10-30"
            GROUP BY from_address
            ORDER BY
                trans_count DESC;
        """
    )

    results = query_job.result()  # Waits for job to complete.

    # for row in results:
    #     print("{} : {} ".format(row.to_address,row.from_address))
    with open('ETH_from_Addred_3month.txt', 'w') as f:
        for row in results:
            f.write("%s\n" % str(row))

def test_extract_schema(client): 
    # project = 'woven-patrol-384204'
    # dataset_id = 'NewETHTable01'
    # table_id = 'eth_oneday_18_19_data'

    project = 'bigquery-public-data'
    dataset_id = 'crypto_ethereum'
    table_id = 'transactions'

    dataset_ref = client.dataset(dataset_id, project=project)
    table_ref = dataset_ref.table(table_id)
    table = client.get_table(table_ref)  # API Request
    f = io.StringIO("")
    client.schema_to_json(table.schema, f)
    print(f.getvalue())

    # View table properties
    result = ["{0} {1}".format(schema.name,schema.field_type) for schema in table.schema]

    print(result)

if __name__ == '__main__':
    print("Start time : ",start_time)
    query_stack(client)
    print("--- %s seconds ---" % (time.time() - start_time))

    #test_extract_schema(client)