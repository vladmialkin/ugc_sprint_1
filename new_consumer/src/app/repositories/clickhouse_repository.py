from aiochclient import ChClient


class ClickHouseRepository:
    def __init__(self, client: ChClient):
        self.client = client

    async def save_data(self, data: dict):
        await self.client.execute('CREATE DATABASE IF NOT EXISTS test ON CLUSTER company_cluster')
        await self.client.execute(
            'CREATE TABLE IF NOT EXISTS test.new_table ON CLUSTER company_cluster (id Int64, name String, year Int8) Engine=MergeTree() ORDER BY id')
        await self.client.execute('INSERT INTO test.new_table (id, name,  year) VALUES',
                                  (data["id"], data["name"], data["year"]),
                                  )
        rows = await self.client.fetchrow('SELECT * FROM test.new_table')
        for row in rows.items():
            print(row)
        return rows

    async def get_data(self):
        data = await self.client.fetchrow('SELECT * FROM test.new_table')
        for val in data.values():
            print(val)
        return data
