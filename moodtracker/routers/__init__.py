from . import moods
from . import users
from . import authentications

def init_router(app):
    app.include_router(authentications.router)
    app.include_router(users.router)
    app.include_router(moods.router)