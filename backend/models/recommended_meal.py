from config import get_db_connection


class RecommendedMeal:
    """`Recommended_Meal` 테이블에서 권장 영양소 정보를 조회하는 클래스."""

    @staticmethod
    def get_by_age(age: int):
        """주어진 나이에 맞는 권장 영양소 데이터를 데이터베이스에서 조회."""
        conn = get_db_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    """
                    SELECT Recommended_calories, Recommended_carbohydrate,
                           Recommended_protein, Recommended_fat, Recommended_sodium
                    FROM Recommended_Meal
                    WHERE age = %s
                    """,
                    (age,)
                )
                row = cursor.fetchone()
                if row:
                    return {
                        'calories': row['Recommended_calories'],
                        'carbohydrate': row['Recommended_carbohydrate'],
                        'protein': row['Recommended_protein'],
                        'fat': row['Recommended_fat'],
                        'sodium': row['Recommended_sodium']
                    }
        finally:
            conn.close()
        return None
