from django.db.models import Avg, Count, Q
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Pyme
from .serializers import (
    EmailTokenObtainPairSerializer,
    PymeSerializer,
    RegisterSerializer,
)


def _level_bounds(level):
    return {
        1: (0, 20),
        2: (20, 40),
        3: (40, 60),
        4: (60, 80),
        5: (80, 100),
    }.get(level)


class PymeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PymeSerializer
    queryset = Pyme.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        search = params.get("search", "").strip()
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(legal_name__icontains=search)
                | Q(locality__icontains=search)
                | Q(province__icontains=search)
                | Q(sector__icontains=search)
            )
        for field in ("work_type", "enterprise_type", "sector", "province"):
            value = params.get(field)
            if value:
                queryset = queryset.filter(**{field: value})
        band = params.get("maturity_band")
        if band == "Inicial":
            queryset = queryset.filter(maturity_score__lte=40)
        elif band == "Medio":
            queryset = queryset.filter(maturity_score__gt=40, maturity_score__lte=80)
        elif band == "Alto":
            queryset = queryset.filter(maturity_score__gt=80)
        try:
            level = int(params.get("maturity_level", ""))
        except ValueError:
            level = None
        bounds = _level_bounds(level)
        if bounds:
            lower, upper = bounds
            queryset = queryset.filter(maturity_score__gt=lower, maturity_score__lte=upper)
        return queryset

    @action(detail=False, methods=["get"])
    def options(self, request):
        queryset = Pyme.objects.all()
        return Response(
            {
                "work_types": list(
                    queryset.exclude(work_type="")
                    .values_list("work_type", flat=True)
                    .distinct()
                    .order_by("work_type")
                ),
                "enterprise_types": list(
                    queryset.exclude(enterprise_type="")
                    .values_list("enterprise_type", flat=True)
                    .distinct()
                    .order_by("enterprise_type")
                ),
                "sectors": list(
                    queryset.exclude(sector="")
                    .values_list("sector", flat=True)
                    .distinct()
                    .order_by("sector")
                ),
                "provinces": list(
                    queryset.exclude(province="")
                    .values_list("province", flat=True)
                    .distinct()
                    .order_by("province")
                ),
            }
        )

    @action(detail=False, methods=["get"])
    def summary(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        average = queryset.aggregate(value=Avg("maturity_score"))["value"]

        def grouped(field):
            rows = queryset.exclude(**{field: ""}).values(field).annotate(count=Count("id")).order_by("-count", field)
            return [{"label": row[field], "count": row["count"]} for row in rows]

        by_level = []
        for level in range(1, 6):
            lower, upper = _level_bounds(level)
            by_level.append(
                {
                    "label": str(level),
                    "count": queryset.filter(
                        maturity_score__gt=lower, maturity_score__lte=upper
                    ).count(),
                }
            )

        table = list(
            queryset.values(
                "province", "work_type", "enterprise_type"
            )
            .annotate(count=Count("id"), average_maturity=Avg("maturity_score"))
            .order_by("province", "work_type", "enterprise_type")
        )
        return Response(
            {
                "total_companies": queryset.count(),
                "distinct_sectors": queryset.exclude(sector="")
                .values("sector")
                .distinct()
                .count(),
                "average_maturity_score": round(float(average), 2) if average else None,
                "high_maturity_count": queryset.filter(maturity_score__gt=80).count(),
                "by_sector": grouped("sector"),
                "by_work_type": grouped("work_type"),
                "by_maturity_band": [
                    {"label": "Inicial", "count": queryset.filter(maturity_score__lte=40).count()},
                    {"label": "Medio", "count": queryset.filter(maturity_score__gt=40, maturity_score__lte=80).count()},
                    {"label": "Alto", "count": queryset.filter(maturity_score__gt=80).count()},
                ],
                "by_maturity_level": by_level,
                "companies": PymeSerializer(queryset, many=True).data,
                "table": table,
            }
        )


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Cuenta creada."}, status=status.HTTP_201_CREATED)


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer
    permission_classes = [AllowAny]
