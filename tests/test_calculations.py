from app.routers.calculations import  add
def test_add():
    print("test add function")
    sum = add(2,3)
    assert sum == 5

