class PlayerBuild:
    def __init__(self, player, kart, wheels, glider):
        self.player = player
        self.kart = kart
        self.wheels = wheels
        self.glider = glider

    def __str__(self):
        return f"Player: {self.player[0]}, Kart: {self.kart[0]}, Wheels: {self.wheels[0]}, Glider: {self.glider[0]}"

    def __repr__(self):
        return str(self)


players = [line.strip().split(",") for line in open("players.csv")]
karts = [line.strip().split(",") for line in open("karts.csv")]
wheels = [line.strip().split(",") for line in open("wheels.csv")]
gliders = [line.strip().split(",") for line in open("gliders.csv")]

builds = []
for player in players:
    for kart in karts:
        for wheel in wheels:
            for glider in gliders:
                builds.append(PlayerBuild(player, kart, wheel, glider))

if input("Optimize with stats or build selection? ") == "stats":
    print("Stats:")
    print("1: Speed, 2: Acceleration, 3: Weight, 4: Handling, 5: Traction, 6: Mini-Turbo")

    answer = input("Enter stats to optimize: ")
    optimize = {}
    if answer != "":
        optimize = {int(x) for x in answer.split(" ")}

    unoptimize = {}
    answer = input("Enter stats to unoptimize: ")
    if answer != "":
        unoptimize = {int(x) for x in answer.split(" ")}
else:
    def getPartFromPartialName(parts, name):
        for part in parts:
            if name in part[0]:
                return part
        return None

    build = PlayerBuild(getPartFromPartialName(players, input("Enter player: ")), getPartFromPartialName(karts, input("Enter kart: ")), getPartFromPartialName(wheels, input("Enter wheels: ")), getPartFromPartialName(gliders, input("Enter glider: ")))

    def analyzeBuild(build):
        statsIndexes = [1, 2, 3, 4, 5, 6]
        statsMappings = {}
        for stat in statsIndexes:
            statsMappings[stat] = float(build.player[stat]) + float(build.kart[stat]) + float(build.wheels[stat]) + float(build.glider[stat])
        def sortKey(e):
            return statsMappings[e]
        statsIndexes.sort(reverse=True, key=sortKey)
        return statsIndexes

    stats = ["Speed", "Acceleration", "Weight", "Handling", "Traction", "Mini-Turbo"]
    indexes = analyzeBuild(build)

    print(f"Your build has been detected to favor {stats[indexes[0]-1]} and {stats[indexes[1]-1]}, and it does not favor {stats[indexes[len(indexes)-1]-1]}")

    optimize = {indexes[0], indexes[1]}
    unoptimize = {indexes[len(indexes)-1]}

def sortKey(e):
    val = 0.0
    for i in range(1, 7):
        if i in optimize:
            val += float(e.player[i]) + float(e.kart[i]) + float(e.wheels[i]) + float(e.glider[i])
        elif i in unoptimize:
            val -= (float(e.player[i]) + float(e.kart[i]) + float(e.wheels[i]) + float(e.glider[i])) / 2
        else:
            continue
    return val

builds.sort(reverse=True, key=sortKey)

for i in range(10):
    print(f"#{i+1} - {builds[i]}")

input()
