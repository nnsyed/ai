from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

class Player(BaseModel):
    name: str
    goals: int
    assists: int

class Team(BaseModel):
    players: list[Player]

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.responses.parse(
    model="gpt-5-mini",
    input="Return the name, goals and assists scored by Argentina national team players at the 2022 FIFA World Cup.",
    text_format=Team,
)

team = response.output_parsed

for player in team.players:
    print(f"{player.name}: {player.goals}")