from . import moods
from . import users
from . import authentications

def init_router(app):
    app.include_router(authentications.router,prefix="", tags=["Authentications"] )
    app.include_router(users.router, prefix="/users", tags=["Users"])
    app.include_router(moods.router, prefix="/moods", tags=["Moods"])