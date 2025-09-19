from bson import ObjectId
from typing import Any, Dict, List


def serialize_objectid(obj: Any) -> Any:
    """Convert MongoDB ObjectId to string recursively."""
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, dict):
        return {key: serialize_objectid(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [serialize_objectid(item) for item in obj]
    else:
        return obj


def convert_doc_to_dict(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Convert MongoDB document to a serializable dictionary."""
    if doc is None:
        return None
    
    # Convert ObjectId fields to strings
    serialized_doc = serialize_objectid(doc)
    
    # Handle the _id field specifically
    if "_id" in serialized_doc:
        serialized_doc["_id"] = str(serialized_doc["_id"])
    
    return serialized_doc


def convert_docs_to_list(docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convert list of MongoDB documents to serializable dictionaries."""
    if not docs:
        return []
    
    return [convert_doc_to_dict(doc) for doc in docs]