import factory
import datetime
from ecommerce.account.models import User
from ecommerce.product.models import (
    Category,
    Product,
    Brand,
    ProductLine,
    ProductImage,
    ProductType,
    Attribute,
    AttributeValue,
)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda x: "Category_%d" % x)


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = "test_brand"


class AttributeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Attribute

    name = "test_attribute"
    description = "test attribute"


class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductType

    name = "test_product_type"

    @factory.post_generation
    def attribute(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.attribute.add(*extracted)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = "test_product"
    description = factory.Sequence(lambda x: "Test_Description_%d" % x)
    is_digtial = True
    brand = factory.SubFactory(BrandFactory)
    category = factory.SubFactory(CategoryFactory)
    is_active = True
    product_type = factory.SubFactory(ProductTypeFactory)


class AttributeValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AttributeValue

    attribute_value = "test_attribute"
    attribute = factory.SubFactory(AttributeFactory)


class ProductLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLine

    price = 10.00
    sku = "12345"
    stock_qty = 1
    product = factory.SubFactory(ProductFactory)
    is_active = True

    @factory.post_generation
    def attribute_value(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.attribute_values.add(*extracted)


class ProductImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductImage

    name = "product_image"
    alternative_text = "test alternative text"
    url = "test.jpg"
    productline = factory.SubFactory(ProductLineFactory)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    
    email = "js@js.com"
    date_of_birth = datetime.datetime(1981, 4, 8)
    fname = "jon"
    remember_me = True
    lname = "Constant"
    phone = "4074946120"
    password = "js.sj"
