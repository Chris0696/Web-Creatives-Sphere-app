from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from ..decorators import customer_required

from ..forms import CustomRegisterForm, CustomerProfileForm
from ..models import CustomerProfile

User = get_user_model()


class RegisterUser(CreateView):
    model = User
    form_class = CustomRegisterForm
    template_name = 'users/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'User created successfully!')
        login(self.request, user)
        return redirect('projects:projects')


@login_required(login_url='users:login')
def customerAccount(request):
    customerprofile = request.user.customerprofile
    print(customerprofile)
    context = {'profile': customerprofile}
    return render(request, 'users/customer_account.html', context)


"""@method_decorator([login_required, customer_required], name='dispatch')
class EditCustomerAccount(UpdateView):
    model = CustomerProfile
    form_class = CustomerProfileForm
    template_name = 'users/customer_profile_form.html'
    success_url = reverse_lazy('users:edit-account')

    def get_object(self):
        return self.request.user.customerprofile

    def form_valid(self, form):
        messages.success(self.request, 'Account updated with success!')
        return super().form_valid(form)
"""


@login_required(login_url='users:login')
@customer_required
def EditCustomerAccount(request):
    customerprofile = request.user.customerprofile
    form = CustomerProfileForm(instance=customerprofile)

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES, instance=customerprofile)
        if form.is_valid():
            form.save()

            return redirect('customer-account')

    context = {'form': form}
    return render(request, 'users/customer_profile_form.html', context)




"""@login_required(login_url='users:login')
def inbox(request):
    customerprofile = request.user.customerprofile

    messageRequests = customerprofile.messages.all()

    unreadCount = messageRequests.filter(is_read=False).count()

    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}

    return render(request, 'users/inbox.html', context)"""
