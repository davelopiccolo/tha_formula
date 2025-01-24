import random
import numpy as np
import pandas as pd

def main():
    for i in range(len(circuits)):
        gran_prix(circuits[i], league)
    
    show_driver_standings(league)
    



class Team():
    def __init__ (self, name, drivers, car):
        self.name = name
        self.drivers = drivers
        self.car = car
        self.points = 0
class Car():
    def __init__ (self, speed, reliability):
        self.speed = speed
        self.reliability = reliability
        

class Driver():
    def __init__ (self, name, pace, exp, speed, management):
        self.name = name
        self.pace = pace
        self.exp = exp
        self.speed = speed
        self.management = management
        self.tyre_wear = 0
        self.total_time = 0
        self.points = 0
        
        
class Track():
    def __init__ (self, name, time, laps, difficulty):
        self.name = name
        self.time = time
        self.laps = laps
        self.difficulty = difficulty

#CARS
st_one = Car(80,90)
ml_one = Car(78, 95)
prin_one = Car(85,85)
rogue_one = Car(90, 76)
pkmn_one = Car(83, 80)
eggy_one = Car(80, 80)

shadow = Driver("Shadow", 80, 67, 91, 82)
rogue = Driver("Rogue", 92, 70, 73, 83)

pikachu = Driver("Pikachu", 73, 75, 80, 81)
grovyle = Driver("Grovyle", 81, 63, 87, 79) 

sonic = Driver("Sonic", 82, 80, 94, 87)
tails = Driver("Tails", 80, 70, 80, 80)

mario = Driver("Mario", 70, 83, 80, 90)
luigi = Driver("Luigi", 71, 83, 75, 84)

peach = Driver("Peach", 80, 73, 84, 79)
daisy = Driver("Daisy", 90, 72, 73, 81)

yoshi = Driver("Yoshi", 80, 80, 90, 80)
koopa = Driver("Koopa", 60, 50, 50, 53)





team_st = Team("ST Racing", [sonic, tails], st_one)
team_ml = Team("Italian Brothers", [mario, luigi], ml_one)
team_prin = Team("Princess Racing", [daisy, peach], prin_one)
team_pkmn = Team("Pokemon Racing", [pikachu, grovyle], pkmn_one)
team_rogue = Team("Rogue Racing", [rogue, shadow], rogue_one)
team_shell = Team("Shell  Racing", [yoshi, koopa], eggy_one)

league = [team_ml, team_st, team_prin, team_pkmn, team_rogue, team_shell]

mondello_circuit = Track("Mondello City Circuit", 80, 55, 1.5)
davoli_circuit = Track("Davoli Marina Bay", 100, 40 , 2.5)
zisa_circuit = Track("Castello Della Zisa Circuit", 75, 50, 2.5)
etna_circuit = Track("Etna Rolex Gran Prix", 70, 60, 1)
catanzaro_circuit = Track("Catanzaro Lido TAG HEUER Gran Prix", 75, 60, 1.5)
motel_agip_circuit = Track("ENI Motel Agip City Circuit", 90, 45, 3.5)
anacapri_circuit = Track("Rolex Anacapri Gran Prix", 65, 70, 0.5)

circuits = [mondello_circuit, davoli_circuit, zisa_circuit, etna_circuit, catanzaro_circuit, motel_agip_circuit, anacapri_circuit]

