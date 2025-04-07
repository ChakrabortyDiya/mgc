from sqlalchemy.orm import Session
from database.models import ResultComparison
from fastapi import HTTPException
from typing import List
from sqlalchemy import and_

class DashboardService:
    @staticmethod
    def fetch_grouped_results(db: Session, input_data):
        results = []

        for i in range(len(input_data.id)):
            query = db.query(ResultComparison).filter(
                and_(
                    ResultComparison.dataset_id == input_data.id[i],
                    ResultComparison.compressor == input_data.comp_name[i],
                    ResultComparison.compressor_type == str(input_data.comp_type[i])
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
                result_dict[metric] = getattr(query, metric, None)

            results.append(result_dict)

        return results
