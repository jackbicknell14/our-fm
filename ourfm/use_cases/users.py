from ourfm.domain.users import operations


def register(email):
    return operations.save_new_user(email)
