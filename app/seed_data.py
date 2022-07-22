from faker import Faker
from datetime import date
import random
import json

fake = Faker()

def create_fake_data(gender):
    entry = {}
    if gender == "male":
        first_name = fake.first_name_male().lower()
        last_name = fake.last_name().lower()
        email_domain = fake.free_email_domain()
        date_of_birth = fake.date_of_birth(minimum_age=18,maximum_age=99)
        entry["registration_id"] = fake.uuid4()
        entry["first_name"] = first_name
        entry["last_name"] = last_name
        entry["email_address"] = f"{first_name}.{last_name}@{email_domain}"
        entry["date_of_birth"] = date_of_birth.strftime("%Y-%m-%d")
        entry["gender"] = "male"
        entry["country_name"] = fake.country()
        entry["job_title"] = fake.job()
        entry["enabled"] = fake.boolean(chance_of_getting_true=90)
    if gender == "female":
        first_name = fake.first_name_female().lower()
        last_name = fake.last_name().lower()
        email_domain = fake.free_email_domain()
        date_of_birth = fake.date_of_birth(minimum_age=18,maximum_age=99)
        entry["registration_id"] = fake.uuid4()
        entry["first_name"] = first_name
        entry["last_name"] = last_name
        entry["email_address"] = f"{first_name}.{last_name}@{email_domain}"
        entry["date_of_birth"] = date_of_birth.strftime("%Y-%m-%d")
        entry["gender"] = "female"
        entry["country_name"] = fake.country()
        entry["job_title"] = fake.job()
        entry["enabled"] = fake.boolean(chance_of_getting_true=90)
    return entry

def generate_entry():
    selected_gender = random.choice(['male', 'female'])
    person = create_fake_data(selected_gender)
    return person
    #print(json.dumps(person, indent=2))