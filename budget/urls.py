from django.urls import path, include

from .views import index, OperationListView, OperationUpdate, \
    delete_category, get_data_for_chart, delete_operation, ChartView, FamilyView, CategoryCreateView, \
    get_category_by_ajax, delete_user_from_family, DeleteFamilyView, family_operation_view, OperationCreate

urlpatterns = [
    path('ajax/<int:pk>/delete/', delete_category, name='b-ajax-delete-operation'),
    path('ajax/chart/', get_data_for_chart),
    path('ajax/category/', get_category_by_ajax),

    path('operation/chart/', ChartView.as_view(), name='b-chart'),
    path('operation/add/', OperationCreate.as_view(), name='b-operation-create'),
    path('operation/<int:pk>/delete/', delete_operation, name='b-operation-delete'),  # is_ajax
    path('operation/<int:pk>/', OperationUpdate.as_view(), name='b-operation-update'),
    path('operation/', OperationListView.as_view(), name='b-list-operation'),

    path('category/', CategoryCreateView.as_view(), name='b-category'),
    path('category/<int:pk>/delete/', delete_category, name='b-category-delete'),

    path('family/user/<int:pk>/remove/', delete_user_from_family, name='b-family-delete-user'),
    path('family/operation/', family_operation_view, name='b-family-operation'),
    path('family/delete/', DeleteFamilyView.as_view(), name='b-family-delete'),
    path('family/', FamilyView.as_view(), name='b-family'),

    path('', index, name='b-index'),
]
