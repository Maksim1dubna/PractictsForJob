class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        self.rows = 10
        self.cols = 15
        self.grid_size = (64, 64)

        self.tower_cost = 100
        self.tower_upgrade_cost = 150
        self.tower_sell_percentage = 0.75

        self.enemy_path = [
            (0, 200), (150, 200), (150, 100), (300, 100),
            (300, 300), (450, 300), (900, 300), (1150, 300)
        ]
        '''Задача №4. Сделать несколько путей для врагов'''
        self.enemy_path_secret = [
            (0, 400), (150, 400), (150, 500), (500, 500),
            (500, 600), (800, 600), (800, 500), (1150, 500)
        ]

        self.tower_sprites = {
            'basic': 'assets/towers/basic_tower.png',
            'sniper': 'assets/towers/sniper_tower.png',
            'money': 'assets/towers/money_tower.png'
        }
        self.enemy_sprite = 'assets/enemies/basic_enemy.png'
        self.bullet_sprite = 'assets/bullets/basic_bullet.png'
        self.background_image = 'assets/backgrounds/game_background.png'
        '''Задача №2. Добавить звуки к выстрелам и появлению врагов'''
        self.shoot_sound = 'assets/sounds/shoot.wav'
        self.upgrade_sound = 'assets/sounds/upgrade.wav'
        self.sell_sound = 'assets/sounds/sell.wav'
        self.enemy_hit_sound = 'assets/sounds/enemy_hit.wav'
        self.enemy_spawns_sound = 'assets/sounds/enemy_spawns.wav'
        self.background_music = 'assets/sounds/background_music.mp3'

        self.starting_money = 500
        self.lives = 20

        self.tower_positions = [(x * self.grid_size[0] + self.grid_size[0] // 2, y * self.grid_size[1] + self.grid_size[1] // 2)
                                for x in range(1, self.cols) for y in range(3, self.rows)]
