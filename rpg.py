import random


class Creature:  # БАЗОВИЙ КЛАС ДЛЯ ВСЬОГО
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp
        self.max_hp = hp

    def is_alive(self):
        return self.hp > 0


class Player(Creature):
    def __init__(self, name, hp=100):
        super().__init__(name, hp)
        self.level = 1
        self.exp = 0
        self.potions = 3
        self.money = 0

        self.skills = [
            {
                'name': 'Швидкий удар',
                'min_dmg': 10,
                'max_dmg': 15,
                'chance': 0.9
            },
            {
                'name': 'Потужний удар',
                'min_dmg': 25,
                'max_dmg': 40,
                'chance': 0.4
            },
            {
                'name': 'Удар в серце',
                'min_dmg': 60,
                'max_dmg': 80,
                'chance': 0.15
            }
        ]

    def heal(self):
        if self.potions > 0:
            amount = 40 + (self.level * 5)
            print(f'Ти вилікувався на {amount} HP!❤️')

            self.hp += amount
            self.potions -= 1

            if self.hp > self.max_hp:
                self.hp = self.max_hp

            print(f'В тебе зараз: {self.hp}❤️')
        else:
            print('В тебе більше немає хілок🧪')

    def gain_exp(self, amount):
        self.exp += amount
        print(f'Ти отримав: {amount} exp💥')

        if self.exp >= 100:
            self.new_level()

    def new_level(self):
        self.level += 1
        self.exp = 0
        self.max_hp += 20
        self.hp = self.max_hp
        print('НОВИЙ РІВЕНЬ!🍾')
        print(f'Твій рівень тепер: {self.level}')
        print(f"Твоє здоров'я: {self.max_hp}")


class Monster(Creature):
    def __init__(self, player_level):
        monster_data = [
            {
                'name': 'Гоблін',
                'hp': 20,
                'damage': 5
            },
            {
                'name': 'Орк-боксер',
                'hp': 10,
                'damage': 12
            },
            {
                'name': 'Орк з сокирою',
                'hp': 10,
                'damage': 20
            },
            {
                'name': 'Мертвий Король',
                'hp': 10,
                'damage': 40
            }
        ]

        monster = random.choice(monster_data)
        multiplier = 1 + (player_level - 1) * 0.2

        super().__init__(monster['name'], int(monster['hp'] * multiplier))

        self.power = int(monster['damage'] * multiplier)


class Event:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def trigger(self, player):
        print('----------------------')
        print(f'⚔️Подія: {self.name}. {self.description}⚔️')


class TrainerEvent(Event):
    def __init__(self):
        super().__init__('Тренер з фехтування!⚔️',
                         'Ви зустрілі тренера, що може навчити вас новому!💪')

        self.skills = [
            {
                'name': 'Гарантований удар',
                'min_dmg': 10,
                'max_dmg': 15,
                'chance': 1.0
            },
            {
                'name': 'Удар з ного',
                'min_dmg': 20,
                'max_dmg': 30,
                'chance': 0.6
            },
            {
                'name': 'Удар смерті',
                'min_dmg': 80,
                'max_dmg': 120,
                'chance': 0.05
            }
        ]

    def trigger(self, player):
        super().trigger(player)

        print('Навички на вибір: ')
        for index, skill in enumerate(self.skills):
            print(f'{index + 1}. {skill['name']} ({skill['min_dmg']}|{skill['max_dmg']}). Шанс: {skill['chance']}')

        player_choice = int(input('Ваш вибір: '))
        new_skill = self.skills[player_choice - 1]
        player.skills.append(new_skill)
        print('Навичок отримано!💪')


class UpgradeEvent(Event):
    def __init__(self):
        super().__init__('Точільний камінь💎️',
                         'Ви знайшли камінь, що допоможе покращити один з скілів!')

    def trigger(self, player):
        super().trigger(player)

        print('Навички на вибір: ')
        for index, skill in enumerate(player.skills):
            print(f'{index + 1}. {skill['name']} ({skill['min_dmg']}|{skill['max_dmg']}). Шанс: {skill['chance']}')

        player_choice = int(input('Ваш вибір: '))
        upgrade_skill = player.skills[player_choice - 1]
        upgrade_skill['chance'] += 0.05
        print(f'Тепер навик {upgrade_skill['name']} має шанс: {upgrade_skill['chance']}')


class ShopEvent(Event):
    def __init__(self):
        super().__init__('Магазин💎️',
                         'Ви знайшли магазин, де можно купити зілля!')

    def trigger(self, player):
        super().trigger(player)

        print('1 зілля: 3 g | 3 зілля: 9 g | 5 зілля: 15 g ')
        player_choice = int(input('Ваш вибір: '))
        if player_choice ==  1:
            if player.money >= 3:
                player.potions += 1
                player.money -= 3

        elif player_choice == 2:
            if player.money >= 9:
                player.potions += 3
                player.money -= 9

        elif player_choice == 3:
            if player.money >= 3:
                player.potions += 5
                player.money -= 15


# =======Гра
print('⚔️Вітаємо у грі "OOP-Battles"⚔️')

player_name = input("🤴Введіть ім'я свого героя:👑 ")
player = Player(player_name)
events = [TrainerEvent(), UpgradeEvent(), ShopEvent()]
print(f'{player.name} починає пригоди!🏇')

while player.is_alive():
    enemy = Monster(player.level)
    print(f'На шляху стоїть: {enemy.name}👹')
    print(f"Його здоров'я: {enemy.hp}❤️")
    print(f'Його сила: {enemy.power}💪')

    while enemy.is_alive() and player.is_alive():
        print('===============================')
        print(f"{player_name} {player.hp}❤️ | {enemy.name} - {enemy.hp}❤️")
        print('Що будеш робити?')

        for index, skill in enumerate(player.skills):
            print(f'{index + 1}. {skill['name']} ({skill['min_dmg']}|{skill['max_dmg']}). Шанс: {skill['chance']}')

        health_index = index + 2
        relax_index = index + 3

        print(f'{health_index}. Полікуватись❤️')
        print(f'{relax_index}. Пропустити🦥')

        try:
            player_choice = int(input('Ваш вибір⚔️: '))
        except ValueError:
            print('Ви ввели не число!')
            continue

        if 1 <= player_choice <= len(player.skills):
            selected_skill = player.skills[player_choice - 1]

            if random.random() <= selected_skill['chance']:
                print('Попав!💪')
                damage = random.randint(selected_skill['min_dmg'], selected_skill['max_dmg'])
                print(f'Ворог отримав {damage} урону!')
                enemy.hp -= damage
            else:
                print('Ворог ухильнувся!💨')
        elif player_choice == health_index:
            player.heal()
        elif player_choice == relax_index:
            print('Ви вірішили відпочити посеред бою')
            player.hp += 10

        if enemy.is_alive():
            damage = random.randint(int(enemy.power * 0.8), int(enemy.power * 1.2))
            print(f'Ворог атакує👹! Ворог наніс {damage} урону!🩸')
            player.hp -= damage

    if player.is_alive():
        print('Монстра переможено!💀⚔️')
        gain_xp = random.randint(40, 70)
        gain_g = random.randint(1, 3)
        player.gain_exp(gain_xp)
        player.potions += 1
        player.money += gain_g
        print(f'Ти отримав {gain_xp} досвіду💥, {gain_g} g! Та одне зілля!')

        if random.random() <= 0.5:
            ev = random.choice(events)
            ev.trigger(player)


print('⚔️Гру завершено!⚔️')
print(f'💀{player.name} протримався до {player.level} рівню!💀')
