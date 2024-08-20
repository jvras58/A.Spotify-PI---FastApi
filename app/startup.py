from api.authentication.router import router as auth_router
from api.spotify.router import router as spotify_router
from api.user.router import router as user_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# ----------------------------------
#  APP CORSMiddleware
# ----------------------------------
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# ----------------------------------
#   APP ROUTERS
# ----------------------------------
app.include_router(user_router, prefix='/users', tags=['Users'])
app.include_router(auth_router, prefix='/auth', tags=['Auth'])
app.include_router(spotify_router, prefix='/spotify', tags=['Spotify'])
# ----------------------------------


@app.get('/')
def read_root():
    return {'message': 'Wellcome to API!'}
