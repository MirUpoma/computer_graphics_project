from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random, time, math


WIN_W, WIN_H = 1000, 800
ASPECT = WIN_W / WIN_H
FOVY   = 70.0

cam_yaw    = 0.0
cam_dist   = 320.0
cam_height = 120.0
first_person = False   
paused = False  

SPAWN_HALF_CONE_DEG = 35.0     

_hit_flash_t = 0.0  
BULLET_SPEED = 420.0  
BULLET_SIZE  = 2.0     
BULLET_TTL   = 1.2     
bullets = []  
player_yaw_deg = 0.0
PLAYER_YAW_STEP = 4.0  

scope_active = False
scope_zoom_factor = 0.5   
ARENA_HALF_X = 160.0   
ARENA_HALF_Y = 320.0   
WALL_H     = 24.0     

CLOSE_RANGE_MIN = 80.0
CLOSE_RANGE_MAX = 100.0
MEDIUM_RANGE_MIN = 175.0
MEDIUM_RANGE_MAX = 200.0
HIGH_RANGE_MIN = 275.0
HIGH_RANGE_MAX = 320.0

def draw_military_base_background():
    fence_post_height = 30.0
    fence_post_width = 1.0
    fence_post_spacing = 20.0
    rail_thickness = 0.7
    fence_color = (0.85, 0.85, 0.85)
    camo_height = fence_post_height + 2
    camo_down = 3  
    glColor3f(*fence_color)
    for y in range(int(-ARENA_HALF_Y), int(ARENA_HALF_Y)+1, int(fence_post_spacing)):
        glPushMatrix()
        glTranslatef(-ARENA_HALF_X - 5, y, fence_post_height / 2)
        glScalef(fence_post_width, fence_post_width, fence_post_height)
        glutSolidCube(1.0)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(ARENA_HALF_X + 5, y, fence_post_height / 2)
        glScalef(fence_post_width, fence_post_width, fence_post_height)
        glutSolidCube(1.0)
        glPopMatrix()
    for x in range(int(-ARENA_HALF_X), int(ARENA_HALF_X)+1, int(fence_post_spacing)):
        glPushMatrix()
        glTranslatef(x, -ARENA_HALF_Y - 5, fence_post_height / 2)
        glScalef(fence_post_width, fence_post_width, fence_post_height)
        glutSolidCube(1.0)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(x, ARENA_HALF_Y + 5, fence_post_height / 2)
        glScalef(fence_post_width, fence_post_width, fence_post_height)
        glutSolidCube(1.0)
        glPopMatrix()
    rail_length_x = ARENA_HALF_X * 2 + 10
    rail_length_y = ARENA_HALF_Y * 2 + 10
    glPushMatrix()
    glTranslatef(-ARENA_HALF_X - 5 + fence_post_width / 2, 0, fence_post_height * 0.6)
    glScalef(rail_thickness, rail_length_y, rail_thickness)
    glutSolidCube(1.0)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(ARENA_HALF_X + 5 - fence_post_width / 2, 0, fence_post_height * 0.6)
    glScalef(rail_thickness, rail_length_y, rail_thickness)
    glutSolidCube(1.0)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, -ARENA_HALF_Y - 5 + fence_post_width / 2, fence_post_height * 0.6)
    glScalef(rail_length_x, rail_thickness, rail_thickness)
    glutSolidCube(1.0)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, ARENA_HALF_Y + 5 - fence_post_width / 2, fence_post_height * 0.6)
    glScalef(rail_length_x, rail_thickness, rail_thickness)
    glutSolidCube(1.0)
    glPopMatrix()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(1.0, 1.0, 1.0, 0.4) 
    glBegin(GL_QUADS)
    glVertex3f(-ARENA_HALF_X - 10, -ARENA_HALF_Y - 10, camo_height)
    glVertex3f(-ARENA_HALF_X - 10, ARENA_HALF_Y + 10, camo_height)
    glVertex3f(-ARENA_HALF_X - 2, ARENA_HALF_Y + 10, camo_height - camo_down)
    glVertex3f(-ARENA_HALF_X - 2, -ARENA_HALF_Y - 10, camo_height - camo_down)
    glEnd()
    glBegin(GL_QUADS)
    glVertex3f(ARENA_HALF_X + 10, -ARENA_HALF_Y - 10, camo_height)
    glVertex3f(ARENA_HALF_X + 10, ARENA_HALF_Y + 10, camo_height)
    glVertex3f(ARENA_HALF_X + 2, ARENA_HALF_Y + 10, camo_height - camo_down)
    glVertex3f(ARENA_HALF_X + 2, -ARENA_HALF_Y - 10, camo_height - camo_down)
    glEnd()
    glBegin(GL_QUADS)
    glVertex3f(-ARENA_HALF_X - 10, -ARENA_HALF_Y - 10, camo_height)
    glVertex3f(ARENA_HALF_X + 10, -ARENA_HALF_Y - 10, camo_height)
    glVertex3f(ARENA_HALF_X + 10, -ARENA_HALF_Y - 2, camo_height - camo_down)
    glVertex3f(-ARENA_HALF_X - 10, -ARENA_HALF_Y - 2, camo_height - camo_down)
    glEnd()
    glBegin(GL_QUADS)
    glVertex3f(-ARENA_HALF_X - 10, ARENA_HALF_Y + 10, camo_height)
    glVertex3f(ARENA_HALF_X + 10, ARENA_HALF_Y + 10, camo_height)
    glVertex3f(ARENA_HALF_X + 10, ARENA_HALF_Y + 2, camo_height - camo_down)
    glVertex3f(-ARENA_HALF_X - 10, ARENA_HALF_Y + 2, camo_height - camo_down)
    glEnd()
    glDisable(GL_BLEND)

