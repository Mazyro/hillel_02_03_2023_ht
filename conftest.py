import pytest
import faker


fake = faker.Faker()


@pytest.fixture(scope='session')
def faker_fixture():
    yield fake


@pytest.fixture(autouse=True)
def django_db_setup(db):
    # from pprint import pp
    # __builtins__['pp'] = pp
    # print('BEFORE')
    # # code before test runs
    yield
    # del __builtins__['pp']
    # print('AFTER')
    # # code after test runs
