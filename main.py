import pygame
import random
import sys
import os

def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso, útil para PyInstaller."""
    try:
        base_path = sys._MEIPASS  # directorio temporal creado por PyInstaller
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
# Inicializar Pygame
pygame.init()
pygame.mixer.init()  # Inicializar el mezclador

# Dimensiones de la ventana
ANCHO = 1024
ALTO = 720
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Terminal Seguro 16-bit")
clock = pygame.time.Clock()

# Guardar el instante de inicio del juego y crear la lista de puntajes
game_start_time = pygame.time.get_ticks()
scoreboard = []  # Aquí se almacenarán los tiempos (en milisegundos)

# Inicializar font para el contador
font = pygame.font.Font(resource_path("fonts/PressStart2P-Regular.ttf"), 24)

# Cargar sonidos
bg_music = pygame.mixer.Sound(resource_path("sounds/background.mp3"))  # Música de fondo
game_over_music = pygame.mixer.Sound(resource_path("sounds/game_over.mp3"))  # Música de game over
victory_music = pygame.mixer.Sound(resource_path("sounds/victory.mp3"))  # Música de victoria
pickup_sfx = pygame.mixer.Sound(resource_path("sounds/pickup.mp3"))  # Efecto al recoger tarja
hit_sfx = pygame.mixer.Sound(resource_path("sounds/hit.mp3"))  # Efecto al ser atropellado

bg_music.play(loops=-1)

# Definición del layout del terminal
mapa_layout = [
    [1, 1, 0, 1, 1, 0, 1, 1],  # Fila 0
    [1, 1, 0, 1, 0, 0, 1, 1],  # Fila 1
    [1, 1, 0, 0, 1, 0, 1, 1],  # Fila 2
    [0, 0, 0, 0, 0, 0, 0, 0],  # Fila 3 (Calle horizontal)
    [1, 1, 0, 1, 1, 0, 1, 1],  # Fila 4
    [1, 1, 0, 1, 1, 0, 1, 1],  # Fila 5
    [1, 1, 0, 1, 1, 0, 1, 1],  # Fila 6
    [0, 0, 0, 0, 0, 0, 0, 0],  # Fila 7 (Calle horizontal)
    [1, 1, 1, 0, 0, 1, 1, 1],  # Fila 8
    [1, 1, 1, 0, 0, 1, 1, 1],  # Fila 9
    [1, 1, 1, 0, 0, 1, 1, 1]  # Fila 10
]

# Cargar los sprites del trabajador para cada dirección
try:
    trabajador_arriba_parado = pygame.image.load(resource_path("sprites/trabajador_arriba_parado.png")).convert_alpha()
    trabajador_arriba_camina = [
        pygame.image.load(resource_path("sprites/trabajador_arriba_camina_1.png")).convert_alpha(),
        pygame.image.load(resource_path("sprites/trabajador_arriba_camina_2.png")).convert_alpha()
    ]
    trabajador_abajo_parado = pygame.image.load(resource_path("sprites/trabajador_abajo_parado.png")).convert_alpha()
    trabajador_abajo_camina = [
        pygame.image.load(resource_path("sprites/trabajador_abajo_camina_1.png")).convert_alpha(),
        pygame.image.load(resource_path("sprites/trabajador_abajo_camina_2.png")).convert_alpha()
    ]
    trabajador_izquierda_parado = pygame.image.load(resource_path("sprites/trabajador_izquierda_parado.png")).convert_alpha()
    trabajador_izquierda_camina = [
        pygame.image.load(resource_path("sprites/trabajador_izquierda_camina_1.png")).convert_alpha(),
        pygame.image.load(resource_path("sprites/trabajador_izquierda_camina_2.png")).convert_alpha()
    ]
    trabajador_derecha_parado = pygame.image.load(resource_path("sprites/trabajador_derecha_parado.png")).convert_alpha()
    trabajador_derecha_camina = [
        pygame.image.load(resource_path("sprites/trabajador_derecha_camina_1.png")).convert_alpha(),
        pygame.image.load(resource_path("sprites/trabajador_derecha_camina_2.png")).convert_alpha()
    ]
    tarja_sprites = [
        pygame.image.load(resource_path("sprites/tarja_1.png")).convert_alpha(),
        pygame.image.load(resource_path("sprites/tarja_2.png")).convert_alpha()
    ]
    success_image = pygame.image.load(resource_path("sprites/success.png")).convert_alpha()
    numero_sprites = [
        pygame.image.load(resource_path("sprites/number_0.png")).convert_alpha(),
        pygame.image.load(resource_path("sprites/number_1.png")).convert_alpha(),
        pygame.image.load(resource_path("sprites/number_2.png")).convert_alpha(),
        pygame.image.load(resource_path("sprites/number_3.png")).convert_alpha(),
        pygame.image.load(resource_path("sprites/number_4.png")).convert_alpha(),
        pygame.image.load(resource_path("sprites/number_5.png")).convert_alpha(),
        pygame.image.load(resource_path("sprites/number_6.png")).convert_alpha(),
        pygame.image.load(resource_path("sprites/number_7.png")).convert_alpha(),
        pygame.image.load(resource_path("sprites/number_8.png")).convert_alpha(),
        pygame.image.load(resource_path("sprites/number_9.png")).convert_alpha()
    ]
    winscreen_image = pygame.image.load(resource_path("sprites/winscreen.png")).convert_alpha()
    grua_derecha_image = pygame.image.load(resource_path("sprites/grua_derecha.png")).convert_alpha()
    grua_izquierda_image = pygame.image.load(resource_path("sprites/grua_izquierda.png")).convert_alpha()
    game_over_image = pygame.image.load(resource_path("sprites/game_over.png")).convert_alpha()
    play_again_image = pygame.image.load(resource_path("sprites/play_again.png")).convert_alpha()
    dead_image = pygame.image.load(resource_path("sprites/dead.png")).convert_alpha()
except pygame.error as e:
    print(f"Error al cargar sprites de dirección: {e}")
    pygame.quit()
    exit()

# Cargar los sprites de los contenedores individuales
try:
    contenedor_sprites = [
        pygame.image.load(resource_path("sprites/contenedor_1.png")).convert(),
        pygame.image.load(resource_path("sprites/contenedor_2.png")).convert(),
        pygame.image.load(resource_path("sprites/contenedor_3.png")).convert(),
        pygame.image.load(resource_path("sprites/contenedor_4.png")).convert()
    ]
except pygame.error as e:
    print(f"Error al cargar sprites de contenedores: {e}")
    pygame.quit()
    exit()

# Cargar el sprite de asfalto
try:
    asfalto_tile = pygame.image.load(resource_path("sprites/asfalto.png")).convert()
except pygame.error as e:
    print(f"Error al cargar el sprite de asfalto: {e}")
    pygame.quit()
    exit()

# Dimensiones en píxeles
trabajador_ancho_px = 32
trabajador_alto_px = 32
ancho_calle_px = 32
contenedor_ancho_px = 53
contenedor_largo_px = 107
distancia_contenedor_px = 3
ancho_bloque_px = 2 * contenedor_ancho_px + distancia_contenedor_px
largo_bloque_px = 3 * contenedor_largo_px + 2 * distancia_contenedor_px
juego_terminado = False

#variables winscreen
mostrar_winscreen = False
winscreen_timer = 0
tiempo_mostrar_winscreen = 5000  # 5000 milisegundos = 5 segundos

# Variable global para el estado de game over
game_over = False

# Calcular las dimensiones del mapa completo
num_filas_mapa = len(mapa_layout)
num_columnas_mapa = len(mapa_layout[0]) if num_filas_mapa > 0 else 0
ancho_total_mapa = num_columnas_mapa * (ancho_bloque_px + ancho_calle_px) - ancho_calle_px if num_columnas_mapa > 0 else 0
alto_total_mapa = num_filas_mapa * (largo_bloque_px + ancho_calle_px) - ancho_calle_px if num_filas_mapa > 0 else 0

# contador tarjas
contador = 0

mapa_completo = pygame.Surface((ancho_total_mapa, alto_total_mapa))

# Tilear el fondo de asfalto
tile_ancho = asfalto_tile.get_width()
tile_alto = asfalto_tile.get_height()
for y in range(0, alto_total_mapa, tile_alto):
    for x in range(0, ancho_total_mapa, tile_ancho):
        mapa_completo.blit(asfalto_tile, (x, y))

# Inicializar la información de los bloques y dibujar en el mapa completo
bloques_contenedores_info = {}
contenedor_rects = []
for fila_bloque, linea in enumerate(mapa_layout):
    for columna_bloque, elemento in enumerate(linea):
        if elemento == 1:
            x_bloque_inicio_mapa = columna_bloque * (ancho_bloque_px + ancho_calle_px)
            y_bloque_inicio_mapa = fila_bloque * (largo_bloque_px + ancho_calle_px)
            bloque_sprites = []
            for i in range(2):
                columna_sprites = []
                for j in range(3):
                    sprite_aleatorio = random.choice(contenedor_sprites)
                    columna_sprites.append(sprite_aleatorio)
                    x_contenedor_mapa = x_bloque_inicio_mapa + i * (contenedor_ancho_px + distancia_contenedor_px)
                    y_contenedor_mapa = y_bloque_inicio_mapa + j * (contenedor_largo_px + distancia_contenedor_px)
                    contenedor_rect = pygame.Rect(x_contenedor_mapa, y_contenedor_mapa, contenedor_ancho_px, contenedor_largo_px)
                    contenedor_rects.append(contenedor_rect)
                    mapa_completo.blit(sprite_aleatorio, (x_contenedor_mapa, y_contenedor_mapa))
                bloque_sprites.append(columna_sprites)
            bloques_contenedores_info[(fila_bloque, columna_bloque)] = (x_bloque_inicio_mapa, y_bloque_inicio_mapa, bloque_sprites)

# Variables para la recolección de tarjas y el efecto "Success"
tarjas_recolectadas = 0
num_tarjas_objetivo = 10
mostrar_success = False
success_timer = 0
tarjas_group = None # Inicializamos tarjas_group aquí

# Clase para el Trabajador
class Trabajador(pygame.sprite.Sprite):
    def __init__(self, parado_sprites, caminando_sprites, start_x, start_y):
        super().__init__()
        self.parado = parado_sprites
        self.camina = caminando_sprites
        self.direccion = "abajo"
        self.image = self.parado[self.direccion]
        self.rect = self.image.get_rect(center=(start_x, start_y))
        self.animacion_velocidad = 10
        self.animacion_contador = 0
        self.fotograma_actual = 0
        self.velocidad = 3
        self.alive = True  # Nuevo atributo para indicar si el jugador está vivo

    def update(self):
        if not self.alive:
            # Si el jugador está muerto, no se actualiza la animación
            return

        if movimiento_x == 0 and movimiento_y == 0:
            self.image = self.parado[self.direccion]
        else:
            self.animacion_contador += 1
            if self.animacion_contador >= self.animacion_velocidad:
                self.animacion_contador = 0
                self.fotograma_actual = (self.fotograma_actual + 1) % len(self.camina[self.direccion])
            self.image = self.camina[self.direccion][self.fotograma_actual]

    def mover(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

# Crear el Trabajador
start_x = ancho_total_mapa // 2
start_y = alto_total_mapa // 2
trabajador_parado_sprites = {"arriba": trabajador_arriba_parado, "abajo": trabajador_abajo_parado, "izquierda": trabajador_izquierda_parado, "derecha": trabajador_derecha_parado}
trabajador_caminando_sprites = {"arriba": trabajador_arriba_camina, "abajo": trabajador_abajo_camina, "izquierda": trabajador_izquierda_camina, "derecha": trabajador_derecha_camina}
trabajador = Trabajador(trabajador_parado_sprites, trabajador_caminando_sprites, start_x, start_y)
trabajador_group = pygame.sprite.GroupSingle(trabajador)

class Tarja(pygame.sprite.Sprite):
    def __init__(self, x, y, sprites, animation_speed):
        super().__init__()
        self.sprites = sprites
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.animation_speed = animation_speed
        self.animation_timer = 0

    def update(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites)
            self.image = self.sprites[self.current_sprite]

class Grua(pygame.sprite.Sprite):
    def __init__(self, y, velocidad):
        super().__init__()
        self.image_derecha = grua_derecha_image
        self.image_izquierda = grua_izquierda_image
        self.image = self.image_derecha
        self.rect = self.image.get_rect(topleft=(0, y))
        self.velocidad = velocidad
        self.direccion = 1  # 1 para derecha, -1 para izquierda

    def update(self):
        self.rect.x += self.velocidad * self.direccion
        if self.direccion == 1:
            self.image = self.image_derecha
        elif self.direccion == -1:
            self.image = self.image_izquierda

        if self.rect.right > ancho_total_mapa:
            self.direccion = -1
        elif self.rect.left < 0:
            self.direccion = 1

# Generar las Tarjas
num_tarjas = 10
tarjas_group = pygame.sprite.Group() # Se inicializa aquí
tarja_animation_speed = 15  # Ajusta la velocidad de la animación de las tarjas

# Calcular las posiciones válidas para las tarjas (calles)
posiciones_validas_tarjas = []
num_filas_layout = len(mapa_layout)
if num_filas_layout > 0:
    num_columnas_layout = len(mapa_layout[0])
    for fila in range(num_filas_layout):
        for columna in range(num_columnas_layout):
            if mapa_layout[fila][columna] == 0:
                # Calcular la posición central de esta "calle"
                x_calle = columna * (ancho_bloque_px + ancho_calle_px) + ancho_calle_px // 2
                y_calle = fila * (largo_bloque_px + ancho_calle_px) + largo_bloque_px // 2
                # Ajustar para que la tarja no se superponga exactamente con el centro
                # Podemos añadir un pequeño desplazamiento aleatorio
                offset_x = random.randint(-ancho_bloque_px // 4, ancho_bloque_px // 4)
                offset_y = random.randint(-largo_bloque_px // 4, largo_bloque_px // 4)
                posiciones_validas_tarjas.append((x_calle + offset_x - tarja_sprites[0].get_width() // 2,
                                                 y_calle + offset_y - tarja_sprites[0].get_height() // 2))

# Seleccionar aleatoriamente 10 posiciones únicas para las tarjas
if len(posiciones_validas_tarjas) >= num_tarjas:
    posiciones_tarjas = random.sample(posiciones_validas_tarjas, num_tarjas)
    for x, y in posiciones_tarjas:
        tarja = Tarja(x, y, tarja_sprites, tarja_animation_speed)
        tarjas_group.add(tarja)
else:
    print("Advertencia: No hay suficientes espacios válidos para colocar todas las tarjas.")

gruas_group = pygame.sprite.Group()
velocidad_grua = 4
for fila_idx, fila in enumerate(mapa_layout):
    es_pasillo_horizontal = all(elemento == 0 for elemento in fila)
    if es_pasillo_horizontal:
        y_pasillo = fila_idx * (largo_bloque_px + ancho_calle_px) + ancho_calle_px // 2 - 50  # posición base
        offset_inferior = 280  # ajuste para mover la grúa de abajo
        # Grúa 1: se genera cerca de los contenedores de arriba
        grua1 = Grua(y_pasillo, velocidad_grua)
        grua1.rect.x = random.randint(0, ancho_total_mapa // 2)
        # Grúa 2: se genera un poco más abajo
        grua2 = Grua(y_pasillo + offset_inferior, velocidad_grua)
        grua2.rect.x = random.randint(ancho_total_mapa // 2, ancho_total_mapa)
        gruas_group.add(grua1, grua2)

# contador de sprites
def dibujar_contador_sprites(superficie, valor, posicion_x, posicion_y, espaciado=5):
    valor_str = str(valor)
    x_offset = 0
    for digito in valor_str:
        indice_digito = int(digito)
        if 0 <= indice_digito < len(numero_sprites):
            sprite_digito = numero_sprites[indice_digito]
            superficie.blit(sprite_digito, (posicion_x + x_offset, posicion_y))
            x_offset += sprite_digito.get_width() + espaciado
        else:
            print(f"Advertencia: No hay sprite para el dígito {digito}")

# Inicializar la cámara
camera = pygame.Rect(0, 0, ANCHO, ALTO)

def actualizar_camara(camera, jugador_rect, ancho_mapa, alto_mapa):
    x = -jugador_rect.centerx + ANCHO // 2
    y = -jugador_rect.centery + ALTO // 2

    # Limitar la cámara horizontalmente
    if ancho_mapa <= ANCHO:
        x = 0
    else:
        x = min(0, x)
        x = max(-(ancho_mapa - ANCHO), x)

    # Limitar la cámara verticalmente
    if alto_mapa <= ALTO:
        y = 0
    else:
        y = min(0, y)
        y = max(-(alto_mapa - ALTO), y)

    return pygame.Rect(x, y, ANCHO, ALTO)

# Bucle principal del juego
ejecutando = True
while ejecutando:
    fps = 60
    clock.tick(fps)

    # Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        # Dentro del manejo de eventos para reiniciar el juego (tanto en game over como en winscreen)
        if (game_over or mostrar_winscreen) and evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            boton_rect = play_again_image.get_rect(center=(ANCHO // 2, ALTO // 2 + 200))
            if boton_rect.collidepoint(mouse_pos):
                # Reiniciar variables del juego...
                tarjas_recolectadas = 0
                trabajador.rect.center = (start_x, start_y)
                trabajador.alive = True
                trabajador.image = trabajador_parado_sprites["abajo"]
                game_over = False
                juego_terminado = False
                mostrar_winscreen = False
                # Reinicializar las tarjas
                tarjas_group.empty()
                if len(posiciones_validas_tarjas) >= num_tarjas:
                    posiciones_tarjas = random.sample(posiciones_validas_tarjas, num_tarjas)
                    for x, y in posiciones_tarjas:
                        tarja = Tarja(x, y, tarja_sprites, tarja_animation_speed)
                        tarjas_group.add(tarja)
                else:
                    print("Advertencia: No hay suficientes espacios válidos para colocar todas las tarjas.")
                # Resetear el tiempo de inicio para el nuevo intento
                game_start_time = pygame.time.get_ticks()
                # Detener las pistas de game over o de victoria y reiniciar la música de fondo
                game_over_music.stop()
                victory_music.stop()
                bg_music.play(loops=-1)

    # Si estamos en estado de game over, esperar 2 segundos y entonces mostrar el overlay
    if game_over:
        elapsed = pygame.time.get_ticks() - game_over_time
        if elapsed >= 2000:
            # Dibujar "game over"
            game_over_rect = game_over_image.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
            pantalla.blit(game_over_image, game_over_rect)

            # Dibujar el contador de tarjas recolectadas
            tarjas_text = f"Tarjas realizadas: {tarjas_recolectadas}"
            tarjas_surface = font.render(tarjas_text, True, (255, 255, 255))
            # Ajusta la posición según desees (en este caso, se coloca entre game_over y el botón)
            tarjas_rect = tarjas_surface.get_rect(center=(ANCHO // 2, ALTO // 2 + 100))
            pantalla.blit(tarjas_surface, tarjas_rect)

            # Dibujar el botón "play again"
            boton_rect = play_again_image.get_rect(center=(ANCHO // 2, ALTO // 2 + 200))
            pantalla.blit(play_again_image, boton_rect)

            pygame.display.flip()
        continue  # Se pausa el bucle hasta que se haga clic en el botón

    # Control del movimiento (solo si el trabajador está vivo)
    if trabajador.alive:
        keys = pygame.key.get_pressed()
        movimiento_x = 0
        movimiento_y = 0
        if keys[pygame.K_w]:
            movimiento_y = -trabajador.velocidad
            trabajador.direccion = "arriba"
        elif keys[pygame.K_s]:
            movimiento_y = trabajador.velocidad
            trabajador.direccion = "abajo"
        elif keys[pygame.K_a]:
            movimiento_x = -trabajador.velocidad
            trabajador.direccion = "izquierda"
        elif keys[pygame.K_d]:
            movimiento_x = trabajador.velocidad
            trabajador.direccion = "derecha"
    else:
        movimiento_x = 0
        movimiento_y = 0

    # Crear un nuevo rectpara la futura posición del trabajador
    trabajador_rect_futuro = trabajador.rect.move(movimiento_x, movimiento_y)

    # Verificar colisiones con contenedores
    colision_contenedor = False
    for contenedor_rect in contenedor_rects:
        if trabajador_rect_futuro.colliderect(contenedor_rect):
            colision_contenedor = True
            break

    # Si NO hay colisión, aplicar el movimiento
    if not colision_contenedor:
        trabajador.rect = trabajador_rect_futuro

    # DELIMITACIÓN DE BORDES (contra los bordes del mapa)
    if trabajador.rect.left < 0:
        trabajador.rect.left = 0
    if trabajador.rect.right > ancho_total_mapa:
        trabajador.rect.right = ancho_total_mapa
    if trabajador.rect.top < 0:
        trabajador.rect.top = 0
    if trabajador.rect.bottom > alto_total_mapa:
        trabajador.rect.bottom = alto_total_mapa

    # Detectar colisiones con las tarjas
    tarjas_colisionadas = pygame.sprite.spritecollide(trabajador, tarjas_group, True)
    if tarjas_colisionadas:
        tarjas_recolectadas += len(tarjas_colisionadas)
        pickup_sfx.play()  # Reproducir el sonido de recolección
        print(f"Tarjas recolectadas: {tarjas_recolectadas}")
        mostrar_success = True # Muestra el mensaje de éxito
        success_timer = pygame.time.get_ticks() # Reinicia el timer

        if tarjas_recolectadas >= num_tarjas_objetivo and not juego_terminado:
            # Calcular el tiempo transcurrido (score)
            finish_time = pygame.time.get_ticks() - game_start_time
            scoreboard.append(finish_time)
            scoreboard.sort()  # Ordena los scores de menor a mayor

            # Convertir finish_time de ms a minutos y segundos
            score_sec = finish_time // 1000
            minutes = score_sec // 60
            seconds = score_sec % 60
            final_time_str = f"Tiempo: {minutes} m {seconds:02d} s"
            # Crear la superficie con la fuente seleccionada
            final_time_surface = font.render(final_time_str, True, (255, 255, 255))

            print("¡Has recolectado todas las tarjas! Mostrando pantalla de victoria.")
            bg_music.stop()  # Detén la música de fondo
            victory_music.play()  # Reproduce la música de victoria

            # Se activa la winscreen y se almacena la superficie del tiempo final para mostrarla
            mostrar_winscreen = True
            winscreen_timer = pygame.time.get_ticks()
            juego_terminado = True
            mostrar_success = False
    # Detección de colisión con grúas que activa game over
    if pygame.sprite.spritecollide(trabajador, gruas_group, False) and not game_over:
        print("¡Game Over! Colisión con una grúa.")
        trabajador.image = dead_image  # Reemplaza el sprite por dead.png
        trabajador.alive = False  # Desactivar las actualizaciones de animación
        hit_sfx.play()  # Reproduce el efecto de atropello
        bg_music.stop()  # Detén la música de fondo
        game_over_music.play()  # Inicia la música de game over
        game_over = True
        game_over_time = pygame.time.get_ticks()  # Registrar el instante de colisión

    # Actualizar las tarjas (animación)
    tarjas_group.update()

    # Actualizar el sprite del trabajador (animación)
    trabajador_group.update()

    gruas_group.update()

    # Actualizar la cámara
    camera = actualizar_camara(camera, trabajador.rect, ancho_total_mapa, alto_total_mapa)

    # Dibujar
    pantalla.fill((50, 50, 50))
    pantalla.blit(mapa_completo, camera)

    # Dibujar las tarjas
    for tarja in tarjas_group:
        pantalla.blit(tarja.image, (tarja.rect.x + camera.x, tarja.rect.y + camera.y))

    # Dibujar al trabajador
    pantalla.blit(trabajador.image, (trabajador.rect.x + camera.x, trabajador.rect.y + camera.y))

    # Dibujar contador de sprites
    dibujar_contador_sprites(pantalla, tarjas_recolectadas, 10, 10)  # Ejemplo de posición (10, 10)

    # Dibujar grúas con offset de cámara (sin rectángulos y sin prints de depuración)
    for grua in gruas_group:
        pantalla.blit(grua.image, (grua.rect.x + camera.x, grua.rect.y + camera.y))

    # Dibujar el contador de tiempo u otros elementos cuando el juego esté activo...
    if not juego_terminado and not game_over:
        # ... dibujar contador, sprites, etc.
        current_time = pygame.time.get_ticks() - game_start_time
        time_sec = current_time // 1000
        minutes = time_sec // 60
        seconds = time_sec % 60
        time_text = f"tiempo: {minutes} m {seconds:02d} s"
        text_surface = font.render(time_text, True, (255, 255, 255))
        x = ANCHO - text_surface.get_width() - 10
        y = 10
        pantalla.blit(text_surface, (x, y))
    elif mostrar_winscreen:
        winscreen_rect = winscreen_image.get_rect(center=(ANCHO // 2, ALTO // 2))
        pantalla.blit(winscreen_image, winscreen_rect)

        # Dibujar el tiempo final justo debajo de winscreen (por ejemplo, 100px debajo del centro)
        # Asegúrate de que la variable final_time_surface se haya definido en la detección de victoria
        if 'final_time_surface' in globals():
            final_time_rect = final_time_surface.get_rect(midbottom=(ANCHO // 2, winscreen_rect.top - 10))
            pantalla.blit(final_time_surface, final_time_rect)

        # Dibujar el botón "play again"
        boton_rect = play_again_image.get_rect(center=(ANCHO // 2, ALTO // 2 + 200))
        pantalla.blit(play_again_image, boton_rect)
    # Mostrar "Success" (solo si la pantalla de victoria no está activa)
    if mostrar_success:
        tiempo_transcurrido = pygame.time.get_ticks() - success_timer
        alpha = max(0, 255 - (tiempo_transcurrido * 255) // 2000)
        success_image.set_alpha(alpha)
        success_rect = success_image.get_rect(center=(ANCHO // 2, ALTO // 2))
        pantalla.blit(success_image, success_rect)
        if tiempo_transcurrido > 2000:
            mostrar_success = False

    pygame.display.flip()

pygame.quit()
