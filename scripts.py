from random import choice

from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation
from django.core.exceptions import ObjectDoesNotExist


def fix_marks(schoolkid):
    """Исправляет оценки 2,3 на 5 у выбранного ученика"""
    try:
        user = Schoolkid.objects.filter(full_name__contains=schoolkid)
        marks = Mark.objects.filter(schoolkid=user[0], points__in=[2, 3])
        for mark in marks:
            mark.points = 5
            mark.save()
    except Schoolkid.DoesNotExist:
        print(f'{schoolkid} не найден в базе данных. Проверьте правильность ввода')
    except Schoolkid.MultipleObjectsReturned:
        print(f'Найдено более 1 записи - {schoolkid}')


def remove_chastisements(schoolkid):
    """Удаляет все замечания у выбранного ученика"""
    try:
        all_chastisement = Chastisement.objects.filter(schoolkid__full_name__contains=schoolkid)
        all_chastisement.delete()
    except Schoolkid.DoesNotExist:
        print(f'{schoolkid} не найден в базе данных. Проверьте правильность ввода')


def get_commedation():
    """Получение текста похвалы"""
    with open('commedations', encoding='utf') as fh:
        lines = fh.read().split('\n')
    return choice(lines)


def create_commendation(schoolkid, lesson_title):
    """Создает похвалу для выбранного ученика и предмета"""
    try:
        user = Schoolkid.objects.get(full_name__contains=schoolkid)
        lesson = Lesson.objects.filter(group_letter=user.group_letter, year_of_study=user.year_of_study, subject__title=lesson_title).order_by('-date').first()
        Commendation.objects.create(text=get_commedation(), schoolkid=user, created=lesson.date, subject=lesson.subject, teacher=lesson.teacher)
    except ObjectDoesNotExist:
        print(f'{schoolkid} не найден в базе данных. Проверьте правильность ввода')
    except AttributeError:
        print(f"{lesson_title} не найден в базе данных. Проверьте правильность ввода")
    except Schoolkid.MultipleObjectsReturned:
        print(f'Найдено более 1 записи - {schoolkid}. Укажите полное ФИО ученика')



