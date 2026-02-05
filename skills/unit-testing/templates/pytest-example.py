import pytest
from mymodule import MyClass, my_function


class TestMyClass:
    """Test suite for MyClass"""

    def test_initialization(self):
        """Test that class initializes correctly"""
        obj = MyClass(value=42)
        assert obj.value == 42

    def test_method_returns_correct_value(self):
        """Test that method returns expected value"""
        obj = MyClass(value=10)
        result = obj.calculate()
        assert result == 100

    def test_method_raises_error_on_invalid_input(self):
        """Test that method raises appropriate error"""
        obj = MyClass(value=-1)
        with pytest.raises(ValueError, match="Value must be positive"):
            obj.validate()


def test_my_function_basic():
    """Test basic functionality"""
    result = my_function("input")
    assert result == "expected output"


def test_my_function_edge_cases():
    """Test edge cases"""
    assert my_function("") == ""
    assert my_function(None) is None


@pytest.fixture
def sample_data():
    """Fixture providing sample data for tests"""
    return {
        "name": "Test",
        "values": [1, 2, 3, 4, 5]
    }


def test_with_fixture(sample_data):
    """Test using fixture data"""
    assert len(sample_data["values"]) == 5
    assert sample_data["name"] == "Test"


@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
    (4, 8),
])
def test_with_parameters(input, expected):
    """Test with multiple parameter combinations"""
    result = my_function(input)
    assert result == expected


@pytest.fixture(scope="module")
def expensive_resource():
    """Fixture with module scope - only runs once per module"""
    # Setup (runs once)
    resource = create_expensive_resource()
    yield resource
    # Teardown (runs once after all tests)
    resource.cleanup()


def test_using_expensive_resource(expensive_resource):
    """Test using module-scoped fixture"""
    assert expensive_resource.is_ready()
