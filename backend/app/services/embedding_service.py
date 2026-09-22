from google import genai
from google.genai import types
from sentence_transformers import SentenceTransformer

from app.config import settings


class EmbeddingService:
    def __init__(self):
        self.provider = settings.embedding_provider

        if self.provider == "local":
            self.model = SentenceTransformer(
                "BAAI/bge-base-en-v1.5"
            )
            self.gemini_client = None

        elif self.provider == "gemini":
            if not settings.gemini_api_key:
                raise ValueError(
                    "GEMINI_API_KEY is required when "
                    "EMBEDDING_PROVIDER=gemini"
                )

            self.model = None

            self.gemini_client = genai.Client(
                api_key=settings.gemini_api_key
            )

        else:
            raise ValueError(
                f"Unsupported embedding provider: {self.provider}"
            )

    def embed_document(self, text: str) -> list[float]:
        if self.provider == "local":
            embedding = self.model.encode(
                text,
                normalize_embeddings=True,
            )

            return embedding.tolist()

        if self.provider == "gemini":
            return self._embed_gemini(
                text=text,
                task_type="RETRIEVAL_DOCUMENT",
            )

        raise ValueError(
            f"Unsupported embedding provider: {self.provider}"
        )

    def embed_query(self, text: str) -> list[float]:
        if self.provider == "local":
            embedding = self.model.encode(
                text,
                normalize_embeddings=True,
            )

            return embedding.tolist()

        if self.provider == "gemini":
            return self._embed_gemini(
                text=text,
                task_type="RETRIEVAL_QUERY",
            )

        raise ValueError(
            f"Unsupported embedding provider: {self.provider}"
        )

    def _embed_gemini(
        self,
        text: str,
        task_type: str,
    ) -> list[float]:
        response = self.gemini_client.models.embed_content(
            model=settings.gemini_embedding_model,
            contents=text,
            config=types.EmbedContentConfig(
                task_type=task_type,
                output_dimensionality=settings.gemini_embedding_dimensions,
            ),
        )

        return response.embeddings[0].values


embedding_service = EmbeddingService()