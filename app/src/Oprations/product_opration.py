# --------------- product functions  --------------- 
def product_is_exist(coll, id: int) -> bool :
    for product in coll.find({'id': id}, {'_id': 0}) :
        if product :
            return True

    return False

def product_get(coll, id: int) -> Product :
    if product_is_exist(coll, id) :
        for product in coll.find({'id': id}, {'_id': 0}) :
            return Product(**product)

    raise HTTPException(
        status.HTTP_409_CONFLICT,
        'the product is not exist',
    )


def product_add(coll, product: Product) -> None:
    if product_is_exist(coll, product.id) :
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            'the product is exist',
        )
    try :
        coll.insert_one(product.dict())
    except :
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            'Database error',
        )

def product_update(coll, id: int, key, value) -> Product :
    if product_is_exist(coll, id) :
        coll.update_one(
            {'id': id} ,
            {'$set': {key : value} },
        )
        return product_get(coll, id)

    raise HTTPException(
        status.HTTP_404_NOT_FOUND,
        'the product is not exist',
    )

def product_delete(coll, id: int) -> bool :
    if product_is_exist(coll, id) :
        coll.delete_one({'id': id})
        return True

    raise HTTPException(
        status.HTTP_404_NOT_FOUND,
        'the product is not exist',
    )