def lap_time(track, driver, car):
    
    lap_error = False    
    error = (track.difficulty + driver.tyre_wear - driver.exp/100)  * random.uniform(0,1.5)
    if error > 3.5:
        lap_error = True
    
          
    sigma = track.difficulty * 2
    random_var = random.gauss(0, sigma)
    

    speed_factor = (driver.pace / 100)*1.1 - (car.speed / 100) - (driver.speed / 100)*1.5
    if driver.tyre_wear > driver.management / 100:
        lap_time = track.time + random_var* (1 + speed_factor) + (driver.tyre_wear - driver.management / 100)
    else:
        lap_time = track.time + random_var * (1 + speed_factor)
    
    if lap_error:
        lap_time += random.randint(1,5)      
    minutes = int(lap_time // 60)
    seconds = int(lap_time % 60)
    cents = int((lap_time - int(lap_time)) * 100)
        
    visual_lap_time = f"{minutes}:{seconds}:{cents:02}"
    driver.tyre_wear += 0.25
    driver.total_time += lap_time
    return lap_time, visual_lap_time
        

def gran_prix(track, teams):
    points = [25,18,15,12,10,8,6,4,2,1]
    laps = []
    for x in range(track.laps):
        for team in teams:
            for driver in team.drivers:
                laps.append({driver.name : lap_time(track, driver, team.car)[0]})
    fastest_lap = None
    for lap in laps:
        if fastest_lap == None:
            fastest_lap = lap
        else:
            if list(fastest_lap.values())[0] > list(lap.values())[0]:
                fastest_lap = lap
    fastest_time = list(fastest_lap.values())[0]
    fastest_driver = list(fastest_lap.keys())[0]
    minutes = int(fastest_time // 60)
    seconds = int(fastest_time % 60)
    cents = int((fastest_time - int(fastest_time)) * 100)
    
                    
                
    
    
                
    
    winner = None
    min_time = float('inf')
    for team in teams:
        for driver in team.drivers:
            if driver.total_time < min_time:
                min_time = driver.total_time
                winner = driver.name
    results = {}
    for team in teams:
        for driver in team.drivers:
            results.update({driver.name : (driver.total_time - min_time)})
    driver_team = {driver.name : team.name for team in teams for driver in team.drivers}
    classification = sorted(results.items(), key=lambda item: item[1])
    df = pd.DataFrame(classification, index=range(1, len(classification) + 1))
    df.columns = ["Driver", "Gap"]
    df["Gap"] = df["Gap"].apply(lambda x: "WINNER" if x == 0 else f"+{x:.3f}s")
    df["Team"] = df["Driver"].map(driver_team)
    points_position = []
    for pilot in classification:
        points_position.append(pilot[0])
    
    for team in teams:
        for driver in team.drivers:
            if driver.name in points_position:
                position = points_position.index(driver.name)
                driver.points += points[position] if position < len(points) else 0
            

      
    print(f"The {track.name} Gran Prix")
    print(df)
    print(f"Fastest Lap: {minutes}:{seconds}:{cents} - {fastest_driver} ")


    
    for team in teams:
        for driver in team.drivers:
            driver.total_time = 0
            driver.tyre_wear = 0
    
def show_driver_standings(teams):
    # Creiamo una lista di tuple (Driver Name, Team Name, Points)
    driver_standings = []
    for team in teams:
        for driver in team.drivers:
            driver_standings.append((driver.name, team.name, driver.points))

    # Ordina i piloti in base ai punti in ordine decrescente
    driver_standings.sort(key=lambda x: x[2], reverse=True)

    # Mostra la classifica
    print("\nDriver Standings:")
    print(f"{'Pos':<5}{'Driver':<15}{'Team':<20}{'Points':<10}")
    for i, (driver_name, team_name, points) in enumerate(driver_standings, start=1):
        print(f"{i:<5}{driver_name:<15}{team_name:<20}{points:<10}")
    



def lap_time_debug(track, driver, car):
    print(f"\n--- Debug Giro: Pilota {driver.name} ---")
    
    # Parametri iniziali
    print(f"Caratteristiche pilota: pace={driver.pace}, speed={driver.speed}, exp={driver.exp}, management={driver.management}")
    print(f"Tyre Wear iniziale: {driver.tyre_wear}")
    print(f"Caratteristiche auto: speed={car.speed}, reliability={car.reliability}")
    print(f"Speed Factor: {max(2, min(1, (driver.pace / 100) - (car.speed / 100) - (driver.speed / 100)))}")
    
    lap_error = False    
    error = (track.difficulty + driver.tyre_wear - driver.exp / 100) * random.uniform(0, 1.5)
    print(f"Errore calcolato: {error:.2f}")
    if error > 3.5:
        lap_error = True
        print(">> ERRORE: Penalità aggiuntiva sul giro per errore del pilota.")

    sigma = track.difficulty * 0.3
    random_var = random.gauss(0, sigma)
    print(f"Random Var (variazione casuale): {random_var:.2f}")
    
    # Calcolo del tempo sul giro
    base_lap_time = track.time
    speed_factor = (1 - min(1, (driver.pace / 100) - (car.speed / 100) - (driver.speed / 100)))
    print(f"Speed Factor: {speed_factor}")
    tyre_penalty = max(0, driver.tyre_wear - driver.management / 100)
    print(tyre_penalty)
    
    lap_time = base_lap_time + random_var * speed_factor + tyre_penalty
    if lap_error:
        penalty = random.randint(1, 5)
        lap_time += penalty
        print(f"Penalità errore aggiunta: +{penalty}s")
    
    driver.tyre_wear += 0.25  # Incremento consumo gomme
    driver.total_time += lap_time

    # Debug del tempo calcolato
    minutes = int(lap_time // 60)
    seconds = int(lap_time % 60)
    cents = int((lap_time - int(lap_time)) * 100)
    visual_lap_time = f"{minutes}:{seconds:02}:{cents:02}"

    print(f"Tempo sul giro: {visual_lap_time}")
    print(f"Tyre Wear aggiornato: {driver.tyre_wear}")
    print(f"Tempo totale aggiornato: {driver.total_time:.2f}s")

    return lap_time, visual_lap_time

# Simulazione di 10 giri per Sonic
sonic_car = st_one  # Auto di ST Racing
track = mondello_circuit

# for lap in range(1, 11):
#     print(f"\n== Giro {lap} ==")
#     lap_time_debug(track, sonic, sonic_car)

            

if __name__ == "__main__":
    main()