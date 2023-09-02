

def detectUser(user):
    if user.role == 1:
        redirectURL = 'venderDashboard'
    elif user.role == 2:
        redirectURL = "custDashboard"

    elif user.role == None and user.is_superadmin:
        redirectURL = "/admin"
    
    return redirectURL