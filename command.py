Family.objects.annotate(sum=Sum('users__operations__value'))[0].sum
Family.objects.filter(users__operations__category__type_pay=1).annotate(sum=Sum('users__operations__value'))[0].sum
u.operations.values('category__name').annotate(count=Sum('value'))
Category.objects.filter( (Q(user_id=None) | Q(user_id=0)) & (Q(type_pay=0)))
{{ value|default:"nothing" }}
u1.operations.filter(category__type_pay=1).aggregate(sum=Sum('value'))

o_list = Operation.objects.filter(user__in=f_users).order_by('-date', '-id')


