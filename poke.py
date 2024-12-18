import requests
import json

# 포켓몬 ID 범위 (Gen 7: 썬/문)
gen7_range = range(1, 810)

# 한글-영문 매핑 (샘플로 몇 개만 추가)
korean_mapping = {}

# 결과 저장용 리스트
pokemon_data = []

for poke_id in gen7_range:
    url = f"https://pokeapi.co/api/v2/pokemon-species/{poke_id}/"
    response = requests.get(url)

    if response.status_code == 200:

        data = response.json()

        name = data["name"]
        names = data["names"]
        # for name in filter(lambda x: x, names):
        #     print(name)

        ko_name = [
            poke_name for poke_name in names if poke_name["language"]["name"] == "ko"
        ]
        if len(ko_name):
            ko_name = ko_name[0]["name"]
        print("poke_id", poke_id, name)
        pokemon_data.append({"poke_id": poke_id, "eng_name": name, "ko_name": ko_name})

with open("pokemon.json", "w", encoding="utf-8") as file:
    json.dump(pokemon_data, file, ensure_ascii=False, indent=4)

print("JSON 파일 생성 완료: pokemon.json")
