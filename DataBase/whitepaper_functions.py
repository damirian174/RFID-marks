# ====== Функции для работы с информацией о компании (whitepaper) ======

async def add_company_info(pool, company_name, inn, logo_path=None, description=None, address=None, phone=None, email=None, website=None):
    """
    Добавление информации о компании.
    """
    try:
        async with pool.acquire() as conn:
            query = """
                INSERT INTO company_info (company_name, inn, logo_path, description, address, phone, email, website)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                ON CONFLICT (inn) DO UPDATE SET
                    company_name = EXCLUDED.company_name,
                    logo_path = EXCLUDED.logo_path,
                    description = EXCLUDED.description,
                    address = EXCLUDED.address,
                    phone = EXCLUDED.phone,
                    email = EXCLUDED.email,
                    website = EXCLUDED.website,
                    updated_at = CURRENT_TIMESTAMP;
            """
            await conn.execute(query, company_name, inn, logo_path, description, address, phone, email, website)
            return "OK"
    except Exception as e:
        print(f"Ошибка при добавлении информации о компании: {e}")
        return str(e)

async def get_company_info(pool, inn=None):
    """
    Получение информации о компании по ИНН или всей информации.
    """
    try:
        async with pool.acquire() as conn:
            if inn:
                query = "SELECT * FROM company_info WHERE inn = $1;"
                company = await conn.fetchrow(query, inn)
                return company
            else:
                query = "SELECT * FROM company_info ORDER BY created_at DESC;"
                companies = await conn.fetch(query)
                return companies
    except Exception as e:
        print(f"Ошибка при получении информации о компании: {e}")
        return None

async def update_company_info(pool, inn, **kwargs):
    """
    Обновление информации о компании.
    """
    try:
        async with pool.acquire() as conn:
            # Формируем динамический запрос на основе переданных параметров
            set_clauses = []
            values = []
            param_count = 1
            
            for key, value in kwargs.items():
                if key in ['company_name', 'logo_path', 'description', 'address', 'phone', 'email', 'website']:
                    set_clauses.append(f"{key} = ${param_count}")
                    values.append(value)
                    param_count += 1
            
            if not set_clauses:
                return "Нет полей для обновления"
            
            set_clauses.append("updated_at = CURRENT_TIMESTAMP")
            values.append(inn)
            
            query = f"""
                UPDATE company_info 
                SET {', '.join(set_clauses)}
                WHERE inn = ${param_count};
            """
            
            await conn.execute(query, *values)
            return "OK"
    except Exception as e:
        print(f"Ошибка при обновлении информации о компании: {e}")
        return str(e)

async def delete_company_info(pool, inn):
    """
    Удаление информации о компании по ИНН.
    """
    try:
        async with pool.acquire() as conn:
            query = "DELETE FROM company_info WHERE inn = $1;"
            await conn.execute(query, inn)
            return "OK"
    except Exception as e:
        print(f"Ошибка при удалении информации о компании: {e}")
        return str(e)

# ====== Функции для работы с продуктами (whitepaper) ======

async def add_product(pool, product_name, product_code, category, description=None, specifications=None, price=None, currency='RUB', production_capacity=None, unit_of_measure='шт'):
    """
    Добавление нового продукта.
    """
    try:
        async with pool.acquire() as conn:
            # Преобразуем specifications в JSON, если это словарь
            if specifications and isinstance(specifications, dict):
                import json
                specifications = json.dumps(specifications)
            
            query = """
                INSERT INTO products (product_name, product_code, category, description, specifications, price, currency, production_capacity, unit_of_measure)
                VALUES ($1, $2, $3, $4, $5::jsonb, $6, $7, $8, $9)
                ON CONFLICT (product_code) DO UPDATE SET
                    product_name = EXCLUDED.product_name,
                    category = EXCLUDED.category,
                    description = EXCLUDED.description,
                    specifications = EXCLUDED.specifications,
                    price = EXCLUDED.price,
                    currency = EXCLUDED.currency,
                    production_capacity = EXCLUDED.production_capacity,
                    unit_of_measure = EXCLUDED.unit_of_measure,
                    updated_at = CURRENT_TIMESTAMP;
            """
            await conn.execute(query, product_name, product_code, category, description, specifications, price, currency, production_capacity, unit_of_measure)
            return "OK"
    except Exception as e:
        print(f"Ошибка при добавлении продукта: {e}")
        return str(e)

async def get_products(pool, product_code=None, category=None, is_active=None):
    """
    Получение продуктов по различным критериям.
    """
    try:
        async with pool.acquire() as conn:
            conditions = []
            values = []
            param_count = 1
            
            if product_code:
                conditions.append(f"product_code = ${param_count}")
                values.append(product_code)
                param_count += 1
            
            if category:
                conditions.append(f"category = ${param_count}")
                values.append(category)
                param_count += 1
            
            if is_active is not None:
                conditions.append(f"is_active = ${param_count}")
                values.append(is_active)
                param_count += 1
            
            where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
            
            query = f"SELECT * FROM products {where_clause} ORDER BY created_at DESC;"
            products = await conn.fetch(query, *values)
            return products
    except Exception as e:
        print(f"Ошибка при получении продуктов: {e}")
        return None

async def update_product(pool, product_code, **kwargs):
    """
    Обновление информации о продукте.
    """
    try:
        async with pool.acquire() as conn:
            set_clauses = []
            values = []
            param_count = 1
            
            for key, value in kwargs.items():
                if key in ['product_name', 'category', 'description', 'price', 'currency', 'production_capacity', 'unit_of_measure', 'is_active']:
                    set_clauses.append(f"{key} = ${param_count}")
                    values.append(value)
                    param_count += 1
                elif key == 'specifications' and isinstance(value, dict):
                    import json
                    set_clauses.append(f"specifications = ${param_count}::jsonb")
                    values.append(json.dumps(value))
                    param_count += 1
            
            if not set_clauses:
                return "Нет полей для обновления"
            
            set_clauses.append("updated_at = CURRENT_TIMESTAMP")
            values.append(product_code)
            
            query = f"""
                UPDATE products 
                SET {', '.join(set_clauses)}
                WHERE product_code = ${param_count};
            """
            
            await conn.execute(query, *values)
            return "OK"
    except Exception as e:
        print(f"Ошибка при обновлении продукта: {e}")
        return str(e)

async def delete_product(pool, product_code):
    """
    Удаление продукта по коду.
    """
    try:
        async with pool.acquire() as conn:
            query = "DELETE FROM products WHERE product_code = $1;"
            await conn.execute(query, product_code)
            return "OK"
    except Exception as e:
        print(f"Ошибка при удалении продукта: {e}")
        return str(e)

async def get_product_categories(pool):
    """
    Получение всех категорий продуктов.
    """
    try:
        async with pool.acquire() as conn:
            query = "SELECT DISTINCT category FROM products WHERE is_active = TRUE ORDER BY category;"
            categories = await conn.fetch(query)
            return [row['category'] for row in categories]
    except Exception as e:
        print(f"Ошибка при получении категорий продуктов: {e}")
        return None
