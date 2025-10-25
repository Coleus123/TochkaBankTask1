import heapq
import sys

objects_room = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
rooms_object = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
skip_positions = [2, 4, 6, 8]
energy = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

def parse_input(lines):
    """
    Разбирает входные строки лабиринта

    Args:
        lines: список строк, представляющих лабиринт

    Returns:
        hall: коридор
        rooms: комнаты
        depth: длина комнат
    """
    depth = 2 if len(lines) == 5 else 4
    hall = lines[1][1:12]
    rooms = tuple(
        ''.join(lines[j][3 + i * 2] for j in range(2, 2 + depth))
        for i in range(4)
    )
    return hall, rooms, depth


def is_goal(rooms, depth):
    """
    Проверяет, соответствует ли состояние лабиринта ответу

    Args:
        rooms: список строк, представляющих комнаты
        depth: длина комнат

    Returns:
        Проверяет, соответствуют ли состояние комнат ответу
    """
    goal = tuple(letter * depth for letter in 'ABCD')
    return rooms == goal


def update_state(heap, states, new_state, new_energy_cost):
    """
    Добавляет состояние в очередь с приоритетом, если оно лучше предыдущего

    Args:
        heap: куча, хранящая энергию и состояние лабиринта
        states: для каждого лабиринта хранит энергию
        new_state: новое состояние лабиринта
        new_energy_cost: затраченная энергия нового лабиринта
    """
    if new_energy_cost < states.get(new_state, float('inf')):
        states[new_state] = new_energy_cost
        heapq.heappush(heap, (new_energy_cost, new_state))


def move_to_hall(hall, rooms, id_room, position, letter,
                 object_depth, room_entrance, energy_cost):
    """Перемещает объект из комнаты в коридор

    Args:
        hall: коридор
        rooms: список строк, представляющих комнаты
        id_room: порядковый номер комнаты начиная с 0
        position: индекс объекта в коридоре
        letter: имя объекта
        object_depth: как глубоко можно положить объект
        room_entrance: индекс входа в комнату в коридоре
        energy_cost: затраченная энергия

    Returns:
        new_hall: новый коридор после передвижения
        new_rooms: новые комнаты после передвижения
        new_energy_cost: затраченная энергия после передвижения
    """
    new_hall = hall[:position] + letter + hall[position + 1:]
    new_rooms = tuple(
        elem.replace(letter, '.', 1) if i == id_room else elem
        for i, elem in enumerate(rooms)
    )
    new_energy_cost = energy_cost + (abs(position - room_entrance)
                                     + 1 + object_depth) * energy[letter]
    return new_hall, new_rooms, new_energy_cost


def move_to_room(hall, rooms, position, letter, room_index,
                 room_entrance, energy_cost):
    """Перемещает объект из коридора в комнату

    Args:
        hall: коридор
        rooms: список строк, представляющих комнаты
        position: индекс объекта в коридоре
        letter: имя объекта
        room_index: индекс комнаты
        room_entrance: индекс входа в комнату в коридоре
        energy_cost: затраченная энергия

    Returns:
        new_hall: новый коридор после передвижения
        new_rooms: новые комнаты после передвижения
        new_energy_cost: затраченная энергия после передвижения
    """
    depth_index = len(rooms[room_index]) - 1
    while rooms[room_index][depth_index] != '.':
        depth_index -= 1
    new_rooms = list(rooms)
    new_rooms[room_index] = (
            rooms[room_index][:depth_index] + letter +
            rooms[room_index][depth_index + 1:]
    )
    new_rooms = tuple(new_rooms)
    new_hall = hall[:position] + '.' + hall[position + 1:]
    new_energy_cost = energy_cost + (abs(position - room_entrance)
                                     + 1 + depth_index) * energy[letter]
    return new_hall, new_rooms, new_energy_cost


def generate_moves_from_rooms(hall, rooms):
    """Все возможные ходы из комнат в коридор

    Args:
        hall: коридор
        rooms: комнаты

    Returns:
        все возможные ходы, содержащие:
        id_room: номер комнаты начиная с 0
        position: позиция объекта в коридоре
        letter: имя объекта
        object_depth: как далеко находится объект в комнате
        room_entrance: позиция входа комнаты в коридоре
    """
    moves = []
    for id_room, room in enumerate(rooms):
        if all(letter == '.' or letter == rooms_object[id_room] for letter in room):
            continue
        room_entrance = 2 + id_room * 2
        object_depth = 0
        while rooms[id_room][object_depth] == '.':
            object_depth += 1
        letter = room[object_depth]
        for position in range(room_entrance - 1, -1, -1):
            if hall[position] != '.':
                break
            if position not in skip_positions:
                moves.append((id_room, position, letter, object_depth, room_entrance))
        for position in range(room_entrance + 1, 11):
            if hall[position] != '.':
                break
            if position not in skip_positions:
                moves.append((id_room, position, letter, object_depth, room_entrance))
    return moves


def generate_moves_to_rooms(hall, rooms):
    """Все возможные ходы из коридора в комнаты

    Args:
        hall: коридор
        rooms: комнаты

    Returns:
        все возможные ходы, содержащие:
        position: позиция объекта в коридоре
        letter: имя объекта
        room_index: номер комнаты начиная с 0
        room_entrance: позиция входа комнаты в коридоре
    """
    moves = []
    for position, letter in enumerate(hall):
        if letter == '.':
            continue
        room_index = objects_room[letter]
        room_entrance = 2 + 2 * room_index
        if any(letter_in_room != '.' and letter_in_room != letter
               for letter_in_room in rooms[room_index]):
            continue
        path = (range(position + 1, room_entrance + 1)
                if position < room_entrance
                else range(room_entrance, position))
        if any(hall[p] != '.' for p in path):
            continue
        moves.append((position, letter, room_index, room_entrance))
    return moves

def solve(lines: list[str]) -> int:
    """
    Решение задачи о сортировке в лабиринте

    Args:
        lines: список строк, представляющих лабиринт

    Returns:
        минимальная энергия для достижения целевой конфигурации
    """
    hall, rooms, depth = parse_input(lines)
    start_state = (hall, rooms)
    heap = [(0, start_state)]
    states = {start_state: 0}

    while heap:
        energy_cost, state = heapq.heappop(heap)
        if energy_cost > states[state]:
            continue
        hall, rooms = state
        if is_goal(rooms, depth):
            return energy_cost
        for id_room, position, letter, obj_depth, room_entrance in generate_moves_from_rooms(hall, rooms):
            new_hall, new_rooms, new_energy_cost = move_to_hall(
                hall, rooms, id_room, position, letter, obj_depth, room_entrance, energy_cost
            )
            update_state(heap, states, (new_hall, new_rooms), new_energy_cost)
        for position, letter, room_index, room_entrance in generate_moves_to_rooms(hall, rooms):
            new_hall, new_rooms, new_energy_cost = move_to_room(
                hall, rooms, position, letter, room_index, room_entrance, energy_cost
            )
            update_state(heap, states, (new_hall, new_rooms), new_energy_cost)

    return 0


def main():
    # Чтение входных данных
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))

    result = solve(lines)
    print(result)


if __name__ == "__main__":
    main()
