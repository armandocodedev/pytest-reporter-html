import pytest

# Sample tests to demonstrate report generation

def test_addition():
    """Test that addition works correctly"""
    assert 1 + 1 == 2

def test_subtraction():
    """Test that subtraction works correctly"""
    assert 5 - 3 == 2

def test_create_user():
    """Test user creation functionality"""
    user = {"name": "Test User", "email": "test@example.com"}
    assert user["name"] == "Test User"

def test_update_user():
    """Test user update functionality"""
    user = {"name": "Original Name", "email": "test@example.com"}
    user["name"] = "Updated Name"
    assert user["name"] == "Updated Name"

def test_delete_user():
    """Test user deletion functionality"""
    users = [{"id": 1, "name": "User 1"}, {"id": 2, "name": "User 2"}]
    initial_count = len(users)
    users = [u for u in users if u["id"] != 1]
    assert len(users) == initial_count - 1

@pytest.mark.skip(reason="Feature not implemented yet")
def test_advanced_feature():
    """Test an advanced feature that's not implemented yet"""
    assert False

def test_failing_test():
    """This test is designed to fail for demonstration purposes"""
    assert 1 == 2, "This test is intentionally failing"