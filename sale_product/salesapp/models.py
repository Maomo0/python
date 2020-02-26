from django.db import models
# Create your models here.


class Employee(models.Model):
    # 员工表
    sex_choices = (
        ('F', '女'),
        ('M', '男'),
    )
    emp_no = models.CharField(verbose_name="员工编号", max_length=5, primary_key=True)
    emp_name = models.CharField(verbose_name="员工姓名", max_length=10)
    sex = models.CharField(verbose_name='性别', max_length=1, choices=sex_choices)
    dept = models.CharField(verbose_name='所属部门', max_length=4)
    title = models.CharField(verbose_name='职称', max_length=6)
    date_hired = models.DateField(verbose_name='入职时间', null=True, blank=True)
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    salary = models.IntegerField(verbose_name='工资')
    addr = models.CharField(verbose_name='住址', null=True, max_length=50, blank=True)
    Mod_date = models.DateTimeField(verbose_name='操作者', auto_now=True, blank=True)
    emp_img = models.ImageField(default="", verbose_name='员工图片', upload_to='emp/')

    class Meta:
        verbose_name = '员工信息表'
        verbose_name_plural = verbose_name
        db_table = 'employee'

    def __str__(self):
        return self.emp_no


class Customer(models.Model):
    # 客户表
    customer_id = models.CharField(verbose_name='客户号', max_length=5, primary_key=True)
    customer_name = models.CharField(verbose_name='客户名称', max_length=20, null=False)
    addr = models.CharField(verbose_name='客户住址', max_length=40, null=False)
    tel_no = models.CharField(verbose_name='客户电话', max_length=12, null=False)
    zip_code = models.CharField(verbose_name='邮政编码', max_length=6, null=True, blank=True)

    class Meta:
        verbose_name = '顾客信息表'
        verbose_name_plural = verbose_name
        db_table = 'customer'

    def __str__(self):
        return self.customer_id


class Sales(models.Model):
    # 销售表
    order_no = models.IntegerField(verbose_name='订单编号', primary_key=True)
    customer_id = models.ForeignKey('Customer', max_length=20, on_delete=models.CASCADE, verbose_name='客户号')
    sale_id = models.ForeignKey('Employee', max_length=5, on_delete=models.CASCADE, verbose_name='员工编号')
    tot_amt = models.DecimalField(verbose_name='订单金额', max_digits=11, decimal_places=2)
    order_date = models.DateField(verbose_name='订货日期', null=True, blank=True)
    ship_date = models.DateField(verbose_name='出货日期', null=True, blank=True)
    invoice_no = models.CharField(verbose_name='发票号码', max_length=10, unique=True)

    class Meta:
        verbose_name = '销售信息表'
        verbose_name_plural = verbose_name
        db_table = 'sales'
        ordering = ['order_no']

    def __str__(self):
        return self.invoice_no  # 外键会关联的字段


class SaleItem(models.Model):
    # 销货明细表
    # 这张表就是不能加__str__()
    order_no = models.ForeignKey('Sales', on_delete=True, verbose_name='订单编号')
    prod_id = models.OneToOneField('Product', verbose_name='产品名称', max_length=5, primary_key=True, on_delete=True)
    qty = models.IntegerField(verbose_name='销售数量')
    unit_price = models.DecimalField(verbose_name='单价', max_digits=11, decimal_places=2)  # 数字11位小数两位
    order_date = models.DateField(verbose_name='订单日期', null=True, blank=True)

    class Meta:
        verbose_name = '售货明细表'
        verbose_name_plural = verbose_name
        db_table = 'sale_item'


class Product(models.Model):
    prod_id = models.CharField(max_length=5, verbose_name='产品编号', primary_key=True)
    prod_img = models.ImageField(verbose_name='产品图片', default="", upload_to='./')
    prod_name = models.CharField(verbose_name='产品名称', max_length=20)

    class Meta:
        verbose_name = '产品信息表'
        verbose_name_plural = verbose_name
        db_table = 'product'
    
    def __str__(self):
        return self.prod_name
