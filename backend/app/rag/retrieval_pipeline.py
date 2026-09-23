from app.rag.hybrid_retriever import hybrid_retriever
from app.rag.reranker import reranker
from app.schemas.retrieval import RetrievalFilters


class RetrievalPipeline:
    def search(
        self,
        query: str,
        top_k: int = 5,
        candidate_k: int = 20,
        filters: RetrievalFilters | None = None,
    ) -> list[dict]:

        # Stage 1: Hybrid retrieval
        candidates = hybrid_retriever.search(
            query=query,
            top_k=candidate_k,
            filters=filters,
        )

        # Stage 2: Cross-encoder reranking
        results = reranker.rerank(
            query=query,
            results=candidates,
            top_k=top_k,
        )

        return results


retrieval_pipeline = RetrievalPipeline()