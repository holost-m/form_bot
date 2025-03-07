"""
Модуль создания результатов
"""
import json

from database.db_operations import AnswerTest

# ДА! Захардкодил. Лень было новую таблицу делать
MOTIVES = {
    '1': 'Мотив вознаграждения – вы работаете ради денег и других благ',
    '2': 'Социальный мотив – вам важно одобрение руководства и коллектива',
    '3': 'Процессный мотив – вы трудитесь ради удовольствия от самого процесса работы',
    '4': 'Мотив достижения – вы стремитесь к самоутверждению и самореализации',
    '5': 'Идейный мотив – вам важно достижение совместных с компанией высоких целей'
}


class UserResult:
    def __init__(self, tg_id):
        self.tg_id = tg_id

    def _save_db_result(self):
        self.db_result = AnswerTest().user_result(self.tg_id)

    def main_motivation_find(self):
        self._save_db_result()
        sum_answer = {'1': 0,
                      '2': 0,
                      '3': 0,
                      '4': 0,
                      '5': 0}
        for record in self.db_result:
            if record['number'] >= 6:
                answer_dict = json.loads(record['answer'])
                for key, value in answer_dict.items():
                    sum_answer[key] += int(value)

        min_key = min(sum_answer, key=lambda x: sum_answer[x])

        return MOTIVES[min_key]

class TotalResul:
    @staticmethod
    def total_count():
