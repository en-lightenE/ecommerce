from django.forms import ValidationError
import pytest

pytestmark = pytest.mark.django_db


class TestCategoryModel:
    def test_str_method(self, category_factory):
        # Arrange

        # Act
        x = category_factory(name="test_category")
        # Assert
        assert x.__str__() == "test_category"
        pass


class TestBrandModel:
    def test_str_method(self, brand_factory):
        # Arrange

        # Act
        x = brand_factory(name="test_brand")
        # Assert
        assert x.__str__() == "test_brand"
        pass


class TestProductModel:
    def test_str_method(self, product_factory):
        # Arrange

        # Act
        x = product_factory(name="test_product")
        # Assert
        assert x.__str__() == "test_product"
        pass


class TestProductLineModel:
    def test_str_method(self, product_line_factory, attribute_value_factory):
        attr = attribute_value_factory(attribute_value="test")
        obj = product_line_factory(sku="12345", attribute_value=(attr,))
        assert obj.__str__() == "12345"

    def test_duplicate_order_values(self, product_line_factory, product_factory):
        obj = product_factory()
        product_line_factory(order=1, product=obj)
        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=obj).clean()


class TestProductImageModel:
    def test_str_method(self, product_image_factory):
        obj = product_image_factory(order=1)
        assert obj.__str__() == "1"


class TestProductTypeModel:
    def test_str_method(self, product_type_factory, attribute_factory):
        test = attribute_factory(name="test")
        obj = product_type_factory.create(name="test_type", attribute=(test,))

        assert obj.__str__() == "test_type"


class TestAttributeModel:
    def test_str_method(self, attribute_factory):
        obj = attribute_factory(name="test_attribute")
        assert obj.__str__() == "test_attribute"


class TestAttributeValueModel:
    def test_str_method(self, attribute_value_factory, attribute_factory):
        obj_a = attribute_factory(name="test_attribute")
        obj_b = attribute_value_factory(attribute_value="test_value", attribute=obj_a)
        assert obj_b.__str__() == "test_attribute-test_value"


class TestUserModel:
    def test_str_method(self, user_factory):
        obj = user_factory()
        assert obj.__str__() == "js@js.com"
