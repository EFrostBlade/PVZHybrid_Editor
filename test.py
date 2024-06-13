# ruff: noqa: F401,F403,F405,E402,F541,E722
import torch
from ChatTTS.core import Chat
from IPython.display import Audio, display

chat = Chat()
chat.load_models()

script = """
文本测试ABCD1234
"""
texts = script.split("---")
# texts = sorted(texts)
print(texts)
params_refine_text = {"prompt": "[oral_2][laugh_0][break_6]"}
wavs = chat.infer(
    texts,
    params_refine_text=params_refine_text,
    use_decoder=True,
    do_text_normalization=False,
)
print("DONE")
from IPython.display import display

for i, t in enumerate(texts[:2]):
    audio = Audio(wavs[i], rate=24000, autoplay=False)
    print(i)
    display(audio)
