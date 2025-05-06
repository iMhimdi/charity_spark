/**
 * Authentication Helper Functions
 */

// Store token in localStorage
function storeAuthToken(token, user) {
    localStorage.setItem('authToken', token);
    localStorage.setItem('user', JSON.stringify(user));
}

// Remove token from localStorage
function removeAuthToken() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
}

// Check if user is authenticated
function isAuthenticated() {
    return !!localStorage.getItem('authToken');
}

// Get current user from localStorage
function getCurrentUser() {
    const userJson = localStorage.getItem('user');
    return userJson ? JSON.parse(userJson) : null;
}

// Get auth token from localStorage
function getAuthToken() {
    return localStorage.getItem('authToken');
}

// API Login
async function apiLogin(username, password) {
    try {
        const response = await fetch('/api/auth/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            storeAuthToken(data.token, data.user);
            return { success: true, data };
        } else {
            return { success: false, error: data.error || 'Login failed' };
        }
    } catch (error) {
        console.error('Login error:', error);
        return { success: false, error: 'Network error occurred' };
    }
}

// API Register
async function apiRegister(userData) {
    try {
        const response = await fetch('/api/auth/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify(userData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            storeAuthToken(data.token, data.user);
            return { success: true, data };
        } else {
            return { success: false, error: data };
        }
    } catch (error) {
        console.error('Registration error:', error);
        return { success: false, error: 'Network error occurred' };
    }
}

// Logout (client-side)
function logout(redirectUrl = '/') {
    removeAuthToken();
    window.location.href = redirectUrl;
}

// Get CSRF token
function getCSRFToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue;
}