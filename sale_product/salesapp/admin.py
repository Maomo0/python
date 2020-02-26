from django.contrib import admin
from .models import Product, Employee, Sales, SaleItem, Customer


# Register your models here.


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('emp_no', 'emp_name', 'sex', 'dept', 'title',)
    list_filter = ('sex', 'dept', 'title',)
    search_fields = ('emp_no', 'emp_name',)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'customer_name', 'addr', 'tel_no',)
    list_filter = ('customer_id',)
    search_fields = ('customer_id', 'customer_name', 'tel_no',)


class SalesAdmin(admin.ModelAdmin):
    list_display = ('order_no', 'tot_amt', 'order_date', 'ship_date', 'invoice_no')
    list_filter = ('order_no',)
    search_fields = ('order_no', 'sale_id')


class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('prod_id', 'qty', 'unit_price', 'order_date',)
    list_filter = ('prod_id', 'order_date',)
    search_fields = ('prod_id',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('prod_id', 'prod_name')
    list_filter = ('prod_id', 'prod_name')
    search_fields = ('prod_id',)
    # fieldsets添加信息时折叠非必要信息


admin.site.site_title = '信息管理页面'  # 页面标题显示
admin.site.site_header = '产品信息管理系统'  # 页面中左上角的显示信息
admin.site.index_title = '详细信息'  # header下的显示和标题栏中的显示,修改admin模板中base_site.html即可在标题栏中不显示
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Sales, SalesAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(SaleItem, SaleItemAdmin)
