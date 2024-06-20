# Batch document's

- `supplier_document` is the document from supplier, in the context of Brazil this is the [CNPJ](https://www.bing.com/search?q=cnpj%20o%20que%20%C3%A9%20&qs=n&form=QBRE&sp=-1&lq=0&pq=cnpj%20o%20que%20%C3%A9%20&sc=19-13&sk=&cvid=F87B2786BC0041099B14B4FB11AA60E7&ghsh=0&ghacc=0&ghpl=)
- `reference` is the reference of the batch, an unique key.
- `inserction_date` the datetime of inserction.
- `expiry_date` the expiry date (just date, not time) of the products from the batch.

# Product document's

- `name` is the name of the product.
- `price` is the unit price.
- `stock` the valid stock.
- `batch` is the reference of the batch.
- `discount_value` is the price for unit discount (default is zero).
- `item_type` is the type of the product, for example: Construction
- `data_type` is the use of product, for example: `for_sale` is to open for sale. See all "data types" on `app/constants.py`