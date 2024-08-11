from fastapi import APIRouter, Depends, Query, HTTPException
from database import get_session, Session, select
from models import Product

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/")
async def create_product(
    *,
    session: Session = Depends(get_session),
    product: Product,
):
    db_product = Product.model_validate(product)
    session.add(db_product)
    session.commit()
    return {"ok": True}


@router.get("/", response_model=list[Product])
async def read_products(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    products = session.exec(select(Product).offset(offset).limit(limit)).all()
    if not products:
        raise HTTPException(status_code=404, detail="Not found")
    return products


@router.get("/{product_id}", response_model=Product)
async def read_product(
    *,
    session: Session = Depends(get_session),
    product_id: int,
):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Not found")
    return product


@router.patch("/{product_id}")
def update_product(*, session: Session = Depends(get_session), product_id: int, product: Product):
    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Not found")
    product_data = product.model_dump(exclude_unset=True)
    for key, value in product_data.items():
        setattr(db_product, key, value)
    session.add(db_product)
    session.commit()
    return {"ok": True}


@router.delete("/{product_id}")
async def delete_product(
    *,
    session: Session = Depends(get_session),
    product_id: int,
):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Not found")
    session.delete(product)
    session.commit()
    return {"ok": True}
