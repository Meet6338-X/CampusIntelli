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

        async update(id, data) {
            return API.request(`/assignments/${id}`, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
        },

        async delete(id) {
            return API.request(`/assignments/${id}`, { method: 'DELETE' });
        },

        async submit(assignmentId, formData) {
            const token = API.getToken();
            const response = await fetch(`${API.BASE_URL}/assignments/${assignmentId}/submit`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` },
                body: formData
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Submission failed');
            return data;
        },

        async getSubmissions(assignmentId) {
            return API.request(`/assignments/${assignmentId}/submissions`);
        },

        async downloadSubmission(submissionId) {
            const token = API.getToken();
            window.open(`${API.BASE_URL}/assignments/submissions/${submissionId}/download?token=${token}`, '_blank');
        },

        async grade(submissionId, marks, feedback = '') {
            return API.request(`/assignments/submissions/${submissionId}/grade`, {
                method: 'POST',
                body: JSON.stringify({ marks, feedback })
            });
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

        async getById(id) {
            return API.request(`/announcements/${id}`);
        },

        async create(data) {
            return API.request('/announcements/', {
                method: 'POST',
                body: JSON.stringify(data)
            });
        },

        async update(id, data) {
            return API.request(`/announcements/${id}`, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
        },

        async delete(id) {
            return API.request(`/announcements/${id}`, { method: 'DELETE' });
        }
    },

    // Materials endpoints
    materials: {
        async getAll(courseId = null) {
            const url = courseId ? `/materials/?course_id=${courseId}` : '/materials/';
            return API.request(url);
        },

        async getById(id) {
            return API.request(`/materials/${id}`);
        },

        async upload(formData) {
            const token = API.getToken();
            const response = await fetch(`${API.BASE_URL}/materials/`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` },
                body: formData
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Upload failed');
            return data;
        },

        async update(id, data) {
            return API.request(`/materials/${id}`, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
        },

        async delete(id) {
            return API.request(`/materials/${id}`, { method: 'DELETE' });
        },

        download(id) {
            const token = API.getToken();
            window.open(`${API.BASE_URL}/materials/${id}/download?token=${token}`, '_blank');
        }
    },

    // Analytics endpoints
    analytics: {
        async getDashboardStats() {
            return API.request('/analytics/dashboard');
        },

        async getGradeDistribution(courseId = null) {
            const url = courseId ? `/analytics/grades/distribution?course_id=${courseId}` : '/analytics/grades/distribution';
            return API.request(url);
        },

        async getAttendanceTrends(courseId = null, days = 30) {
            let url = `/analytics/attendance/trends?days=${days}`;
            if (courseId) url += `&course_id=${courseId}`;
            return API.request(url);
        },

        async getClassPerformance(courseId) {
            return API.request(`/analytics/performance/class/${courseId}`);
        },

        async getStudentPerformance(studentId = null) {
            const url = studentId ? `/analytics/performance/student?student_id=${studentId}` : '/analytics/performance/student';
            return API.request(url);
        },

        async getInstitutionSummary() {
            return API.request('/analytics/summary');
        }
    },

    // Admin endpoints
    admin: {
        async getUsers(page = 1, perPage = 20, role = null, search = '') {
            let url = `/admin/users?page=${page}&per_page=${perPage}`;
            if (role) url += `&role=${role}`;
            if (search) url += `&search=${encodeURIComponent(search)}`;
            return API.request(url);
        },

        async getUser(id) {
            return API.request(`/admin/users/${id}`);
        },

        async createUser(data) {
            return API.request('/admin/users', {
                method: 'POST',
                body: JSON.stringify(data)
            });
        },

        async updateUser(id, data) {
            return API.request(`/admin/users/${id}`, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
        },

        async deleteUser(id) {
            return API.request(`/admin/users/${id}`, { method: 'DELETE' });
        },

        async restoreUser(id) {
            return API.request(`/admin/users/${id}/restore`, { method: 'POST' });
        },

        async updateUserRole(id, role) {
            return API.request(`/admin/users/${id}/role`, {
                method: 'PUT',
                body: JSON.stringify({ role })
            });
        },

        async getSystemStats() {
            return API.request('/admin/stats');
        },

        async bulkCreateUsers(users) {
            return API.request('/admin/users/bulk-create', {
                method: 'POST',
                body: JSON.stringify({ users })
            });
        }
    },

    // Calendar & Events endpoints
    calendar: {
        // Events
        async getEvents(params = {}) {
            let url = '/calendar/events?';
            if (params.type) url += `type=${params.type}&`;
            if (params.start_date) url += `start_date=${params.start_date}&`;
            if (params.end_date) url += `end_date=${params.end_date}&`;
            if (params.include_past !== undefined) url += `include_past=${params.include_past}`;
            return API.request(url);
        },

        async getEvent(id) {
            return API.request(`/calendar/events/${id}`);
        },

        async createEvent(data) {
            return API.request('/calendar/events', {
                method: 'POST',
                body: JSON.stringify(data)
            });
        },

        async updateEvent(id, data) {
            return API.request(`/calendar/events/${id}`, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
        },

        async deleteEvent(id) {
            return API.request(`/calendar/events/${id}`, { method: 'DELETE' });
        },

        // Academic Calendar
        async getAcademicCalendar(params = {}) {
            let url = '/calendar/academic?';
            if (params.academic_year) url += `academic_year=${params.academic_year}&`;
            if (params.semester) url += `semester=${params.semester}&`;
            if (params.type) url += `type=${params.type}`;
            return API.request(url);
        },

        async createAcademicItem(data) {
            return API.request('/calendar/academic', {
                method: 'POST',
                body: JSON.stringify(data)
            });
        },

        async updateAcademicItem(id, data) {
            return API.request(`/calendar/academic/${id}`, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
        },

        async deleteAcademicItem(id) {
            return API.request(`/calendar/academic/${id}`, { method: 'DELETE' });
        },

        // Timetable
        async getTimetable(params = {}) {
            let url = '/calendar/timetable?';
            if (params.course_id) url += `course_id=${params.course_id}&`;
            if (params.day !== undefined) url += `day=${params.day}&`;
            if (params.semester) url += `semester=${params.semester}&`;
            if (params.section) url += `section=${params.section}`;
            return API.request(url);
        },

        async createTimetableSlot(data) {
            return API.request('/calendar/timetable', {
                method: 'POST',
                body: JSON.stringify(data)
            });
        },

        async updateTimetableSlot(id, data) {
            return API.request(`/calendar/timetable/${id}`, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
        },

        async deleteTimetableSlot(id) {
            return API.request(`/calendar/timetable/${id}`, { method: 'DELETE' });
        },

        // Subjects
        async getSubjectsSchedule() {
            return API.request('/calendar/subjects');
        },

        async updateSubjectDates(courseId, data) {
            return API.request(`/calendar/subjects/${courseId}/dates`, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
        }
    }
};

// Export for use
window.API = API;
