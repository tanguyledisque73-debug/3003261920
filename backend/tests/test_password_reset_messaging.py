"""
Backend API Tests for Password Reset and Messaging Features
- Tests forgot-password endpoint
- Tests reset-password endpoint
- Tests messaging CRUD operations
"""

import pytest
import requests
import os
import uuid

# Use environment variable for base URL
BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

# Test credentials from environment variables
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@test.local")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "test_password")


class TestPasswordReset:
    """Password Reset flow tests"""
    
    def test_forgot_password_existing_email(self):
        """Test forgot password with existing email returns success message"""
        response = requests.post(
            f"{BASE_URL}/api/auth/forgot-password",
            json={"email": ADMIN_EMAIL}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        # Should not reveal if email exists (security)
        assert "lien de réinitialisation" in data["message"]
    
    def test_forgot_password_nonexistent_email(self):
        """Test forgot password with nonexistent email still returns success (security)"""
        response = requests.post(
            f"{BASE_URL}/api/auth/forgot-password",
            json={"email": "nonexistent@example.com"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        # Same message for security
        assert "lien de réinitialisation" in data["message"]
    
    def test_reset_password_invalid_token(self):
        """Test reset password with invalid token returns error"""
        response = requests.post(
            f"{BASE_URL}/api/auth/reset-password",
            json={
                "token": "invalid_token_12345",
                "new_password": "NewPassword123!"
            }
        )
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "invalide" in data["detail"].lower() or "expiré" in data["detail"].lower()


class TestMessaging:
    """Internal messaging system tests"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Login and get token before each test"""
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
        )
        if response.status_code != 200:
            pytest.skip("Authentication failed - skipping messaging tests")
        data = response.json()
        self.token = data["token"]
        self.user_id = data["user"]["id"]
        self.user = data["user"]
    
    def test_get_received_messages(self):
        """Test getting received messages"""
        response = requests.get(
            f"{BASE_URL}/api/messages/received",
            params={"token": self.token}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_sent_messages(self):
        """Test getting sent messages"""
        response = requests.get(
            f"{BASE_URL}/api/messages/sent",
            params={"token": self.token}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_unread_count(self):
        """Test getting unread message count"""
        response = requests.get(
            f"{BASE_URL}/api/messages/unread-count",
            params={"token": self.token}
        )
        assert response.status_code == 200
        data = response.json()
        assert "count" in data
        assert isinstance(data["count"], int)
        assert data["count"] >= 0
    
    def test_send_message_to_nonexistent_user(self):
        """Test sending message to non-existent user returns error"""
        response = requests.post(
            f"{BASE_URL}/api/messages",
            params={"token": self.token},
            json={
                "destinataire_id": "nonexistent-user-id-12345",
                "sujet": "Test Subject",
                "contenu": "Test content"
            }
        )
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Destinataire non trouvé" in data["detail"]
    
    def test_send_message_to_self(self):
        """Test sending message to self works"""
        response = requests.post(
            f"{BASE_URL}/api/messages",
            params={"token": self.token},
            json={
                "destinataire_id": self.user_id,
                "sujet": "TEST_Message to myself",
                "contenu": "This is a test message to myself"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "id" in data
        message_id = data["id"]
        
        # Verify message appears in received
        response = requests.get(
            f"{BASE_URL}/api/messages/received",
            params={"token": self.token}
        )
        assert response.status_code == 200
        messages = response.json()
        message_ids = [m["id"] for m in messages]
        assert message_id in message_ids
        
        # Verify message appears in sent
        response = requests.get(
            f"{BASE_URL}/api/messages/sent",
            params={"token": self.token}
        )
        assert response.status_code == 200
        messages = response.json()
        message_ids = [m["id"] for m in messages]
        assert message_id in message_ids
    
    def test_mark_message_as_read(self):
        """Test marking a message as read"""
        # First send a message to self
        send_response = requests.post(
            f"{BASE_URL}/api/messages",
            params={"token": self.token},
            json={
                "destinataire_id": self.user_id,
                "sujet": "TEST_Read test",
                "contenu": "Test marking as read"
            }
        )
        assert send_response.status_code == 200
        message_id = send_response.json()["id"]
        
        # Get initial unread count
        unread_response = requests.get(
            f"{BASE_URL}/api/messages/unread-count",
            params={"token": self.token}
        )
        initial_unread = unread_response.json()["count"]
        
        # Mark as read
        read_response = requests.put(
            f"{BASE_URL}/api/messages/{message_id}/read",
            params={"token": self.token}
        )
        assert read_response.status_code == 200
        
        # Verify unread count decreased
        unread_response = requests.get(
            f"{BASE_URL}/api/messages/unread-count",
            params={"token": self.token}
        )
        new_unread = unread_response.json()["count"]
        assert new_unread < initial_unread
    
    def test_mark_nonexistent_message_as_read(self):
        """Test marking non-existent message as read returns error"""
        response = requests.put(
            f"{BASE_URL}/api/messages/nonexistent-message-id/read",
            params={"token": self.token}
        )
        assert response.status_code == 404
    
    def test_message_requires_auth(self):
        """Test that messaging endpoints require authentication"""
        # Test without token
        response = requests.get(f"{BASE_URL}/api/messages/received")
        assert response.status_code == 422  # Missing required parameter
        
        # Test with invalid token
        response = requests.get(
            f"{BASE_URL}/api/messages/received",
            params={"token": "invalid_token"}
        )
        assert response.status_code == 401


class TestAuthEndpoints:
    """Additional auth endpoint tests"""
    
    def test_login_valid_credentials(self):
        """Test login with valid credentials"""
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
        )
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert "user" in data
        assert data["user"]["email"] == ADMIN_EMAIL
        assert data["user"]["role"] == "admin"
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": ADMIN_EMAIL, "password": "WrongPassword"}
        )
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
