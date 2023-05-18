from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    Brand,
    Category,
    Product,
    ProductLine,
    ProductImage,
    AttributeValue,
    Attribute,
    ProductType
)


class EditLinkLineInline(object):
    def edit(self, instance):
        url = reverse(
            f"admin:{instance._meta.app_label}_{instance._meta.model_name}_change",
            args=[instance.id],
        )
        if instance.pk:
            link = mark_safe('<a href="{u}">edit</a>'.format(u=url))
            return link
        else:
            return ""


class ProductLineImageInline(admin.TabularInline):
    model = ProductImage


class ProductLineInline(EditLinkLineInline, admin.TabularInline):
    model = ProductLine
    readonly_fields = ("edit",)


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductLineInline]


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue.product_line_attribute_values.through


class ProductLineAdmin(admin.ModelAdmin):
    inlines = [ProductLineImageInline, AttributeValueInline]


class AttributeInline(admin.TabularInline):
    model = Attribute.product_type_attribute.through


class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [AttributeInline]

admin.site.register(ProductLine, ProductLineAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(ProductType, ProductTypeAdmin)
