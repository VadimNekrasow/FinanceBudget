import datetime, time, re
from pprint import pprint

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse, Http404
from django.views.generic import ListView, UpdateView, CreateView
from django.db.models import Q, Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.dates import MonthArchiveView
from django.core.exceptions import PermissionDenied
from django.db.models import Sum, Count

from django.contrib.auth.models import User

from .forms import OperationForm, CategoryForm, FamilyForm
from .models import Category, Operation, Family

colors = [
    ['#A35EEB', '#EBB76A', '#525AEB', '#EAEB3B', '#46A5EB'],
    ['#0E966D', '#1CC40A', '#CCC900', '#E3A40B', '#D9550B'],
]


# Create your views here.


def get_category_by_ajax(request):
    """Получение категорий по ajax"""
    if request.user.is_anonymous:
        raise PermissionDenied
    if request.is_ajax():
        type_pay = request.GET.get('type_pay', 0)
        categories = list(
            Category.objects.filter((Q(user_id=None) | Q(user_id=request.user.id)) &
                                    Q(type_pay=type_pay)).values('id', 'name').order_by('name'))
        return JsonResponse({'categories': categories}, status=200)


def family_view(request):
    # families = Family.objects.filter(users=request.user)
    # family_id = request.GET.get('fid', families[0].id)
    # family = families.get(id=family_id)
    #
    # operations = Operation.objects.filter(user__in=family.users.all()).order_by('-date', '-id')
    # total = operations.filter(category__type_pay=1).aggregate(total=Sum('value'))['total']
    # total_cost = operations.filter(category__type_pay=0).aggregate(total=Sum('value'))['total']
    # if total is None:
    #     total = 0
    # if total_cost is None:
    #     total_cost = 0
    # total -= total_cost
    #
    # context = {
    #     'family': family,
    #     'families': families,
    #     'operations': operations,
    #     'total': total,
    # }
    if request.user.is_anonymous:
        raise PermissionDenied

    if request.method == 'POST':
        uuid = request.POST.get('uuid', None)
        if uuid and re.match(r'[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}', uuid) is not None:
            family = Family.objects.get(uuid=uuid)
            family.users.add(request.user)
            return redirect('b-family')
        form = FamilyForm(request.POST)
        if form.is_valid():
            form.save()
            form.instance.users.add(request.user)
            return redirect('b-family')

    families = Family.objects.filter(users=request.user)
    context = {
        'family': families[0] if families else None,
    }

    return render(request, 'budget/family.html', context=context)


def get_data_for_chart(request):
    """Получение данных для построения диаграммы. ajax"""
    if request.user.is_anonymous:
        raise PermissionDenied

    type_pay = int(request.GET.get('type_pay', 0))
    year = int(request.GET.get('year', datetime.datetime.now().year))
    month = int(request.GET.get('month', -1))

    data = Operation.objects.values('category__name').filter(category__type_pay=type_pay,
                                                             user__id=request.user.id)
    # .annotate(total=(Sum('value')))
    if month == -1:
        data = data.filter(date__year=year)
    else:
        data = data.filter(date__year=year, date__month=month)
    data = data.annotate(total=(Sum('value')))
    data = list(data)

    for i in range(len(data)):
        item = data[i]
        item.update({'color': colors[type_pay][i % len(colors[type_pay])]})

    return JsonResponse({'data': data}, status=200)


def view_chart(request):
    """Отображание страницы с пустой диаграммой"""
    return render(request, 'budget/chart.html')


def delete_category(request, pk):
    """Удаление категории. Вызов происходит при помощи ajax"""
    if request.user.is_anonymous:
        raise PermissionDenied
    category = Category.objects.get(id=pk)
    if category is not None:
        if category.user == request.user:
            category.delete()
            return JsonResponse({'result': 'ok'}, status=200)
        return JsonResponse({'result': 'bad'}, status=200)


def delete_operation(request, pk):
    """Удаление операции. Вызов происходит при помощи ajax"""
    if request.user.is_anonymous:
        raise PermissionDenied
    operation = Operation.objects.get(id=pk)
    if operation is not None:
        if operation.user == request.user:
            operation.delete()
            return JsonResponse({'result': 'ok'}, status=200)
        return JsonResponse({'result': 'bad'}, status=200)


