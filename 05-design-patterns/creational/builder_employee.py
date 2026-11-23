"""Builder: refactor the HR onboarding system.

Before: create_employee() with 17 positional parameters (False, True, True...).
After: an Employee data class built step by step with chainable methods,
plus preset builders for common profiles.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Employee:
    """The product: a plain data container."""

    first_name: str
    last_name: str
    email: str
    department: str
    position: str
    salary: float
    start_date: str
    manager_id: Optional[int] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    has_parking: bool = False
    has_laptop: bool = False
    has_vpn_access: bool = False
    has_admin_rights: bool = False
    office_location: Optional[str] = None
    contract_type: str = "permanent"


class EmployeeBuilder:
    """Collects the fields step by step; build() validates and returns the Employee."""

    def __init__(self):
        self._fields = {"start_date": "TBD", "salary": 0.0}

    # Each method stores some fields and returns self, so calls can be chained.
    def with_name(self, first_name: str, last_name: str) -> "EmployeeBuilder":
        self._fields.update(first_name=first_name, last_name=last_name)
        return self

    def with_email(self, email: str) -> "EmployeeBuilder":
        self._fields["email"] = email
        return self

    def with_job(self, department: str, position: str, salary: float) -> "EmployeeBuilder":
        self._fields.update(department=department, position=position, salary=salary)
        return self

    def with_start_date(self, start_date: str) -> "EmployeeBuilder":
        self._fields["start_date"] = start_date
        return self

    def with_manager(self, manager_id: int) -> "EmployeeBuilder":
        self._fields["manager_id"] = manager_id
        return self

    def with_contact(self, phone=None, address=None, emergency_contact=None) -> "EmployeeBuilder":
        self._fields.update(phone=phone, address=address, emergency_contact=emergency_contact)
        return self

    def with_equipment(self, laptop: bool = False, parking: bool = False) -> "EmployeeBuilder":
        self._fields.update(has_laptop=laptop, has_parking=parking)
        return self

    def with_access(self, vpn: bool = False, admin: bool = False) -> "EmployeeBuilder":
        self._fields.update(has_vpn_access=vpn, has_admin_rights=admin)
        return self

    def with_office(self, office_location: str) -> "EmployeeBuilder":
        self._fields["office_location"] = office_location
        return self

    def with_contract(self, contract_type: str) -> "EmployeeBuilder":
        self._fields["contract_type"] = contract_type
        return self

    def build(self) -> Employee:
        # All validation in one place, instead of scattered in a giant function.
        f = self._fields
        if not f.get("first_name") or not f.get("last_name"):
            raise ValueError("Name is required")
        if "@" not in (f.get("email") or ""):
            raise ValueError("Valid email is required")
        if "department" not in f or "position" not in f:
            raise ValueError("Job (department and position) is required")
        if f["salary"] < 0:
            raise ValueError("Salary cannot be negative")
        return Employee(**f)


class DeveloperBuilder(EmployeeBuilder):
    """Preset: a senior developer always gets a laptop, VPN and admin rights."""

    def __init__(self, first_name: str, last_name: str, email: str, salary: float = 75000):
        super().__init__()
        (self.with_name(first_name, last_name)
             .with_email(email)
             .with_job("Engineering", "Senior Developer", salary)
             .with_equipment(laptop=True)
             .with_access(vpn=True, admin=True)
             .with_office("Paris HQ"))


class InternBuilder(EmployeeBuilder):
    """Preset: interns get a laptop only, on an internship contract."""

    def __init__(self, first_name: str, last_name: str, email: str, department: str, manager_id: int):
        super().__init__()
        (self.with_name(first_name, last_name)
             .with_email(email)
             .with_job(department, "Intern", 15000)
             .with_manager(manager_id)
             .with_equipment(laptop=True)
             .with_office("Paris HQ")
             .with_contract("internship"))


if __name__ == "__main__":
    employee = (
        EmployeeBuilder()
        .with_name("John", "Doe")
        .with_email("john.doe@company.com")
        .with_job("Engineering", "Senior Developer", 75000)
        .with_start_date("2024-01-15")
        .with_equipment(laptop=True, parking=False)
        .with_access(vpn=True, admin=True)
        .build()
    )
    print(employee)

    dev = DeveloperBuilder("John", "Doe", "john.doe@company.com").build()
    intern = InternBuilder("Jane", "Smith", "jane.smith@company.com", "Marketing", 42).build()
    print(dev)
    print(intern)
