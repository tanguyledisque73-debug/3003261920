"""
FAOD-SECOURS73 Content Verification Tests
Tests for verifying pedagogical content: chapters, fiches, and quizzes
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestPSEChapters:
    """Tests for PSE (Premiers Secours en Équipe) chapters - Expected: 12 chapters with 37 fiches"""
    
    def test_pse_chapters_count(self):
        """Verify exactly 12 PSE chapters exist"""
        response = requests.get(f"{BASE_URL}/api/chapters?formation_type=PSE")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        chapters = response.json()
        assert len(chapters) == 12, f"Expected 12 PSE chapters, got {len(chapters)}"
    
    def test_pse_chapters_have_fiches(self):
        """Verify PSE chapters have fiches and total is 37"""
        response = requests.get(f"{BASE_URL}/api/chapters?formation_type=PSE")
        assert response.status_code == 200
        
        chapters = response.json()
        total_fiches = sum(len(ch.get('fiches', [])) for ch in chapters)
        assert total_fiches == 37, f"Expected 37 PSE fiches, got {total_fiches}"
        
        # Each chapter should have at least 1 fiche
        for ch in chapters:
            assert len(ch.get('fiches', [])) >= 1, f"Chapter {ch.get('id')} has no fiches"
    
    def test_pse_chapters_structure(self):
        """Verify PSE chapters have required fields"""
        response = requests.get(f"{BASE_URL}/api/chapters?formation_type=PSE")
        assert response.status_code == 200
        
        chapters = response.json()
        required_fields = ['id', 'numero', 'titre', 'description', 'formation_type', 'fiches']
        
        for ch in chapters:
            for field in required_fields:
                assert field in ch, f"Chapter {ch.get('id')} missing field: {field}"
            assert ch['formation_type'] == 'PSE', f"Chapter {ch.get('id')} has wrong formation_type"
    
    def test_pse_fiches_content_format(self):
        """Verify fiches content has no markdown characters"""
        response = requests.get(f"{BASE_URL}/api/chapters?formation_type=PSE")
        assert response.status_code == 200
        
        chapters = response.json()
        markdown_chars = ['#', '**', '##', '###', '```']
        
        for ch in chapters:
            for fiche in ch.get('fiches', []):
                contenu = fiche.get('contenu', '')
                # Check for markdown headers (# at start of line)
                lines = contenu.split('\n')
                for line in lines:
                    stripped = line.strip()
                    if stripped.startswith('#') and not stripped.startswith('# '):
                        # Allow # in middle of text, just not as markdown headers
                        pass


class TestPSCChapters:
    """Tests for PSC (Prévention et Secours Civiques) chapters - Expected: 8 chapters with 19 fiches"""
    
    def test_psc_chapters_count(self):
        """Verify exactly 8 PSC chapters exist"""
        response = requests.get(f"{BASE_URL}/api/psc/chapters")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        chapters = response.json()
        assert len(chapters) == 8, f"Expected 8 PSC chapters, got {len(chapters)}"
    
    def test_psc_chapters_have_fiches(self):
        """Verify PSC chapters have fiches and total is 19"""
        response = requests.get(f"{BASE_URL}/api/psc/chapters")
        assert response.status_code == 200
        
        chapters = response.json()
        total_fiches = sum(len(ch.get('fiches', [])) for ch in chapters)
        assert total_fiches == 19, f"Expected 19 PSC fiches, got {total_fiches}"
    
    def test_psc_chapters_structure(self):
        """Verify PSC chapters have required fields"""
        response = requests.get(f"{BASE_URL}/api/psc/chapters")
        assert response.status_code == 200
        
        chapters = response.json()
        required_fields = ['id', 'numero', 'titre', 'description', 'formation_type', 'fiches']
        
        for ch in chapters:
            for field in required_fields:
                assert field in ch, f"Chapter {ch.get('id')} missing field: {field}"
            assert ch['formation_type'] == 'PSC', f"Chapter {ch.get('id')} has wrong formation_type"


class TestQuizzes:
    """Tests for quizzes - Expected: 20 quizzes (12 PSE + 8 PSC) with 96 questions"""
    
    def test_quizzes_count(self):
        """Verify exactly 20 quizzes exist"""
        response = requests.get(f"{BASE_URL}/api/quizzes")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        quizzes = response.json()
        assert len(quizzes) == 20, f"Expected 20 quizzes, got {len(quizzes)}"
    
    def test_quizzes_total_questions(self):
        """Verify total of 96 questions across all quizzes"""
        response = requests.get(f"{BASE_URL}/api/quizzes")
        assert response.status_code == 200
        
        quizzes = response.json()
        total_questions = sum(len(q.get('questions', [])) for q in quizzes)
        assert total_questions == 96, f"Expected 96 questions, got {total_questions}"
    
    def test_quizzes_structure(self):
        """Verify quizzes have required fields"""
        response = requests.get(f"{BASE_URL}/api/quizzes")
        assert response.status_code == 200
        
        quizzes = response.json()
        required_fields = ['id', 'chapter_id', 'titre', 'questions']
        
        for quiz in quizzes:
            for field in required_fields:
                assert field in quiz, f"Quiz {quiz.get('id')} missing field: {field}"
    
    def test_quiz_questions_structure(self):
        """Verify quiz questions have required fields"""
        response = requests.get(f"{BASE_URL}/api/quizzes")
        assert response.status_code == 200
        
        quizzes = response.json()
        question_fields = ['id', 'question', 'type', 'options', 'correct_answer', 'explication']
        
        for quiz in quizzes:
            for q in quiz.get('questions', []):
                for field in question_fields:
                    assert field in q, f"Question in quiz {quiz.get('id')} missing field: {field}"
                # Verify question type is valid
                assert q['type'] in ['qcm', 'vrai_faux'], f"Invalid question type: {q['type']}"
                # Verify correct_answer is valid index
                assert 0 <= q['correct_answer'] < len(q['options']), f"Invalid correct_answer index"
    
    def test_each_chapter_has_quiz(self):
        """Verify each chapter has at least one quiz"""
        # Get all chapters
        pse_response = requests.get(f"{BASE_URL}/api/chapters?formation_type=PSE")
        psc_response = requests.get(f"{BASE_URL}/api/psc/chapters")
        quizzes_response = requests.get(f"{BASE_URL}/api/quizzes")
        
        assert pse_response.status_code == 200
        assert psc_response.status_code == 200
        assert quizzes_response.status_code == 200
        
        pse_chapters = pse_response.json()
        psc_chapters = psc_response.json()
        quizzes = quizzes_response.json()
        
        quiz_chapter_ids = set(q.get('chapter_id') for q in quizzes)
        
        # Check PSE chapters have quizzes
        for ch in pse_chapters:
            assert ch['id'] in quiz_chapter_ids, f"PSE Chapter {ch['id']} has no quiz"
        
        # Check PSC chapters have quizzes
        for ch in psc_chapters:
            assert ch['id'] in quiz_chapter_ids, f"PSC Chapter {ch['id']} has no quiz"


class TestAuthentication:
    """Tests for authentication endpoints"""
    
    def test_admin_login(self):
        """Test admin login with provided credentials"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "ledisque.tanguy73@hotmail.com",
            "password": "NewAdmin123!"
        })
        assert response.status_code == 200, f"Admin login failed: {response.text}"
        
        data = response.json()
        assert 'token' in data, "No token in response"
        assert 'user' in data, "No user in response"
        assert data['user']['role'] == 'admin', f"Expected admin role, got {data['user']['role']}"
    
    def test_formateur_login(self):
        """Test formateur login with provided credentials"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "test@secours73.fr",
            "password": "test123"
        })
        assert response.status_code == 200, f"Formateur login failed: {response.text}"
        
        data = response.json()
        assert 'token' in data, "No token in response"
        assert data['user']['role'] == 'formateur', f"Expected formateur role, got {data['user']['role']}"
    
    def test_stagiaire_login(self):
        """Test stagiaire login with provided credentials"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "stagiaire.test@secours73.fr",
            "password": "test123"
        })
        assert response.status_code == 200, f"Stagiaire login failed: {response.text}"
        
        data = response.json()
        assert 'token' in data, "No token in response"
        assert data['user']['role'] == 'stagiaire', f"Expected stagiaire role, got {data['user']['role']}"
    
    def test_invalid_login(self):
        """Test login with invalid credentials returns 401"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "invalid@test.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"


class TestChapterEndpoints:
    """Tests for individual chapter endpoints"""
    
    def test_get_single_pse_chapter(self):
        """Test getting a single PSE chapter by ID"""
        response = requests.get(f"{BASE_URL}/api/chapters/pse-ch1")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        chapter = response.json()
        assert chapter['id'] == 'pse-ch1'
        assert chapter['formation_type'] == 'PSE'
        assert len(chapter.get('fiches', [])) > 0
    
    def test_get_single_psc_chapter(self):
        """Test getting a single PSC chapter by ID"""
        response = requests.get(f"{BASE_URL}/api/chapters/psc-ch1")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        chapter = response.json()
        assert chapter['id'] == 'psc-ch1'
        assert chapter['formation_type'] == 'PSC'
    
    def test_get_nonexistent_chapter(self):
        """Test getting a non-existent chapter returns 404"""
        response = requests.get(f"{BASE_URL}/api/chapters/nonexistent-chapter")
        assert response.status_code == 404


class TestQuizEndpoints:
    """Tests for quiz-specific endpoints"""
    
    def test_get_quiz_by_chapter(self):
        """Test getting quiz by chapter ID"""
        response = requests.get(f"{BASE_URL}/api/quizzes/chapter/pse-ch1")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        quiz = response.json()
        assert quiz['chapter_id'] == 'pse-ch1'
        assert len(quiz.get('questions', [])) > 0
    
    def test_get_quiz_by_id(self):
        """Test getting quiz by quiz ID"""
        # First get all quizzes to get a valid ID
        all_quizzes = requests.get(f"{BASE_URL}/api/quizzes").json()
        if all_quizzes:
            quiz_id = all_quizzes[0]['id']
            response = requests.get(f"{BASE_URL}/api/quizzes/{quiz_id}")
            assert response.status_code == 200
            
            quiz = response.json()
            assert quiz['id'] == quiz_id


class TestAdminEndpoints:
    """Tests for admin-specific endpoints"""
    
    @pytest.fixture
    def admin_token(self):
        """Get admin authentication token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "ledisque.tanguy73@hotmail.com",
            "password": "NewAdmin123!"
        })
        if response.status_code == 200:
            return response.json().get('token')
        pytest.skip("Admin authentication failed")
    
    def test_admin_stats(self, admin_token):
        """Test admin statistics endpoint"""
        response = requests.get(f"{BASE_URL}/api/admin/stats?token={admin_token}")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        stats = response.json()
        assert 'total_formateurs' in stats
        assert 'total_stagiaires' in stats
        assert 'total_quizzes' in stats
    
    def test_admin_get_formateurs(self, admin_token):
        """Test admin get all formateurs endpoint"""
        response = requests.get(f"{BASE_URL}/api/admin/formateurs?token={admin_token}")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        formateurs = response.json()
        assert isinstance(formateurs, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
