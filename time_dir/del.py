# def get_queryset(self, params):
#     sneakers = Sneakers.objects.all()
#     sort_by = self.request.GET.get("sort", "all")
#     search_fields = ["brand_sneakers", "model_sneakers"]
#     for param_name, param_value in params.items():
#         if param_name == "search_text":
#             request.session[f"search_text_{datetime.datetime.now()}"] = param_value
#             or_filter = Q()
#             for field in search_fields:
#                 or_filter |= Q(**{f"{field}__contains": param_value})
#             sneakers = sneakers.filter(or_filter)
#         else:
#             sneakers = sneakers.filter(**{param_name: param_value})
#         return render(request, template_name="shop.html", context={"sneakers": sneakers})
