Family.objects.annotate(sum=Sum('users__operations__value'))[0].sum
Family.objects.filter(users__operations__category__type_pay=1).annotate(sum=Sum('users__operations__value'))[0].sum
u.operations.values('category__name').annotate(count=Sum('value'))
Category.objects.filter( (Q(user_id=None) | Q(user_id=0)) & (Q(type_pay=0)))
{{ value|default:"nothing" }}
u1.operations.filter(category__type_pay=1).aggregate(sum=Sum('value'))

o_list = Operation.objects.filter(user__in=f_users).order_by('-date', '-id')


https://cs3-5v4.vkuseraudio.net/p1/d2bb9792fc7/562e692c20b41b/index.m3u8?extra=37Yecuk9G-1J_qn86AvJidVCIORZWUKdLVGOsJsGz7DVpo4morQDo6XEjIkwlobf8EqOSKV6sSKWYSQx3cvgpKGXVVRfFvda2X2ITfgZdPE0gsQ7VABjaZWRC7dhIpX1YNc2jdfVY1Gq6LVPQz_5Or0X3w&long_chunk=1
https://cs3-5v4.vkuseraudio.net/p1/562e692c20b41b.mp3?extra=37Yecuk9G-1J_qn86AvJidVCIORZWUKdLVGOsJsGz7DVpo4morQDo6XEjIkwlobf8EqOSKV6sSKWYSQx3cvgpKGXVVRfFvda2X2ITfgZdPE0gsQ7VABjaZWRC7dhIpX1YNc2jdfVY1Gq6LVPQz_5Or0X3w&long_chunk=1

