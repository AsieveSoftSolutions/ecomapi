from fastapi import APIRouter
from src.endpoints import (users, addresses, bank_details, category, sub_category,
                           product_type, fabric_type, sleeve_pattern, neck_design,
                           occasion, product_size, file_upload, product, advertisement, common, carts,
                           wishlist, order, ratting,brand,postal_service,tax,delivery_charge,dashboard_rev)

router = APIRouter()

router.include_router(users.router)
router.include_router(addresses.router)
router.include_router(bank_details.router)
router.include_router(category.router)
router.include_router(sub_category.router)
router.include_router(product_type.router)
router.include_router(fabric_type.router)
router.include_router(sleeve_pattern.router)
router.include_router(neck_design.router)
router.include_router(occasion.router)
router.include_router(product_size.router)
router.include_router(file_upload.router)
router.include_router(product.router)
router.include_router(advertisement.router)
router.include_router(common.router)
router.include_router(carts.router)
router.include_router(wishlist.router)
router.include_router(order.router)
router.include_router(ratting.router)
router.include_router(brand.router)
router.include_router(postal_service.router)
router.include_router(tax.router)
router.include_router(delivery_charge.router)
router.include_router(dashboard_rev.router)