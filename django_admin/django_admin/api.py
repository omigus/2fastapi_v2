from rest_framework import routers
from migrationCore import api_views as myapp_views

router = routers.DefaultRouter()
router.register(r'Company', myapp_views.CompanyViewset)
