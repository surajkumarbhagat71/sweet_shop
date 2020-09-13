from django.shortcuts import render , redirect,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.views.generic import  ListView ,DetailView , TemplateView , View
from .models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.utils.timezone import timezone

# Create your views here.

class HomeView(ListView):
    model = Sweets
    template_name = 'users/home.html'

##############################################  User Work ########################################

class UserRegistationView(View):
    def get(self,request,*args,**kwargs):
        form = UserForm(request.POST or None)
        data = {"form":form}
        return render(request,'users/registations.html', data)

    def post(self,requset,*args,**kwargs):
        form = UserForm(requset.POST or None)
        if form.is_valid():
            form.save()
            return redirect('login')


class LoginView(View):
    def get(self,request,*args,**keargs):

        return render(request,'users/login.html')

    def post(self,request,*args,**kwargs):
        if request.method == 'POST':
            username = self.request.POST.get('username')
            password = self.request.POST.get('password')

            cond = Q(email_id = username) & Q(password = password)

            check = Users.objects.filter(cond).count()

            if (check == 1):
                request.session['login'] = username
                return redirect('order_summary')
            else:
                return redirect('login')




class AddToCartView(View):
    def get(self,request,pk,*args,**kwargs):

        if not request.session.has_key('login'):
            return redirect('login')

        user = Users.objects.get(email_id=request.session['login']).user_id

        product = get_object_or_404(Sweets,sweet_id = pk)

        get_product , create = AddToCart.objects.get_or_create(user_id = Users(user),orders=False,sweet_id=product)

        order_query = Order.objects.filter(user_id = user,ordered=False)

        if order_query.exists():
            order = order_query[0]
            if order.items.filter(sweet_id__sweet_id=product.sweet_id).exists():
                get_product.qty += 1
                get_product.save()
                return redirect('order_summary')
            else:
                order.items.add(get_product)
                return redirect('order_summary')
        else:
            order = Order.objects.create(user_id=Users(user),ordered=False,order_date=timezone)
            order.items.add(get_product)
            return redirect('order_summary')


class OrderSummaryView(View):
    def get(self, request, *args, **kwargs):
        if not request.session.has_key('login'):
            return redirect('login')

        user = Users.objects.get(email_id=request.session['login']).user_id
        try:
            context = {"order":Order.objects.get(user_id= Users(user),ordered=False)}
            return render(request, 'users/cart_item.html', context)
        except:
            return render(request,'users/cart_item.html')


class MyOrderView(View):
    def get(self,request,*args,**kwargs):
        if not request.session.has_key('login'):
            return redirect('login')
        user = Users.objects.get(email_id=request.session['login']).user_id

        context = {"myorder":Order.objects.filter(user_id=Users(user),ordered=True)}

        return render(request,'users/my_order.html',context)



class RemoveItemFormCart(View):
    def get(self,request,pk,*args,**kwargs):

        if not request.session.has_key('login'):
            return redirect('login')

        item = get_object_or_404(Sweets,sweet_id=pk)

        user = Users.objects.get(email_id=request.session['login']).user_id

        order = Order.objects.filter(user_id=Users(user),ordered=False)

        if order.exists():
            order_query = order[0]
            if order_query.items.filter(sweet_id__sweet_id=item.sweet_id,orders=False).exists():

                cart_item = AddToCart.objects.filter(user_id = Users(user),orders=False,sweet_id = item.sweet_id)[0]
                if cart_item.qty > 1:
                    cart_item.qty -= 1
                    cart_item.save()
                    return redirect('order_summary')
                else:
                    order_query.items.remove(item.sweet_id)
                    return redirect('order_summary')
            else:
                return redirect('order_summary')
        else:
            return render(request,'users/home.html')


class CheckoutView(View):
    def get(self,request,*args,**kwargs):
        form = CheckoutForm()

        data = {"forms":form}
        return render(request,'users/checkout.html',data)

    def post(self,request,*args,**kwargs):
        if not request.session.has_key('login'):
            return redirect('login')

        user = Users.objects.get(email_id=request.session['login']).user_id

        order = Order.objects.get(user_id=Users(user),ordered=False)

        form = CheckoutForm(request.POST or None)

        if form.is_valid():
            u = form.save(commit=False)
            u.user = Users(user)
            u.save()

            order.user_address = u
            order.save()
            return redirect('payment')
        else:
            return redirect('checkout')


class UserLogoutView(View):
    def get(self,request):
        if request.session.has_key('login'):
            del request.session['login']
        return render(self.request,'users/login.html')


class PaymentView(View):
    def get(self,request,*args,**kwargs):
        if not request.session.has_key('login'):
            return redirect('login')

        user = Users.objects.get(email_id=request.session['login']).user_id

        order = Order.objects.get(user_id = Users(user),ordered=False)

        if order.user_address:
            return render(request,'users/payment.html')
        else:
            return render(request,'users/checkout.html')

    def post(self,request,*args,**kwargs):
        if not request.session.has_key('login'):
            return redirect('login')

        user = Users.objects.get(email_id=request.session['login']).user_id
        order = Order.objects.get(user_id= user,ordered=False)

        if self.request.POST.get('cod') == "cod":
            p = Payment()
            p.user = Users(user)
            p.amount = order.get_total_price()
            p.order_id = order
            p.save()

            order_item = order.items.all()
            order_item.update(orders = True)
            for x in order_item:
                x.save()

            order.ordered = True
            order.save()
            return redirect('myorder')
        return render(request,'users/home.html')



###############################################  Owner #########################


class Dashaboard(View):
    def get(self,request,*args,**kwargs):

        context = {
            "allsweet":Sweets.objects.all().count(),
            "allorder":Order.objects.filter(ordered=True).count(),
            "alluser":Users.objects.all().count(),
        }
        return render(request,'owner/dashaboard.html',context)


class OwnerLoginView(View):
    def get(self,request,*args,**keargs):

        return render(request,'owner/login.html')

    def post(self,request,*args,**kwargs):
        if request.method == 'POST':
            username = self.request.POST.get('username')
            password = self.request.POST.get('password')

            cond = Q(email_id = username) & Q(password = password)

            check = Owner.objects.filter(cond).count()

            if (check == 1):
                request.session['owner_login'] = username
                return redirect('dashaboard')
            else:
                return redirect('owner_login')


class AddSweet(View):
    def get(self,request,*args,**kwargs):
        if not request.session.has_key('owner_login'):
            return redirect('owner_login')

        form = SweetForm()
        context = {"sweetform":form}

        return render(request,'owner/add_sweet.html',context)

    def post(self,request,*args,**kwargs):
        if not request.session.has_key('owner_login'):
            return redirect('owner_login')

        form = SweetForm(request.POST or None , request.FILES or None)

        if form.is_valid():
            form.save()
            return redirect('dashaboard')


class AllSweetView(View):
    def get(self,request,*args,**kwargs):
        if not request.session.has_key('owner_login'):
            return redirect('owner_login')

        try:
            data = {"allsweet":Sweets.objects.all()}
        except ObjectDoesNotExist:
            raise Http404('Itam Not Avalable')
        return render(request,'owner/all_sweet.html',data)


class AdminLogoutView(View):
    def get(self,request,*args,**kwargs):
        if request.session.has_key('owner_login'):
            del request.session['owner_login']
        return render(request,'owner/login.html')






