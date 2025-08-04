import './MyPageMenuBar.css';

const MyPageMenuBar = ({ activeSection, onSectionChange }) => {
  return (
    <div className="mypage-menu-bar">
      <div className="mypage-menu-container">
        <button 
          className={`mypage-menu-item ${activeSection === 'profile' ? 'active' : ''}`}
          onClick={() => onSectionChange('profile')}
        >
          <div className="mypage-menu-icon">👤</div>
          <span className="mypage-menu-text">회원정보 수정</span>
        </button>
        
        <button 
          className={`mypage-menu-item ${activeSection === 'password' ? 'active' : ''}`}
          onClick={() => onSectionChange('password')}
        >
          <div className="mypage-menu-icon">🔒</div>
          <span className="mypage-menu-text">비밀번호 변경</span>
        </button>
        
        <button 
          className={`mypage-menu-item ${activeSection === 'allergy' ? 'active' : ''}`}
          onClick={() => onSectionChange('allergy')}
        >
          <div className="mypage-menu-icon">⚠️</div>
          <span className="mypage-menu-text">알레르기정보 수정</span>
        </button>
      </div>
    </div>
  );
};

export default MyPageMenuBar; 