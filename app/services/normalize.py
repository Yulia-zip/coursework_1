import re


class SQL_Normalize:

    def normalize(self,query:str)->str:
        if not query:
            return ""

        query=self.delete_comments(query)
        query=self.normalize_whitespace(query)
        query=self.upper_sql(query)

        return query


    def delete_comments(self,query:str)->str:
        query=re.sub(r'--.*$','', query,flags=re.MULTILINE)
        query=re.sub(r'/\*.*?\*/','',query,flags=re.DOTALL)

        return query.strip()


    def upper_sql(self,query:str)->str:
        keywords = [
            'SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'JOIN',
            'INNER', 'LEFT', 'RIGHT', 'ON', 'INSERT', 'UPDATE',
            'DELETE', 'CREATE', 'DROP', 'TABLE', 'ORDER BY',
            'GROUP BY', 'HAVING', 'LIMIT', 'OFFSET', 'BETWEEN',
            'IN', 'LIKE', 'IS', 'NULL', 'NOT'
        ]

        keywords.sort(key=len, reverse=True)
        non_table_keyw=[k for k in keywords if k!='TABLE']
        for keyword in non_table_keyw:
            pattern=r'\b'+re.escape(keyword)+r'\b'
            query=re.sub(pattern,keyword,query,flags=re.IGNORECASE)

        query=re.sub(r'\b(CREATE|DROP)\s+table\b',r'\1 TABLE',query,flags=re.IGNORECASE)
        return query

    def normalize_whitespace (self,query:str)->str:
        query = re.sub(r'\s+', ' ', query)


        operators = ['<=', '>=', '<>', '<', '>', '=']
        for op in operators:
            query = query.replace(op, f' {op} ')

        query = query.replace(',', ', ')

        query = re.sub(r'\s+', ' ', query)

        return query.strip()
