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
        SELECT from_address,to_address
        FROM `bigquery-public-data.crypto_ethereum.transactions`
        WHERE to_address IN ("0xdafea492d9c6733ae3d56b7ed1adb60692c98bc5","0xfd0a9fa2c6ead612fb15d4216947467637be98f2","0xd60b07ba7d9dacca5ba62d45de66b6597aaaac4e","0xe9c2d3bf3a898f700cade5f5f4a89a5e5756f4e4","0x7e46f6f93ce730c93e92e72304b193589aaa3f50","0xcb26cc0c396e1712c3da71a248c3e9b1767fcb65","0x68721714c9591eb349711a50933105c70fb9cbf8","0xcd74c0cf3f0778cea9e24faed624d37e220d7a56","0x6a5bc5fcbbee5bb8e55bf1df8efdbc36a5cf65b8","0xe0e4fb03a802dd3f7ee71c3e32acb96a4070e230","0xbaa82dc5cf1617fa8f180988fd6db589f16c6081","0x51623f990d65b782e5a658e693dd8a5f851e9670","0xcb62f9154b26672ef948281c2d14aa54bbba3e96","0xdfad8c8a6172d33b95038ec5bb067239b71f70d0","0xbf69274744a8458f31df0d1e4261b456e0cc5b69","0x1eb47e1dfa185ec847e411f66c071a5cc1f29f18","0x958a4504e6f95619748c931193b87192bcfb6037","0x684149553c22b223da8d324eb59309aa78fde225","0xe6573b88261e5d981cc720fb60184c314648978a","0xa1f408cb73288d8a23ee2ad158e663e690e462b5") and
        DATE(block_timestamp) BETWEEN "2023-04-10" AND "2023-04-26" ;         
        """
    )

    results = query_job.result()  # Waits for job to complete.

    # for row in results:
    #     print("{} : {} ".format(row.to_address,row.from_address))
    with open('test_gcp2.txt', 'w') as f:
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