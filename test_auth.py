import pytest
from class_defines import data, User
from auth import auth_login, auth_logout, auth_register, reset_request, reset_reset
from helper_functions import user_from_uid

def auth_register_test():
    auth_register('jeffrey.oh@student.unsw.edu.au', 'password', 'Jeffrey', 'Oh')
    assert 
    assert auth_register('jeffrey.oh@student.unsw.edu.au', 'right password', 'Jeffrey', 'Oh') == ('12345', 'correct token')
    with pytest.raises(ValueError): # Following should raise exceptions
        assert auth_register('jeffrey.oh@student.unsw.edu.au', 'good     password', 'Jeffrey', 'This is a string that is much longer than the max length')
        assert auth_register('jeffrey.oh@student.unsw.edu.au', 'good password', 'This is a string that is much longer than the max length', 'Oh')
        assert auth_register('jeffrey.oh@student.unsw.edu.au', 'password that does not meet requirements', 'Jeffrey', 'Oh')
        assert auth_register('bad email', 'good password', 'Jeffrey', 'Oh')

def auth_login_test():
    assert auth_login('z5555555@student.unsw.edu.au', 'right password') == (12345, 'correct token')
    with pytest.raises(ValueError): # Following should raise exceptions
        assert auth_login('bad email', 'right password')
        assert auth_login('z5555555@asdfghjkl', 'right password')
        assert auth_login('z55555@.com', 'right password')
        assert auth_login('@', 'right password')
        assert auth_login('.com', 'right password')
        assert auth_login('z5555555@student.unsw.edu.au', 'wrong password')
        assert auth_login('z5555555@asdfghjkl', 'wrong password')

def auth_logout_test():
    auth_logout('Active token') # Should log out user
    auth_logout('Inactive token')   # Should do nothing

def auth_passwordreset_request_test():
    auth_passwordreset_request('Registered email')  # Should send reset requesy
    auth_passwordreset_request('Unregistered email')    # Should do nothing

def auth_passwordreset_reset_test():
    auth_passwordreset_reset('Valid reset code', 'Valid password')    # No exception raised
    with pytest.raises(ValueError):   # Following should raise exceptions
        auth_passwordreset_reset('Invalid reset code', 'Valid password')
        auth_passwordreset_reset('Valid reset code', 'Invalid password')
        auth_passwordreset_reset('Invalid reset code', 'Invalid password')