# Cody by Curtis Wang
# Edited by Abigail Zulueta
# RECONSIDERATION: I just tried making another server file like suggested.

import uvicorn
from typing import Optional
from fastapi import FastAPI, HTTPException, Path, status, Query, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.screen.client import Client
import socket
from gui import Battleship

# ======================================================================================================================
# RECONSIDERATION: I just tried making another server file like suggested.
# ======================================================================================================================


security = HTTPBasic()
app = FastAPI(
    title="Battleship Server",
    description="Implementation of a simultaneous multi-game Battleship server by[Your name here]."
)


# ======================================================================================================================
# RECONSIDERATION: I just tried making another server file like suggested. Looked online, and youtube-- used sockets.
# NOTE: There was no excuse on my end, I just couldn't figure it out in time. I allocated more time to getting a
#       "working" GUI instead of the WEB API, and that's just poor management on my end.
# ======================================================================================================================


async def get_game(game_id: str):
    """
    Get a game from the battleship game database, otherwise raise a 404.

    :param game_id: the uuid in str of the game to retrieve
    """
    the_game = await Battleship.get_game(game_id)
    if the_game is None:
        raise HTTPException(status_code=404, detail=f"Game {game_id} not found.")
    return the_game


@app.get('/')
async def home():
    return {"message": "Welcome to Battleship!"}


@app.post('/user/create')
async def create_user(username: Optional[str] = Query(..., description='the username')):
    user, password = create_user(username)
    return {'success': True, 'username': user, 'password': password}


@app.get('/game/create/{num_players}', status_code=status.HTTP_201_CREATED)
async def create_game(num_players: int = Path(..., gt=0, description='the number of players'),
                      num_decks: Optional[int] = Query(2, description='the number of decks to use'),
                      credentials: HTTPBasicCredentials = Depends(security)):
    new_uuid, new_term_pass, game_owner = await Battleship
    if credentials.username != game_owner:
        return False
    else:
        print(f"{credentials.username} = {game_owner}")
        return {'success': True,
                'game_id': new_uuid,
                'termination_password': new_term_pass,
                'game_owner': game_owner}


@app.post('/game/{game_id}/add_player')
async def add_player(game_id: str = Path(..., description='the unique game id'),
                     username: str = Query(..., description='the username'),
                     credentials: HTTPBasicCredentials = Depends(security)):
    print(credentials.username)
    the_game = await get_game(game_id)
    if the_game.num_players > 2:  # Fixed number of max players = 2
        raise HTTPException(status_code=400)
    else:
        player_idx = the_game.num_players + 1
        return {'success': True, 'game_uuid': game_id, 'player_username': username, 'player_idx': player_idx}


@app.post('/game/{game_id}/initialize')
async def init_game(game_id: str = Path(..., description='the unique game id'),
                    credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username:
        print(credentials.username)
        the_game = await get_game(game_id)
        the_game.initial_deal()
        dealer_stack, player_stacks = the_game.get_stacks()
        return {'success': True, 'dealer_stack': dealer_stack, 'player_stacks': player_stacks}


@app.post('/game/{game_id}/player/{player_idx}/hit')
async def player_hit(game_id: str = Path(..., description='the unique game id'),
                     player_idx: int = Path(..., description='the player index (zero-indexed)'),
                     credentials: HTTPBasicCredentials = Depends(security)):
    the_game = await get_game(game_id)
    drawn_card = the_game.player_draw(player_idx)
    return {'player': player_idx,
            'drawn_card': str(drawn_card),
            'player_stack': the_game.get_stacks()[1][player_idx]}


@app.get('/game/{game_id}/player/{player_idx}/stack')
async def player_stack(game_id: str = Path(..., description='the unique game id'),
                       player_idx: int = Path(..., description='the player index (zero-indexed)')):
    the_game = await get_game(game_id)
    return {'player': player_idx,
            'player_stack': the_game.get_stacks()[1][player_idx]}


@app.post('/game/{game_id}/dealer/play')
async def dealer_play(game_id: str = Path(..., description='the unique game id'),
                      credentials: HTTPBasicCredentials = Depends(security)):
    new_uuid, new_term_pass, game_owner = await Battleship
    the_game = await get_game(game_id)
    if credentials.username != game_owner:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    dealer_stop = the_game.dealer_draw()
    while dealer_stop is False:
        dealer_stop = the_game.dealer_draw()
    return {'player': 'dealer',
            'player_stack': the_game.get_stacks()[0]}


@app.get('/game/{game_id}/winners')
async def get_winners(game_id: str = Path(..., description='the unique game id')):
    the_game = await get_game(game_id)
    winner_list = the_game.compute_winners()
    return {'game_id': game_id,
            'winners': winner_list}


@app.post('/game/{game_id}/terminate')
async def delete_game(game_id: str = Path(..., description='the unique game id'),
                      password: str = Query(..., description='the termination password'),
                      credentials: HTTPBasicCredentials = Depends(security)):
    the_game = await Battleship.del_game(game_id, password)
    if the_game is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Game not found.")

    if credentials.password is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    elif credentials.password != password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    elif credentials.password == password:
        return {'success': True, 'deleted_id': game_id}


if __name__ == '__main__':
    # running from main instead of terminal allows for debugger
    # TODO: modify the below to add HTTPS (SSL/TLS) support
    uvicorn.run('gui:app', port=8000, log_level='info', reload=True)
