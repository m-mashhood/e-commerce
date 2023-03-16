import uuid

from django.db import models

from users.models import User


class Product(models.Model):
    COSMETICS = ('cosmetic', 'Cosmetic')
    MART = ('mart', 'Mart')
    GROCERIES = ('groceries', 'Groceries')
    HEALTH = ('health', 'Health')
    FASHION = ('fashion', 'Fashion')
    ELECTRONIC = ('electronic', 'Electronic')
    MOBILE = ('mobile', 'Mobile')
    SPORTS = ('sports', 'Sports')
    DIGITAL = ('digital', 'Digital')
    FOOD = ('food', 'Food')
    OTHERS = ('others', 'Others')

    CATEGORY_CHOICES = (
        COSMETICS,
        MART,
        GROCERIES,
        HEALTH,
        FASHION,
        ELECTRONIC,
        MOBILE,
        SPORTS,
        DIGITAL,
        FOOD,
        OTHERS
    )
    NOS = ('nos', 'Nos')
    DOZEN = ('dozen', 'Dozen')
    KGS = ('kgs', 'Kgs')
    METER = ('meter', 'Meter')
    SQFT = ('sqft', 'Sqft')
    SQM = ('sqm', 'sqm')
    UNIT_CHOICES = (
        NOS,
        DOZEN,
        KGS,
        METER,
        SQFT,
        SQM
    )

    name = models.CharField(max_length=250, null=False, blank=False)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default=OTHERS[0])
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default=NOS[0])
    picture = models.ImageField(upload_to='product_pic', default='product_default.png')
    description = models.TextField(null=True, blank=True)
    in_stock = models.IntegerField(default=0)
    owned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    bought_on = models.DateField(blank=True, null=True)
    latest_price = models.FloatField(blank=False, null=False)
    key = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return f'{self.name}'


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sale_set')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_bought')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_sold')
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    purchased_quantity = models.IntegerField(null=False, blank=False)
    selling_price = models.FloatField(null=False, blank=False)
    purchase_price = models.FloatField(null=False, blank=False)

    def __str__(self):
        return f'{self.product.name} {self.buyer.username} {self.seller.username}'
