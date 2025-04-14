from sqlalchemy.orm import Session
from database.models import ResultComparison
from sqlalchemy import and_


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
        ).first()

        if not query:
            return

        result_dict = {
            "dataset_id": query.dataset_id,
            "compressor": query.compressor,
            "compressor_type": query.compressor_type
        }

        for metric in metrics:
            metric_attr = metric.lower().replace(" ", "_")
            result_dict[metric] = getattr(query, metric_attr, 0)

        results.append(result_dict)
