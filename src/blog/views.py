from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from faker import Faker

from blog.models import Blog, Entity


# Create your views here.
def create_blog(request):
    faker = Faker("UK")
    saved_data = Entity(
        blog=[
            Blog(name=faker.word(), text=faker.paragraph(nb_sentences=5), author=faker.last_name()) for _ in range(10)
        ],
        headline=faker.paragraph(nb_sentences=1),
    ).save()
    return HttpResponse(f"done {saved_data}")


def all_blogs(request) -> HttpResponse:
    blogs = Entity.objects.all()
    print(blogs)
    return HttpResponse(f"done{[blog.headline for blog in blogs]}")
