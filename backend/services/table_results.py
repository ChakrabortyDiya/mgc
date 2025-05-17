import logging
from pymongo.collection import Collection
from utils import TableData

# Configure logging if not already configured
logging.basicConfig(level=logging.INFO)

# Mapping for new metric names to MongoDB document keys.
METRIC_MAP = {
    "wacr": "compression_ratio",
    "compression size": "compressed_size",
    "tct": "compression_time",
    "pcm": "compression_memory",
    "tcm": "compression_memory",
    "pcc": "compression_cpu",
    "tcc": "compression_cpu",
    "tdt": "decompression_time",
    "pdm": "decompression_memory",
    "tdm": "decompression_memory",
    "pdc": "decompression_cpu",
    "tdc": "decompression_cpu",
}

RESULT_METRIC_MAP = {
    "compression_ratio": "WACR",
    "compressed_size": "Compression Size (KB)",
    "compression_time": "TCT (s)",
    "compression_memory": "PCM (MB)",
    "decompression_time": "TDT (s)",
    "decompression_memory": "PDM (MB)",
    "compression_cpu": "PCC (%)",
    "decompression_cpu": "PDC (%)",
}

class TabularData:
    @staticmethod
    def fetch_grouped_results(collection: Collection, input_data: TableData) -> dict:
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
        
        metrices = []
        
        for metric in input_data.metric:
            # Normalize metric names.
            metric_key = metric.lower().strip()
            if metric_key not in METRIC_MAP:
                logging.warning("Metric '%s' is not recognized. Skipping.", metric)
                continue
            metric = METRIC_MAP[metric_key]
            metrices.append(metric)
            logging.info("Normalized metric '%s' to '%s'", metric_key, metric)
        
        logging.info("Metrics to be processed: %s", metrices)
        # Loop over each dataset.   
        for dataset_id in input_data.id:
            # Process standard compressors.
            if "standard" in selected_types:
                for comp_name in input_data.standard_comp_name:
                    if comp_name:  # Skip if None or empty string.
                        if comp_name == "7zip":
                            comp_name = "7-zip"
                        TabularData._process_query(
                            collection, dataset_id, comp_name, "standard", metrices, results
                        )
            # Process proposed compressors.
            if "proposed" in selected_types:
                for comp_name in input_data.proposed_comp_name:
                    if comp_name:
                        if comp_name == "7zip":
                            comp_name = "7-zip"
                        TabularData._process_query(
                            collection, dataset_id, comp_name, "proposed", metrices, results
                        )

        # Rearrange results: group by compressor type, preserve compressor order
        rearranged = []
        # Build a lookup for quick access
        result_lookup = {
            (item["Dataset ID"], item["Compressor"], item["Compressor Type"]): item
            for item in results
        }
        for dataset_id in input_data.id:
            # Standard first
            for comp_name in input_data.standard_comp_name:
                key = (dataset_id, "7-zip" if comp_name == "7zip" else comp_name, "standard")
                if key in result_lookup:
                    rearranged.append(result_lookup[key])
            # Then proposed
            for comp_name in input_data.proposed_comp_name:
                key = (dataset_id, "7-zip" if comp_name == "7zip" else comp_name, "proposed")
                if key in result_lookup:
                    rearranged.append(result_lookup[key])
        return rearranged

    @staticmethod
    def _process_query(collection: Collection, dataset_id, comp_name, comp_type_str, metrics, results: list):
        try:
            # Build the query filter.
            query_filter = {
                "dataset_id": dataset_id,
                "compressor": comp_name,
                "compressor_type": comp_type_str
            }
            logging.info("Querying MongoDB with filter: %s", query_filter)
            # Fetch matching documents.
            docs = list(collection.find(query_filter))
        except Exception as e:
            logging.error("Database query failed for dataset_id %s, compressor %s, type %s: %s",
                          dataset_id, comp_name, comp_type_str, e, exc_info=True)
            return

        if not len(docs):
            logging.info("No results found for dataset_id %s, compressor %s, type %s",
                         dataset_id, comp_name, comp_type_str)
            return

        result_dict = {
            "Dataset ID": dataset_id,
            "Compressor": comp_name,
            "Compressor Type": comp_type_str
        }

        for metric in metrics:
            try:
                # Normalize the metric key.
                # metric_key = metric.lower().strip()
                # # db_field = METRIC_MAP.get(metric_key)
                # db_field = METRIC_MAP[metric_key]
                db_field = metric.lower().strip()
                logging.info("DB field for metric '%s': %s", metric, db_field)
                if not db_field:
                    result_dict[metric] = None
                    continue

                # Compute the desired value based on the metric type.
                values = [doc.get(db_field, 0) for doc in docs if doc.get(db_field) is not None]
                if not values:
                    result_dict[metric] = None
                # elif "p" in db_field:
                #     result_dict[metric] = max(values)
                # elif "t" in db_field:
                #     result_dict[metric] = sum(values)
                else:
                    # Fallback: take the first document's value.
                    result_dict[RESULT_METRIC_MAP[metric]] = values[0]
            except Exception as e:
                logging.error("Error processing metric '%s' for dataset_id %s, compressor %s: %s",
                              metric, dataset_id, comp_name, e, exc_info=True)
                result_dict[metric] = None

        results.append(result_dict)
