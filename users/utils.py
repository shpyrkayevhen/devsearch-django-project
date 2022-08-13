from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def searchProfiles(request):
    search_query = ''

    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    skills = Skill.objects.filter(name__icontains=search_query)

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) | Q(short_intro__icontains=search_query) | Q(skill__in=skills))

    return profiles, search_query


def paginateProfiles(request, profiles, results):
    # Розбити profiles_set по 3 prprofile

    page = request.GET.get("page")

    paginator = Paginator(profiles, results)

    try:
        # Яку сторінку ми хочемо отримати -> 1 сторінка перших 2 проекти
        profiles = paginator.page(page)
    except PageNotAnInteger:
        # First Load
        page = 1
        profiles = paginator.page(page)
    # Якщо користувач переходить на сторінку якої в нас немає
    except EmptyPage:
        # Отримаємо кількість сторінок відповідно останю
        page = paginator.num_pages
        # Виводимо останню сторінку
        profiles = paginator.page(page)

    # Відображення кнопок пагінаційної панелі
    leftIndex = (int(page) - 1)
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return profiles, custom_range
