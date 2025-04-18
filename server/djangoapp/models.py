from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib import admin


class CarMake(models.Model):
    """Model representing a car manufacturer."""
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Other fields as needed

    def __str__(self):
        """String representation of the CarMake model."""
        return self.name


class CarModel(models.Model):
    """Model representing a specific car model."""
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('COUPE', 'Coupe'),
        ('CONVERTIBLE', 'Convertible'),
        ('HATCHBACK', 'Hatchback'),
    ]

    car_make = models.ForeignKey(
        CarMake,
        on_delete=models.CASCADE,
        related_name='models'
    )
    name = models.CharField(max_length=100)
    type = models.CharField(
        max_length=20,
        choices=CAR_TYPES,
        default='SUV'
    )
    year = models.IntegerField(
        default=2023,
        validators=[
            MaxValueValidator(2023),
            MinValueValidator(2015)
        ]
    )
    # Additional fields
    color = models.CharField(max_length=50, blank=True, null=True)
    engine = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    def __str__(self):
        """String representation of the CarModel model."""
        return f"{self.car_make.name} {self.name} ({self.year})"


# Register models with admin site
@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'type', 'year')
    list_filter = ('car_make', 'type', 'year')
    search_fields = ('name', 'car_make__name')