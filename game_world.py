world = [[] for _ in range(4)]
collision_pairs = {}

def add_object(o, depth = 0):
    world[depth].append(o)

def add_objects(ol, depth = 0):
    world[depth] += ol


def update():
    for layer in world:
        for o in layer:
            o.update()


def render():
    for layer in world:
        for o in layer:
            o.draw()

def remove_collisions_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o) # world에서 o를 삭제
            remove_collisions_object(o) # collision pairs에서 o를 삭제
            del o # 메모리에서 객체 자체를 삭제
            return
    raise ValueError('Cannot delete non existing object')


def clear():
    for layer in world:
        layer.clear()



# fill here
def collide(a, b):
    al, ab, ar, at = a.get_bb()
    bl, bb, br, bt = b.get_bb()

    if al > br: return False
    if ar < bl: return False
    if at < bb: return False
    if ab > bt: return False

    return True

def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        collision_pairs[group] = [[],[]]
    if a:#a가 있을떄만 추가하도록
        collision_pairs[group][0].append(a)
    if b:#b가 있을떄만 추가하도록
        collision_pairs[group][1].append(b)


def handle_collisions():
    #game_world 에 등록된 충돌 정보를 바탕으로 실제 정보를  수행
    for group, pairs in collision_pairs.items():
        for a in pairs[0]: # a 리스트에서 하나 뽑고
            for b in pairs[1]: # b 리스트에서 하나 뽑고
                if collide(a, b):
                    print(f'{group} collision')
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)