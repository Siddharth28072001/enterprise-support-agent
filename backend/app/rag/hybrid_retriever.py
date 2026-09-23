from app.database import SessionLocal
from app.rag.keyword_retriever import keyword_retriever
from app.rag.vector_retriever import vector_retriever
from app.schemas.retrieval import RetrievalFilters


class HybridRetriever:
    def __init__(self, rrf_k: int = 60):
        self.rrf_k = rrf_k

    def search(
        self,
        query: str,
        top_k: int = 10,
        filters: RetrievalFilters | None = None,
    ) -> list[dict]:
        db = SessionLocal()

        try:
            vector_results = vector_retriever.search(
                db=db,
                query=query,
                top_k=top_k,
                filters=filters,
            )

            keyword_results = keyword_retriever.search(
                db=db,
                query=query,
                top_k=top_k,
                filters=filters,
            )

            return self._fuse_results(
                vector_results=vector_results,
                keyword_results=keyword_results,
                top_k=top_k,
            )

        finally:
            db.close()

    def _fuse_results(
        self,
        vector_results: list[dict],
        keyword_results: list[dict],
        top_k: int,
    ) -> list[dict]:
        fused_scores: dict[int, float] = {}
        result_map: dict[int, dict] = {}

        for rank, result in enumerate(vector_results, start=1):
            chunk_id = result["chunk_id"]

            fused_scores[chunk_id] = (
                fused_scores.get(chunk_id, 0.0)
                + 1 / (self.rrf_k + rank)
            )

            result_map[chunk_id] = result

        for rank, result in enumerate(keyword_results, start=1):
            chunk_id = result["chunk_id"]

            fused_scores[chunk_id] = (
                fused_scores.get(chunk_id, 0.0)
                + 1 / (self.rrf_k + rank)
            )

            result_map[chunk_id] = result

        ranked_chunk_ids = sorted(
            fused_scores,
            key=fused_scores.get,
            reverse=True,
        )[:top_k]

        results = []

        for chunk_id in ranked_chunk_ids:
            result = result_map[chunk_id].copy()

            result["retrieval_score"] = fused_scores[chunk_id]

            results.append(result)

        return results


hybrid_retriever = HybridRetriever()