def draw_arena():
    glColor3f(0.12, 0.13, 0.16)
    glBegin(GL_QUADS)
    glVertex3f(-ARENA_HALF_X, -ARENA_HALF_Y, 0.0)
    glVertex3f(+ARENA_HALF_X, -ARENA_HALF_Y, 0.0)
    glVertex3f(+ARENA_HALF_X, +ARENA_HALF_Y, 0.0)
    glVertex3f(-ARENA_HALF_X, +ARENA_HALF_Y, 0.0)
    glEnd()

    glLineWidth(2.0) 
    glColor3f(0.18, 0.20, 0.24)  
    step = 20.0
    glBegin(GL_LINES)
    for x in range(-int(ARENA_HALF_X), int(ARENA_HALF_X) + 1, int(step)):
        glVertex3f(x, -ARENA_HALF_Y, 0.05) 
        glVertex3f(x, +ARENA_HALF_Y, 0.05)  
    for y in range(-int(ARENA_HALF_Y), int(ARENA_HALF_Y) + 1, int(step)):
        glVertex3f(-ARENA_HALF_X, y, 0.05)  
        glVertex3f(+ARENA_HALF_X, y, 0.05)  
    glEnd()

    glColor3f(0.22, 0.26, 0.32)
    glBegin(GL_QUADS)
    glVertex3f(-ARENA_HALF_X, -ARENA_HALF_Y, 0.0)
    glVertex3f(+ARENA_HALF_X, -ARENA_HALF_Y, 0.0)
    glVertex3f(+ARENA_HALF_X, -ARENA_HALF_Y, WALL_H)
    glVertex3f(-ARENA_HALF_X, -ARENA_HALF_Y, WALL_H)
    glEnd()
    glBegin(GL_QUADS)
    glVertex3f(-ARENA_HALF_X, +ARENA_HALF_Y, 0.0)
    glVertex3f(+ARENA_HALF_X, +ARENA_HALF_Y, 0.0)
    glVertex3f(+ARENA_HALF_X, +ARENA_HALF_Y, WALL_H)
    glVertex3f(-ARENA_HALF_X, +ARENA_HALF_Y, WALL_H)
    glEnd()
    glBegin(GL_QUADS)
    glVertex3f(-ARENA_HALF_X, -ARENA_HALF_Y, 0.0)
    glVertex3f(-ARENA_HALF_X, +ARENA_HALF_Y, 0.0)
    glVertex3f(-ARENA_HALF_X, +ARENA_HALF_Y, WALL_H)
    glVertex3f(-ARENA_HALF_X, -ARENA_HALF_Y, WALL_H)
    glEnd()
    glBegin(GL_QUADS)
    glVertex3f(+ARENA_HALF_X, -ARENA_HALF_Y, 0.0)
    glVertex3f(+ARENA_HALF_X, +ARENA_HALF_Y, 0.0)
    glVertex3f(+ARENA_HALF_X, +ARENA_HALF_Y, WALL_H)
    glVertex3f(+ARENA_HALF_X, -ARENA_HALF_Y, WALL_H)
    glEnd()

LANES = [-80.0, 0.0, +80.0] 
player_lane = 1
PLAYER_X    = LANES[player_lane]
PLAYER_Y    = -ARENA_HALF_Y * 0.55
LEG_H, TORSO_H, HEAD_R = 12.0, 14.0, 6.0
ARM_LEN = 12.0

def draw_player():
    glPushMatrix()
    glTranslatef(PLAYER_X, PLAYER_Y, 0.0)
    glRotatef(player_yaw_deg, 0,0,1)
    leg_h, torso_h, head_r = LEG_H, TORSO_H, HEAD_R
    arm_len = ARM_LEN
    gun_len = 15.0
    glColor3f(0.6, 0.0, 0.6)
    glPushMatrix(); glTranslatef(-4.0, 0.0, 0.0 + leg_h*0.5); glScalef(4,3,leg_h); glutSolidCube(1.0); glPopMatrix()
    glPushMatrix(); glTranslatef(+4.0, 0.0, 0.0 + leg_h*0.5); glScalef(4,3,leg_h); glutSolidCube(1.0); glPopMatrix()
    glColor3f(0.8, 0.6, 1.0) 
    torso_z0 = 0.0 + leg_h
    glPushMatrix(); glTranslatef(0.0, 0.0, torso_z0 + torso_h*0.5); glScalef(10,6,torso_h); glutSolidCube(1.0); glPopMatrix()
    glColor3f(0.95,0.88,0.78)
    head_z = torso_z0 + torso_h + head_r
    glPushMatrix()
    glTranslatef(0.0, 0.0, head_z)
    gluSphere(gluNewQuadric(), head_r, 16, 12)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0.0, 0.0, head_z + head_r)
    glColor3f(1.0, 0.84, 0.0)

    num_spikes = 6
    spike_height = head_r * 1.2
    spike_base_radius = head_r * 0.15

    for i in range(num_spikes):
        glPushMatrix()
        angle = 360.0 / num_spikes * i
        glRotatef(angle, 0, 0, 1)
        glTranslatef(spike_base_radius * 2, 0, 0)
        glRotatef(-90, 1, 0, 0)
        quad = gluNewQuadric()
        gluCylinder(quad, spike_base_radius, 0.0, spike_height, 16, 1)
        glPopMatrix()

    glPopMatrix()

    eye_offset_x = head_r * 0.4 
    eye_offset_y = head_r * 0.9  
    eye_offset_z = head_z + head_r * 0.1 
    glColor3f(0.0, 0.0, 0.0)  
    eye_radius = 1 

    glPushMatrix()
    glTranslatef(-eye_offset_x, eye_offset_y, eye_offset_z)
    quad = gluNewQuadric()
    gluSphere(quad, eye_radius, 16, 12)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(eye_offset_x, eye_offset_y, eye_offset_z)
    quad = gluNewQuadric()
    gluSphere(quad, eye_radius, 16, 12)
    glPopMatrix()

    glColor3f(0.95,0.88,0.78)
    arm_z = torso_z0 + torso_h*0.8
    glPushMatrix(); glTranslatef(-6.5, 0.0, arm_z); glRotatef(-90,1,0,0); glRotatef(+12,0,1,0); gluCylinder(gluNewQuadric(),1.8,1.8,arm_len,12,1); glPopMatrix()
    glPushMatrix(); glTranslatef(+6.5, 0.0, arm_z); glRotatef(-90,1,0,0); glRotatef(-12,0,1,0); gluCylinder(gluNewQuadric(),1.8,1.8,arm_len,12,1); glPopMatrix()

    glColor3f(0.20,0.22,0.28)
    gun_z = torso_z0 + torso_h*0.75
    glPushMatrix(); glTranslatef(0.0, +2.0, gun_z); glRotatef(-90,1,0,0)
    gluCylinder(gluNewQuadric(),2.0,2.0,gun_len,16,1)
    glTranslatef(0,0,gun_len); glRotatef(-90,1,0,0); glScalef(4,4,4); glutSolidCube(1.0)
    glPopMatrix()
    glPopMatrix()

