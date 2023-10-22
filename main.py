import pygame

pygame.font.init()
pygame.mixer.init()

ANCHO = 900
LARGO = 500
TUPLA_TAMANNIO = (ANCHO, LARGO)
VENTANA = pygame.display.set_mode(TUPLA_TAMANNIO)
pygame.display.set_caption('Pelea de Naves')

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 0)
AZUL = (0, 0, 255)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

RECTANGULO_DIVISOR = pygame.Rect(ANCHO // 2 - 5, 0, 10, LARGO)

FPS = 60
VEL_NAVES = 5
VEL_BALA = 7
MAX_BALA = 3
ANCHO_NAVE = 55
ALTO_NAVE = 40

AZUL_HIT = pygame.USEREVENT + 1
ROJO_HIT = pygame.USEREVENT + 2
# Imagenes
ESPACIO = pygame.transform.scale(pygame.image.load('Assets/espacio.jpg'), TUPLA_TAMANNIO)

IMAGEN_NAVE_AZUL = pygame.image.load('Assets/spaceship_yellow.png')
NAVE_AZUL = pygame.transform.rotate(pygame.transform.scale(
    IMAGEN_NAVE_AZUL, (ANCHO_NAVE, ALTO_NAVE)), 90)

IMAGEN_NAVE_ROJA = pygame.image.load('Assets/spaceship_red.png')
NAVE_ROJA = pygame.transform.rotate(pygame.transform.scale(
    IMAGEN_NAVE_ROJA, (ANCHO_NAVE, ALTO_NAVE)), 270)


def dibujar_ventana(nave_roja, nave_azul, balas_roja, balas_azul, salud_roja, salud_azul):
    # Background Espacio
    VENTANA.blit(ESPACIO, (0, 0))
    # Linea mitad divisoria
    pygame.draw.rect(VENTANA, BLANCO, RECTANGULO_DIVISOR)

    # Mostrar salud actual
    salud_roja_texto = HEALTH_FONT.render(
        "Salud: " + str(salud_roja), 1, ROJO
    )
    VENTANA.blit(salud_roja_texto, (ANCHO - salud_roja_texto.get_width() - 20, 10))
    salud_azul_texto = HEALTH_FONT.render(
        "Salud: " + str(salud_azul), 1, AZUL
    )
    VENTANA.blit(salud_azul_texto, (20, 10))

    # Dibujar las navess
    VENTANA.blit(NAVE_AZUL, (nave_azul.x, nave_azul.y))
    VENTANA.blit(NAVE_ROJA, (nave_roja.x, nave_roja.y))

    for bala in balas_azul:
        pygame.draw.rect(VENTANA, AZUL, bala)

    for bala in balas_roja:
        pygame.draw.rect(VENTANA, ROJO, bala)

    pygame.display.update()


def manejar_nave_azul(teclas_presionadas, azul):
    if teclas_presionadas[pygame.K_a] and azul.x - VEL_NAVES > 0:  # LEFT
        azul.x -= VEL_NAVES
    if teclas_presionadas[pygame.K_d] and azul.x + VEL_NAVES + azul.width < RECTANGULO_DIVISOR.x:  # RIGHT
        azul.x += VEL_NAVES
    if teclas_presionadas[pygame.K_w] and azul.y - VEL_NAVES > 0:  # UP
        azul.y -= VEL_NAVES
    if teclas_presionadas[pygame.K_s] and azul.y + VEL_NAVES + azul.height < LARGO - 15:  # DOWN

        azul.y += VEL_NAVES


def manejar_nave_roja(teclas_presionadas, rojo):
    if teclas_presionadas[pygame.K_LEFT] and rojo.x - VEL_NAVES > RECTANGULO_DIVISOR.x + RECTANGULO_DIVISOR.width:  # LEFT
        rojo.x -= VEL_NAVES
    if teclas_presionadas[pygame.K_RIGHT] and rojo.x + VEL_NAVES + rojo.width < ANCHO:  # RIGHT
        rojo.x += VEL_NAVES
    if teclas_presionadas[pygame.K_UP] and rojo.y - VEL_NAVES > 0:  # UP
        rojo.y -= VEL_NAVES
    if teclas_presionadas[pygame.K_DOWN] and rojo.y + VEL_NAVES + rojo.height < LARGO - 15 :  # DOWN
        rojo.y += VEL_NAVES


def movimiento_balas(azul_balas, rojo_balas, azul, roja):
    for bala in azul_balas:
        bala.x += VEL_BALA
        if roja.colliderect(bala):
            pygame.event.post(pygame.event.Event(ROJO_HIT))
            azul_balas.remove(bala)
        elif bala.x > ANCHO:
            azul_balas.remove(bala)

    for bala in rojo_balas:
        bala.x -= VEL_BALA
        if azul.colliderect(bala):
            pygame.event.post(pygame.event.Event(AZUL_HIT))
            rojo_balas.remove(bala)
        elif bala.x < 0:
            rojo_balas.remove(bala)


def dibujar_ganador(texto):
    texto_fuente = WINNER_FONT.render(texto, 1, BLANCO)
    VENTANA.blit(texto_fuente, (ANCHO / 2 - texto_fuente.get_width() /
                                2, LARGO / 2 - texto_fuente.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)


def mostrar_menu():
    run = True
    play = False
    while run:
        VENTANA.blit(ESPACIO, (0, 0))
        texto = "Presiona w o ^ para iniciar"
        texto_fuente = HEALTH_FONT.render(texto, 1, AMARILLO)
        VENTANA.blit(texto_fuente, (ANCHO / 2 - texto_fuente.get_width() /
                                    2, LARGO / 2 - texto_fuente.get_height() / 2 -100))

        texto = "Muevete: WASD o <^>"
        texto_fuente = HEALTH_FONT.render(texto, 1, BLANCO)
        VENTANA.blit(texto_fuente, (ANCHO / 2 - texto_fuente.get_width() /
                                    2 , LARGO / 2 - texto_fuente.get_height() / 2 + 25))
        texto = "Dispara con: X o -"
        texto_fuente = HEALTH_FONT.render(texto, 1, BLANCO)
        VENTANA.blit(texto_fuente, (ANCHO / 2 - texto_fuente.get_width() /
                                    2 , LARGO / 2 - texto_fuente.get_height() / 2 + 85))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    run = False
                    play = True
            pygame.display.update()
    if not run and play:
        return True
    else:
        return False


def jugar():
    roja = pygame.Rect(700, 300, ANCHO_NAVE, ALTO_NAVE)
    azul = pygame.Rect(100, 300, ANCHO_NAVE, ALTO_NAVE)
    balas_rojo = []
    balas_azul = []
    salud_rojo = 10
    salud_azul = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x and len(balas_azul) < MAX_BALA:
                    bala = pygame.Rect(azul.x + azul.width, azul.y + azul.height // 2 - 2, 10, 5)
                    balas_azul.append(bala)
                if event.key == pygame.K_MINUS and len(balas_rojo) < MAX_BALA:
                    bala = pygame.Rect(roja.x, roja.y + roja.height // 2 - 2, 10, 5)
                    balas_rojo.append(bala)
            if event.type == ROJO_HIT:
                salud_rojo -= 1
            if event.type == AZUL_HIT:
                salud_azul -= 1

        texto_ganador = ""
        if salud_rojo <= 0:
            texto_ganador = "GANASTE AZUL!"

        if salud_azul <= 0:
            texto_ganador = "GANASTE ROJO!"

        if texto_ganador != "":
            dibujar_ganador(texto_ganador)
            break

        teclas_presionadas = pygame.key.get_pressed()
        manejar_nave_azul(teclas_presionadas, azul)
        manejar_nave_roja(teclas_presionadas, roja)
        movimiento_balas(balas_azul, balas_rojo, azul, roja)
        dibujar_ventana(roja, azul, balas_rojo, balas_azul, salud_rojo, salud_azul)

    if run is False:
        pygame.quit()
    else:
        play = mostrar_menu()
        if play:
            jugar()


if __name__ == '__main__':
    play = mostrar_menu()
    if play:
        jugar()
