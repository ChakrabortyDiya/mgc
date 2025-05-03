import logging
from pymongo.collection import Collection

# Configure logging if not already configured
logging.basicConfig(level=logging.INFO)

# Mapping for new metric names to MongoDB document keys.
METRIC_MAP = {
    "wacr": "compression_ratio",
    "compression size": "compressed_size",
    "total compression time": "compression_time",
    "peak compression memory": "compression_memory",
    "total compression memory": "compression_memory",
    "peak compression cpu usage": "compression_cpu",
    "total compression cpu usage": "compression_cpu",
    "total decompression time": "decompression_time",
    "peak decompression memory": "decompression_memory",
    "total decompression memory": "decompression_memory",
    "peak decompression cpu usage": "decompression_cpu",
    "total decompression cpu usage": "decompression_cpu",
}

class DashboardService:
    @staticmethod
    def fetch_grouped_results(collection: Collection, input_data) -> list:
        """
        Fetches grouped results from a MongoDB collection based on input_data.
        Expects input_data to have:
          - id: list of dataset IDs
          - comp_type: list of flags (e.g., [1, 0]) mapping to comp types (0 -> standard, 1 -> proposed)
          - standard_comp_name: list of standard compressor names
          - proposed_comp_name: list of proposed compressor names
          - metric: list of metrics (string) to be fetched
        """
        results = []

        try:
            # Map comp_type index to type string.
            comp_type_map = {0: "standard", 1: "proposed"}
            selected_types = [comp_type_map[i]
                              for i, flag in enumerate(input_data.comp_type) if flag == 1]
        except Exception as e:
            logging.error("Error processing comp_type mapping: %s", e, exc_info=True)
            return results  # Return empty results or re-raise exception if needed

        # Loop over each dataset.
        for dataset_id in input_data.id:
            # Process standard compressors.
            if "standard" in selected_types:
                for comp_name in input_data.standard_comp_name:
                    if comp_name:  # Skip if None or empty string.
                        DashboardService._process_query(
                            collection, dataset_id, comp_name, "standard", input_data.metric, results
                        )
            # Process proposed compressors.
            if "proposed" in selected_types:
                for comp_name in input_data.proposed_comp_name:
                    if comp_name:
                        DashboardService._process_query(
                            collection, dataset_id, comp_name, "proposed", input_data.metric, results
                        )

        return results

    @staticmethod
    def _process_query(collection: Collection, dataset_id, comp_name, comp_type_str, metrics, results: list):
        try:
            # Build the query filter.
            query_filter = {
                "dataset_id": dataset_id,
                "compressor": comp_name,
                "compressor_type": comp_type_str
            }
            # Fetch matching documents.
            docs = list(collection.find(query_filter))
        except Exception as e:
            logging.error("Database query failed for dataset_id %s, compressor %s, type %s: %s",
                          dataset_id, comp_name, comp_type_str, e, exc_info=True)
            return

        if not docs:
            logging.info("No results found for dataset_id %s, compressor %s, type %s",
                         dataset_id, comp_name, comp_type_str)
            return

        result_dict = {
            "dataset_id": dataset_id,
            "compressor": comp_name,
            "compressor_type": comp_type_str
        }

        for metric in metrics:
            try:
                # Normalize the metric key.
                metric_key = metric.lower().strip()
                db_field = METRIC_MAP.get(metric_key)
                if not db_field:
                    result_dict[metric] = None
                    continue

                # Compute the desired value based on the metric type.
                values = [doc.get(db_field, 0) for doc in docs if doc.get(db_field) is not None]
                if not values:
                    result_dict[metric] = None
                elif "peak" in metric_key:
                    result_dict[metric] = max(values)
                elif "total" in metric_key:
                    result_dict[metric] = sum(values)
                else:
                    # Fallback: take the first document's value.
                    result_dict[metric] = values[0]
            except Exception as e:
                logging.error("Error processing metric '%s' for dataset_id %s, compressor %s: %s",
                              metric, dataset_id, comp_name, e, exc_info=True)
                result_dict[metric] = None

        results.append(result_dict)



