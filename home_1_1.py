from pydantic import BaseModel, EmailStr, field_validator, model_validator
import json

class Address(BaseModel):
    city: str
    street: str
    house_number: int

    @field_validator('city')
    def city_must_be_long_enough(cls, v):
        if len(v) < 2:
            raise ValueError('City name must be at least 2 characters long')
        return v

    @field_validator('street')
    def street_must_be_long_enough(cls, v):
        if len(v) < 3:
            raise ValueError('Street name must be at least 3 characters long')
        return v

    @field_validator('house_number')
    def house_number_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('House number must be positive')
        return v

class User(BaseModel):
    name: str
    age: int
    email: EmailStr
    is_employed: bool
    address: Address

    @field_validator('name')
    def name_must_be_alpha(cls, v):
        if not v.isalpha() or len(v) < 2:
            raise ValueError('Name must consist of at least 2 alphabetic characters')
        return v

    @field_validator('age')
    def age_must_be_valid(cls, v):
        if not (0 <= v <= 120):
            raise ValueError('Age must be between 0 and 120')
        return v

    @model_validator(mode='before')
    def check_employment_status(cls, values):
        age = values.get('age')
        is_employed = values.get('is_employed')
        if is_employed and age is not None and age < 18:
            raise ValueError('Employed users must be at least 18 years old')
        return values

def process_user_registration(json_string: str) -> str:
    try:
        user = User.parse_raw(json_string)
        return user.json()
    except Exception as e:
        return json.dumps({"error": str(e)})

successful_json = '''
{
    "name": "Alice",
    "age": 30,
    "email": "alice@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 10
    }
}
'''

invalid_age_json = '''
{
    "name": "Bob",
    "age": 150,
    "email": "bob@example.com",
    "is_employed": false,
    "address": {
        "city": "Los Angeles",
        "street": "Sunset Boulevard",
        "house_number": 5
    }
}
'''

invalid_employment_status_json = '''
{
    "name": "Charlie",
    "age": 16,
    "email": "charlie@example.com",
    "is_employed": true,
    "address": {
        "city": "Boston",
        "street": "Cambridge Street",
        "house_number": 12
    }
}
'''

invalid_address_json = '''
{
    "name": "David",
    "age": 25,
    "email": "david@example.com",
    "is_employed": false,
    "address": {
        "city": "NY",
        "street": "A",
        "house_number": -1
    }
}
'''

print(process_user_registration(successful_json))
print(process_user_registration(invalid_age_json))
print(process_user_registration(invalid_employment_status_json))
print(process_user_registration(invalid_address_json))