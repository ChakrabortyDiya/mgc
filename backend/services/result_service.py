from sqlalchemy.orm import Session
from database.models import ResultComparison
from sqlalchemy import and_

# Mapping for new metric names to DB columns
METRIC_MAP = {
    "wacr": "compression_ratio",
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
    def fetch_grouped_results(db: Session, input_data):
        results = []

        # Map comp_type list index to type string
        comp_type_map = {0: "standard", 1: "proposed"}
        selected_types = [comp_type_map[i]
                          for i, flag in enumerate(input_data.comp_type) if flag == 1]

        for dataset_id in input_data.id:
            # Handle standard compressors
            if "standard" in selected_types:
                for comp_name in input_data.standard_comp_name:
                    if comp_name:  # skip if None or empty string
                        DashboardService._process_query(
                            db, dataset_id, comp_name, "standard", input_data.metric, results
                        )

            # Handle proposed compressors
            if "proposed" in selected_types:
                for comp_name in input_data.proposed_comp_name:
                    if comp_name:
                        DashboardService._process_query(
                            db, dataset_id, comp_name, "proposed", input_data.metric, results
                        )

        return results

    @staticmethod
    def _process_query(db, dataset_id, comp_name, comp_type_str, metrics, results):
        query = db.query(ResultComparison).filter(
            and_(
                ResultComparison.dataset_id == dataset_id,
                ResultComparison.compressor == comp_name,
                ResultComparison.compressor_type == comp_type_str
            )
        ).all()

        if not query:
            return

        # Aggregate logic for peak (max) and total (sum)
        result_dict = {
            "dataset_id": dataset_id,
            "compressor": comp_name,
            "compressor_type": comp_type_str
        }

        for metric in metrics:
            metric_key = metric.lower().strip()
            db_col = METRIC_MAP.get(metric_key)
            if not db_col:
                result_dict[metric] = None
                continue

            if "peak" in metric_key:
                value = max(getattr(row, db_col, 0) for row in query)
            elif "total" in metric_key:
                value = sum(getattr(row, db_col, 0) for row in query)
            else:
                # fallback: just take the first row's value
                value = getattr(query[0], db_col, 0)
            result_dict[metric] = value

        results.append(result_dict)
