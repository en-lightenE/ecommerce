from django.db import models
from django.forms import ValidationError
from mptt.models import MPTTModel, TreeForeignKey

from ecommerce.product.fields import OrderField


class ActiveQuerySet(models.QuerySet):
    # def get_queryset(self):
    #     return super().get_queryset().filter(is_active=True)
    def isactive(self):
        return self.filter(is_active=True)


class Category(MPTTModel):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=255)
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    objects = ActiveQuerySet.as_manager()

    class MMPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self) -> str:
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    is_digtial = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, related_name="brand", on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, default="empty")
    category = TreeForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, blank=True
    )
    is_active = models.BooleanField(default=False)
    product_type = models.ForeignKey("ProductType", on_delete=models.PROTECT)
    objects = ActiveQuerySet.as_manager()

    def __str__(self) -> str:
        return self.name


class Attribute(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name

class AttributeValue(models.Model):
    attribute_value = models.CharField(max_length=100)
    attribute = models.ForeignKey(
        Attribute, related_name="attribute_value", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f'{self.attribute.name}-{self.attribute_value}'


class ProductLine(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=5)
    sku = models.CharField(max_length=100)
    stock_qty = models.IntegerField()
    product = models.ForeignKey(
        Product, related_name="product_line", on_delete=models.CASCADE
    )
    is_active = models.BooleanField(default=False)
    order = OrderField(unique_for_field="product", blank=True)
    attribute_values = models.ManyToManyField(
        AttributeValue,
        through="ProductLineAttributeValue",
        related_name="product_line_attribute_values",
    )
    
    objects = ActiveQuerySet.as_manager()

    def clean(self):
        qs = ProductLine.objects.filter(product=self.product)
        for obj in qs:
            if self.id != obj.id and self.order == obj.order:
                raise ValidationError("Duplicate value.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductLine, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.sku)


class ProductLineAttributeValue(models.Model):
    attribute_value = models.ForeignKey(
        AttributeValue,
        related_name="attribute_value_product_line",
        on_delete=models.CASCADE,
    )
    product_line = models.ForeignKey(
        ProductLine,
        related_name="product_line_attribute_value",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ("attribute_value", "product_line")

    def clean(self):
        qs  = ProductLineAttributeValue\
        .objects\
        .filter(attribute_value=self.attribute_value)\
        .filter(product_line=self.product_line)\
            .exists()
        
        if not qs:
            iqs = Attribute.objects\
            .filter(attribute_value__product_line_attribute_values=self.product_line\
                ).values_list("pk", flat=True)
            
            if self.attribute_value.attribute.id in list(iqs):
                raise ValueError("Duplicate attribute exists")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductLineAttributeValue, self).save(*args, **kwargs)
        
class ProductImage(models.Model):
    name = models.CharField(max_length=150, unique=True)
    alternative_text = models.CharField(max_length=150)
    url = models.ImageField(upload_to=None, default="test.jpg")
    productline = models.ForeignKey(
        ProductLine, on_delete=models.CASCADE, related_name="product_image"
    )
    order = OrderField(unique_for_field="productline", blank=True)

    def clean(self):
        qs = ProductImage.objects.filter(productline=self.productline)
        for obj in qs:
            if self.id != obj.id and self.order == obj.order:
                raise ValidationError("Duplicate value.")

    def save(self, *arge, **kwargs):
        self.full_clean()
        return super(ProductImage, self).save(*arge, **kwargs)

    def __str__(self):
        return str(self.order)


class ProductType(models.Model):
    name = models.CharField( max_length=100)
    attribute = models.ManyToManyField(
        Attribute, 
        through="ProductTypeAttribute",
        related_name="product_type_attribute")
    
    def __str__(self):
        return str(self.name)
    
class ProductTypeAttribute(models.Model):
    
    product_type = models.ForeignKey(
       ProductType,
        related_name="product_type_attribute_pt",
        on_delete=models.CASCADE,
    )
    attribute = models.ForeignKey(
        Attribute,
       related_name="product_type_attribute_att",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ("product_type", "attribute")