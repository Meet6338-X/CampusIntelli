/**
 * CampusIntelli API Client
 * Handles all API communication with the backend
 */

const API = {
    BASE_URL: '/api',
    
    // Get auth token from localStorage
    getToken() {
        const user = localStorage.getItem('campus_user');
        if (user) {
            try {
                return JSON.parse(user).token;
            } catch (e) {
                return null;
            }
        }
        return null;
    },
    
    // Make API request
    async request(endpoint, options = {}) {
        const url = `${this.BASE_URL}${endpoint}`;
        const token = this.getToken();
        
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };
        
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        try {
            const response = await fetch(url, {
                ...options,
                headers
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Request failed');
            }
            
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },
    
    // Auth endpoints
    auth: {
        async login(email, password) {
            return API.request('/auth/login', {
                method: 'POST',
                body: JSON.stringify({ email, password })
            });
        },
        
        async register(userData) {
            return API.request('/auth/register', {
                method: 'POST',
                body: JSON.stringify(userData)
            });
        },
        
        async logout() {
            return API.request('/auth/logout', { method: 'POST' });
        },
        
        async getMe() {
            return API.request('/auth/me');
        }
    },
    
    // Users endpoints
    users: {
        async getAll() {
            return API.request('/users/');
        },
        
        async getById(id) {
            return API.request(`/users/${id}`);
        },
        
        async update(id, data) {
            return API.request(`/users/${id}`, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
        },
        
        async getDirectory(query = '') {
            return API.request(`/users/directory?q=${encodeURIComponent(query)}`);
        }
    },
    
    // Courses endpoints
    courses: {
        async getAll() {
            return API.request('/courses/');
        },
        
        async getById(id) {
            return API.request(`/courses/${id}`);
        },
        
        async create(data) {
            return API.request('/courses/', {
                method: 'POST',
                body: JSON.stringify(data)
            });
        },
        
        async getTimetable() {
            return API.request('/courses/timetable');
        }
    },
    
    // Assignments endpoints
    assignments: {
        async getAll() {
            return API.request('/assignments/');
        },
        
        async getById(id) {
            return API.request(`/assignments/${id}`);
        },
        
        async create(data) {
            return API.request('/assignments/', {
                method: 'POST',
                body: JSON.stringify(data)
            });
        },
        
        async submit(assignmentId, formData) {
            const token = API.getToken();
            return fetch(`${API.BASE_URL}/assignments/${assignmentId}/submit`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` },
                body: formData
            }).then(r => r.json());
        },
        
        async getGrades() {
            return API.request('/assignments/grades');
        }
    },
    
    // Bookings endpoints
    bookings: {
        async getRooms() {
            return API.request('/bookings/rooms');
        },
        
        async getAvailable(date, startTime, endTime) {
            return API.request(`/bookings/rooms/available?date=${date}&start_time=${startTime}&end_time=${endTime}`);
        },
        
        async getMyBookings() {
            return API.request('/bookings/');
        },
        
        async create(data) {
            return API.request('/bookings/', {
                method: 'POST',
                body: JSON.stringify(data)
            });
        },
        
        async cancel(id) {
            return API.request(`/bookings/${id}`, { method: 'DELETE' });
        }
    },
    
    // Attendance endpoints
    attendance: {
        async generateQR(courseId) {
            return API.request('/attendance/generate-qr', {
                method: 'POST',
                body: JSON.stringify({ course_id: courseId })
            });
        },
        
        async mark(qrData) {
            return API.request('/attendance/mark', {
                method: 'POST',
                body: JSON.stringify({ qr_data: qrData })
            });
        },
        
        async getRecords(courseId = null) {
            const url = courseId ? `/attendance/?course_id=${courseId}` : '/attendance/';
            return API.request(url);
        },
        
        async getSummary() {
            return API.request('/attendance/summary');
        }
    },
    
    // Announcements endpoints
    announcements: {
        async getAll() {
            return API.request('/announcements/');
        },
        
        async create(data) {
            return API.request('/announcements/', {
                method: 'POST',
                body: JSON.stringify(data)
            });
        },
        
        async delete(id) {
            return API.request(`/announcements/${id}`, { method: 'DELETE' });
        }
    }
};

// Export for use
window.API = API;
