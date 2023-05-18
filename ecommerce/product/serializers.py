from rest_framework import serializers

from .models import (
    Brand,
    Category,
    Product,
    ProductLine,
    ProductImage,
    Attribute,
    AttributeValue,
)


class CategorySerializer(serializers.ModelSerializer):
    catagory_slug = serializers.CharField(source="slug")

    class Meta:
        model = Category
        fields = [
            "catagory_slug",
        ]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        exclude = ("id",)


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ["name", "id"]


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(many=False)

    class Meta:
        model = AttributeValue
        fields = ["attribute", "attribute_value"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ("id",)


class ProductLineSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)
    attribute_values = AttributeValueSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = [
            "price",
            "sku",
            "stock_qty",
            "order",
            "product_image",
            "attribute_values",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        av_data = data.pop("attribute_values")
        attr_values = {}
        for key in av_data:
            attr_values.update({key["attribute"]["id"]: key["attribute"]["name"]})
        data.update({"specification": attr_values})
        return data
    


class ProductSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source="brand.name")
    category_name = serializers.CharField(source="category.name")
    product_line = ProductLineSerializer(many=True)
    attribute = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            "name",
            "slug",
            "description",
            "brand_name",
            "category_name",
            "product_line",
            "attribute"
        ]

    def get_attribute(self, obj):
        attribute = Attribute.objects.filter(product_type_attribute__product__id=obj.id)
        return AttributeSerializer(attribute, many=True).data
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        av_data = data.pop("attribute")
        attr_values = {}
        for key in av_data:
            attr_values.update({key["id"]: key["name"]})
        data.update({"type specification": attr_values})
        return data