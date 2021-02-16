from django import template

from ..forms import OperationForm

register = template.Library()


@register.inclusion_tag('budget/include/form_finance.html')
def form_finance(*args):
    form = OperationForm()
    return {'form': form}
