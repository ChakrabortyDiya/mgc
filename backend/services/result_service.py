from sqlalchemy.orm import Session
from database.models import ResultComparison
from fastapi import HTTPException
from sqlalchemy import and_

class DashboardService:
    @staticmethod
    def fetch_grouped_results(db: Session, input_data):
        results = []

        # Map indexes to actual compressor types
        comp_type_map = {0: "standard", 1: "proposed"}
        selected_types = [comp_type_map[i]
                          for i, flag in enumerate(input_data.comp_type) if flag == 1]

        for dataset_id in input_data.id:
            for comp_name in input_data.comp_name:
                for comp_type_str in selected_types:
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
                        if hasattr(query, metric):
                            result_dict[metric] = getattr(query, metric)
                        else:
                            result_dict[metric] = None

                    results.append(result_dict)

        return results
