import pygame
from enemy import Enemy
from tower import BasicTower, SniperTower, MoneyTower
from settings import Settings
import random


class Level:
    def __init__(self, game):

        self.settings = Settings()

        self.game = game
        self.enemies = pygame.sprite.Group()
        self.towers = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        '''Задача №4. Сделать несколько путей для врагов'''
        self.random_path = [self.game.settings.enemy_path, self.game.settings.enemy_path_secret]
        '''Задача №7. Создать более разнообразных врагов.'''
        '''Задача №8. Добавить больше волн врагов'''
        self.waves = [
            [{'path': random.choice(self.random_path), 'speed': 1, 'health': 100,
              'image_path': 'assets/enemies/basic_enemy.png'}] * 5,
            [{'path': random.choice(self.random_path), 'speed': 1.5, 'health': 150,
              'image_path': 'assets/enemies/fast_enemy.png'}] * 7,
            [{'path': random.choice(self.random_path), 'speed': 0.75, 'health': 200,
              'image_path': 'assets/enemies/strong_enemy.png'}] * 4,
            [{'path': random.choice(self.random_path), 'speed': 2, 'health': 1000,
              'image_path': 'assets/enemies/hardcore_enemy.png'}] * 10,
        ]
        self.current_wave = 0
        self.spawned_enemies = 0
        self.spawn_delay = 1000
        self.last_spawn_time = pygame.time.get_ticks()
        self.all_waves_complete = False
        self.start_next_wave()
        self.font = pygame.font.SysFont("Arial", 24)

    def start_next_wave(self):
        if self.current_wave < len(self.waves):
            self.spawned_enemies = 0
            self.spawn_next_enemy()

    def spawn_next_enemy(self):
        if self.spawned_enemies < len(self.waves[self.current_wave]):
            enemy_info = self.waves[self.current_wave][self.spawned_enemies]
            new_enemy = Enemy(**enemy_info, game=self.game)
            self.enemies.add(new_enemy)
            self.spawned_enemies += 1
            '''Задача №2. Добавить звуки к выстрелам и появлению врагов'''
            self.enemy_spawns_sound = pygame.mixer.Sound(self.settings.enemy_spawns_sound)
            self.enemy_spawns_sound.play()

    def attempt_place_tower(self, mouse_pos, tower_type, placing_tower=False):
        '''Задача №1. Убрать постоянное отображение позиций'''
        if placing_tower == True:
            tower_classes = {'basic': BasicTower, 'sniper': SniperTower, 'money': MoneyTower}
            if tower_type in tower_classes and self.game.settings.starting_money >= self.game.settings.tower_cost:
                grid_pos = self.game.grid.get_grid_position(mouse_pos)
                if self.game.grid.is_spot_available(grid_pos):
                    self.game.settings.starting_money -= self.game.settings.tower_cost
                    new_tower = tower_classes[tower_type](grid_pos, self.game)
                    self.towers.add(new_tower)
                    print("Tower placed.")
                else:
                    print("Invalid position for tower.")
            else:
                print("Not enough money or unknown tower type.")

    def update(self):
        current_time = pygame.time.get_ticks()

        if self.current_wave < len(self.waves) and self.spawned_enemies < len(self.waves[self.current_wave]):
            if current_time - self.last_spawn_time > self.spawn_delay:
                '''Задача №4. Сделать несколько путей для врагов'''
                self.waves[self.current_wave][self.spawned_enemies].update({"path": random.choice(self.random_path)})
                enemy_info = self.waves[self.current_wave][self.spawned_enemies].copy()
                enemy_info['game'] = self.game
                new_enemy = Enemy(**enemy_info)
                self.enemies.add(new_enemy)
                self.spawned_enemies += 1
                self.last_spawn_time = current_time
                '''Задача №2. Добавить звуки к выстрелам и появлению врагов'''
                self.enemy_spawns_sound = pygame.mixer.Sound(self.settings.enemy_spawns_sound)
                self.enemy_spawns_sound.play()

        collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, False)
        for bullet in collisions:
            for enemy in collisions[bullet]:
                enemy.take_damage(bullet.damage)

        self.enemies.update()
        for tower in self.towers:
            tower.update(self.enemies, current_time, self.bullets)
        self.bullets.update()

        if len(self.enemies) == 0 and self.current_wave < len(self.waves) - 1:
            self.current_wave += 1
            self.start_next_wave()
        elif len(self.enemies) == 0 and self.current_wave == len(self.waves) - 1:
            self.all_waves_complete = True
        '''Задача №8. Добавить больше волн врагов'''
        try:
            if len(self.enemies) != 0 and self.current_wave == len(self.waves) - 1:
                speed = [0.75, 1, 1.5, 2]
                spd = random.choice(speed)
                health = [100, 150, 200, 1000]
                hp = random.choice(health)
                if spd == 2 or hp == 1000:
                    self.waves[self.current_wave][self.spawned_enemies].update({'image_path': 'assets/enemies/hardcore_enemy.png'})
                    self.waves[self.current_wave][self.spawned_enemies].update({"speed": spd})
                    self.waves[self.current_wave][self.spawned_enemies].update({"health": hp})
                else:
                    self.waves[self.current_wave][self.spawned_enemies].update(
                        {'image_path': 'assets/enemies/strong_enemy.png'})
                    self.waves[self.current_wave][self.spawned_enemies].update({"speed": spd})
                    self.waves[self.current_wave][self.spawned_enemies].update({"health": hp})
        except:
            pass

    def draw_path(self, screen, draw_position=False):
        pygame.draw.lines(screen, (0, 128, 0), False, self.game.settings.enemy_path, 5)
        pygame.draw.lines(screen, (0, 128, 0), False, self.game.settings.enemy_path_secret, 5)
        '''Задача №1. Убрать постоянное отображение позиций'''
        if draw_position == True:
            for pos in self.game.settings.tower_positions:
                pygame.draw.circle(screen, (128, 0, 0), pos, 10)

    def draw(self, screen):
        self.draw_path(screen)
        self.enemies.draw(screen)
        self.towers.draw(screen)
        self.bullets.draw(screen)
        mouse_pos = pygame.mouse.get_pos()
        for tower in self.towers:
            tower.draw(screen)
            if tower.is_hovered(mouse_pos):
                tower_stats_text = self.font.render(f"Damage: {tower.damage}, Range: {tower.tower_range}", True,
                                                    (255, 255, 255))
                screen.blit(tower_stats_text, (tower.rect.x, tower.rect.y - 20))
