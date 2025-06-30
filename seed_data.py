import random
import string
from app.database import SessionLocal
from app.models import Base, Organization, Employee
from app.database import engine

# Initialize DB
Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Create or get organizations
orgs = [
    Organization(id=1, name="Acme Corp"),
    Organization(id=2, name="Globex Inc")
]
for org in orgs:
    if not db.query(Organization).filter_by(id=org.id).first():
        db.add(org)
db.commit()

first_names = ["Alice", "Bob", "Carol", "Dave", "Eva", "Frank", "Grace", "Heidi"]
last_names = ["Smith", "Johnson", "Brown", "Taylor", "Anderson", "Thomas", "Jackson"]
statuses = ["active", "not_started", "terminated"]
departments = ["Engineering", "HR", "Marketing", "Finance"]
positions = ["Manager", "Engineer", "Intern", "Director"]
locations = ["New York", "London", "Berlin", "Bangalore"]

# Bulk insert 10,000 random employees
BATCH_SIZE = 1000
total = 10000

def random_string(length=5):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

for batch in range(0, total, BATCH_SIZE):
    employees = []
    for _ in range(BATCH_SIZE):
        org_id = random.choice([1, 2])
        emp = Employee(
            first_name=random.choice(first_names),
            last_name=random.choice(last_names),
            email=f"{random_string()}@example.com",
            phone=f"+1-{random.randint(1000000000, 9999999999)}",
            status=random.choice(statuses),
            department=random.choice(departments),
            position=random.choice(positions),
            location=random.choice(locations),
            organization_id=org_id
        )
        employees.append(emp)
    db.bulk_save_objects(employees)
    db.commit()
    print(f"Inserted {batch + BATCH_SIZE} records...")

db.close()
print("✅ Done seeding 10,000 employees.")
