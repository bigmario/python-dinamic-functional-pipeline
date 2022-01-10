from connection.db_conn import ConnectionMongo


class CriteriaRepo(ConnectionMongo):
    def __init__(self):
        super().__init__()

    def get_customer_from_id(self, customer_id_list):
        match_stage = {"$match": {"_id": {"$in": customer_id_list}}}

        lookup_stage = {
            "$lookup": {
                "from": "pms",
                "localField": "_id",
                "foreignField": "customer_id",
                "as": "pms_details",
            }
        }

        pipeline = [match_stage, lookup_stage]

        result = self.customer.aggregate(pipeline)

        return result