def draw_viewmodel():
    if not first_person: return
    glPushMatrix(); glLoadIdentity()
    glTranslatef(0.0, -8.0, -25.0)
    glPushMatrix(); glColor3f(0.85,0.65,0.45); glTranslatef(-2.5,-1.0,-2.0); glRotatef(15,0,1,0); glScalef(1.0,1.0,6.0); glutSolidCube(1.0); glPopMatrix()
    glPushMatrix(); glColor3f(0.85,0.65,0.45); glTranslatef(+2.5,-1.0,-2.0); glRotatef(-15,0,1,0); glScalef(1.0,1.0,6.0); glutSolidCube(1.0); glPopMatrix()
    glPushMatrix(); glColor3f(0.15,0.15,0.18); glTranslatef(0.0,-1.0,-4.5); glScalef(1.5,1.5,8.0); glutSolidCube(1.0); glPopMatrix()
    glPushMatrix(); glColor3f(0.20,0.20,0.25); glTranslatef(0.0,-1.0,-9.5); glScalef(0.6,0.6,5.0); glutSolidCube(1.0); glPopMatrix()
    glPushMatrix(); glColor3f(0.1,0.1,0.12); glTranslatef(0.0,-2.5,-4.0); glScalef(1.0,2.0,1.0); glutSolidCube(1.0); glPopMatrix()
    glPopMatrix()

def clamp(v,a,b): return max(a, min(b, v))
_last = time.time()

def gun_muzzle_world():
    base_z = (LEG_H + TORSO_H * 0.75)
    px, py = PLAYER_X, PLAYER_Y
    yaw = math.radians(player_yaw_deg)
    fx, fy = -math.sin(yaw), math.cos(yaw) 
    forward_offset = 8.0  
    x = px + fx * forward_offset
    y = py + fy * forward_offset
    return x, y, base_z, fx, fy

def spawn_bullet():
    x, y, z, fx, fy = gun_muzzle_world()
    vx = fx * BULLET_SPEED
    vy = fy * BULLET_SPEED
    vz = 0.0
    bullets.append({'x':x, 'y':y, 'z':z, 'vx':vx, 'vy':vy, 'vz':vz, 'ttl':BULLET_TTL})


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18, rgb=(1,1,1)):
    r,g,b = rgb
    glColor3f(r,g,b)
    glMatrixMode(GL_PROJECTION); glPushMatrix(); glLoadIdentity()
    gluOrtho2D(0, WIN_W, 0, WIN_H)
    glMatrixMode(GL_MODELVIEW); glPushMatrix(); glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text: glutBitmapCharacter(font, ord(ch))
    glPopMatrix(); glMatrixMode(GL_PROJECTION); glPopMatrix(); glMatrixMode(GL_MODELVIEW)

def project_point_to_screen(x, y, z):
    model = glGetDoublev(GL_MODELVIEW_MATRIX)
    proj  = glGetDoublev(GL_PROJECTION_MATRIX)
    vp    = glGetIntegerv(GL_VIEWPORT)
    sx, sy, sz = gluProject(x, y, z, model, proj, vp)
    return sx, sy, sz

def aim_world_point(distance=300.0, z_offset=-10.0):
    (ox, oy, oz), (fx, fy, fz) = player_vectors()
    return ox + fx*distance, oy + fy*distance, (oz + z_offset)

CHEAT_DURATION = 8.0
cheat_active = False
cheat_time_left = 0.0
cheat_used = False 

def random_spawn_in_front_range(dist_min, dist_max, max_attempts=16):
    px, py = PLAYER_X, PLAYER_Y
    yaw = math.radians(player_yaw_deg)
    fwdx, fwdy = -math.sin(yaw), math.cos(yaw)

    left  = -ARENA_HALF_X + TARGET_MARGIN
    right = +ARENA_HALF_X - TARGET_MARGIN
    bottom= -ARENA_HALF_Y + TARGET_MARGIN
    top   = +ARENA_HALF_Y - TARGET_MARGIN

    for _ in range(max_attempts):
        a_off = math.radians(random.uniform(-SPAWN_HALF_CONE_DEG, SPAWN_HALF_CONE_DEG))
        ca, sa = math.cos(a_off), math.sin(a_off)
        dirx = fwdx*ca - fwdy*sa
        diry = fwdx*sa + fwdy*ca
        dist = random.uniform(dist_min, dist_max)
        x = px + dirx * dist
        y = py + diry * dist

        proj = (x - px) * fwdx + (y - py) * fwdy
        if proj <= 0.0: continue
        if x < left or x > right or y < bottom or y > top: continue

        return x, y

    x = px + fwdx * dist_min
    y = py + fwdy * dist_min
    return clamp(x, left, right), clamp(y, bottom, top)

