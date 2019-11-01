from django.contrib import admin

from .models import Reviews
# Register your models here.

def review_display():
    # Admin cannot handle many to many relationships
    # Tag is in a many to many relationship
    list_display = [field.name for field in Reviews._meta.get_fields()]
    return list_display

class ReviewAdmin(admin.ModelAdmin):
    model = Reviews
    list_display = review_display()

admin.site.register(Reviews,ReviewAdmin)