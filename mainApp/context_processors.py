def avatar_context (request):
    user = request.user
    try:
        avatar = user.first_name[0] + user.last_name[0]
        return {
            'avatar': avatar
        }
    except:
        return {
            'avatar': 'UU'
        }