import datetime

from django.shortcuts import render
from django.views import View
from .models import Employee, Customer, Product, SaleItem, Sales
from django.contrib.auth import authenticate, login
from django.db.models import Sum


# Create your views here.


class LoginView(View):
    @classmethod
    def get(cls, request):
        return render(request, './home/index.html', {})

    @classmethod
    def post(cls, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            prod = Product.objects.all()
            return render(request, './home/home.html', {'prod': prod})
        else:
            return render(request, './home/index.html', {})


class HomeView(View):
    @classmethod
    def get(cls, request):
        prod = Product.objects.all()
        return render(request, './home/home.html', {'prod': prod})

    @classmethod
    def post(cls, request):
        #  主页面
        prod = Product.objects.all()
        print(request.method)
        print('主页')
        return render(request, './home/home.html', {'prod': prod})

    @classmethod
    def check_msg(cls, request, msg_id):
        """
        显示购买的商品详细信息
        :param request:
        :param msg_id:
        :return:
        """
        # 商品信息
        prod = Product.objects.all()
        # prod_id = prod[msg_id - 1].prod_id
        prod_name = prod[msg_id - 1].prod_name
        prod_img = prod[msg_id - 1].prod_img
        qty = prod[msg_id - 1].saleitem.qty  # 销售数量
        unit_price = float(prod[msg_id - 1].saleitem.unit_price)  # 单价

        #  从关联数据中获取信息
        order_no = prod[msg_id - 1].saleitem.order_no
        tot_amt = order_no.tot_amt  # 订单总额
        emp_id = order_no.sale_id  # 操作职员信息
        customer_id = order_no.customer_id  # 顾客id

        # 显示的信息
        emp_name = emp_id.emp_name  # 操作员
        customer_name = customer_id.customer_name  # 顾客姓名
        customer_addr = customer_id.addr  # 顾客住址
        ship_date = order_no.ship_date  # 发货日期
        order_date = order_no.order_date  # 订货日期
        print(prod_name, unit_price)
        now_date = datetime.datetime.now()

        # 前端接收的是key值
        return render(request, './customer/cust_home.html', {
            'prod_name': prod_name, 'prod_img': prod_img, 'emp_name': emp_name, 'customer_name': customer_name,
            'customer_addr': customer_addr, 'order_date': order_date,
            'ship_date': ship_date, 'qty': qty, 'price': unit_price,
            'tot_amt': tot_amt, 'now_date': now_date
        })


class CustomerView(View):
    @classmethod
    def get(cls, request):
        si = SaleItem.objects.all()
        return render(request, './customer/customer_msg.html', {'si': si})

    @classmethod
    def post(cls, request):
        if request.method == 'POST':
            try:
                name = (dict(request.POST).get('customer'))[0]  # 获取搜索的名字
                if name:
                    customer = Customer.objects.filter(customer_name=name.strip()).values()[0]
                    id1 = customer['customer_id']
                    id2 = Sales.objects.filter(customer_id=id1)[0].order_no  # 获取订单编号
                    prod_name = SaleItem.objects.filter(order_no=id2)[0].prod_id.prod_name  # 通过订单编号获取产品名称
                    return render(request, './customer/search_customer.html', {'customer_id': customer['customer_id'],
                                                                               'customer_name': customer[
                                                                                   'customer_name'],
                                                                               'tel_no': customer['tel_no'],
                                                                               'prod_name': prod_name,
                                                                               'zip_code': customer['zip_code'],
                                                                               'addr': customer['addr']})
                else:
                    return render(request, './customer/customer_msg.html', {})
            except Exception:
                return cls.get(request)


class ProductView(View):
    @classmethod
    def get(cls, request):
        prod = Product.objects.all()
        return render(request, './home/home.html', {'prod': prod})

    @classmethod
    def post(cls, request):
        print('请求1')
        if request.method == 'POST':
            name = (dict(request.POST).get('prod'))[0]  # 获取搜索的名字
            print(name)
            prod_id = Product.objects.filter(prod_name=name)[0].prod_id
            prod_name = Product.objects.filter(prod_name=name)[0].prod_name
            prod_img = Product.objects.filter(prod_name=name)[0].prod_img
            print(prod_name)
            return render(request, './home/prod_search.html', {'prod_id': prod_id, 'prod_name': prod_name,
                                                               'prod_img': prod_img})

    @classmethod
    def add_prod(cls, request):
        emp_list = []
        if request.method == 'GET':
            emp_no = Sales.objects.values("sale_id").annotate(Sum("sale_id")).order_by()  # 拿到销售员工的id
            for emp in emp_no:
                emp_list.append(emp['sale_id'])
            return render(request, './product/addproduct.html', {'emp_no': emp_list})

        # 获取提交数据
        if request.method == 'POST':
            print(request.POST)
            res_dict = dict(request.POST)

            # 顾客信息
            customer_name = res_dict['customer_name'][0]
            customer_id = res_dict['customer_id'][0]
            tel_no = res_dict['tel_no'][0]
            addr = res_dict['addr'][0]
            Customer.objects.create(customer_name=customer_name, customer_id=customer_id, tel_no=tel_no, addr=addr)

            # 商品信息
            prod_id = res_dict['prod_id'][0]
            prod_name = res_dict['prod_name'][0]
            Product.objects.create(prod_id=prod_id, prod_name=prod_name)

            # 销售信息
            order_no = res_dict['order_no'][0]
            tot_mat = res_dict['tot_mat'][0]
            sale_id = res_dict['emp_no'][0]
            Sales.objects.create(order_no=order_no, tot_amt=tot_mat, sale_id=Employee(emp_no=sale_id),
                                 customer_id=Customer(customer_id=customer_id), order_date=datetime.date.today())

            # 销售明细
            unit_price = res_dict['unit_price'][0]
            qty = res_dict['qty'][0]
            SaleItem.objects.create(order_no=Sales(order_no=order_no), unit_price=unit_price, qty=qty,
                                    prod_id=Product(prod_id=prod_id))

        prod = Product.objects.all()
        return render(request, './home/home.html', {'prod': prod})

    @classmethod
    def delete_prod(cls, request):
        prod = Product.objects.all()
        if request.method == "GET":
            return render(request, './product/deleteproduct.html', {'pro': prod})
        if request.method == "POST":
            prod_dict = dict(request.POST)
            prod_name = prod_dict['prod_name'][0]

            # 获取删除对象
            prod_id = Product.objects.get(prod_name=prod_name)
            order_no = SaleItem.objects.get(prod_id=prod_id).order_no
            sa = SaleItem.objects.get(prod_id=prod_id)
            customer_id = order_no.customer_id

            # 删除
            sa.delete()
            order_no.delete()
            customer_id.delete()
            prod_id.delete()

        prod = Product.objects.all()
        return render(request, './home/home.html', {'prod': prod})

    @classmethod
    def modify_msg(cls, request):
        if request.method == "GET":
            return render(request, './product/modify_msg.html', {})
        if request.method == "POST":
            return render(request, './product/modify_msg.html', {})
