import main
import pytest
import os
from DatabaseUrlGenerator import getLines

def getCreds():
    if (os.path.exists("creds.txt")):
        lines = getLines("creds.txt")
        return (lines[0], lines[1])
    else:
        return (os.environ["Username"],os.environ["Password"])

creds = getCreds()
print("Hello World")

expectedInventory = """<tr>
        <td>
         Soda
        </td>
        <td>
         3
       </td>"""

@pytest.fixture
def client(request):
    client = main.app.test_client()
    return client

def test_login(client):
    rv = client.get("/login")
    assert "Please Log In" in rv.data

def test_inventory(client):
    rv = client.post("/login", data = {
        "username": creds[0],
        "password": creds[1]})
    rv = client.get("/inventory")
    assert expectedInventory in rv.data

def test_pos(client):
    rv = client.post("/login", data = {
        "username": creds[0],
        "password": creds[1]})
    rv = client.get("/pos")
    assert "<h1> Bob's Grocery</h1>" in rv.data

def test_logout(client):
    rv = client.post("/login", data = {
        "username": creds[0],
        "password": creds[1]})
    rv = client.get("/logout")
    print(rv.data)
    assert "<h2>Logged Out</h2>" in rv.data