# import logging
# from sqlalchemy.orm import Session
# from database.models import ResultComparison
# from sqlalchemy import and_

# # Configure logging if not already configured
# logging.basicConfig(level=logging.INFO)

# # Mapping for new metric names to DB columns
# METRIC_MAP = {
#     "wacr": "compression_ratio",
#     "compression size": "compressed_size",
#     "total compression time": "compression_time",
#     "peak compression memory": "compression_memory",
#     "total compression memory": "compression_memory",
#     "peak compression cpu usage": "compression_cpu",
#     "total compression cpu usage": "compression_cpu",
#     "total decompression time": "decompression_time",
#     "peak decompression memory": "decompression_memory",
#     "total decompression memory": "decompression_memory",
#     "peak decompression cpu usage": "decompression_cpu",
#     "total decompression cpu usage": "decompression_cpu",
# }

# class DashboardService:
#     @staticmethod
#     def fetch_grouped_results(db: Session, input_data):
#         results = []

#         try:
#             # Map comp_type list index to type string
#             comp_type_map = {0: "standard", 1: "proposed"}
#             selected_types = [comp_type_map[i]
#                               for i, flag in enumerate(input_data.comp_type) if flag == 1]
#         except Exception as e:
#             logging.error("Error processing comp_type mapping: %s", e, exc_info=True)
#             return results  # Return empty results or re-raise exception if needed

#         for dataset_id in input_data.id:
#             # Handle standard compressors
#             if "standard" in selected_types:
#                 for comp_name in input_data.standard_comp_name:
#                     if comp_name:  # skip if None or empty string
#                         DashboardService._process_query(
#                             db, dataset_id, comp_name, "standard", input_data.metric, results
#                         )

#             # Handle proposed compressors
#             if "proposed" in selected_types:
#                 for comp_name in input_data.proposed_comp_name:
#                     if comp_name:
#                         DashboardService._process_query(
#                             db, dataset_id, comp_name, "proposed", input_data.metric, results
#                         )

#         return results

#     @staticmethod
#     def _process_query(db, dataset_id, comp_name, comp_type_str, metrics, results):
#         try:
#             query = db.query(ResultComparison).filter(
#                 and_(
#                     ResultComparison.dataset_id == dataset_id,
#                     ResultComparison.compressor == comp_name,
#                     ResultComparison.compressor_type == comp_type_str
#                 )
#             ).all()
#         except Exception as e:
#             logging.error("Database query failed for dataset_id %s, compressor %s, type %s: %s",
#                           dataset_id, comp_name, comp_type_str, e, exc_info=True)
#             return

#         if not query:
#             logging.info("No results found for dataset_id %s, compressor %s, type %s",
#                          dataset_id, comp_name, comp_type_str)
#             return

#         result_dict = {
#             "dataset_id": dataset_id,
#             "compressor": comp_name,
#             "compressor_type": comp_type_str
#         }

#         for metric in metrics:
#             try:
#                 metric_key = metric.lower().strip()
#                 db_col = METRIC_MAP.get(metric_key)
#                 if not db_col:
#                     result_dict[metric] = None
#                     continue

#                 if "peak" in metric_key:
#                     value = max(getattr(row, db_col, 0) for row in query)
#                 elif "total" in metric_key:
#                     value = sum(getattr(row, db_col, 0) for row in query)
#                 else:
#                     # fallback: take the first row's value
#                     value = getattr(query[0], db_col, 0)
#                 result_dict[metric] = value
#             except Exception as e:
#                 logging.error("Error processing metric '%s' for dataset_id %s, compressor %s: %s",
#                               metric, dataset_id, comp_name, e, exc_info=True)
#                 result_dict[metric] = None

#         results.append(result_dict)
