from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import  HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db.models import Prefetch
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView, TemplateView
from django.core.cache import cache

from common.mixins import CacheMixin
from orders.models import Order, OrderItem
from carts.utils import delete_carts_duplicates
from carts.models import Cart
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm

class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    # success_url = reverse_lazy('main:index')

    def get_success_url(self):
        redirect_page = self.request.POST.get('next', None)
        if redirect_page and redirect_page != reverse('user:logout'):
            return redirect_page
        return reverse_lazy('main:index')
    
    def form_valid(self, form: AuthenticationForm):
        session_key = self.request.session.session_key
        user = form.get_user()
        if user:
            auth.login(self.request, user)
            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)
                carts = Cart.objects.filter(user=user)
                delete_carts_duplicates(user, carts)
            messages.success(self.request,'Вход успешно выполнен')
            return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Авторизация'
        return context

class UserRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)
            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)
                carts = Cart.objects.filter(user=user)
                delete_carts_duplicates(user, carts)
            messages.success(self.request,'Регистрация и вход успешно выполнены')
            return HttpResponseRedirect('/users/profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Регистрация'
        return context

class UserProfileView(LoginRequiredMixin, CacheMixin, UpdateView):
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Профайл успешно обновлен')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Кабинет"
        orders = Order.objects.filter(user=self.request.user).prefetch_related(
                    Prefetch(
                        'orderitem_set',
                        queryset = OrderItem.objects.select_related('product'),
                    )
                ).order_by('-id')
        context['orders'] = self.set_get_cache(orders, f'user_orders_{self.request.user.id}')
        return context

class UserCartView(TemplateView):
    template_name = 'users/users_cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Корзина"
        return context


# @login_required
# def profile(req):
#     if req.method == "POST":
#         print('true')
#         form = UserProfileForm(data=req.POST, instance=req.user, files=req.FILES)
#         if form.is_valid():
#             form.save()
#             messages.warning(req,'Данные успешно обновились')
#             return HttpResponseRedirect(reverse('user:profile'))
#     else:
#         form = UserRegistrationForm(instance=req.user)

#     orders = (
#         Order.objects.filter(user=req.user).prefetch_related(
#             Prefetch(
#                 'orderitem_set',
#                 queryset = OrderItem.objects.select_related('product'),
#             )
#         )
#         .order_by('-created_timestamp')
#     )
        
#     context = {
#         'title': 'Home - Кабинет',
#         'form': form,
#         'orders': orders
#     }
#     return render(req, 'users/profile.html', context)

# def users_cart(req):
#     return render(req, 'users/users_cart.html')

# @login_required
# def logout(req):
#     auth.logout(req)
#     messages.success(req,'Выход успешно выполнен')
#     return redirect(reverse('main:index'))

# def login(req):
#     if req.method == 'POST':
#         form = UserLoginForm(data=req.POST)
#         if form.is_valid():
#             username = req.POST['username']
#             password = req.POST['password']
#             user = auth.authenticate(username=username, password=password)

#             session_key = req.session.session_key

#             if user:
#                 auth.login(req, user)
#                 messages.success(req,'Вход успешо выполнен')
                
#                 if session_key:
#                    Cart.objects.filter(session_key=session_key).update(user=user)
#                    carts = Cart.objects.filter(user=user)
#                    delete_carts_duplicates(user, carts)

#                 redirect_page = req.POST.get('next', None)
#                 if redirect_page and redirect_page != reverse('user:logout'):
#                     return HttpResponseRedirect(req.POST.get('next'))
                
#                 return HttpResponseRedirect(reverse('main:index'))
#     else:
#         form = UserLoginForm() 

#     context = {
#         'title': 'Home - Авторизация',
#         'form': form
#     }
#     return render(req, 'users/login.html', context)

# def registration(req):
#     if req.method == "POST":
#         form = UserRegistrationForm(req.POST)
#         if form.is_valid():
#             form.save() 
#             user = form.instance

#             session_key = req.session.session_key

#             auth.login(req, user)

#             if session_key:
#                 Cart.objects.filter(session_key=session_key).update(user=user)
#                 carts = Cart.objects.filter(user=user)
#                 delete_carts_duplicates(user, carts)

#             messages.success(req,'Регистрация и вход успешно выполнены')
#             return HttpResponseRedirect(reverse('main:index'))
#     else:
#         form = UserRegistrationForm()

#     context = {
#         'title': 'Home - Регистрация',
#         'form': form
#     }
#     return render(req, 'users/registration.html', context)