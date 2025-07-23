
## Requisitos

- Llave para API de LLM: https://platform.deepseek.com/api_keys
- Docker o Podman: https://podman.io/docs/installation
- Python 3.13+: https://www.python.org/ftp/python/3.13.5/

---

### Ejemplar de Variables de Entorno
```bash
#env vars
DEEPSEEK_API_KEY='Tu API Key aqui'
```

```python
from dataclasses import dataclass
import enum
from typing import List

from dotenv import load_dotenv, dotenv_values
import os
from openai import OpenAI

load_dotenv()

class Role(enum.StrEnum):
    User = "user"
    System = "system"

@dataclass
class Message:
    role: Role 
    content: str

    def __str__(self):
        return { "role": self.role.str(), "content": self.content }

client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), 
                base_url="https://api.deepseek.com/v1")

messages: List[Message] = []

system_prompts: List[Message] = [
    {
        "role": Role.System,
        "content": "You  are a university professor assistant"
    },
]

while True:
    msg = input(">>>")
    msgs = [ { "role" : "user", "content": msg } ]
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages= msgs,
    )
    msgs.append(response.choices[0].message)
    print(f"Messages Round 1: {msgs}")
```

```bash
# requirements.txt
annotated-types==0.7.0
anyio==4.9.0
certifi==2025.7.14
distro==1.9.0
dotenv==0.9.9
h11==0.16.0
httpcore==1.0.9
httpx==0.28.1
idna==3.10
jiter==0.10.0
openai==1.97.0
pydantic==2.11.7
pydantic_core==2.33.2
python-dotenv==1.1.1
sniffio==1.3.1
tqdm==4.67.1
typing-inspection==0.4.1
typing_extensions==4.14.1
```

```bash
python3 -m venv venv
source /venv/bin/activate
pip3 install -r requirements.txt
```

```Dockerfile
FROM python:3.13

#RUN adduser -D nonroot &&\
RUN   mkdir /home/app/
#&& chown -R nonroot:nonroot /home/app
WORKDIR /home/app
#USER nonroot
ENV DEEPSEEK_API_KEY=$DEEPSEEK_API_KEY
#COPY --chown=nonroot:nonroot . .
COPY . .

# venv
ENV VIRTUAL_ENV=/home/app/venv

# python setup
RUN python -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install -r requirements.txt

CMD ["python", "test.py"]
```

### Docker

```console
docker build -t my-username/my-image .
```

```bash
docker run -e "DEEPSEEK_API_KEY=TuLlaveAqui" 
```

### Podman
```bash
podman build -t deepseek_trial .
```

```bash
 podman run --env 'DEEPSEEK_API_KEY=$ENV_VAR' -it deepseek_trial
```

## Ejemplar de Respuesta
```bash
>>> How many protons are there in an atom of Gold ?

ChatCompletion(id='5d250b63-9a65-459b-b0a5-2d210a843d7b',
choices=[
   Choice(finish_reason='stop', 
          index=0, 
          logprobs=None, 
          message=ChatCompletionMessage(
                    content="An atom of **Gold (Au)** has **79 protons** in its nucleus. \n\nThe number of protons defines the atomic number of an element, and gold's atomic number is **79**. This means every gold atom has 79 protons, regardless of its isotope. \n\n- **Symbol:** Au  \n- **Atomic Number (Z):** 79  \n- **Protons:** 79  \n- **Electrons (in a neutral atom):** 79  \n- **Common Isotopes:** Au-197 (most stable, with 118 neutrons).  \n\nLet me know if you'd like further details!",
                    refusal=None, 
                    role='assistant', 
                    annotations=None, 
                    audio=None, 
                    function_call=None, 
                    tool_calls=None))
],
created=1753234849, 
model='deepseek-chat', 
object='chat.completion', 
service_tier=None, 
system_fingerprint='fp_8802369eaa_prod0623_fp8_kvcache', usage=CompletionUsage(completion_tokens=123, prompt_tokens=14, total_tokens=137, completion_tokens_details=None, prompt_tokens_details=PromptTokensDetails(audio_tokens=None, cached_tokens=0), prompt_cache_hit_tokens=0, prompt_cache_miss_tokens=14))
```
```bash
Messages Round 1: [{'role': 'user', 'content': 'How many protons are there in an atom of Gold ?'}, {'role': 'system', 'content': ChatCompletionMessage(content="An atom of **Gold (Au)** has **79 protons** in its nucleus. \n\nThe number of protons defines the atomic number of an element, and gold's atomic number is **79**. This means every gold atom has 79 protons, regardless of its isotope. \n\n- **Symbol:** Au  \n- **Atomic Number (Z):** 79  \n- **Protons:** 79  \n- **Electrons (in a neutral atom):** 79  \n- **Common Isotopes:** Au-197 (most stable, with 118 neutrons).  \n\nLet me know if you'd like further details!", refusal=None, role='assistant', annotations=None, audio=None, function_call=None, tool_calls=None)}]
```
## Referencias
1. https://api-docs.deepseek.com/guides/multi_round_chat
2. https://docs.docker.com/build/concepts/dockerfile/
3. https://stackoverflow.com/questions/39597925/how-do-i-set-environment-variables-during-the-docker-build-process
