from rest_framework.response import Response

class OptionalPaginationMixin:
    def get_paginate_queryset(self, queryset):
        """
        Handles DRF's pagination logic.
        """
        if self.get_pagination_class() is None:
            return None
        return super().paginate_queryset(queryset)

    def get_pagination_class(self):
        if self.request.query_params.get("pagination") == "false":
            return None
        return self.pagination_class

    def paginate_queryset(self, queryset):
        if self.get_pagination_class() is None:
            return None
        return super().paginate_queryset(queryset)

    def get_paginated_response(self, data):
        if self.get_pagination_class() is None:
            return Response(data)
        return super().get_paginated_response(data)
