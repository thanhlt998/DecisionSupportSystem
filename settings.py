SEARCH_RESULTS_FN = 'search_results.json'
NEW_GAMES_INFO_FN = 'new_game_info.json'
MAX_NO_SEARCH_RESULT = 100
TOKENIZER_PATH = 'tokenizer.pickle'
MODEL_PATH = 'model_improvement-03-0.90.h5'
CLASSIFIED_RESULT_FN = 'classified_result.json'
TOPSIS_WEIGHT = [0.3, 0.2, 0.25, 0.25]
NO_ATTRIBUTES = 4
# json_path = 'home/Downloads/game.json'

GAME_TAGS = {"Indie": "492", "Action": "19", "Adventure": "21", "Casual": "597", "Strategy": "9", "Simulation": "599",
             "RPG": "122", "Early Access": "493", "Free to Play": "113", "Singleplayer": "4182", "Violent": "4667",
             "Sports": "701", "Massively Multiplayer": "128", "Gore": "4345", "Racing": "699", "Nudity": "6650",
             "Great Soundtrack": "1756", "Atmospheric": "4166", "Multiplayer": "3859", "Sexual Content": "12095",
             "2D": "3871", "Puzzle": "1664", "VR": "21978", "Anime": "4085", "Story Rich": "1742", "Difficult": "4026",
             "Fantasy": "1684", "Horror": "1667", "Funny": "4136", "Open World": "1695", "Sci-fi": "3942",
             "Shooter": "1774", "Pixel Graphics": "3964", "Utilities": "87", "Female Protagonist": "7208",
             "Co-op": "1685", "Platformer": "1625", "First-Person": "3839", "Survival": "1662",
             "Design & Illustration": "84", "FPS": "1663", "Movie": "4700", "Family Friendly": "5350",
             "Turn-Based": "1677", "Comedy": "1719", "Retro": "4004", "Arcade": "1773", "Sandbox": "3810",
             "Online Co-Op": "3843", "Visual Novel": "3799", "Exploration": "3834", "Cute": "4726", "Classic": "1693",
             "Replay Value": "4711", "Controller": "7481", "Point & Click": "1698", "Masterpiece": "5144",
             "Psychological Horror": "1721", "Third Person": "1697", "Relaxing": "1654", "Space": "1755",
             "Zombies": "1659", "Audio Production": "1027", "Education": "1036", "Colorful": "4305",
             "Animation & Modeling": "872", "Memes": "10397", "Tactical": "1708", "Local Multiplayer": "7368",
             "Fast-Paced": "1734", "Dark": "4342", "Physics": "3968", "Mystery": "5716", "Software": "8013",
             "Web Publishing": "1038", "Rogue-like": "1716", "Short": "4234", "Realistic": "4175",
             "Shoot 'Em Up": "4255", "Building": "1643", "Survival Horror": "3978", "RPGMaker": "5577",
             "Local Co-Op": "3841", "Mature": "5611", "Management": "12472", "Party-Based RPG": "10695",
             "Video Production": "784", "Action RPG": "4231", "Action-Adventure": "4106", "Side Scroller": "3798",
             "Walking Simulator": "5900", "Crafting": "1702", "Turn-Based Strategy": "1741", "War": "1678",
             "Puzzle-Platformer": "5537", "RTS": "1676", "Historical": "3987", "Hidden Object": "1738",
             "Stealth": "1687", "Choices Matter": "6426", "Top-Down": "4791", "PvP": "1775", "Music": "1621",
             "Bullet Hell": "4885", "Character Customization": "4747", "Hack and Slash": "1646", "Competitive": "3878",
             "Dating Sim": "9551", "Fighting": "1743", "JRPG": "4434", "Rogue-lite": "3959", "Minimalist": "4094",
             "Post-apocalyptic": "3835", "Third-Person Shooter": "3814", "Tower Defense": "1645",
             "Dark Fantasy": "4604", "Procedural Generation": "5125", "Moddable": "1669", "4 Player Local": "4840",
             "Futuristic": "4295", "Dungeon Crawler": "1720", "Drama": "5984", "Medieval": "4172", "Episodic": "4242",
             "Old School": "3916", "Romance": "4947", "Multiple Endings": "6971", "Stylized": "4252",
             "Base Building": "7332", "MMORPG": "1754", "Illuminati": "7478", "Turn-Based Combat": "4325",
             "Magic": "4057", "World War II": "4150", "Surreal": "1710", "Isometric": "5851", "Card Game": "1666",
             "Top-Down Shooter": "4637", "Software Training": "1445", "Robots": "5752", "Cartoony": "4195",
             "Addictive": "4190", "Cyberpunk": "4115", "Beautiful": "5411", "Beat 'em up": "4158",
             "Resource Management": "8945", "Dark Humor": "5923", "Team-Based": "5711", "Blood": "5228", "Epic": "3965",
             "Military": "4168", "Choose Your Own Adventure": "4486", "Thriller": "4064", "Driving": "1644",
             "Experimental": "13782", "Turn-Based Tactics": "14139", "Metroidvania": "1628", "Economy": "4695",
             "Perma Death": "1759", "3D Platformer": "5395", "Hand-drawn": "6815", "City Builder": "4328",
             "Aliens": "1673", "Soundtrack": "7948", "Twin Stick Shooter": "4758", "Board Game": "1770",
             "Parkour": "4036", "Crime": "6378", "Game Development": "13906", "Flight": "15045", "Level Editor": "8122",
             "Interactive Fiction": "11014", "Destruction": "5363", "Text-Based": "31275", "Detective": "5613",
             "Cartoon": "4562", "Loot": "4236", "Arena Shooter": "5547", "PvE": "6730", "Psychological": "5186",
             "Abstract": "4400", "Real-Time": "4161", "3D": "4191", "Cult Classic": "7782", "Steampunk": "1777",
             "Photo Editing": "809", "MOBA": "1718", "Grand Strategy": "4364", "Documentary": "15339",
             "Mouse only": "11123", "Kickstarter": "5153", "1990's": "6691", "Match 3": "1665", "Lovecraftian": "7432",
             "Demons": "9541", "2.5D": "4975", "Dystopian ": "5030", "1980s": "7743", "Real-Time with Pause": "7107",
             "Trains": "1616", "Alternate History": "4598", "2D Fighter": "4736", "Space Sim": "16598",
             "3D Vision": "29363", "Split Screen": "10816", "Clicker": "379975", "Rhythm": "1752", "4X": "1670",
             "GameMaker": "1649", "Mod": "5348", "Touch-Friendly": "25085", "Dark Comedy": "19995", "Mechs": "4821",
             "Strategy RPG": "17305", "Tutorial": "12057", "Tactical RPG": "21725", "Logic": "6129",
             "Score Attack": "5154", "Science": "5794", "Pirates": "1681", "Remake": "5708", "Dinosaurs": "5160",
             "Psychedelic": "1714", "Ninja": "1688", "Linear": "7250", "Wargame": "4684", "Voxel": "1732",
             "Dragons": "4046", "Political": "4853", "e-sports": "5055", "Dungeons & Dragons": "14153",
             "Otome": "31579", "Trading Card Game": "9271", "Battle Royale": "176981", "Narration": "5094",
             "Lore-Rich": "3854", "TrackIR": "8075", "Tanks": "13276", "Real Time Tactics": "3813",
             "Comic Book": "1751", "Swordplay": "4608", "CRPG": "4474", "Games Workshop": "5310", "Hex Grid": "1717",
             "Western": "1647", "Hacking": "5502", "Supernatural": "10808", "Politics": "4754", "Superhero": "1671",
             "Runner": "8666", "Cold War": "5179", "Assassin": "4376", "Noir": "6052", "Co-op Campaign": "4508",
             "Character Action Game": "3955", "Gaming": "150626", "God Game": "5300", "Gun Customization": "5765",
             "Naval": "6910", "Satire": "1651", "Silent Protagonist": "15954", "Cinematic": "4145", "Parody ": "4878",
             "Modern": "5673", "Emotional": "5608", "Time Management": "16689", "NSFW": "24904",
             "Inventory Management": "6276", "Hunting": "9564", "Grid-Based Movement": "7569", "Crowdfunded": "7113",
             "Experience": "9994", "Villain Protagonist": "11333", "Football": "7226", "Gothic": "3952",
             "Heist": "1680", "Nonlinear": "6869", "Quick-Time Events": "4559", "Agriculture": "22602",
             "Mythology": "16094", "Souls-like": "29482", "Time Travel": "10679", "Underwater": "9157",
             "Class-Based": "4155", "Trading": "4202", "Dog": "1638", "Vampire": "4018", "Philisophical": "134316",
             "America": "13190", "Soccer": "1679", "World War I": "5382", "FMV": "18594", "Martial Arts": "6915",
             "Bullet Time": "5796", "Fishing": "15564", "Time Attack": "5390", "Conspiracy": "5372", "Cats": "17894",
             "Spectacle fighter": "4777", "Sniper": "7423", "Minigames": "8093", "Based On A Novel": "3796",
             "Programming": "5432", "Warhammer 40K": "12286", "Time Manipulation": "6625", "360 Video": "776177",
             "Mining": "5981", "Capitalism": "4845", "LEGO": "1736", "Pinball": "6621", "Sailing": "13577",
             "Asynchronous Multiplayer": "17770", "Investigation": "8369", "Music-Based Procedural Generation": "8253",
             "Mystery Dungeon": "198631", "6DOF": "4835", "Offroad": "7622", "Horses": "6041", "Chess": "4184",
             "Star Wars": "1735", "Sequel": "5230", "Artificial Intelligence": "7926", "Diplomacy": "6310",
             "Dynamic Narration": "9592", "Faith": "180368", "Steam Machine": "348922", "Rome": "6948", "Mars": "6702",
             "Gambling": "16250", "Word Game": "24003", "Typing": "1674", "On-Rails Shooter": "56690",
             "Werewolves": "17015", "Batman": "1694", "Unforgiving": "1733", "Underground": "21006",
             "Conversation": "15172", "Sokoban": "1730", "Basketball": "1746", "Golf": "7038", "Benchmark": "5407",
             "Hardware": "603297", "Intentionally Awkward Controls": "14906", "Transhumanism": "4137",
             "Mini Golf": "22955", "Bikes": "123332", "Feature Film": "233824", "Submarine": "19780",
             "Wrestling": "47827", "Baseball": "5727", "Foreign": "51306", "Motorbike": "198913", "Tennis": "5914",
             "Lara Croft": "21722", "Pool": "17927", "Cycling": "19568", "Snow": "9803", "Bowling": "7328",
             "Lemmings": "17337", "Motocross": "15868", "Hockey": "324176", "Voice Control": "27758",
             "Spelling": "71389", "Skateboarding": "1753", "BMX": "252854", "Skating": "96359", "Jet": "92092",
             "Snowboarding": "28444", "ATV": "129761", "Skiing": "7309"}
PLATFORMS = ['PC', 'PS4', 'X360', 'PS3', 'XONE', 'iOS', 'VITA', 'WIIU', '3DS', 'WII', 'DS', 'XBOX',
             'PS2', 'PSP', 'PS', 'DC', 'GBA', 'GC', 'N64',
             ]
# num = len(response.xpath("//div[contains(@class, 'tab_filter_control') and @data-param='tags']").getall())
# tags = {}
# for i in range(num):
#     tag_name = response.xpath(f"//div[contains(@class, 'tab_filter_control') and @data-param='tags'][{i+1}]/@data-loc").get()
#     id = response.xpath(f"//div[contains(@class, 'tab_filter_control') and @data-param='tags'][{i+1}]/@data-value").get()
#     tags[tag_name] = id
#
# import json
# with open('tags.json', mode='w', encoding='utf8') as f:
#     json.dump(tags, f)
#     f.close()
