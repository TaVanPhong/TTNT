import random
# Định nghĩa lớp học
class Class:
    def __init__(self, subject, teacher, students, duration, required_equipment):
        self.subject = subject
        self.teacher = teacher
        self.students = students
        self.duration = duration
        self.required_equipment = required_equipment

# Định nghĩa phòng học
class Room:
    def __init__(self, capacity, equipment, available_times):
        self.capacity = capacity
        self.equipment = equipment
        self.available_times = available_times

# Định nghĩa giáo viên
class Teacher:
    def __init__(self, name, available_times, subjects):
        self.name = name
        self.available_times = available_times
        self.subjects = subjects

# Định nghĩa lịch học
class Schedule:
    def __init__(self):
        self.schedule = []  # Danh sách các lớp học đã xếp lịch

    def add_class(self, class_obj, room, time_slot):
        self.schedule.append((class_obj, room, time_slot))

    def fitness(self):
        score = 0
        teacher_schedule = {}
        student_schedule = {}

        for class_obj, room, time_slot in self.schedule:
            # Kiểm tra xung đột lịch giáo viên
            if class_obj.teacher.name in teacher_schedule:
                if time_slot in teacher_schedule[class_obj.teacher.name]:
                    score -= 10
            else:
                teacher_schedule[class_obj.teacher.name] = []
            teacher_schedule[class_obj.teacher.name].append(time_slot)

            # Kiểm tra xung đột lịch sinh viên
            for student in class_obj.students:
                if student in student_schedule:
                    if time_slot in student_schedule[student]:
                        score -= 10
                else:
                    student_schedule[student] = []
                student_schedule[student].append(time_slot)

            # Kiểm tra phòng học
            if room.capacity < len(class_obj.students):
                score -= 5
            if not all(equipment in room.equipment for equipment in class_obj.required_equipment):
                score -= 5

            # Ưu tiên thời gian mong muốn của giáo viên
            if time_slot in class_obj.teacher.available_times:
                score += 5

        return score

# Giao phối hai cá thể
def crossover(parent1, parent2, lops_hoc, phong_hoc):
    child = Schedule()
    used_time_slots = set()

    for class_obj in lops_hoc:
        room = random.choice(phong_hoc)
        time_slot = random.choice(room.available_times)
        if time_slot not in used_time_slots:
            child.add_class(class_obj, room, time_slot)
            used_time_slots.add(time_slot)

    return child

# Thuật toán di truyền
def genetic_algorithm(lops_hoc, phong_hoc, generations=100, population_size=50):
    population = [Schedule() for _ in range(population_size)]
    
    for generation in range(generations):
        fitness_scores = [schedule.fitness() for schedule in population]
        best_schedules = sorted(zip(population, fitness_scores), key=lambda x: x[1], reverse=True)
        population = [schedule for schedule, _ in best_schedules[:population_size // 2]]

        new_population = []
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population, 2)
            child = crossover(parent1, parent2, lops_hoc, phong_hoc)

            if random.random() < 0.1:  # 10% xác suất đột biến
                random_class = random.choice(lops_hoc)
                room = random.choice(phong_hoc)
                time_slot = random.choice(room.available_times)
                child.add_class(random_class, room, time_slot)

            new_population.append(child)

        population.extend(new_population)

    return max(population, key=lambda s: s.fitness())

# Khởi tạo danh sách giáo viên
giao_vien = [
    Teacher("Cô Alice", ["9:00-10:30", "11:00-12:30"], ["Toán"]),
    Teacher("Thầy Bob", ["9:00-10:30", "11:00-12:30"], ["Vật lý"]),
    Teacher("Cô Charlie", ["10:30-12:00", "13:00-14:50"], ["Hóa học"]),
]

teacher_dict = {teacher.name: teacher for teacher in giao_vien}

# Khởi tạo danh sách lớp học
lops_hoc = [
    Class("Toán", teacher_dict["Cô Alice"], ["Học sinh 1", "Học sinh 2"], 90, ["Máy chiếu"]),
    Class("Vật lý", teacher_dict["Thầy Bob"], ["Học sinh 1", "Học sinh 3"], 90, ["Máy chiếu"]),
    Class("Hóa học", teacher_dict["Cô Charlie"], ["Học sinh 2", "Học sinh 4"], 90, ["Bảng tương tác"]),
]

# Khởi tạo danh sách phòng học
phong_hoc = [
    Room(30, ["Máy chiếu"], ["9:00-10:30", "11:00-12:30"]),
    Room(20, ["Bảng tương tác"], ["9:00-10:30", "10:30-12:00"]),
    Room(25, ["Máy chiếu", "Bảng tương tác"], ["10:30-12:00", "13:00-14:30"]),
]

# Chạy thuật toán di truyền
best_schedule = genetic_algorithm(lops_hoc, phong_hoc)

# In ra lịch học tốt nhất
print("Lịch học tốt nhất:")
for class_obj, room, time_slot in best_schedule.schedule:
    print(f"Môn: {class_obj.subject}, Giáo viên: {class_obj.teacher.name}, Phòng: {room.equipment}, Thời gian: {time_slot}")
