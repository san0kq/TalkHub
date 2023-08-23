from django.db import connection


def print_queries() -> int:
    queries_count = 0
    for _ in connection.queries:
        queries_count += 1
    return queries_count
