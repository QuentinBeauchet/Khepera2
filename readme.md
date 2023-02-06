# Installation

## V1

```c
1. Lancer webots
2. File / Open world
3. Ouvrir khepera3.wbt
4. Selectionner le controller de Khepera2
5. Choisir v1
```

## V2

```c
1. Lancer webots
2. File / Open world
3. Ouvrir khepera3.wbt
4. Selectionner le controller de Khepera2
5. Choisir v2
6. Lancer la commande 'docker-compose up -d' depuis le dossier components
```

# Choix algorithmiques

Nous avons choisis d'implementer une coordination basé sur des poids attribués a chaque comportement.

La coordinations basé sur des votes nous aurait empeché d'utiliser l'agorithme de braitengerg car les consignes aurait été trop precises et donc trop nombreuses. En revanche nous implementons tout du meme un systeme de veto car des lors que braitengerg detecte un obstacle il prend la priorité sur la recherche de source lumineuse.

Nous avons fait le choix de stopper la recherche de sources lumineuse des lors que la luminosité maximum detectés par un capteur passe sous un seuil predefini.

Notre comportement final est donc celui d'un robot parcourant son environement tout en evitant les obstacles jusqu'a ce que celui ci decouvre une source lumineuse. Tel un papillion dans le noir, il se retrouve alors a tourner autour de celle ci a pour toujours.

# Examples

```python
braitengerg = [10,10]  #Pas d'obstacle
light = [0,0]          #Pas de lumiere
speed = [10,10]        #Tout droit
```

```python
braitengerg = [10,10]  #Pas d'obstacle
light = [5,10]         #Detection de lumiere
speed = [7.5,10]       #Deplacement du robot vers la source lumineuse
```

```python
braitengerg = [5.3,10] #Detection d'un obstacle
light = [10,5]         #Detection de lumiere
speed = [10,10]        #L'evitement de l'obstacle prend la priorité
```
## Prérequis
Avant de commencer à utiliser ce projet, veuillez vous assurer d'avoir installé les éléments suivants sur votre ordinateur :
- Python 3
- Mosquitto (Broker MQTT)
- Paho (Client MQTT pour Python)

## Installation de Paho
Pour installer Paho, utilisez la commande suivante :

```
pip install paho-mqtt
```

## Lancer le broker Mosquitto

```
mosquitto -p 1880
```
