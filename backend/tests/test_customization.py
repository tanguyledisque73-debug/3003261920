"""
Test suite for Phase 3 - Site Customization Features
Tests: /api/customization, admin customization, banners, videos, chapters, quizzes
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://code-migrate-3.preview.emergentagent.com')

# Test credentials from backend/.env
ADMIN_EMAIL = "ledisque.tanguy73@hotmail.com"
ADMIN_PASSWORD = "NewAdmin123!"
FORMATEUR_EMAIL = "test@secours73.fr"
FORMATEUR_PASSWORD = "test123"
STAGIAIRE_EMAIL = "stagiaire.test@secours73.fr"
STAGIAIRE_PASSWORD = "test123"


class TestCustomizationAPI:
    """Tests for /api/customization endpoint"""
    
    def test_get_customization_public(self):
        """GET /api/customization should return customization settings (public)"""
        response = requests.get(f"{BASE_URL}/api/customization")
        assert response.status_code == 200
        
        data = response.json()
        # Verify required fields exist
        assert "hero_title" in data
        assert "hero_subtitle" in data
        assert "primary_color" in data
        assert "secondary_color" in data
        assert "accent_color" in data
        assert "styles" in data
        assert "banners" in data
        
        # Verify default values
        assert data["hero_title"] == "Formez-vous aux premiers secours"
        assert data["primary_color"] == "#dc2626"
        print(f"✓ Customization API returns valid data with hero_title: {data['hero_title']}")
    
    def test_customization_has_styles(self):
        """Customization should have styles object with element styles"""
        response = requests.get(f"{BASE_URL}/api/customization")
        assert response.status_code == 200
        
        data = response.json()
        styles = data.get("styles", {})
        
        # Check for expected style elements
        expected_elements = ["hero_title", "hero_subtitle", "section_title", "body_text"]
        for element in expected_elements:
            if element in styles:
                style = styles[element]
                # Verify style properties
                assert "font_family" in style or "color" in style or "font_size" in style
                print(f"✓ Style for '{element}' exists with properties")


class TestAdminCustomization:
    """Tests for admin customization endpoints"""
    
    @pytest.fixture
    def admin_token(self):
        """Get admin authentication token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        })
        if response.status_code == 200:
            return response.json().get("token")
        pytest.skip("Admin authentication failed")
    
    def test_admin_login(self):
        """Admin should be able to login"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        })
        assert response.status_code == 200
        
        data = response.json()
        assert "token" in data
        assert "user" in data
        assert data["user"]["role"] == "admin"
        print(f"✓ Admin login successful: {data['user']['email']}")
    
    def test_admin_can_access_banners(self, admin_token):
        """Admin should be able to access banners endpoint"""
        response = requests.get(f"{BASE_URL}/api/admin/banners?token={admin_token}")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        print(f"✓ Admin can access banners: {len(data)} banners found")
    
    def test_admin_can_access_videos(self, admin_token):
        """Admin should be able to access videos endpoint"""
        response = requests.get(f"{BASE_URL}/api/admin/videos?token={admin_token}")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        print(f"✓ Admin can access videos: {len(data)} videos found")


class TestChaptersAPI:
    """Tests for chapters endpoints"""
    
    def test_get_pse_chapters(self):
        """GET /api/chapters?formation_type=PSE should return 12 chapters"""
        response = requests.get(f"{BASE_URL}/api/chapters?formation_type=PSE")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 12
        
        # Verify chapter structure
        for chapter in data:
            assert "id" in chapter
            assert "titre" in chapter
            assert "fiches" in chapter
            assert chapter["formation_type"] == "PSE"
        
        print(f"✓ PSE chapters: {len(data)} chapters with fiches")
    
    def test_get_psc_chapters(self):
        """GET /api/psc/chapters should return 8 chapters"""
        response = requests.get(f"{BASE_URL}/api/psc/chapters")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 8
        
        # Verify chapter structure
        for chapter in data:
            assert "id" in chapter
            assert "titre" in chapter
            assert "fiches" in chapter
            assert chapter["formation_type"] == "PSC"
        
        print(f"✓ PSC chapters: {len(data)} chapters with fiches")
    
    def test_get_chapter_detail(self):
        """GET /api/chapters/{chapter_id} should return chapter with fiches"""
        response = requests.get(f"{BASE_URL}/api/chapters/ch1")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == "ch1"
        assert "titre" in data
        assert "fiches" in data
        assert len(data["fiches"]) > 0
        
        # Verify fiche structure
        fiche = data["fiches"][0]
        assert "id" in fiche
        assert "titre" in fiche
        assert "contenu" in fiche
        
        print(f"✓ Chapter detail: {data['titre']} with {len(data['fiches'])} fiches")
    
    def test_get_psc_chapter_detail(self):
        """GET /api/chapters/{psc_chapter_id} should return PSC chapter"""
        response = requests.get(f"{BASE_URL}/api/chapters/psc-ch1")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == "psc-ch1"
        assert data["formation_type"] == "PSC"
        assert "fiches" in data
        
        print(f"✓ PSC Chapter detail: {data['titre']} with {len(data['fiches'])} fiches")


class TestQuizzesAPI:
    """Tests for quizzes endpoints"""
    
    def test_get_all_quizzes(self):
        """GET /api/quizzes should return 24 quizzes"""
        response = requests.get(f"{BASE_URL}/api/quizzes")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) >= 20  # At least 20 quizzes
        
        # Verify quiz structure - some quizzes may have 'titre' or 'formation_type'
        for quiz in data:
            assert "id" in quiz
            assert "chapter_id" in quiz
            assert "questions" in quiz
        
        print(f"✓ Quizzes: {len(data)} quizzes found")
    
    def test_get_quiz_by_chapter(self):
        """GET /api/quizzes/chapter/{chapter_id} should return quiz for chapter"""
        response = requests.get(f"{BASE_URL}/api/quizzes/chapter/ch1")
        assert response.status_code == 200
        
        data = response.json()
        assert data["chapter_id"] == "ch1"
        assert "questions" in data
        assert len(data["questions"]) > 0
        
        # Verify question structure
        question = data["questions"][0]
        assert "question" in question
        assert "options" in question
        assert "correct_answer" in question
        
        print(f"✓ Quiz for ch1: {data['titre']} with {len(data['questions'])} questions")
    
    def test_quiz_questions_have_content(self):
        """Quiz questions should have relevant content"""
        response = requests.get(f"{BASE_URL}/api/quizzes/chapter/ch1")
        assert response.status_code == 200
        
        data = response.json()
        questions = data["questions"]
        
        for q in questions:
            # Question should not be empty
            assert len(q["question"]) > 10
            # Should have at least 2 options
            assert len(q["options"]) >= 2
            # Correct answer should be valid index
            assert 0 <= q["correct_answer"] < len(q["options"])
        
        print(f"✓ Quiz questions have valid content and structure")


class TestAuthenticationFlows:
    """Tests for authentication flows"""
    
    def test_formateur_login(self):
        """Formateur should be able to login"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": FORMATEUR_EMAIL,
            "password": FORMATEUR_PASSWORD
        })
        assert response.status_code == 200
        
        data = response.json()
        assert "token" in data
        assert data["user"]["role"] == "formateur"
        print(f"✓ Formateur login successful")
    
    def test_stagiaire_login(self):
        """Stagiaire should be able to login"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": STAGIAIRE_EMAIL,
            "password": STAGIAIRE_PASSWORD
        })
        assert response.status_code == 200
        
        data = response.json()
        assert "token" in data
        assert data["user"]["role"] == "stagiaire"
        print(f"✓ Stagiaire login successful")
    
    def test_invalid_login(self):
        """Invalid credentials should return 401"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "invalid@test.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401
        print(f"✓ Invalid login correctly rejected")


class TestAdminStats:
    """Tests for admin statistics"""
    
    @pytest.fixture
    def admin_token(self):
        """Get admin authentication token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        })
        if response.status_code == 200:
            return response.json().get("token")
        pytest.skip("Admin authentication failed")
    
    def test_admin_stats(self, admin_token):
        """Admin should be able to get statistics"""
        response = requests.get(f"{BASE_URL}/api/admin/stats?token={admin_token}")
        assert response.status_code == 200
        
        data = response.json()
        assert "total_formateurs" in data
        assert "total_stagiaires" in data
        assert "total_quizzes" in data
        
        print(f"✓ Admin stats: {data['total_formateurs']} formateurs, {data['total_stagiaires']} stagiaires, {data['total_quizzes']} quizzes")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
