import datetime
import random
import traceback

from services.meal_filter import filter_foods_by_allergy
from models.meal import Meal
from models.recommended_meal import RecommendedMeal
from models.user import User
from services.meal_nutrition import (
    get_nutrition_by_food_id,
    save_meal_total_nutrition,
)

def generate_daily_meal(user_id, date=None):
    """
    사용자 맞춤 하루 식단을 생성하고, 식단 영양소도 저장합니다.
    """
    if date is None:
        date = datetime.date.today()

    try:
        print(f"🌟 하루 식단 생성: user_id={user_id}, date={date}")

        # ✅ 1️⃣ 사용자 알러지 기반 음식 데이터 필터링
        filtered_foods = filter_foods_by_allergy(user_id)

        # ✅ 2️⃣ 카테고리별 음식 분류
        rice_list = [f for f in filtered_foods if f['Food_role'] == '밥']
        soup_list = [f for f in filtered_foods if f['Food_role'] == '국&찌개']
        side_dishes_list = [f for f in filtered_foods if f['Food_role'] == '반찬']
        main_dish_list = [f for f in filtered_foods if f['Food_role'] == '일품']
        dessert_list = [f for f in filtered_foods if f['Food_role'] == '후식']

        # ✅ 2️⃣-1️⃣ 각 카테고리별 후보 수 제한 (과도한 조합 탐색 방지)
        def limit_candidates(lst, max_count=30):
            if len(lst) > max_count:
                return random.sample(lst, max_count)
            return lst

        rice_list = limit_candidates(rice_list)
        soup_list = limit_candidates(soup_list)
        side_dishes_list = limit_candidates(side_dishes_list)
        main_dish_list = limit_candidates(main_dish_list)
        dessert_list = limit_candidates(dessert_list)

        # ✅ 3️⃣ 권장 영양소 기준에 맞는 조합 탐색
        user = User.get_by_id(user_id)
        age = None
        if user:
            age = user.get('Age') or user.get('age')
        recommended = RecommendedMeal.get_by_age(age) if age is not None else None
        target_nutrition = {}
        if recommended:
            # 1회 식사의 권장량으로 계산 (1일 권장량의 1/3)
            target_nutrition = {
                key: value / 3 for key, value in recommended.items()
            }

        # 음식별 영양소 정보 캐시
        candidates_for_nutrition = (
            rice_list
            + soup_list
            + side_dishes_list
            + main_dish_list
            + dessert_list
        )
        nutrition_cache = {
            f['Food_id']: get_nutrition_by_food_id(f['Food_id'])
            for f in candidates_for_nutrition
        }

        def calc_totals(selected):
            totals = {
                'calories': 0,
                'carbohydrate': 0,
                'protein': 0,
                'fat': 0,
                'sodium': 0,
            }
            for food in selected:
                nutri = nutrition_cache.get(food['Food_id'], {})
                for k in totals:
                    totals[k] += nutri.get(k, 0)
            return totals

        def score_totals(totals):
            if not target_nutrition:
                return float('inf')
            score = 0
            for k, target in target_nutrition.items():
                if target:
                    score += abs(totals[k] - target) / target
            return score

        def within_range(totals, margin=0.2):
            if not target_nutrition:
                return True
            for k, target in target_nutrition.items():
                if target and not (target * (1 - margin) <= totals[k] <= target * (1 + margin)):
                    return False
            return True

        best_combo = None
        best_score = float('inf')

        # ✅ 무작위 탐색으로 조합 수 감소
        attempts = 500
        for _ in range(attempts):
            rice = random.choice(rice_list) if rice_list else None
            soup = random.choice(soup_list) if soup_list else None
            main_dish = random.choice(main_dish_list) if main_dish_list else None
            dessert = random.choice(dessert_list) if dessert_list else None

            if len(side_dishes_list) >= 2:
                sides = random.sample(side_dishes_list, 2)
            elif len(side_dishes_list) == 1:
                sides = [side_dishes_list[0]]
            else:
                sides = []

            selected = [x for x in [rice, soup, main_dish, dessert] if x] + list(sides)
            totals = calc_totals(selected)

            if within_range(totals):
                best_combo = (rice, soup, sides, main_dish, dessert)
                break

            score = score_totals(totals)
            if score < best_score or best_combo is None:
                best_score = score
                best_combo = (rice, soup, sides, main_dish, dessert)

        rice, soup, side_dishes, main_dish, dessert = best_combo

        print(
            f"  🍚 선택 결과: rice={rice['Food_id'] if rice else None}, "
            f"soup={soup['Food_id'] if soup else None}, "
            f"side_dishes={[d['Food_id'] for d in side_dishes] if side_dishes else []}, "
            f"main_dish={main_dish['Food_id'] if main_dish else None}, "
            f"dessert={dessert['Food_id'] if dessert else None}"
        )

        # ✅ 4️⃣ 각 항목의 음식 ID
        rice_id = rice['Food_id'] if rice else None
        soup_id = soup['Food_id'] if soup else None
        main_dish_id = main_dish['Food_id'] if main_dish else None
        dessert_id = dessert['Food_id'] if dessert else None
        side_dish1_id = side_dishes[0]['Food_id'] if len(side_dishes) > 0 else None
        side_dish2_id = side_dishes[1]['Food_id'] if len(side_dishes) > 1 else None

        # ✅ 5️⃣ Meal 객체 생성 및 저장
        meal = Meal(
            User_id=user_id,
            Date=date,
            Rice_id=rice_id,
            Soup_id=soup_id,
            SideDish1_id=side_dish1_id,
            SideDish2_id=side_dish2_id,
            MainDish_id=main_dish_id,
            Dessert_id=dessert_id
        )
        print("  📝 식단 저장 중...")
        meal_id = meal.save()
        print(f"  ✅ 식단 저장 완료: meal_id={meal_id}")

        # ✅ 6️⃣ 음식 ID 리스트로 영양소 총합 저장
        food_ids = [f['Food_id'] for f in [rice, soup, main_dish, dessert] + side_dishes if f]
        save_meal_total_nutrition(meal_id, food_ids)

        return meal_id

    except Exception as e:
        print(f"❌ 하루 식단 생성 오류: {e}")
        traceback.print_exc()
        return None
