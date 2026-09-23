from sqlalchemy import Select

from app.models.document import Document
from app.schemas.retrieval import RetrievalFilters


def apply_metadata_filters(
    statement: Select,
    filters: RetrievalFilters | None,
) -> Select:
    if not filters:
        return statement

    if filters.category:
        statement = statement.where(
            Document.document_metadata["category"].as_string()
            == filters.category
        )

    if filters.document_type:
        statement = statement.where(
            Document.document_metadata["document_type"].as_string()
            == filters.document_type
        )

    if filters.department:
        statement = statement.where(
            Document.document_metadata["department"].as_string()
            == filters.department
        )

    if filters.source_type:
        statement = statement.where(
            Document.document_metadata["source_type"].as_string()
            == filters.source_type
        )

    return statement