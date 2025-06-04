import React, { useState, useEffect } from 'react';
import { getFoodDetail, getFoodNutrition } from '../../services/foodService';
import './FoodDetail.css';

const FoodDetail = ({ foodId, onClose }) => {
  const [foodDetail, setFoodDetail] = useState(null);
  const [nutrition, setNutrition] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchFoodDetail = async () => {
      try {
        setLoading(true);
        setError(null);
        if (!foodId) {
          setError('음식 ID가 제공되지 않았습니다.');
          setLoading(false);
          return;
        }
        const response = await getFoodDetail(foodId);
        if (response.success) setFoodDetail(response);
        else setError(response.message || '음식 정보를 가져오는데 실패했습니다.');
      } catch (err) {
        setError('서버에 연결할 수 없거나 데이터를 가져오는데 실패했습니다.');
      } finally {
        setLoading(false);
      }
    };
    fetchFoodDetail();
  }, [foodId]);

  useEffect(() => {
    if (foodId) {
      getFoodNutrition(foodId)
        .then(res => res.success && setNutrition(res.nutrition))
        .catch(() => setNutrition(null));
    }
  }, [foodId]);

  const formatMaterials = (str) => str ? str.split(',').map(item => item.trim()) : [];
  const formatCookingSteps = (str) => str ? str.split('\n').filter(step => step.trim() !== '') : [];
  const extractImageUrl = (url) => url ? (url.startsWith('http') ? url : `http:${url}`) : '';

  return (
    <div className="food-detail-container">
      <div className="food-detail-header">
        <h2 className="food-detail-title">
          {loading ? '로딩 중...' : foodDetail?.food?.Food_name || '음식 정보 없음'}
        </h2>
        <button className="close-button" onClick={onClose}>×</button>
      </div>

      {loading ? (
        <div className="loading-message">음식 정보를 불러오는 중...</div>
      ) : error ? (
        <div className="error-message">{error}</div>
      ) : foodDetail ? (
        <div className="food-detail-content">
          {/* 왼쪽: 이미지 + 영양정보 + 재료 + 조리법 */}
          <div className="food-main-info">
            <div className="food-image-nutrition">
              <div className="food-image">
                {foodDetail.food.Food_img && (
                  <img
                    src={extractImageUrl(foodDetail.food.Food_img)}
                    alt={foodDetail.food.Food_name}
                    className="food-detail-img"
                  />
                )}
              </div>
              {nutrition && (
                <div className="food-nutrition-card">
                  <h3>영양 정보</h3>
                  <ul>
                    <li><strong>칼로리</strong> <span>{nutrition.calories} kcal</span></li>
                    <li><strong>탄수화물</strong> <span>{nutrition.carbohydrate} g</span></li>
                    <li><strong>단백질</strong> <span>{nutrition.protein} g</span></li>
                    <li><strong>지방</strong> <span>{nutrition.fat} g</span></li>
                    <li><strong>나트륨</strong> <span>{nutrition.sodium} mg</span></li>
                  </ul>
                </div>
              )}
            </div>

            <div className="food-materials">
              <h3>재료</h3>
              <ul className="materials-list">
                {formatMaterials(foodDetail.food.Food_materials).map((m, idx) => (
                  <li key={idx}>{m}</li>
                ))}
              </ul>
            </div>

            <div className="food-recipe">
              <h3>조리 방법</h3>
              {foodDetail.cooking?.Food_cooking_method ? (
                <ol className="cooking-steps">
                  {formatCookingSteps(foodDetail.cooking.Food_cooking_method).map((s, idx) => (
                    <li key={idx}>{s}</li>
                  ))}
                </ol>
              ) : (
                <p className="no-recipe">레시피 정보가 없습니다.</p>
              )}
            </div>
          </div>

          {/* 오른쪽: 관련 상품 */}
          <div className="related-products-section">
            <h3>관련 상품</h3>
            {foodDetail.related_products?.length > 0 ? (
              <div className="products-grid">
                {foodDetail.related_products.map((p, idx) => (
                  <div key={idx} className="product-card">
                    {p.img && (
                      <img
                        src={extractImageUrl(p.img)}
                        alt={p.food_products}
                        className="product-img"
                      />
                    )}
                    <div className="product-info">
                      <div className="product-name">{p.food_products}</div>
                      <div className="product-category">{p.category}</div>
                      <div className="product-price">
                        {Number(p.price).toLocaleString()} 원
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="no-products">관련 상품이 없습니다.</p>
            )}
          </div>
        </div>
      ) : (
        <div className="no-data-message">음식 정보가 없습니다.</div>
      )}
    </div>
  );
};

export default FoodDetail;
