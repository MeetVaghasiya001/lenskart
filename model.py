from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Product(BaseModel):
    product_id: int
    brand: Optional[str]
    product_name: Optional[str]
    model_number: Optional[str]
    gallary: Optional[Dict[str, Optional[List[str]]]]
    price: Optional[Dict[str, float]]
    review: Optional[float]
    rating_count: Optional[int]
    customer_reviews: Optional[Dict[str, List[Dict[str,Any]]]]
    custome_review_graph: Optional[List[Dict[str, Any]]]
    specification: Optional[List[Dict[str, Any]]]
    similar_products: Optional[List[Dict[str, Any]]]
    highlight: Optional[Dict[str, Any]]
    near_by_stores: Optional[List[Dict[str, Any]]]
    sizes: Optional[Dict[str, Any]]
    colors: Optional[Dict[str, Any]]
    promis: Optional[Dict[str, Any]]