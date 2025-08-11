import chainlit as cl
from chainlit.auth import create_jwt
from ello.client import chat


@cl.on_chat_start
def start_chat():
    cl.user_session.set(
        "message_history",
        [
            {
                "content": "You are Ello, you always reply in Emojis. Do not use words. Just emojis to communicate your message",
                "role": "system",
            }
        ],
    )


@cl.step(name="Reasoning", show_input=False)
async def reasoning_step(user_message: str):
    current_step = cl.context.current_step
    current_step.output = ""
    has_thinking = False
    message_history = cl.user_session.get("message_history", [])
    message_history.append({"role": "user", "content": user_message})
    response = await chat(messages=message_history, stream=True, )

    async for chunkie in response:
        chunk = chunkie.choices[0].delta
        if chunk.content == "<think>":
            has_thinking = True
            continue
        elif chunk.content == "</think>":
            break
        else:
            await current_step.stream_token(chunk.content)
    return has_thinking, response


@cl.on_message
async def on_message(message: cl.Message):
    message_history = cl.user_session.get("message_history", [])
    has_thinking, response = await reasoning_step(message.content)
    final_message = cl.Message(content="")

    ai_response = ""
    async for chunkie in response:
        chunk = chunkie.choices[0].delta 
        if has_thinking and chunk.content != "</think>":
            continue
        elif chunk:
            await final_message.stream_token(chunk.content)
            ai_response += chunk.context
        else:
            await final_message.update()
    if ai_response:
        message_history.append({"role": "assistant", "content": ai_response})
        cl.user_session.set("message_history", message_history)


if __name__ == "__main__":
    from chainlit.cli import run_chainlit
    run_chainlit(__file__)
