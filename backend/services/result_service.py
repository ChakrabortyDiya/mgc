from sqlalchemy.orm import Session
from database.models import ResultComparison
from fastapi import HTTPException
from sqlalchemy import and_


class DashboardService:
    @staticmethod
    def fetch_grouped_results(db: Session, input_data):
        results = []

        # Map index to compressor types
        comp_type_map = {0: "standard", 1: "proposed"}
        selected_types = [comp_type_map[i]
                          for i, flag in enumerate(input_data.comp_type) if flag == 1]

        print(f"[INFO] Fetching dashboard data...")
        print(
            f"[INFO] Data: id={input_data.id} comp_type={input_data.comp_type} comp_name={input_data.comp_name} metric={input_data.metric}")

        for dataset_id in input_data.id:
            for comp_name_entry in input_data.comp_name:
                for comp_type_str in selected_types:
                    # Determine compressor name based on type
                    if isinstance(comp_name_entry, list) and len(comp_name_entry) == 2:
                        comp_name = comp_name_entry[0] if comp_type_str == "standard" else comp_name_entry[1]
                    else:
                        comp_name = comp_name_entry

                    query = db.query(ResultComparison).filter(
                        and_(
                            ResultComparison.dataset_id == dataset_id,
                            ResultComparison.compressor == comp_name,
                            ResultComparison.compressor_type == comp_type_str
                        )
                    ).first()

                    if not query:
                        continue

                    result_dict = {
                        "dataset_id": query.dataset_id,
                        "compressor": query.compressor,
                        "compressor_type": query.compressor_type
                    }

                    for metric in input_data.metric:
                        metric_attr = metric.lower().replace(" ", "_")
                        if hasattr(query, metric_attr):
                            result_dict[metric] = getattr(query, metric_attr)
                        else:
                            result_dict[metric] = None

                    results.append(result_dict)

        return results
