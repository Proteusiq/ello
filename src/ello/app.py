import chainlit as cl
from ello.client import chat 


@cl.on_message
async def on_message(message: cl.Message):
    response = await chat(
        messages=[
            {
                "content": "You are a helpful bot, you always reply in Emojis",
                "role": "system"
            },
            {
                "content": message.content,
                "role": "user"
            }
        ],
        stream=False,
    )
    await cl.Message(content=response.choices[0].message.content).send()

