from random import choice

from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, \
    Commendation


def fix_marks(full_name):
    """Исправляет оценки 2,3 на 5 у выбранного ученика."""
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=full_name)
        marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
        for mark in marks:
            mark.points = 5
            mark.save()
    except Schoolkid.DoesNotExist:
        print(f'{full_name} не найден в базе данных. Проверьте правильность'
              f'ввода')
    except Schoolkid.MultipleObjectsReturned:
        print(f'Найдено более 1 записи - {full_name}')


def remove_chastisements(full_name):
    """Удаляет все замечания у выбранного ученика."""
    all_chastisement = Chastisement.objects.filter(
        schoolkid__full_name__contains=full_name)
    all_chastisement.delete()


def get_commedation():
    """Получение текста похвалы."""
    with open('commedations', encoding='utf') as fh:
        lines = fh.read().splitlines()
    return choice(lines)


def create_commendation(full_name, lesson_title):
    """Создает похвалу для выбранного ученика и предмета."""
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=full_name)
        lesson = Lesson.objects.filter(group_letter=schoolkid.group_letter,
                                       year_of_study=schoolkid.year_of_study,
                                       subject__title=lesson_title)\
            .order_by('-date').first()
        if not lesson:
            print(f"{lesson_title} не найден в базе данных."
                  f" Проверьте правильность ввода")
            return
        Commendation.objects.create(text=get_commedation(),
                                    schoolkid=schoolkid,
                                    created=lesson.date,
                                    subject=lesson.subject,
                                    teacher=lesson.teacher)
    except Schoolkid.DoesNotExist:
        print(f'{full_name} не найден в базе данных. Проверьте правильность '
              f'ввода')
    except Schoolkid.MultipleObjectsReturned:
        print(f'Найдено более 1 записи - {full_name}. Укажите полное ФИО '
              f'ученика')

