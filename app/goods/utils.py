from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    SearchHeadline,
)
from goods.models import Products


def q_search(query):
    if query.isdigit() and len(query) <= 5:
        return Products.objects.filter(id=int(query))

    # удобный поиск с postgres

    vector = SearchVector("name", "description")
    q = SearchQuery(query)

    result = (
        Products.objects.annotate(rank=SearchRank(vector, q))
        .filter(rank__gt=0)
        .order_by("-rank")
    )

    result = result.annotate(
        headline=SearchHeadline(
            "name", query, start_sel='<span class="bg-warning">', stop_sel="</span>"
        )
    )

    result = result.annotate(
        bodyline=SearchHeadline(
            "description",
            query,
            start_sel='<span class="bg-warning">',
            stop_sel="</span>",
        )
    )

    return result

    # Базовый метод поиска для всех бд

    # keywords = [keyword for keyword in query.split() if len(keyword) > 2]

    # q_objects = Q()

    # for token in keywords:
    #     q_objects |= Q(description__icontains=token)
    #     q_objects |= Q(name__icontains=token)

    # return Products.objects.filter(q_objects)
