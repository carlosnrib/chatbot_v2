import chainlit as cl
from embedchain import App
from funcoes import text_to_audio, get_movie, verifica_itens, get_itens
from movie_scrapping import find_movie
from music_scrapping import find_music
from unidecode import unidecode
import re
import random
from dotenv import load_dotenv

import os

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

@cl.on_chat_start
async def on_chat_start():
    await cl.Avatar(
        name="ARIA",
        url="/public/icon.png",
    ).send()
    await cl.Avatar(
        name="You",
        url="/public/icon_user.png",
    ).send()
    app = App.from_config(config_path="config.yaml")
    app.collect_metrics = False
    cl.user_session.set("app", app)

@cl.action_callback("more_about")
async def on_action(action):
    message = cl.Message(content=action.label, author="You", disable_feedback=True, type="user_message")
    await message.send()

    sugestions = cl.user_session.get("sugestions")
    await sugestions.remove()

    app = cl.user_session.get("app")
    msg = cl.Message(content="Pensando... Aguarde alguns instantes.")

    await msg.send()

    msg.content = ""
    

    for chunk in await cl.make_async(app.chat)(message.content):
        await msg.stream_token(chunk)

    await msg.update()

    return "Executado"

@cl.action_callback("where_watch")
async def on_action(action):
    await cl.Message(content=action.label, author="You", disable_feedback=True, type="user_message").send()

    filme = action.description

    sugestions = cl.user_session.get("sugestions")
    await sugestions.remove()

    msg2 = cl.Message(content="Pesquisando...", author="ARIA")
    await msg2.send()
    link = await find_movie(filme)
    msg2.content = ""
    msg2.content =  f"{link}"
    
    await msg2.update()
    return "Executado"

@cl.action_callback("where_listen")
async def on_action(action):
    await cl.Message(content=action.label, author="You", disable_feedback=True, type="user_message").send()

    filme = action.description

    sugestions = cl.user_session.get("sugestions")
    await sugestions.remove()

    msg2 = cl.Message(content="Pesquisando...", author="ARIA")
    await msg2.send()
    link = await find_music(f"{filme} musica")
    msg2.content = ""
    msg2.content =  f"{link}"
    
    await msg2.update()
    return "Executado"

@cl.on_message
async def check_action_movies_series(resposta: str):
    movies = await get_itens(resposta)

    movie_example1 = random.choice(movies)
    movie_example2 = random.choice(movies)

    actions=[
            cl.Action(name="where_watch", value=movie_example1, label=f"Onde posso assistir {movie_example1}?", description=movie_example1),
            cl.Action(name="more_about", value=movie_example2, label=f"Quero saber mais sobre {movie_example2}."),
    ]

    sugestions = cl.Message(content="Sugestões de próximas perguntas:", actions=actions)
    cl.user_session.set("sugestions", sugestions)
    await sugestions.send()

@cl.on_message
async def check_action_musics(resposta: str):
    musics = await get_itens(resposta)

    music_example1 = random.choice(musics)

    actions=[
            cl.Action(name="where_listen", value=music_example1, label=f"Onde posso escutar {music_example1}?", description=music_example1),
    ]

    sugestions = cl.Message(content="Sugestões de próximas perguntas:", actions=actions)
    cl.user_session.set("sugestions", sugestions)
    await sugestions.send()

@cl.on_message
async def on_message(message: cl.Message):
    app = cl.user_session.get("app")
    msg = cl.Message(content="Pensando... Aguarde alguns instantes.")
    
    palavras = message.content
    if("Aonde" in palavras.strip() or "Onde" in palavras.strip()):
        if ("filme" in palavras.strip() or "filmes" in palavras.strip()):
            msg2 = cl.Message(content="Pesquisando...")
            await msg2.send()
            filme = await get_movie(unidecode(palavras))
            link = await find_movie(filme)
            msg2.content = ""
            msg2.content =  f"{link}"
            await msg2.update()
        elif("música" in palavras.strip() or "músicas" in palavras.strip()):
            msg2 = cl.Message(content="Pesquisando...")
            await msg2.send()
            filme = await get_movie(unidecode(palavras))
            link = await find_music(filme)
            msg2.content = ""
            msg2.content =  f"{link}"
            await msg2.update()
        else:
            await cl.Message(content="Desculpa não fui capaz de encontrar a sua resposta...").send()

    else:
        query = f"""
    {message.content}

    As respostas devem estar em português e utilize sempre emojis nas respostas, eles devem estar somente no final das frases. Organize o texto de forma clara e evite código bruto. É importante não incluir conteúdo em inglês, exceto nomes. Certifique-se de que suas respostas sejam claras, já que este chat é acessível e pode ser utilizado por pessoas idosas.
    """
        await msg.send()

        msg.content = ""
        

        for chunk in await cl.make_async(app.chat)(query):
            await msg.stream_token(chunk)
        
        await text_to_audio(msg.content, "output.mp3")

        msg.elements.append(cl.Audio(name="", path="./output.mp3", display="inline"))
        
        await msg.update()

        resposta = msg.content
        
        check_itens = await verifica_itens(resposta)
        if(check_itens):
            try:
                await check_action_movies_series(resposta)

                if "música" in resposta.split() or "músicas" in resposta.split() or "músicas:" in resposta.split() or "musicais" in resposta.split() or "musicais:" in resposta.split():
                    await check_action_musics(resposta)
            except:
                pass
