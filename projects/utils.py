from django.db.models import Q
from .models import Project, Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProjects(request, projects, results):
    # Розбити projects_queryset по 2 projects

    page = request.GET.get("page")

    paginator = Paginator(projects, results)

    try:
        # Яку сторінку ми хочемо отримати -> 1 сторінка перших 2 проекти
        projects = paginator.page(page)
    except PageNotAnInteger:
        # First Load
        page = 1
        projects = paginator.page(page)
    # Якщо користувач переходить на сторінку якої в нас немає
    except EmptyPage:
        # Отримаємо кількість сторінок відповідно останю
        page = paginator.num_pages
        # Виводимо останню сторінку
        projects = paginator.page(page)

    # Відображення кнопок пагінаційної панелі
    leftIndex = (int(page) - 1)
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, projects


def searchProject(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query)

    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
    )

    return search_query, projects
