from decimal import Decimal

from django.conf import settings
from django.db import connection
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import SqlLexer
from sqlparse import format


def masud_for_sql_middleware(get_response):
    def middleware(request):
        response = get_response(request)
        if settings.DEBUG:
            num_queries = len(connection.queries)
            check_duplicates = set()
            total_execution_time = Decimal()

            print("🏹🏹🏹🏹🏹🏹🏹🏹🏹🏹")
            # result_all = []
            for query in connection.queries:
                total_execution_time += Decimal(query["time"])
                check_duplicates.add(query["sql"])
                print("🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼")
                sqlformatted = (
                    format(str(query["sql"]), reindent=True)
                    .replace(chr(34), "`")
                    .replace("CAST(", "")
                    .replace("AS NUMERIC)", "")
                )
                result = highlight(sqlformatted, SqlLexer(), TerminalFormatter())
                # reslt = []
                # for x in connection.cursor().execute(query["sql"]):
                #     reslt.append([x])

                # result_all += reslt
                print(result)
            # myfile = open("xyz.txt", "w")
            # myfile.write(str(result_all))
            # myfile.close()
        print("🌿🌿🌿🌿🌿🌿🌿🌿🌿🌿🌿🌿")
        print(
            f"[SQL Stats] : Total Queries: {num_queries},  Total Duplicates: {num_queries - len(check_duplicates)}"
        )
        # print(f"{num_queries} Total Queries")
        # print(f"{num_queries - len(check_duplicates)} Total Duplicates")
        print(f"⏰ Exeqution Time: {total_execution_time}")
        print("🌿🌿🌿🌿🌿🌿🌿🌿🌿🌿🌿🌿")
        return response

    return middleware
