import pytest
import jwt
from json import dumps
from class_defines import data, User
from auth import auth_login, auth_logout, auth_register, reset_request, reset_reset
from helper_functions import user_from_uid

def test_register_basic():
    global data
    token = jwt.encode({'email': 'jeffrey.oh@student.unsw.edu.au'}, 'password', algorithm = 'HS256')
    token = token.decode('utf-8')
    # register works
    assert auth_register('jeffrey.oh@student.unsw.edu.au', 'password', 'Jeffrey', 'Oh') == dumps({'u_id': 0,'token': token})
    assert user_from_uid(0) == data['accounts'][0]

def test_register_errors():
    with pytest.raises(ValueError): # bad last name
        assert auth_register('jeffrey.poh@student.unsw.edu.au', 'password', 'Jeffrey', 'This is a string that is much longer than the max length')
    with pytest.raises(ValueError): # bad first name
        assert auth_register('jeffrey.noh@student.unsw.edu.au', 'good password', 'This is a string that is much longer than the max length', 'Oh')
    with pytest.raises(ValueError): # bad password     
        assert auth_register('jeffrey.doh@student.unsw.edu.au', 'short', 'Jeffrey', 'Oh')
    with pytest.raises(ValueError): # bad email    
        auth_register('bad email', 'good password', 'Jeffrey', 'Oh')

def test_login_basic():
    token = jwt.encode({'email': 'jeffrey.oh@student.unsw.edu.au'}, 'password', algorithm = 'HS256')
    token = token.decode('utf-8')
    # login works
    assert auth_login('jeffrey.oh@student.unsw.edu.au', 'password') == dumps({'u_id': 0,'token': token})
 
def test_login_errors():
    with pytest.raises(ValueError): # email doesnt exist
        assert auth_login('jeffrey.crow@student.unsw.edu.au', 'password')
    with pytest.raises(ValueError): # wrong password
        assert auth_login('jeffrey.oh@gmail.com', 'wrong password')
    with pytest.raises(ValueError): # password corresponding to wrong email
        assert auth_login('jeffrey.moh@gmail.com', 'password')

def test_logout_basic():
    token = jwt.encode({'email': 'jeffrey.oh@student.unsw.edu.au'}, 'password', algorithm = 'HS256')
    token = token.decode('utf-8')
    # logout works
    assert auth_logout(token) == dumps({'is_success': True}) # Should log out user
    assert auth_logout(token) == dumps({'is_success': False}) # Should do nothing
    assert data['accounts'][0].token == ''
    assert auth_logout('Inactive token') == dumps({'is_success': False})  # Should do nothing

def test_passwordreset_request():
    assert reset_request('jeffrey.oh@student.unsw.edu.au') == dumps({})  # Should send reset requesy
    assert reset_request('Unregistered email') == dumps({})   # Should do nothing

def test_passwordreset_reset():
    resetcode = data['accounts'][0].reset_code
    with pytest.raises(ValueError):   # wrong reset code
        reset_reset('null reset code', 'new_password')
    with pytest.raises(ValueError):   # bad password
        reset_reset(data['accounts'][0].reset_code,'short')
    # password changed, if this doesnt work possible error in request
    assert reset_reset(resetcode, 'new_password') == dumps({})
    assert data['accounts'][0].password == 'new_password'
    assert data['accounts'][0].reset_code == ''
    with pytest.raises(ValueError):   # code should be invalid
        reset_reset(resetcode, 'new_password')