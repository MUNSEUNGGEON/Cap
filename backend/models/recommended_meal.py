class RecommendedMeal:
    """권장 영양소 데이터를 age 범위별로 보관하고 조회하는 클래스."""

    DATA = [
        {
            'min_age': 1,
            'max_age': 3,
            'calories': 1000,
            'carbohydrate': 130,
            'protein': 13,
            'fat': 35,
            'sodium': 1200
        },
        {
            'min_age': 4,
            'max_age': 6,
            'calories': 1400,
            'carbohydrate': 195,
            'protein': 19,
            'fat': 45,
            'sodium': 1500
        },
        {
            'min_age': 7,
            'max_age': 10,
            'calories': 1600,
            'carbohydrate': 225,
            'protein': 34,
            'fat': 55,
            'sodium': 1800
        },
        {
            'min_age': 11,
            'max_age': 14,
            'calories': 2000,
            'carbohydrate': 275,
            'protein': 44,
            'fat': 65,
            'sodium': 2000
        },
        {
            'min_age': 15,
            'max_age': 18,
            'calories': 2400,
            'carbohydrate': 330,
            'protein': 55,
            'fat': 80,
            'sodium': 2300
        }
    ]

    @staticmethod
    def get_by_age(age: int):
        """주어진 나이에 해당하는 권장 영양소 데이터를 반환."""
        for row in RecommendedMeal.DATA:
            if row['min_age'] <= age <= row['max_age']:
                return {
                    'calories': row['calories'],
                    'carbohydrate': row['carbohydrate'],
                    'protein': row['protein'],
                    'fat': row['fat'],
                    'sodium': row['sodium']
                }
        return None
