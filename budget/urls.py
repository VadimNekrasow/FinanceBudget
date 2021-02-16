from django.urls import path, include

from .views import index, OperationListView, category_view, update_operation, OperationUpdate, \
    delete_category, get_data_for_chart, delete_operation, view_chart, family_view, CategoryCreateView, \
    get_category_by_ajax

urlpatterns = [
    path('ajax/<int:pk>/delete/', delete_category, name='b-ajax-delete-operation'),
    path('ajax/chart/', get_data_for_chart),
    path('ajax/category/', get_category_by_ajax),

    path('operation/chart/', view_chart, name='b-chart'),
    path('operation/<int:pk>/delete/', delete_operation, name='b-operation-delete'), # is_ajax
    path('operation/<int:pk>/', OperationUpdate.as_view(), name='b-operation-update'),
    path('operation/', OperationListView.as_view(), name='b-list-operation'),

    path('category/', CategoryCreateView.as_view(), name='b-category'),
    path('category/<int:pk>/delete/', delete_category, name='b-category-delete'),

    path('family/', family_view, name='b-family'),
    path('', index, name='b-index'),
]
