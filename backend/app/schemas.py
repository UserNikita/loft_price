from .models import Apartment


ApartmentSchema = Apartment.schema.as_marshmallow_schema()


class UpdateApartmentSchema(ApartmentSchema):
    class Meta:
        fields = ["url", "address"]


class CreateApartmentSchema(ApartmentSchema):
    class Meta:
        fields = ["url", "address"]