def category_view(request):
    if request.user.is_anonymous:
        return redirect('/')

    form = CategoryForm(initial={'user_id': request.user.id})
    if request.method == "POST":
        bound_form = CategoryForm(request.POST)
        if bound_form.is_valid():
            bound_form.instance.user = request.user
            bound_form.save()
            return redirect('/category/')
        else:
            form = bound_form
    category_list = Category.objects.filter(user_id=request.user.id).order_by('type_pay', 'name')
    return render(request, 'budget/category.html', {'form': form, 'category_list': category_list})


class CategoryCreateView(CreateView):
    template_name = 'budget/category.html'
    form_class = CategoryForm
    model = Category
    success_url = reverse_lazy('b-category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_list = Category.objects.filter(user_id=self.request.user.id).order_by('type_pay', 'name')
        context.update({'category_list': category_list})
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'].update({'user_id': self.request.user.id})
        return kwargs

    def form_valid(self, form):
        form.instance.user_id = form.cleaned_data['user_id']
        return super().form_valid(form)


def index(request):
    if request.is_ajax():
        type_pay = request.GET.get('type_pay', 0)
        categories = list(Category.objects.filter(type_pay=type_pay).values('id', 'name').order_by('name'))
        return JsonResponse({'categories': categories}, status=200)

    if request.method == "POST":
        bound_form = OperationForm(request.POST)
        if bound_form.is_valid():
            bound_form.instance.user_id = request.user.id
            bound_form.save()
            return redirect('/')
        else:
            return render(request, 'budget/index.html', {'form': bound_form})

    if request.method == "GET":
        form = OperationForm()
        # queryset = Category.objects.filter(
        #    (Q(user_id=None) | Q(user_id=request.user.id)) & (Q(type_pay=request.GET.get('type_pay', 0)))).order_by(
        #    'name')
        # form.fields['category'].queryset = queryset
        return render(request, 'budget/index.html', {'form': form})


def update_operation(request, pk):
    operation = Operation.objects.get(pk=pk)
    form_data = {'type_pay': operation.category.type_pay, 'instance': operation.category_id}
    form = OperationForm(instance=operation)

    if request.method == "POST":
        bound_form = OperationForm(request.POST, instance=operation)
        if bound_form.is_valid():
            bound_form.save()
            return redirect('/operation/' + str(pk) + '/')

    return render(request, 'budget/operation_update.html', {'form': form, 'form_data': form_data})


class OperationUpdate(UpdateView):
    form_class = OperationForm
    model = Operation
    template_name = 'budget/operation_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_data = {'type_pay': self.object.category.type_pay, 'instance': self.object.category_id}
        context.update({'form_data': form_data})
        pprint(context)
        return context

    def get_success_url(self):
        return '/operation/' + str(self.object.pk) + '/'


class OperationCreate(CreateView):
    form_class = OperationForm
    model = Operation
    template_name = 'budget/index.html'
    success_url = reverse_lazy('b-list-operation')


class OperationListView(LoginRequiredMixin, MonthArchiveView):
    login_url = '/'
    model = Operation
    template_name = 'budget/list_operation.html'
    context_object_name = 'list_operation'

    date_field = 'date'
    month_format = '%m'
    allow_empty = True

    def get_month(self):
        try:
            month = super().get_month()
        except Http404:
            month = datetime.datetime.now().strftime(self.get_month_format())
        return month

    def get_year(self):
        try:
            year = super().get_year()
        except Http404:
            year = datetime.datetime.now().strftime(self.get_year_format())
        return year

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id).order_by('-date', '-id')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        total = self.object_list.filter(category__type_pay=1).aggregate(total=Sum('value'))['total']
        if total is None:
            total = 0
        total_cost = self.object_list.filter(category__type_pay=0).aggregate(total=Sum('value'))['total']
        if total_cost is None:
            total_cost = 0
        total -= total_cost
        context.update({'total': total})
        return context