def camera_vectors():

    if first_person:
        eyeX, eyeY, eyeZ = PLAYER_X, PLAYER_Y, LEG_H + TORSO_H + HEAD_R
        lookX, lookY, lookZ = PLAYER_X, PLAYER_Y + 60.0, eyeZ
    else:
        yaw = math.radians(cam_yaw)
        cx = math.sin(yaw) * cam_dist
        cy = -math.cos(yaw) * cam_dist
        cz = cam_height
        eyeX, eyeY, eyeZ = cx, cy, cz
        lookX, lookY, lookZ = 0.0, 0.0, 18.0
    fx, fy, fz = (lookX-eyeX, lookY-eyeY, lookZ-eyeZ)
    m = math.sqrt(fx*fx + fy*fy + fz*fz) + 1e-6
    return (eyeX, eyeY, eyeZ), (fx/m, fy/m, fz/m)

def setup_camera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if first_person and scope_active:
        gluPerspective(FOVY * scope_zoom_factor, ASPECT, 0.5, 4000.0)
    else:
        gluPerspective(FOVY, ASPECT, 0.5, 4000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if first_person:
        eyeZ = LEG_H + TORSO_H + HEAD_R
        yaw  = math.radians(player_yaw_deg)
        eyeX, eyeY = PLAYER_X, PLAYER_Y
        yaw  = math.radians(player_yaw_deg)
        fx, fy = -math.sin(yaw), math.cos(yaw)
        lookX = eyeX + fx * 60.0
        lookY = eyeY + fy * 60.0
        lookZ = eyeZ
        gluLookAt(eyeX, eyeY, eyeZ, lookX, lookY, lookZ, 0, 0, 1)
    else:
        yaw = math.radians(cam_yaw)
        cx = math.sin(yaw) * cam_dist
        cy = -math.cos(yaw) * cam_dist
        cz = cam_height
        gluLookAt(cx, cy, cz, 0.0, 0.0, 18.0, 0, 0, 1)

STATE_MENU, STATE_PLAY, STATE_SUMMARY, STATE_SELECT_MODE = 0, 1, 2, 3
state = STATE_SELECT_MODE

total_rounds    = 3
round_index     = 1

ROUND_TIME_START = 30.0
round_time_left  = ROUND_TIME_START

score = 0
combo = 0
best_combo = 0

shots_fired = 0
shots_hit   = 0
miss_penalty = 3      
round_shots_fired = 0
round_shots_hit   = 0
round_kills       = 0

MAG_CAPACITY = 8
ammo_in_mag  = MAG_CAPACITY
reloading    = False
reload_time  = 0.8
reload_t     = 0.0

kills_total = 0
BASE_TTL   = 5.0
MIN_TTL    = 2.0
BASE_SPEED = 18.0
SPEED_STEP = 2.0

ROUND_SPEED_INC = 3.0    
TTL_ROUND_REDUCTION = 0.3 

MAX_ACTIVE_TARGETS = 5
TARGET_MIN_Z = 10.0
TARGET_MAX_Z = 38.0
TARGET_MARGIN = 20.0
targets = []

real_game_mode = False
initial_targets_to_hit = 5
giant_target_hits_needed = 10
giant_target_active = False
giant_target_alive = False
giant_target_hit_count = 0
giant_target_ttl = 20.0
giant_target_timer = 0.0
real_game_initial_time = 30.0 
giant_outcome_message = None   

giant_target_speed = 25.0
giant_target_x = 0.0
giant_target_y = 0.0
giant_target_z = 15.0
giant_target_dir = 1
giant_target_spin = 0.0
giant_target_spin_speed = 200.0
practice_message_show = False

def current_ttl():
    step = 0.5 * (kills_total // 5)
    round_step = TTL_ROUND_REDUCTION * (max(0, round_index - 1))
    return max(MIN_TTL, BASE_TTL - step - round_step)

def current_speed():
    step = SPEED_STEP * (kills_total // 5)
    round_step = ROUND_SPEED_INC * (max(0, round_index - 1))
    return BASE_SPEED + step + round_step

def random_kind():  return random.choice(["sphere","cube","pyramid"])
def random_color(): return (random.uniform(0.35,1.0), random.uniform(0.35,1.0), random.uniform(0.35,1.0))

def gun_height():
    return (LEG_H + TORSO_H * 0.75)

def spawn_target():
    if len([t for t in targets if t['alive']]) >= MAX_ACTIVE_TARGETS:
        return
    if not real_game_mode: 
        if round_index == 1:
            dist_min, dist_max = CLOSE_RANGE_MIN, CLOSE_RANGE_MAX
        elif round_index == 2:
            dist_min, dist_max = MEDIUM_RANGE_MIN, MEDIUM_RANGE_MAX
        else:
            dist_min, dist_max = HIGH_RANGE_MIN, HIGH_RANGE_MAX
    else:
        dist_min, dist_max = CLOSE_RANGE_MAX, HIGH_RANGE_MIN

    x, y = random_spawn_in_front_range(dist_min, dist_max)
    z = gun_height()

    moving = (random.random() < 0.7)
    speed  = current_speed() if moving else 0.0
    dir_   = random.choice([-1, +1]) if moving else 0
    targets.append({
        'kind': random_kind(),
        'x': x, 'y': y, 'z': z,
        'color': random_color(),
        'spin': random.uniform(0.0, 360.0),
        'spin_speed': random.uniform(20.0, 90.0),
        'ttl': current_ttl(),
        'alive': True,
        'moving': moving,
        'vx': speed,
        'dir': dir_,
        'flash_t': 0.0,
    })

def ensure_targets():
    attempts = 0
    while len([t for t in targets if t['alive']]) < MAX_ACTIVE_TARGETS and attempts < 32:
        spawn_target()
        attempts += 1

def player_vectors():
    """Origin at player chest/gun height, forward from player_yaw (consistent with mesh)."""
    eyeX = PLAYER_X
    eyeY = PLAYER_Y
    eyeZ = LEG_H + TORSO_H * 0.75
    yaw  = math.radians(player_yaw_deg)
    fx, fy, fz = -math.sin(yaw), math.cos(yaw), 0.0 
    return (eyeX, eyeY, eyeZ), (fx, fy, fz)

def draw_bullets():
    if not bullets: return
    glColor3f(0.95, 0.95, 0.95)
    for b in bullets:
        glPushMatrix()
        glTranslatef(b['x'], b['y'], b['z'])
        glScalef(BULLET_SIZE, BULLET_SIZE, BULLET_SIZE)
        glutSolidCube(1.0)
        glPopMatrix()

def draw_target(t):
    r,g,b = t['color']
    if t['flash_t'] > 0.0:
        mix = clamp(t['flash_t']/0.12, 0.0, 1.0)
        r = 1.0*mix + r*(1.0-mix)
        g = 1.0*mix + g*(1.0-mix)
        b = 1.0*mix + b*(1.0-mix)
    glPushMatrix(); glTranslatef(t['x'], t['y'], t['z']); glColor3f(r,g,b)
    glRotatef(t['spin'], 0,0,1)
    if t['kind'] == 'sphere':
        gluSphere(gluNewQuadric(), 7.0, 16, 12)
    elif t['kind'] == 'cube':
        glScalef(14.0, 14.0, 14.0); glutSolidCube(1.0)
    else:
        glRotatef(-90, 1,0,0); glutSolidCone(8.0, 18.0, 4, 1)
    glPopMatrix()

def pick_centered_target(max_angle_deg=4.0, max_range=1200.0):
    (cx,cy,cz), (fx,fy,fz) = player_vectors()  
    best=None; best_ang=999.0
    for t in targets:
        if not t['alive']: continue
        vx,vy,vz = t['x']-cx, t['y']-cy, t['z']-cz
        dist = math.sqrt(vx*vx+vy*vy+vz*vz)
        if dist>max_range: continue
        dot = (fx*vx + fy*vy + fz*vz) / (dist + 1e-6)
        dot = clamp(dot, -1.0, 1.0)
        ang = math.degrees(math.acos(dot))
        if ang < best_ang:
            best_ang=ang; best=t
    if best and best_ang <= max_angle_deg:
        return best
    return None

def base_points_for_kind(kind):
    if kind == 'sphere':  return 10
    if kind == 'cube':    10   
    if kind == 'pyramid': 10   
    return 10

def draw_giant_target():
    if not giant_target_alive:
        return
    glPushMatrix()
    jump_offset = abs(math.sin(time.time() * 6.0)) * 20.0 
    glTranslatef(giant_target_x, giant_target_y, giant_target_z + jump_offset)
    glColor3f(1.0, 0.0, 0.0)
    glRotatef(giant_target_spin, 0, 0, 1)
    glutSolidSphere(12.5, 32, 32)
    glPopMatrix()

def update_giant_target(dt):
    global giant_target_x, giant_target_y, giant_target_dir, giant_target_spin
    left_bound = -ARENA_HALF_X+ 30
    right_bound = ARENA_HALF_X- 30
    giant_target_x += giant_target_dir * giant_target_speed * dt
    if giant_target_x < left_bound:
        giant_target_x = left_bound
        giant_target_dir = 1
    elif giant_target_x > right_bound:
        giant_target_x = right_bound
        giant_target_dir = -1
    giant_target_y = math.sin(time.time() * 6.0) * 20.0 
    giant_target_spin = (giant_target_spin + giant_target_spin_speed * dt) % 360.0


def reset_combo_on_miss():
    global combo, score
    combo = 0
    score = max(0, score - miss_penalty)

def try_fire():
    global ammo_in_mag, shots_fired, reloading, round_shots_fired
    if reloading or ammo_in_mag <= 0 or state != STATE_PLAY or paused:
        return
    ammo_in_mag -= 1
    shots_fired += 1
    round_shots_fired += 1
    spawn_bullet()

def target_hit_radius(t):
    if t['kind'] == 'sphere':  return 8.0
    if t['kind'] == 'cube':    return 10.5
    if t['kind'] == 'pyramid': return 9.0
    return 9.0

def start_round(idx=1):
    global state, paused, round_index, round_time_left
    global ammo_in_mag, reloading, reload_t, targets
    global cheat_active, cheat_time_left, cheat_used
    global round_shots_fired, round_shots_hit, round_kills
    global practice_message_show
    global giant_target_active, giant_target_alive, giant_target_hit_count, giant_target_timer 
    global giant_outcome_message 
    global state, targets, score, combo, best_combo, shots_fired, shots_hit

    score = 0
    combo = 0
    best_combo = 0
    shots_fired = 0
    shots_hit = 0
    state = STATE_PLAY
    paused = False
    round_index = idx
    round_time_left = ROUND_TIME_START
    ammo_in_mag = MAG_CAPACITY
    reloading = False
    reload_t = 0.0
    cheat_active = False
    cheat_time_left = 0.0
    cheat_used = False
    round_shots_fired = 0
    round_shots_hit = 0
    round_kills = 0
    achievements_unlocked.clear()
    practice_message_show = False
    giant_outcome_message = None
    giant_target_active = False     
    giant_target_alive = False
    giant_target_hit_count = 0
    giant_target_timer = 0.0
    targets[:] = []
    ensure_targets()

def end_round():
    global state, best_combo
    best_combo = max(best_combo, combo)
    check_achievements()
    state = STATE_SUMMARY

achievements_unlocked = set()
hit_times = []
sniper_streak = 0

def check_achievements():
    global achievements_unlocked, round_shots_fired, round_shots_hit, best_combo, hit_times
    acc = (round_shots_hit / round_shots_fired * 100.0) if round_shots_fired > 0 else 0.0
    if acc >= 85.0 and best_combo >= 2:
        achievements_unlocked.add("Sharpshooter")
    if best_combo >= 5:
        achievements_unlocked.add("Combo Master")
    if len(hit_times) >= 8 and hit_times[-1] - hit_times[-8] <= 10.0:
        achievements_unlocked.add("Speed Demon")

def update(dt):
    global round_time_left, reloading, reload_t, ammo_in_mag, state, _hit_flash_t
    global shots_hit, combo, best_combo, score, kills_total
    global cheat_active, cheat_time_left
    global round_shots_hit, round_kills
    global real_game_mode, giant_target_active, giant_target_alive
    global giant_target_hit_count, giant_target_timer
    global practice_message_show
    global giant_outcome_message 

    if state != STATE_PLAY or paused: return
    round_time_left = max(0.0, round_time_left - dt)
    if not real_game_mode:
        if round_time_left <= 0.0:
            end_round()
            return
    if real_game_mode:
        if not giant_target_active:
            round_time_left = max(0.0, round_time_left - dt)
            if round_time_left == 0.0 and round_kills < initial_targets_to_hit:
                practice_message_show = True  
                end_round()
                return

            if round_kills >= initial_targets_to_hit:
                giant_target_active = True
                giant_target_alive = True
                giant_target_hit_count = 0
                giant_target_timer = giant_target_ttl
                for t in targets:
                    t['alive'] = False
        
        else:
            giant_target_timer = max(0.0, giant_target_timer - dt)
            update_giant_target(dt)
            if giant_target_timer == 0.0:
                giant_outcome_message = "You Lost"
                end_round()
                return
    if reloading:
        reload_t -= dt
        if reload_t <= 0.0:
            reloading = False
            ammo_in_mag = MAG_CAPACITY

    if cheat_active:
        cheat_time_left = max(0.0, cheat_time_left - dt)
        if cheat_time_left == 0.0:
            cheat_active = False


    if _hit_flash_t > 0.0:
        _hit_flash_t = max(0.0, _hit_flash_t - dt)


    for t in targets:
        if not t['alive']: continue
        t['ttl'] -= dt
        t['spin'] = (t['spin'] + t['spin_speed']*dt) % 360.0
        if t['moving']:
            if not cheat_active:
                t['x'] += t['dir'] * t['vx'] * dt
                left = -ARENA_HALF_X + TARGET_MARGIN
                right = +ARENA_HALF_X - TARGET_MARGIN
                if t['x'] < left:  t['x']=left;  t['dir']=+1
                if t['x'] > right: t['x']=right; t['dir']=-1
            
        if t['flash_t']>0.0: t['flash_t']=max(0.0, t['flash_t']-dt)

    new_bullets = []
    for b in bullets:
        hit_any = False
        b['x'] += b['vx'] * dt
        b['y'] += b['vy'] * dt
        b['z'] += b['vz'] * dt
        b['ttl'] -= dt
        if b['ttl'] <= 0.0:
            reset_combo_on_miss()
            continue
        if giant_target_active and giant_target_alive:
            dx = giant_target_x - b['x']
            dy = giant_target_y - b['y']
            dz = giant_target_z + abs(math.sin(time.time() * 6.0)) * 20.0 - b['z']  
            dist_sq = dx*dx + dy*dy + dz*dz
            radius = 12.5
            if dist_sq <= radius*radius:
                giant_target_hit_count += 1
                score += 10
                _hit_flash_t = 0.25
                if giant_target_hit_count >= giant_target_hits_needed:
                    giant_target_alive = False
                    giant_outcome_message = "win"
                    end_round()
                hit_any = True
        if not hit_any and not giant_target_active:
            for t in targets:
                if not t['alive']:
                    continue
                dx = t['x'] - b['x']
                dy = t['y'] - b['y']
                dz = t['z'] - b['z']
                if (dx*dx + dy*dy + dz*dz) <= (target_hit_radius(t) ** 2):
                    shots_hit += 1
                    round_shots_hit += 1
                    combo += 1
                    best_combo = max(best_combo, combo)
                    now = time.time()
                    hit_times.append(now)
                    if len(hit_times) > 20:
                        hit_times.pop(0)

                    dist = math.sqrt(dx*dx + dy*dy + dz*dz)
                    if dist > HIGH_RANGE_MIN * 0.7:
                        sniper_streak += 1
                    else:
                        sniper_streak = 0
                    if combo % 3 == 0:
                        score += 5 
                    score += base_points_for_kind(t['kind'])
                    t['alive'] = False
                    t['flash_t'] = 0.12
                    _hit_flash_t = 0.18
                    kills_total += 1
                    round_kills += 1
                    hit_any = True
                    break

        if hit_any:
            pass
        else:
            new_bullets.append(b)

    bullets[:] = new_bullets
    keep=[]
    for t in targets:
        if t['alive']:
            if t['ttl'] <= 0.0:
                reset_combo_on_miss()
            else:
                keep.append(t)
    targets[:] = keep
    if not giant_target_active:
         ensure_targets()
def draw_hud():
    left_x = 35
    draw_text(left_x, WIN_H-75, f"Score: {score}")
    draw_text(left_x, WIN_H-95, f"Combo: {combo}")
    draw_text(left_x, 100, f"Ammo: {ammo_in_mag}/{MAG_CAPACITY} {'[RELOADING]' if reloading else ''}")
    right_x = WIN_W - 240 
    draw_text(right_x, WIN_H-55, f"Round: {round_index}/{total_rounds}")
    draw_text(right_x, WIN_H-79, f"Kills : {round_kills}")

    if first_person and scope_active and state == STATE_PLAY:
        glColor4f(0, 0, 0, 0.7)
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(WIN_W, 0)
        glVertex2f(WIN_W, WIN_H)
        glVertex2f(0, WIN_H)
        glEnd()
        glColor3f(0, 0, 0)
        glLineWidth(3.0)
        num_segments = 100
        radius = 250
        cx, cy = WIN_W//2, WIN_H//2
        glBegin(GL_LINE_LOOP)
        for i in range(num_segments):
            theta = 2.0 * math.pi * i / num_segments
            x = cx + radius * math.cos(theta)
            y = cy + radius * math.sin(theta)
            glVertex2f(x, y)
        glEnd()
        glBegin(GL_LINES)
        glVertex2f(cx - 30, cy); glVertex2f(cx + 30, cy)
        glVertex2f(cx, cy - 30); glVertex2f(cx, cy + 30)
        glEnd()

    if giant_target_active:
        draw_text(right_x, WIN_H-119, f"Giant Target Hits: {giant_target_hit_count}/{giant_target_hits_needed}")
        draw_text(right_x, WIN_H-143, f"Giant Target Time Left: {giant_target_timer:0.1f}s")
    else:
        draw_text(right_x, WIN_H-103, f"Time: {round_time_left:0.1f}s")
  
    if cheat_active:
        draw_text((WIN_W//2)-100, 100, f"CHEAT: FREEZE {cheat_time_left:0.1f}s",
                  GLUT_BITMAP_HELVETICA_18, (0.95,0.95,0.2))
    elif cheat_used and state == STATE_PLAY:
        draw_text((WIN_W//2)-120, 100, "CHEAT: USED THIS ROUND",
                  GLUT_BITMAP_HELVETICA_18, (0.8,0.6,0.2))
    if paused:
        draw_text((WIN_W//2)-42, WIN_H//2, "PAUSED",
                  GLUT_BITMAP_HELVETICA_18, (1,0.9,0.2))

    if state == STATE_MENU:
        draw_text((WIN_W//2)-120, WIN_H//2 + 30, "TARGET PRACTICE RANGE")
        draw_text((WIN_W//2)-80, WIN_H//2 - 10, "Press R to Start")

    elif state == STATE_SUMMARY:

        if giant_outcome_message == "win":
            draw_text((WIN_W//2)-80, WIN_H//2 + 60, "EXCELLENT WORK!", GLUT_BITMAP_HELVETICA_18, (0.2,1.0,0.2))
            draw_text((WIN_W//2)-100, WIN_H//2 - 20, "Press R to Restart Game")
            return  

        elif giant_outcome_message == "You Lost":
            draw_text((WIN_W//2)-60, WIN_H//2 + 60, "YOU LOST!", GLUT_BITMAP_HELVETICA_18, (1.0,0.2,0.2))
            draw_text((WIN_W//2)-100, WIN_H//2 - 20, "Press R to Restart Game")
            return  
        else:
            acc = (round_shots_hit/round_shots_fired*100.0) if round_shots_fired>0 else 0.0

            draw_text((WIN_W//2)-80, WIN_H//2 + 170, "ROUND SUMMARY")

            # Stats (centered lines)
            draw_text((WIN_W//2)-100, WIN_H//2 + 140,
                    f"Score: {score}   Best Combo: {best_combo}")
            draw_text((WIN_W//2)-120, WIN_H//2+ 110, 
                    f"Accuracy: {acc:0.1f}%  Hits: {round_shots_hit}/{round_shots_fired}")

        if achievements_unlocked:
            draw_text((WIN_W//2)-100, WIN_H//2 - 150, "Achievements Unlocked:")
            for i, ach in enumerate(sorted(list(achievements_unlocked))):
                draw_text((WIN_W//2)-90, WIN_H//2 - 175 - 25*i,
                          f"- {ach}", GLUT_BITMAP_HELVETICA_18, (0.9,0.9,0.2))

        if round_index < total_rounds:
            draw_text((WIN_W//2)-90, WIN_H//2 - 230, "Press R for Next Round")
        else:
            draw_text((WIN_W//2)-100, WIN_H//2 - 230, "Press R to Restart Game")
    if practice_message_show and state == STATE_SUMMARY:
        draw_text(400, WIN_H - 80, "Need more practice, try again!", GLUT_BITMAP_HELVETICA_18, (1.0, 0.2, 0.2))

    if real_game_mode and state == STATE_PLAY and not giant_target_active:
        mid_x = WIN_W // 2
        if round_kills < initial_targets_to_hit:
            draw_text(mid_x - 100, WIN_H - 55, "Clear 5 Targets and face the", GLUT_BITMAP_HELVETICA_18, (1,1,1))
            draw_text(mid_x - 80, WIN_H - 80, "MONSTER SURPRISE! ", GLUT_BITMAP_HELVETICA_18, (1,0,0))
            draw_text(mid_x - 15, WIN_H - 103, "muhaha", GLUT_BITMAP_HELVETICA_12, (0.85,0.85,0.85))

    if state == STATE_PLAY:
 
        glColor3f(0.2, 0.2, 0.2)  
        glBegin(GL_QUADS)
        glVertex2f(10, WIN_H - 35)
        glVertex2f(110, WIN_H - 35)
        glVertex2f(110, WIN_H - 10)
        glVertex2f(10, WIN_H - 10)
        glEnd()

        draw_text(35, WIN_H - 40, "Back", GLUT_BITMAP_HELVETICA_18, (1,1,1))
    if state in (STATE_PLAY, STATE_SUMMARY):
        glColor3f(0.2, 0.2, 0.2)
        glBegin(GL_QUADS)
        glVertex2f(10, WIN_H - 35)
        glVertex2f(110, WIN_H - 35)
        glVertex2f(110, WIN_H - 10)
        glVertex2f(10, WIN_H - 10)
        glEnd()
        draw_text(35, WIN_H - 40, "Back", GLUT_BITMAP_HELVETICA_18, (1,1,1))

_old_render = None
def render():
    global _old_render, state
    if _old_render is None:
        _old_render = _render_original
    if state == STATE_SELECT_MODE:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        setup_camera()
        draw_military_base_background()
        draw_arena()

        draw_text((WIN_W//2) - 90, (WIN_H//2) + 60, "Select Game Mode")
        draw_text((WIN_W//2) - 60, (WIN_H//2) + 20, "1: Practice ")
        draw_text((WIN_W//2) - 60, (WIN_H//2) - 20, "2: Play Game ")

        glutSwapBuffers()
    elif state == STATE_PLAY:
        _render_original()
    else:
        _old_render()

def _render_original():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_camera()
    draw_military_base_background() 
    draw_arena()

    if not first_person: draw_player()

    for t in targets:
        if t['alive']: draw_target(t)
        
    if giant_target_active and giant_target_alive:
        draw_giant_target()

    draw_bullets()

    draw_hud()
    draw_viewmodel()
    glutSwapBuffers()

def keyboard(key, x, y):
    global first_person, paused, state, round_index
    global score, combo, best_combo, shots_fired, shots_hit, kills_total
    global reloading, reload_t, ammo_in_mag
    global player_yaw_deg
    global cheat_active, cheat_time_left, cheat_used
    global total_rounds 
    global state, round_index, total_rounds, real_game_mode, ROUND_TIME_START, round_time_left
    global giant_target_active, giant_target_alive
    global scope_active, scope_zoom_factor

    if state == STATE_SELECT_MODE:
        if key == b'1': 
            real_game_mode = False
            total_rounds = 3
            ROUND_TIME_START = 20.0
            round_time_left = ROUND_TIME_START
            giant_target_active = False
            giant_target_alive = False
            state = STATE_PLAY
            round_index = 1
            start_round(round_index)
            return
        elif key == b'2':  
            real_game_mode = True
            total_rounds = 1
            ROUND_TIME_START = 30.0
            round_time_left = ROUND_TIME_START
            giant_target_active = False
            giant_target_alive = False
            state = STATE_PLAY
            round_index = 1
            start_round(round_index)
            return

    if key in (b'f', b'F'):
        first_person = not first_person
        return

    if key in (b'v', b'V'):
        if first_person:   
                scope_active = not scope_active
        return

    if key in (b'p', b'P'):
        if state == STATE_PLAY:
            paused = not paused
        return

    if key in (b'c', b'C'):
        if state == STATE_PLAY and not cheat_used:
            cheat_active = True
            cheat_time_left = CHEAT_DURATION
            cheat_used = True
        return
    if key in (b'q', b'Q'):
        state = STATE_SELECT_MODE
        return

    if key in (b'r', b'R'):
        if state in (STATE_MENU, STATE_SUMMARY):
            if state == STATE_SUMMARY:
                if round_index < total_rounds:
                    round_index += 1
                    start_round(round_index)
                else:
                    score = combo = best_combo = 0
                    shots_fired = shots_hit = 0
                    kills_total = 0
                    round_index = 1
                    
                    start_round(round_index)
            else:
                start_round(round_index)
        elif state == STATE_PLAY:
            start_round(round_index)
        if first_person:
            first_person = False  
        return

    if key in (b'a', b'A'):
        player_yaw_deg = (player_yaw_deg + PLAYER_YAW_STEP) % 360.0  
        return
    elif key in (b'd', b'D'):
        player_yaw_deg = (player_yaw_deg - PLAYER_YAW_STEP) % 360.0 
        return

def special(key, x, y):
    global cam_yaw, cam_dist
    if key == GLUT_KEY_LEFT:  cam_yaw += 3.0
    elif key == GLUT_KEY_RIGHT: cam_yaw -= 3.0
    elif key == GLUT_KEY_UP:   cam_dist = max(60.0, cam_dist - 10.0)   
    elif key == GLUT_KEY_DOWN: cam_dist = min(600.0, cam_dist + 10.0) 


def mouse(button, state_btn, x, y):
    global reloading, reload_t, cam_dist, ammo_in_mag
    global state, paused
    if state_btn != GLUT_DOWN: return
    flipped_y = WIN_H - y
    if button == GLUT_LEFT_BUTTON:
        if 10 <= x <= 110 and (WIN_H - 35) <= flipped_y <= (WIN_H - 10):
            if state in (STATE_PLAY, STATE_SUMMARY):
                paused = False
                state = STATE_SELECT_MODE
                return
    if button == GLUT_LEFT_BUTTON:
        try_fire()
    elif button == GLUT_RIGHT_BUTTON:
        if state == STATE_PLAY and not reloading and ammo_in_mag < MAG_CAPACITY:
            reloading = True; reload_t = reload_time
    elif button == 3: 
        cam_dist = max(60.0, cam_dist - 10.0)
    elif button == 4:  
        cam_dist = min(600.0, cam_dist + 10.0)

def idle():
    global _last
    now = time.time(); dt = max(0.0, min(0.05, now-_last)); _last = now
    if not paused: update(dt)
    glutPostRedisplay()

def init_gl():
    glClearColor(0.05, 0.06, 0.08, 1.0)
    glEnable(GL_DEPTH_TEST) 
_last = time.time()

def main():
    random.seed(7)
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WIN_W, WIN_H)
    glutCreateWindow(b"Target Practice Range ")
    init_gl()
    ensure_targets()
    glutDisplayFunc(render)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special)
    glutMouseFunc(mouse)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()
