import pytest
from org_struct.domain.services import Service

from tests.fakes import (
    FakeDepartmentRepo,
    FakeEmployeeRepo
)



class FakeRepos:
    def __init__(self):
        self.department = FakeDepartmentRepo()
        self.employee = FakeEmployeeRepo()


@pytest.fixture
def service():
    repos = FakeRepos()
    return Service(repos), repos
