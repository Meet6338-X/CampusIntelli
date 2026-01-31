/**
 * CampusIntelli Main Application
 */

const App = {
    user: null,

    // Initialize app
    init() {
        this.checkAuth();
        this.bindEvents();
    },

    // Check if user is logged in
    checkAuth() {
        const stored = localStorage.getItem('campus_user');
        if (stored) {
            try {
                this.user = JSON.parse(stored);
                this.showMainApp();
            } catch (e) {
                this.showAuthScreen();
            }
        } else {
            this.showAuthScreen();
        }
    },

    // Show auth screen
    showAuthScreen() {
        document.getElementById('auth-screen').classList.add('active');
        document.getElementById('main-app').classList.remove('active');
    },

    // Show main app
    showMainApp() {
        document.getElementById('auth-screen').classList.remove('active');
        document.getElementById('main-app').classList.add('active');

        document.getElementById('user-name').textContent = this.user.name || 'User';
        document.getElementById('user-role').textContent = this.user.role || 'student';

        // Show/hide role-specific elements
        this.updateRoleUI();

        // Load dashboard
        this.loadDashboard();
    },

    // Update UI based on role
    updateRoleUI() {
        const role = this.user?.role || 'student';

        document.querySelectorAll('.faculty-only').forEach(el => {
            el.classList.toggle('hidden', role !== 'faculty' && role !== 'admin');
        });

        document.querySelectorAll('.student-only').forEach(el => {
            el.classList.toggle('hidden', role !== 'student');
        });

        document.querySelectorAll('.admin-only').forEach(el => {
            el.classList.toggle('hidden', role !== 'admin');
        });
    },

    // Bind all events
    bindEvents() {
        // Auth tabs
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                document.querySelectorAll('.auth-form').forEach(f => f.classList.remove('active'));
                btn.classList.add('active');
                document.getElementById(`${btn.dataset.tab}-form`).classList.add('active');
            });
        });

        // Login form
        document.getElementById('login-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.handleLogin();
        });

        // Register form
        document.getElementById('register-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.handleRegister();
        });

        // Logout
        document.getElementById('logout-btn').addEventListener('click', () => this.logout());

        // Navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                this.navigateTo(link.dataset.page);
            });
        });

        // Modal close
        document.querySelector('.modal-close')?.addEventListener('click', () => this.closeModal());
        document.getElementById('modal')?.addEventListener('click', (e) => {
            if (e.target.id === 'modal') this.closeModal();
        });

        // Page-specific buttons
        document.getElementById('add-course-btn')?.addEventListener('click', () => this.showCourseForm());
        document.getElementById('add-assignment-btn')?.addEventListener('click', () => this.showAssignmentForm());
        document.getElementById('generate-qr-btn')?.addEventListener('click', () => this.showQRGenerator());
        document.getElementById('scan-qr-btn')?.addEventListener('click', () => this.showQRScanner());
        document.getElementById('new-booking-btn')?.addEventListener('click', () => this.showBookingForm());
        document.getElementById('new-announcement-btn')?.addEventListener('click', () => this.showAnnouncementForm());

        // Profile form
        document.getElementById('profile-form')?.addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.updateProfile();
        });
    },

    // Handle login
    async handleLogin() {
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;

        try {
            const data = await API.auth.login(email, password);
            this.user = data.user;
            localStorage.setItem('campus_user', JSON.stringify(data.user));
            this.showMainApp();
            this.showToast('Welcome back!', 'success');
        } catch (error) {
            this.showToast(error.message, 'error');
        }
    },

    // Handle register
    async handleRegister() {
        const userData = {
            name: document.getElementById('reg-name').value,
            email: document.getElementById('reg-email').value,
            password: document.getElementById('reg-password').value,
            role: document.getElementById('reg-role').value,
            department: document.getElementById('reg-dept').value
        };

        try {
            const data = await API.auth.register(userData);
            this.showToast('Account created! Please login.', 'success');
            document.querySelector('[data-tab="login"]').click();
        } catch (error) {
            this.showToast(error.message, 'error');
        }
    },

    // Logout
    logout() {
        localStorage.removeItem('campus_user');
        this.user = null;
        this.showAuthScreen();
        this.showToast('Logged out', 'success');
    },

    // Navigate to page
    navigateTo(page) {
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        document.querySelector(`[data-page="${page}"]`)?.classList.add('active');

        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.getElementById(`page-${page}`)?.classList.add('active');

        // Load page data
        switch (page) {
            case 'dashboard': this.loadDashboard(); break;
            case 'courses': this.loadCourses(); break;
            case 'assignments': this.loadAssignments(); break;
            case 'attendance': this.loadAttendance(); break;
            case 'bookings': this.loadBookings(); break;
            case 'announcements': this.loadAnnouncements(); break;
            case 'profile': this.loadProfile(); break;
        }
    },

    // Load dashboard
    async loadDashboard() {
        try {
            // Courses count
            const coursesData = await API.courses.getAll();
            document.getElementById('stat-courses').textContent = coursesData.courses?.length || 0;

            // Assignments
            const assignmentsData = await API.assignments.getAll();
            const pending = assignmentsData.assignments?.filter(a => !a.submitted)?.length || 0;
            document.getElementById('stat-assignments').textContent = pending;

            // Attendance summary
            try {
                const attData = await API.attendance.getSummary();
                const summary = attData.summary || {};
                let total = 0, present = 0;
                Object.values(summary).forEach(v => {
                    total += v.total || 0;
                    present += v.present || 0;
                });
                const pct = total > 0 ? Math.round((present / total) * 100) : 0;
                document.getElementById('stat-attendance').textContent = `${pct}%`;
            } catch (e) {
                document.getElementById('stat-attendance').textContent = 'N/A';
            }

            // Bookings
            const bookingsData = await API.bookings.getMyBookings();
            const activeBookings = bookingsData.bookings?.filter(b => b.status === 'confirmed')?.length || 0;
            document.getElementById('stat-bookings').textContent = activeBookings;

            // Upcoming assignments
            const upcoming = document.getElementById('upcoming-assignments');
            const upcomingList = (assignmentsData.assignments || []).slice(0, 3);
            if (upcomingList.length > 0) {
                upcoming.innerHTML = upcomingList.map(a => `
                    <div class="list-item">
                        <h4>${a.title}</h4>
                        <p>Due: ${new Date(a.due_date).toLocaleDateString()}</p>
                    </div>
                `).join('');
            } else {
                upcoming.innerHTML = '<p class="empty-state">No upcoming assignments</p>';
            }

            // Announcements
            const annData = await API.announcements.getAll();
            const recent = document.getElementById('recent-announcements');
            const recentList = (annData.announcements || []).slice(0, 3);
            if (recentList.length > 0) {
                recent.innerHTML = recentList.map(a => `
                    <div class="list-item">
                        <h4>${a.is_pinned ? '📌 ' : ''}${a.title}</h4>
                        <p>${a.content?.substring(0, 100)}...</p>
                    </div>
                `).join('');
            } else {
                recent.innerHTML = '<p class="empty-state">No announcements</p>';
            }

        } catch (error) {
            console.error('Dashboard load error:', error);
        }
    },

    // Load courses
    async loadCourses() {
        const container = document.getElementById('courses-list');
        try {
            const data = await API.courses.getAll();
            if (data.courses?.length > 0) {
                container.innerHTML = data.courses.map(c => `
                    <div class="course-card">
                        <h3>${c.code} - ${c.name}</h3>
                        <p>${c.description || 'No description'}</p>
                        <p><strong>Credits:</strong> ${c.credits} | <strong>Dept:</strong> ${c.department}</p>
                    </div>
                `).join('');
            } else {
                container.innerHTML = '<p class="empty-state">No courses available</p>';
            }
        } catch (error) {
            container.innerHTML = '<p class="empty-state">Failed to load courses</p>';
        }
    },

    // Load assignments
    async loadAssignments() {
        const container = document.getElementById('assignments-list');
        try {
            const data = await API.assignments.getAll();
            if (data.assignments?.length > 0) {
                container.innerHTML = data.assignments.map(a => `
                    <div class="assignment-card">
                        <h3>${a.title}</h3>
                        <p>${a.description || 'No description'}</p>
                        <p><strong>Due:</strong> ${new Date(a.due_date).toLocaleString()}</p>
                        <p><strong>Max Marks:</strong> ${a.max_marks}</p>
                        ${a.submitted ? '<span class="badge" style="background: var(--secondary);">Submitted</span>' : '<span class="badge" style="background: var(--accent);">Pending</span>'}
                    </div>
                `).join('');
            } else {
                container.innerHTML = '<p class="empty-state">No assignments yet</p>';
            }
        } catch (error) {
            container.innerHTML = '<p class="empty-state">Failed to load assignments</p>';
        }
    },

    // Load attendance
    async loadAttendance() {
        const container = document.getElementById('attendance-summary');
        try {
            const data = await API.attendance.getSummary();
            const summary = data.summary || {};

            if (Object.keys(summary).length > 0) {
                container.innerHTML = Object.entries(summary).map(([courseId, stats]) => `
                    <div class="stat-card">
                        <span class="stat-icon">📚</span>
                        <div class="stat-info">
                            <span class="stat-value">${stats.present}/${stats.total}</span>
                            <span class="stat-label">${courseId.substring(0, 8)}...</span>
                        </div>
                    </div>
                `).join('');
            } else {
                container.innerHTML = '<p class="empty-state">No attendance records</p>';
            }
        } catch (error) {
            container.innerHTML = '<p class="empty-state">Failed to load attendance</p>';
        }
    },

    // Load bookings
    async loadBookings() {
        try {
            const data = await API.bookings.getMyBookings();
            const container = document.getElementById('my-bookings');

            if (data.bookings?.length > 0) {
                container.innerHTML = data.bookings.map(b => `
                    <div class="list-item">
                        <h4>${b.room_name || 'Room'}</h4>
                        <p>${b.date} ${b.start_time} - ${b.end_time}</p>
                        <span class="badge">${b.status}</span>
                    </div>
                `).join('');
            } else {
                container.innerHTML = '<p class="empty-state">No bookings</p>';
            }

            const roomsData = await API.bookings.getRooms();
            const roomsContainer = document.getElementById('available-rooms');

            if (roomsData.rooms?.length > 0) {
                roomsContainer.innerHTML = roomsData.rooms.map(r => `
                    <div class="room-card">
                        <h3>${r.name}</h3>
                        <p><strong>Building:</strong> ${r.building} | <strong>Floor:</strong> ${r.floor}</p>
                        <p><strong>Capacity:</strong> ${r.capacity} | <strong>Type:</strong> ${r.room_type}</p>
                    </div>
                `).join('');
            } else {
                roomsContainer.innerHTML = '<p class="empty-state">No rooms available</p>';
            }
        } catch (error) {
            console.error('Bookings error:', error);
        }
    },

    // Load announcements
    async loadAnnouncements() {
        const container = document.getElementById('announcements-list');
        try {
            const data = await API.announcements.getAll();
            if (data.announcements?.length > 0) {
                container.innerHTML = data.announcements.map(a => `
                    <div class="announcement-card ${a.is_pinned ? 'pinned' : ''}">
                        <h3>${a.is_pinned ? '📌 ' : ''}${a.title}</h3>
                        <p>${a.content}</p>
                        <small>By ${a.author_name} | ${new Date(a.published_at).toLocaleDateString()}</small>
                    </div>
                `).join('');
            } else {
                container.innerHTML = '<p class="empty-state">No announcements</p>';
            }
        } catch (error) {
            container.innerHTML = '<p class="empty-state">Failed to load announcements</p>';
        }
    },

    // Load profile
    loadProfile() {
        document.getElementById('profile-name').value = this.user?.name || '';
        document.getElementById('profile-email').value = this.user?.email || '';
        document.getElementById('profile-dept').value = this.user?.department || '';
    },

    // Update profile
    async updateProfile() {
        try {
            const data = {
                name: document.getElementById('profile-name').value,
                department: document.getElementById('profile-dept').value
            };

            await API.users.update(this.user.id, data);
            this.user = { ...this.user, ...data };
            localStorage.setItem('campus_user', JSON.stringify(this.user));
            document.getElementById('user-name').textContent = this.user.name;
            this.showToast('Profile updated!', 'success');
        } catch (error) {
            this.showToast(error.message, 'error');
        }
    },

    // Show QR generator (faculty)
    async showQRGenerator() {
        try {
            const coursesData = await API.courses.getAll();
            if (!coursesData.courses?.length) {
                this.showToast('No courses assigned', 'error');
                return;
            }

            const modalBody = `
                <h2>Generate Attendance QR</h2>
                <div class="form-group">
                    <label>Select Course</label>
                    <select id="qr-course">
                        ${coursesData.courses.map(c => `<option value="${c.id}">${c.code}</option>`).join('')}
                    </select>
                </div>
                <button class="btn btn-primary" onclick="App.generateQR()">Generate</button>
                <div id="qr-result"></div>
            `;
            this.showModal(modalBody);
        } catch (error) {
            this.showToast(error.message, 'error');
        }
    },

    // Generate QR
    async generateQR() {
        const courseId = document.getElementById('qr-course').value;
        try {
            const data = await API.attendance.generateQR(courseId);
            document.getElementById('qr-result').innerHTML = `
                <img src="${data.qr_image}" alt="QR Code">
                <p>Expires in ${Math.floor(data.expires_in_seconds / 60)} minutes</p>
            `;
        } catch (error) {
            this.showToast(error.message, 'error');
        }
    },

    // Show QR scanner (student)
    showQRScanner() {
        const modalBody = `
            <h2>Mark Attendance</h2>
            <p>Enter the QR code data or scan:</p>
            <div class="form-group">
                <input type="text" id="qr-input" placeholder="Paste QR code data">
            </div>
            <button class="btn btn-primary" onclick="App.markAttendance()">Mark Present</button>
        `;
        this.showModal(modalBody);
    },

    // Mark attendance
    async markAttendance() {
        const qrData = document.getElementById('qr-input').value;
        try {
            const data = await API.attendance.mark(qrData);
            this.showToast(data.message, 'success');
            this.closeModal();
            this.loadAttendance();
        } catch (error) {
            this.showToast(error.message, 'error');
        }
    },

    // Show booking form
    showBookingForm() {
        const modalBody = `
            <h2>Book a Room</h2>
            <div class="form-group">
                <label>Date</label>
                <input type="date" id="booking-date">
            </div>
            <div class="form-group">
                <label>Start Time</label>
                <input type="time" id="booking-start">
            </div>
            <div class="form-group">
                <label>End Time</label>
                <input type="time" id="booking-end">
            </div>
            <div class="form-group">
                <label>Purpose</label>
                <textarea id="booking-purpose" rows="2"></textarea>
            </div>
            <button class="btn btn-secondary" onclick="App.checkAvailability()">Check Availability</button>
            <div id="booking-rooms"></div>
        `;
        this.showModal(modalBody);
    },

    // Check availability
    async checkAvailability() {
        const date = document.getElementById('booking-date').value;
        const start = document.getElementById('booking-start').value;
        const end = document.getElementById('booking-end').value;

        try {
            const data = await API.bookings.getAvailable(date, start, end);
            const container = document.getElementById('booking-rooms');

            if (data.rooms?.length > 0) {
                container.innerHTML = '<h4>Available Rooms:</h4>' + data.rooms.map(r => `
                    <button class="btn btn-secondary" style="margin:4px" onclick="App.bookRoom('${r.id}')">${r.name}</button>
                `).join('');
            } else {
                container.innerHTML = '<p>No rooms available</p>';
            }
        } catch (error) {
            this.showToast(error.message, 'error');
        }
    },

    // Book room
    async bookRoom(roomId) {
        const booking = {
            room_id: roomId,
            date: document.getElementById('booking-date').value,
            start_time: document.getElementById('booking-start').value,
            end_time: document.getElementById('booking-end').value,
            purpose: document.getElementById('booking-purpose').value
        };

        try {
            await API.bookings.create(booking);
            this.showToast('Room booked!', 'success');
            this.closeModal();
            this.loadBookings();
        } catch (error) {
            this.showToast(error.message, 'error');
        }
    },

    // Show announcement form
    showAnnouncementForm() {
        const modalBody = `
            <h2>New Announcement</h2>
            <div class="form-group">
                <label>Title</label>
                <input type="text" id="ann-title">
            </div>
            <div class="form-group">
                <label>Content</label>
                <textarea id="ann-content" rows="4"></textarea>
            </div>
            <div class="form-group">
                <label>Category</label>
                <select id="ann-category">
                    <option value="general">General</option>
                    <option value="academic">Academic</option>
                    <option value="event">Event</option>
                    <option value="urgent">Urgent</option>
                </select>
            </div>
            <button class="btn btn-primary" onclick="App.createAnnouncement()">Publish</button>
        `;
        this.showModal(modalBody);
    },

    // Create announcement
    async createAnnouncement() {
        try {
            await API.announcements.create({
                title: document.getElementById('ann-title').value,
                content: document.getElementById('ann-content').value,
                category: document.getElementById('ann-category').value
            });
            this.showToast('Announcement published!', 'success');
            this.closeModal();
            this.loadAnnouncements();
        } catch (error) {
            this.showToast(error.message, 'error');
        }
    },

    // Modal helpers
    showModal(content) {
        document.getElementById('modal-body').innerHTML = content;
        document.getElementById('modal').classList.remove('hidden');
    },

    closeModal() {
        document.getElementById('modal').classList.add('hidden');
    },

    // Toast notification
    showToast(message, type = 'info') {
        const toast = document.getElementById('toast');
        toast.textContent = message;
        toast.className = `toast ${type}`;
        toast.classList.remove('hidden');

        setTimeout(() => {
            toast.classList.add('hidden');
        }, 3000);
    }
};

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => App.init());
