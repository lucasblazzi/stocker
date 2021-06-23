insert_user_query = """
            INSERT INTO stocker.user VALUES (%(cpf)s, %(name)s, %(username)s, crypt(%(password)s, gen_salt(\'bf\', 8)),
            %(email)s, %(profile)s, %(cvm_license)s);
            """

update_user_query = """
            UPDATE stocker.user SET name=%(name)s, username=%(username)s, password=%(password)s, 
                email=%(email)s, profile=%(profile)s, cvm_license=%(cvm_license)s 
            WHERE cpf = %(cpf)s;
            """

select_user_by_id = """
            SELECT * FROM stocker.user WHERE stocker.user.cpf = %s;
            """

insert_prices_query = """
            INSERT INTO stocker.price (symbol, date, open, close, high, low, volume) VALUES 
                (%(symbol)s, %(date)s, %(open)s, %(close)s, %(high)s, %(low)s, %(volume)s)
            ON CONFLICT (symbol, date) DO UPDATE SET (open, close, high, low, volume)=(%(open)s, %(close)s, %(high)s, 
                %(low)s, %(volume)s);
            """

insert_news_query = """
            INSERT INTO stocker.news (symbol, date, title, source, url, description, image) VALUES (%(symbol)s, 
                %(date)s, %(title)s, %(source)s, %(url)s, %(description)s, %(image)s);
            """

news_query = """
            SELECT * FROM stocker.news n WHERE n.symbol = %s ORDER BY n.date DESC
"""

login_query = """
            SELECT * FROM login (%s, %s)
            """

insert_company_query = """
            INSERT INTO stocker.company (symbol, name, exchange, industry, website, description, CEO, sector, 
                employees, state, city, country, logo) VALUES (%(symbol)s, %(name)s, %(exchange)s, %(industry)s,
                %(website)s, %(description)s, %(CEO)s, %(sector)s, %(employees)s, %(state)s, %(city)s, %(country)s,
                %(logo)s)
            ON CONFLICT (symbol) DO UPDATE SET (name, exchange, industry, website, description, CEO, sector, 
                employees, state, city, country, logo)=(%(name)s, %(exchange)s, %(industry)s, %(website)s,
                %(description)s, %(CEO)s, %(sector)s, %(employees)s, %(state)s, %(city)s, %(country)s, %(logo)s);
            """

get_company_list = """
    SELECT symbol FROM stocker.company
    """

price_series_query = """
        SELECT * FROM get_prices(%s, %s)
        """