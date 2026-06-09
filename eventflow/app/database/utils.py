from bson import ObjectId


def doc(item) -> dict:
    """Converte um documento MongoDB para dict serializável."""
    if item is None:
        return None
    item["id"] = str(item.pop("_id"))
    return item


def docs(cursor) -> list:
    """Converte uma lista de documentos MongoDB."""
    return [doc(i) for i in cursor]


def to_oid(id_str: str) -> ObjectId:
    return ObjectId(id_str)
